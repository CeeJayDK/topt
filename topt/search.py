"""Structured search over down / blur / up pipelines built from bilinear taps.

A design is:  down steps (x2 or x4, each a separable box * binomial filter)
           -> blur at the bottom level (single-pass 2D or separable 2xN bilinear)
           -> up steps (x2, x4 or one direct step, each bilinear * binomial,
              optionally with iq's smoothstep on the bilinear fraction).
The bottom blur's sigma is fitted so the whole pipeline hits the target sigma.

Candidates are evaluated cheapest-first (by the cost model) and the search stops
once it passes a candidate that meets the strictest quality profile: nothing
more expensive can improve the cost/quality Pareto front.
"""
from __future__ import annotations

import itertools
import math
from functools import lru_cache
from dataclasses import asdict, dataclass

import numpy as np

from .cost import pipeline_cost
from .methods import bisect, gauss, pair_taps, var1d
from .quality import default_phases, eval_radius, responses, score
from .sim import Pass, Pipeline
from .uptaps import load as _load_up

UP_PIN = _load_up()
try:
    from .downtaps import load as _load_down
    DOWN_PIN = _load_down()
except FileNotFoundError:  # run `python -m topt.downtaps` to create it
    DOWN_PIN = {}

# Single-pass pinwheel shapes (scripts.small_kernels, medium profile) used as the
# building block of multi-pass pinwheel chains at the bottom level.
PIN_BASE = {
    5: [(1.113, 0.302, 0.1893), (0.0, 0.0, 0.2429)],
    9: [(0.358, 1.179, 0.1821), (1.658, 1.267, 0.0298), (0.0, 0.0, 0.1526)],
}


def rotate(taps, deg: float) -> tuple:
    if deg == 0:
        return tuple(taps)
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return tuple((dx * c - dy * s, dx * s + dy * c, w) for dx, dy, w in taps)


def _c4(groups: list) -> list:
    """Expand [(a, b, w_per_tap), ..., (0, 0, w_centre)] into all 90-degree rotations."""
    out = []
    for a, b, w in groups:
        if a == 0 and b == 0:
            out.append((0.0, 0.0, w))
        else:
            out += [(a, b, w), (-b, a, w), (-a, -b, w), (b, -a, w)]
    return out


def _pin_var(taps: list, scale: float) -> float:
    """Per-axis variance of a same-resolution pass of bilinear taps at scale x offsets."""
    v = 0.0
    for dx, _, w in taps:
        x = scale * dx
        fr = x - math.floor(x)
        v += w * (x * x + fr * (1 - fr))
    return v

# Quality profiles, strictest first. The search prunes against the first one.
PROFILES = {
    # leak/tv/curv calibrated on truncated Gaussians by eye (sigma 6):
    # strict ~ radius 3 sigma ("most smooth"), medium ~ 2.5 sigma ("useful and
    # smooth"), loose ~ 2.25 sigma ("borderline"). block: pyramid k=3 direct-up
    # (0.69) and chain+iq (1.57) looked blocky, k=2 chain+iq (0.41) a little,
    # k=3 chain (0.31) not.
    # phase: k=3 chain (0.097) looked fine and no method flickered visibly in
    # the fine-detail motion test, so shift variance is limited mainly by block.
    # Second look (isotropy.png, sigma 16): 3 sigma "barely see it", 2.5 sigma
    # "visible if you look, acceptable for some things", 2.25 "would not use",
    # 2.75 confirmed "very close, still very smooth" -> medium moved to the 2.75 sigma truncation (leak
    # 0.008-0.012, tv 0.026-0.031, curv 0.25-0.39, iso 0.015-0.018), loose to
    # 2.5 sigma. Pinwheel chain pw9x3 (block 0.35) and down 8 | up 8 p4 (iso
    # 0.029, block 0.26) look fine; pw9x2 (block 1.55) does not.
    # Interleaved (per-pixel pattern) noise, noise_s*.png: block 0.32 acceptable,
    # 0.37-0.40 "not good enough" -> see NOISE_BLOCK_MAX.
    "strict": {"leak": 0.01, "tv": 0.02, "curv": 0.2, "block": 0.1, "aniso": 0.03, "phase": 0.01,
               "iso": 0.01, "sigma_err": 0.02},
    "medium": {"leak": 0.012, "tv": 0.032, "curv": 0.4, "block": 0.35, "aniso": 0.03, "phase": 0.10,
               "iso": 0.032, "sigma_err": 0.02},
    "loose": {"leak": 0.015, "tv": 0.055, "curv": 0.7, "block": 0.45, "aniso": 0.05, "phase": 0.15,
              "iso": 0.04, "sigma_err": 0.03},
}


NOISE_BLOCK_MAX = 0.35  # static grain from interleaved patterns is judged harsher than grid blockiness


def passes_profile(q: dict, prof: dict) -> bool:
    return all(k in q and abs(q[k]) <= v for k, v in prof.items())  # a missing metric fails


def binom(n: int) -> np.ndarray:
    return np.array([math.comb(n - 1, j) for j in range(n)], float)


def down_taps_1d(f: int, e: int) -> list:
    """Downsample by f with kernel box_f * binomial_e, paired into linear taps."""
    k = np.convolve(np.ones(f), binom(e))
    k /= k.sum()
    pos = np.arange(len(k)) - (len(k) - 1) / 2  # texel centres relative to output centre
    return pair_taps(pos, k)


def up_taps_1d(e: int) -> list:
    """Bilinear interpolation followed by binomial_e at unit source spacing."""
    w = binom(e)
    w /= w.sum()
    return list(zip(np.arange(e) - (e - 1) / 2, w))


def outer(t1: list) -> tuple:
    return tuple((ox, oy, wx * wy) for ox, wx in t1 for oy, wy in t1)


@dataclass(frozen=True)
class Design:
    down: tuple        # factors, e.g. (4, 2, 2)
    down_e: int        # binomial length added to each down box filter
    bottom: str        # 'direct' (1 pass) or 'sep' (2xN / Nx2 bilinear)
    trunc: float       # bottom kernel radius in bottom-level sigmas
    up: tuple          # factors, e.g. (2, 2, 2) or (8,)
    up_e: int          # binomial length after bilinear interpolation (or tap count if up_pin)
    warp: str | None
    up_pin: bool = False  # up_e = taps of a free-position "pinwheel" upsampler (topt.uptaps)
    down_pin: int = 0     # >0: taps of a pinwheel downsample filter (topt.downtaps) instead of box*binomial
    rot: bool = False     # rotate every other pinwheel down/up step by 45 degrees

    @classmethod
    def from_params(cls, p: dict) -> "Design":
        return cls(tuple(p["down"]), p["down_e"], p["bottom"], p["trunc"], tuple(p["up"]), p["up_e"],
                   p["warp"], p.get("up_pin", False), p.get("down_pin", 0), p.get("rot", False))

    @property
    def D(self) -> int:
        return math.prod(self.down)

    def label(self) -> str:
        d = "x".join(map(str, self.down))
        u = "x".join(map(str, self.up))
        w = "+iq" if self.warp else ""
        ue = f"p{self.up_e}" if self.up_pin else f"e{self.up_e}"
        de = f"p{self.down_pin}" if self.down_pin else f"e{self.down_e}"
        r = " rot45" if self.rot else ""
        b = self.bottom if self.bottom.startswith("pw") else f"{self.bottom} {self.trunc:g}s"
        return f"down {d} {de} | {b} | up {u} {ue}{w}{r}"


@lru_cache(maxsize=65536)
def bottom_passes(kind: str, sl: float, trunc: float, div: int) -> list | None:
    """Bottom blur with variance exactly sl^2 (in bottom-level texels)."""
    if kind.startswith("pw"):  # 'pw5x2': K passes of a scaled 5-tap pinwheel, rotated 90/K deg each
        n, K = map(int, kind[2:].split("x"))
        base = _c4(PIN_BASE[n])
        c = bisect(lambda c: _pin_var(base, c), sl * sl / K, 1e-3, 50.0)
        if c is None:
            return None
        scaled = [(dx * c, dy * c, w) for dx, dy, w in base]
        return [Pass(div, rotate(scaled, j * 90.0 / K)) for j in range(K)]
    if kind == "direct":
        r = max(1, math.ceil(trunc * sl))
        pos = np.arange(-r, r + 1, dtype=float)
        s = bisect(lambda s: var1d(pos, gauss(pos, s)), sl * sl, 1e-3, 1e6)
        if s is None:
            return None
        t = pair_taps(pos, gauss(pos, s))
        return [Pass(div, outer(t))]
    m = max(1, math.ceil(trunc * sl))
    pos = np.arange(-m, m, dtype=float)
    s = bisect(lambda s: var1d(pos, gauss(pos + 0.5, s)), sl * sl - 0.25, 1e-3, 1e6)
    if s is None:
        return None
    t = pair_taps(pos, gauss(pos + 0.5, s))
    return [Pass(div, tuple((o, -0.5, w) for o, w in t)),
            Pass(div, tuple((0.5, o + 1.0, w) for o, w in t))]


def build(d: Design, sl: float) -> Pipeline | None:
    passes, div = [], 1
    for i, f in enumerate(d.down):
        div *= f
        if d.down_pin:
            taps = rotate(DOWN_PIN[(f, d.down_pin)], 45.0 if d.rot and i % 2 else 0.0)
        else:
            taps = outer(down_taps_1d(f, d.down_e))
        passes.append(Pass(div, taps))
    b = bottom_passes(d.bottom, sl, d.trunc, div)
    if b is None:
        return None
    passes += b
    up = tuple(UP_PIN[d.up_e]) if d.up_pin else outer(up_taps_1d(d.up_e))
    for i, u in enumerate(d.up):
        div //= u
        passes.append(Pass(div, rotate(up, 45.0 if d.rot and d.up_pin and i % 2 else 0.0), warp=d.warp))
    return Pipeline("hybrid", {**asdict(d), "sl": sl, "label": d.label()}, passes)


def min_sl(d: Design) -> float:
    if d.bottom.startswith("pw"):
        return 0.2 * math.sqrt(int(d.bottom.split("x")[1]))
    return 0.51 if d.bottom == "sep" else 0.2


def fit(d: Design, sigma: float, tol: float = 0.003, iters: int = 5):
    """Fit the bottom sigma. Phase-averaged variance is ~affine in sl^2."""
    F = d.D
    ph, rad = default_phases(F), eval_radius(sigma, F)
    D2 = float(F * F)

    def measure(sl):
        pl = build(d, sl)
        if pl is None:
            return None, None, None
        ks, R = responses(pl, ph, rad)
        q = score(ks, R, sigma)
        return pl, q, q["sigma"] ** 2

    x0 = max(min_sl(d), 0.8 * sigma / F) ** 2
    pl, q, v0 = measure(math.sqrt(x0))
    if pl is None:
        return None
    x1 = x0 + (sigma * sigma - v0) / D2
    for _ in range(iters):
        if x1 < min_sl(d) ** 2:
            return None  # the down/up chain alone is already too blurry
        pl, q, v1 = measure(math.sqrt(x1))
        if pl is None:
            return None
        if abs(q["sigma_err"]) < tol:
            return pl, q
        slope = (v1 - v0) / (x1 - x0) if x1 != x0 else D2
        x0, v0 = x1, v1
        x1 = x1 + (sigma * sigma - v1) / (slope if slope > 0 else D2)
    return None


def _down_plans(k: int) -> set:
    """Factor sequences (largest step first) with product 2^k: the classic all-x2 /
    x4 chains plus up to three steps from {2, 4, 8, 16}."""
    plans = {tuple([2] * k)}
    if k >= 2:
        plans.add(tuple([4] + [2] * (k - 2)))
        plans.add(tuple([4] * (k // 2) + [2] * (k % 2)))

    def rec(rem, maxf, seq):
        if rem == 0:
            plans.add(tuple(seq))
            return
        if len(seq) == 3:
            return
        for f in (16, 8, 4, 2):
            if f <= maxf and rem >= int(math.log2(f)):
                rec(rem - int(math.log2(f)), f, seq + [f])

    rec(k, 16, [])
    return plans


def _up_plans(k: int) -> set:
    D = 2 ** k
    plans = {tuple([2] * k), (D,)}
    if k >= 2:
        plans.add(tuple([4] * (k // 2) + [2] * (k % 2)))
        for j in range(1, k):  # two steps: coarse step first, then the rest into the composite
            plans.add((2 ** j, 2 ** (k - j)))
    return plans


UP_FILTERS = [(1, False), (2, False), (3, False), (4, True), (5, True), (8, True), (9, True)]
BOTTOMS = [("direct", t) for t in (2.0, 2.5, 3.0)] + [("sep", t) for t in (2.0, 2.5, 3.0)] + \
          [(k, 0.0) for k in ("pw5x3", "pw9x2", "pw9x3")]


def designs(sigma: float):
    for k in range(1, 10):
        D = 2 ** k
        if not 0.25 <= sigma / D <= 12:
            continue
        for down, up in itertools.product(sorted(_down_plans(k)), sorted(_up_plans(k))):
            downs = [(e, 0) for e in (1, 3, 5, 9)]
            # pinwheel downsamples only for x2/x4 steps: 8-16 taps cannot cover an 8x8+ block
            downs += [(1, n) for n in (8, 16) if all(f <= 4 and (f, n) in DOWN_PIN for f in down)]
            for (down_e, dpin), (bottom, trunc), (up_e, pin) in itertools.product(downs, BOTTOMS, UP_FILTERS):
                # rotation alternation only matters for multi-step pinwheel chains
                can_rot = (dpin and len(down) > 1) or (pin and len(up) > 1)
                for rot in ((False, True) if can_rot else (False,)):
                    yield Design(down, down_e, bottom, trunc, up, up_e, None, pin, dpin, rot)


def search(sigma: float, W: int = 1920, H: int = 1080, log=None) -> list:
    """Evaluate designs cheapest-first; returns records of every evaluated candidate."""
    queue = []
    for d in designs(sigma):
        est = build(d, max(min_sl(d), sigma / d.D))
        if est is not None:
            queue.append((pipeline_cost(est, W, H)["us"], d))
    queue.sort(key=lambda t: t[0])
    strict = next(iter(PROFILES.values()))
    stop_at, out = math.inf, []
    for est_us, d in queue:
        if est_us > stop_at * 1.02:  # estimate vs fitted cost can differ a little
            break
        r = fit(d, sigma)
        if r is None:
            continue
        pl, q = r
        c = pipeline_cost(pl, W, H)
        rec = {"design": d.label(), "params": pl.params, **{k: c[k] for k in ("us", "passes", "fetch_per_px")}, **q}
        rec["profiles"] = [n for n, p in PROFILES.items() if passes_profile(q, p)]
        out.append(rec)
        if passes_profile(q, strict):
            stop_at = min(stop_at, c["us"])
        if log and len(out) % 50 == 0:
            log(f"  sigma {sigma:g}: {len(out)} evaluated, at {est_us:.0f} us, stop at {stop_at:.0f}")
    return out


def pareto(recs: list, key: str = "phase") -> list:
    """Records not beaten on both cost and `key` by another record."""
    front, best = [], math.inf
    for r in sorted(recs, key=lambda r: (r["us"], r[key])):
        if r[key] < best:
            front.append(r)
            best = r[key]
    return front
