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
from dataclasses import asdict, dataclass

import numpy as np

from .cost import pipeline_cost
from .methods import bisect, gauss, pair_taps, var1d
from .quality import default_phases, eval_radius, responses, score
from .sim import Pass, Pipeline

# Quality profiles, strictest first. The search prunes against the first one.
PROFILES = {
    "strict": {"leak": 0.02, "tv": 0.05, "aniso": 0.03, "phase": 0.01, "curv": 0.35, "sigma_err": 0.02},
    "medium": {"leak": 0.02, "tv": 0.05, "aniso": 0.03, "phase": 0.03, "curv": 1.5, "sigma_err": 0.02},
    "loose": {"leak": 0.03, "tv": 0.08, "aniso": 0.05, "phase": 0.06, "curv": 3.0, "sigma_err": 0.03},
}


def passes_profile(q: dict, prof: dict) -> bool:
    return all(abs(q[k]) <= v for k, v in prof.items())


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
    up_e: int          # binomial length after bilinear interpolation
    warp: str | None

    @property
    def D(self) -> int:
        return math.prod(self.down)

    def label(self) -> str:
        d = "x".join(map(str, self.down))
        u = "x".join(map(str, self.up))
        w = "+iq" if self.warp else ""
        return f"down {d} e{self.down_e} | {self.bottom} {self.trunc:g}s | up {u} e{self.up_e}{w}"


def bottom_passes(kind: str, sl: float, trunc: float, div: int) -> list | None:
    """Bottom blur with variance exactly sl^2 (in bottom-level texels)."""
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
    for f in d.down:
        div *= f
        passes.append(Pass(div, outer(down_taps_1d(f, d.down_e))))
    b = bottom_passes(d.bottom, sl, d.trunc, div)
    if b is None:
        return None
    passes += b
    for u in d.up:
        div //= u
        passes.append(Pass(div, outer(up_taps_1d(d.up_e)), warp=d.warp))
    return Pipeline("hybrid", {**asdict(d), "sl": sl, "label": d.label()}, passes)


def min_sl(d: Design) -> float:
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


def _plans(k: int, fixed_first: int | None = None) -> set:
    plans = {tuple([2] * k)}
    if k >= 2:
        plans.add(tuple([4] + [2] * (k - 2)))
        plans.add(tuple([4] * (k // 2) + [2] * (k % 2)))
    return plans


def designs(sigma: float):
    for k in range(1, 10):
        D = 2 ** k
        if not 0.25 <= sigma / D <= 12:
            continue
        downs = _plans(k)
        ups = _plans(k) | {(D,)}
        for down, up in itertools.product(sorted(downs), sorted(ups)):
            for down_e, bottom, trunc, up_e, warp in itertools.product(
                    (1, 3, 5), ("direct", "sep"), (2.0, 2.5, 3.0), (1, 2, 3), (None, "iq")):
                yield Design(down, down_e, bottom, trunc, up, up_e, warp)


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
