"""Blur method families, each built from bilinear-tap passes.

Every builder takes explicit parameters; `candidates(family, sigma)` yields
parameterisations fitted to a target Gaussian sigma (in full-res pixels).
"""
from __future__ import annotations

import math

import numpy as np

from .quality import measured_sigma, default_phases
from .sim import Pass, Pipeline


# ---------------------------------------------------------------- 1D helpers

def gauss(pos: np.ndarray, s: float) -> np.ndarray:
    d2 = pos * pos
    w = np.exp(-0.5 * (d2 - d2.min()) / (s * s))
    return w / w.sum()


def var1d(pos: np.ndarray, w: np.ndarray) -> float:
    m = (pos * w).sum()
    return float((w * (pos - m) ** 2).sum())


def bisect(fn, target: float, lo: float, hi: float, iters: int = 60) -> float | None:
    """Solve fn(x) = target for monotone increasing fn on [lo, hi]."""
    flo, fhi = fn(lo), fn(hi)
    if not (flo <= target <= fhi):
        return None
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if fn(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def pair_taps(pos: np.ndarray, w: np.ndarray) -> list:
    """Merge consecutive texels into linear-filtered taps: [(offset, weight)]."""
    taps, i = [], 0
    while i < len(pos):
        if i + 1 < len(pos):
            a, b = w[i], w[i + 1]
            taps.append((pos[i] + b / (a + b), a + b))
            i += 2
        else:
            taps.append((pos[i], w[i]))
            i += 1
    return taps


# ---------------------------------------------------------------- families

def sep_linear(r: int, s: float) -> Pipeline:
    """Classic separable Gaussian, 2 texels per fetch: (r+1) fetches per pass."""
    pos = np.arange(-r, r + 1, dtype=float)
    t = pair_taps(pos, gauss(pos, s))
    return Pipeline("sep_linear", {"r": r, "s": s}, [
        Pass(1, tuple((o, 0.0, w) for o, w in t)),
        Pass(1, tuple((0.0, o, w) for o, w in t)),
    ])


def sep_bilinear(m: int, s: float, div: int = 1) -> Pipeline:
    """Separable 2xN / Nx2 bilinear passes (M. Day 2012; CeeJay): m fetches per pass.

    Pass 1 = K'(x) (x) box(y, rows -1..0);  pass 2 = box(x, cols 0..1) (x) K'(y).
    Result = (K' * box) in each axis: a (2m+1)^2 kernel from 2m fetches.
    """
    pos = np.arange(-m, m, dtype=float)          # centred on -0.5
    t = pair_taps(pos, gauss(pos + 0.5, s))
    return Pipeline("sep_bilinear", {"m": m, "s": s}, [
        Pass(div, tuple((o, -0.5, w) for o, w in t)),
        Pass(div, tuple((0.5, o + 1.0, w) for o, w in t)),
    ])


def direct2d(r: int, s: float) -> Pipeline:
    """Single pass, 2x2 texels per fetch: (r+1)^2 fetches."""
    pos = np.arange(-r, r + 1, dtype=float)
    t = pair_taps(pos, gauss(pos, s))
    return Pipeline("direct2d", {"r": r, "s": s},
                    [Pass(1, tuple((ox, oy, wx * wy) for ox, wx in t for oy, wy in t))])


def kawase_var(t: float) -> float:
    x0 = math.floor(t)
    f = t - x0
    return (1 - f) * x0 * x0 + f * (x0 + 1) ** 2


def kawase(offsets: list) -> Pipeline:
    """Kawase: per pass 4 diagonal taps at (+-t, +-t)."""
    return Pipeline("kawase", {"offsets": [round(t, 3) for t in offsets]}, [
        Pass(1, tuple((sx * t, sy * t, 0.25) for sx in (-1, 1) for sy in (-1, 1)))
        for t in offsets
    ])


def dual_filter(levels: int, o: float) -> Pipeline:
    """Dual filtering / dual Kawase (M. Bjorge, SIGGRAPH 2015), offset o in source texels."""
    passes = []
    for l in range(levels):
        passes.append(Pass(2 ** (l + 1), ((0.0, 0.0, 0.5),) + tuple(
            (sx * o, sy * o, 0.125) for sx in (-1, 1) for sy in (-1, 1))))
    for l in range(levels):
        e, d = o, 0.5 * o
        passes.append(Pass(2 ** (levels - 1 - l),
                           ((-e, 0.0, 1 / 12), (e, 0.0, 1 / 12), (0.0, -e, 1 / 12), (0.0, e, 1 / 12))
                           + tuple((sx * d, sy * d, 2 / 12) for sx in (-1, 1) for sy in (-1, 1))))
    return Pipeline("dual_filter", {"levels": levels, "o": o}, passes)


def pyramid(k: int, m: int, s: float, up: str = "chain", warp: str | None = None) -> Pipeline:
    """k x (2x2 box downsample), sep_bilinear blur at 1/2^k, bilinear upsample."""
    passes = [Pass(2 ** (j + 1), ((0.0, 0.0, 1.0),)) for j in range(k)]
    if m > 0:
        passes += sep_bilinear(m, s, div=2 ** k).passes
    if up == "chain":
        passes += [Pass(2 ** (k - 1 - j), ((0.0, 0.0, 1.0),), warp=warp) for j in range(k)]
    else:
        passes.append(Pass(1, ((0.0, 0.0, 1.0),), warp=warp))
    return Pipeline("pyramid", {"k": k, "m": m, "s": s, "up": up, "warp": warp}, passes)


# ---------------------------------------------------------------- fitted candidates

def _radii(lo: int, hi: int):
    """Integer radii from lo to hi, dense when small, ~6 % steps when large."""
    out, r = [], lo
    while r <= hi:
        out.append(r)
        r = max(r + 1, int(round(r * 1.06)))
    return out


def cand_sep_linear(sigma):
    for r in _radii(max(1, math.ceil(math.sqrt(3) * sigma - 0.5)), math.ceil(4 * sigma)):
        pos = np.arange(-r, r + 1, dtype=float)
        s = bisect(lambda s: var1d(pos, gauss(pos, s)), sigma ** 2, 1e-3, 1e6)
        if s:
            yield sep_linear(r, s)


def cand_sep_bilinear(sigma, div: int = 1):
    target = (sigma / div) ** 2 - 0.25
    if target <= 0:
        return
    for m in _radii(max(1, math.ceil(math.sqrt(3 * target + 0.25))), math.ceil(4 * sigma / div) + 1):
        pos = np.arange(-m, m, dtype=float)
        s = bisect(lambda s: var1d(pos, gauss(pos + 0.5, s)), target, 1e-3, 1e6)
        if s:
            yield sep_bilinear(m, s, div)


def cand_direct2d(sigma, max_fetch: int = 1024):
    for p in cand_sep_linear(sigma):
        r = p.params["r"]
        if (r + 1) ** 2 > max_fetch:
            return
        yield direct2d(r, p.params["s"])


def cand_kawase(sigma, max_passes: int = 64):
    rem, offs, k = sigma ** 2, [], 0
    while rem > kawase_var(k + 0.5) + 1e-9:
        offs.append(k + 0.5)
        rem -= kawase_var(k + 0.5)
        k += 1
        if len(offs) > max_passes:
            return
    if rem > 1e-6:
        offs.append(bisect(kawase_var, rem, 0.0, k + 0.5))
    yield kawase(offs)


def _fit_measured(make, sigma, lo, hi, iters=14):
    """Fit a scalar parameter by simulation (for shift-variant pipelines)."""
    ph = default_phases(make(lo).max_div, 2)

    def fn(v):
        try:
            return measured_sigma(make(v), ph)
        except ValueError:  # too large to simulate: certainly above target
            return math.inf

    x = bisect(fn, sigma, lo, hi, iters)
    return None if x is None else make(x)


def cand_dual_filter(sigma):
    for L in range(1, 11):
        if not 2 ** L / 2.5 <= sigma <= 2.5 * 2 ** L:  # o in [0.25, 3] spans ~[0.5, 2.5] * 2^L
            continue
        p = _fit_measured(lambda o: dual_filter(L, o), sigma, 0.25, 2.5)
        if p:
            yield p


def cand_pyramid(sigma, truncs=(2.0, 3.0)):
    for k in range(1, 10):
        low = sigma / 2 ** k
        if low < 0.6 or low > 8:
            continue
        for trunc in truncs:
            for up, warp in (("chain", None), ("chain", "iq"), ("direct", None)):
                def make(sl, k=k, trunc=trunc, up=up, warp=warp):
                    m = max(1, math.ceil(trunc * sl))
                    pos = np.arange(-m, m, dtype=float)
                    s = bisect(lambda s: var1d(pos, gauss(pos + 0.5, s)), sl * sl - 0.25, 1e-3, 1e6) or 1e6
                    return pyramid(k, m, s, up, warp)
                p = _fit_measured(make, sigma, 0.55, 3 * low + 4)
                if p:
                    yield p


FAMILIES = {
    "direct2d": cand_direct2d,
    "sep_linear": cand_sep_linear,
    "sep_bilinear": cand_sep_bilinear,
    "kawase": cand_kawase,
    "dual_filter": cand_dual_filter,
    "pyramid": cand_pyramid,
}
