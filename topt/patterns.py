"""Sample point sets for stochastic / interleaved blur passes.

Point sets on the unit disk (uniform density):
  vogel      golden-angle spiral (Vogel 1979): r = sqrt((i + .5) / n), theta = i * 137.5 deg
  r2         Roberts' R2 low-discrepancy sequence (plastic-number additive recurrence)
  strat      jittered grid (one point per cell), mapped to the disk
  sot        sliced optimal transport (Paulin et al. 2020 style): points are moved
             along random 1D projections until every projection matches the
             disk's Radon profile - very even spacing in every direction

Mapping to a Gaussian blur of scale s (source texels), truncated at radius k * s:
  'importance'  radii warped so the point density follows the Gaussian; equal weights
  'weighted'    uniform points in the disk; weights follow the Gaussian

Per-pixel variants rotate the whole set. The rotation index comes from the
pixel position within a tile: 'bayer' (P x P ordered-dither index, P^2 variants)
or 'dot' ((x + k*y) mod P, P variants - a single dot/frac in the shader).
"""
from __future__ import annotations

import math

import numpy as np

GOLDEN_ANGLE = math.pi * (3.0 - math.sqrt(5.0))
PLASTIC = 1.324717957244746


def vogel(n: int, seed: float = 0.0) -> np.ndarray:
    i = np.arange(n) + 0.5
    r = np.sqrt(i / n)
    th = i * GOLDEN_ANGLE + seed * 2 * math.pi
    return np.stack([r * np.cos(th), r * np.sin(th)], 1)


def _to_disk(u: np.ndarray) -> np.ndarray:
    r = np.sqrt(u[:, 0])
    th = 2 * math.pi * u[:, 1]
    return np.stack([r * np.cos(th), r * np.sin(th)], 1)


def r2(n: int, seed: float = 0.5) -> np.ndarray:
    a = np.array([1 / PLASTIC, 1 / PLASTIC ** 2])
    u = (seed + np.outer(np.arange(1, n + 1), a)) % 1.0
    return _to_disk(u)


def strat(n: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    g = int(math.ceil(math.sqrt(n)))
    cells = np.stack(np.meshgrid(np.arange(g), np.arange(g)), -1).reshape(-1, 2)
    cells = cells[rng.permutation(len(cells))[:n]]
    u = (cells + rng.random((n, 2))) / g
    return _to_disk(u)


_X = np.linspace(-1, 1, 4001)
_CDF = (_X * np.sqrt(1 - _X ** 2) + np.arcsin(_X)) / math.pi + 0.5  # projection CDF of the unit disk


def sot(n: int, iters: int = 400, dirs: int = 32, seed: int = 0) -> np.ndarray:
    """Evenly spread points in the unit disk by sliced optimal transport."""
    rng = np.random.default_rng(seed)
    p = r2(n, 0.5 + 0.1 * seed)
    target = np.interp((np.arange(n) + 0.5) / n, _CDF, _X)  # ideal sorted 1D positions
    for it in range(iters):
        phi = (np.arange(dirs) + rng.random()) * math.pi / dirs
        d = np.stack([np.cos(phi), np.sin(phi)], 1)          # (dirs, 2)
        proj = p @ d.T                                        # (n, dirs)
        order = np.argsort(proj, 0)
        delta = np.zeros_like(proj)
        for j in range(dirs):
            delta[order[:, j], j] = target - proj[order[:, j], j]
        p = p + (delta @ d) / dirs
    return p


GENERATORS = {"vogel": vogel, "r2": r2, "strat": strat, "sot": sot}


def to_gaussian(pts: np.ndarray, s: float, k: float, mapping: str) -> list:
    """Unit-disk points -> [(dx, dy, w)] for a Gaussian of scale s truncated at k*s."""
    r = np.linalg.norm(pts, axis=1)
    u = pts / np.maximum(r, 1e-12)[:, None]
    if mapping == "importance":
        c = 1.0 - math.exp(-0.5 * k * k)
        rho = s * np.sqrt(-2.0 * np.log(1.0 - np.clip(r * r, 0, 1) * c))
        w = np.full(len(pts), 1.0 / len(pts))
    else:
        rho = r * k * s
        w = np.exp(-0.5 * (rho / s) ** 2)
        w /= w.sum()
    xy = u * rho[:, None]
    return [(float(x), float(y), float(ww)) for (x, y), ww in zip(xy, w)]


def rotate(taps: list, a: float) -> tuple:
    c, s = math.cos(a), math.sin(a)
    return tuple((dx * c - dy * s, dx * s + dy * c, w) for dx, dy, w in taps)


def bayer(P: int) -> np.ndarray:
    m = np.zeros((1, 1), int)
    while m.shape[0] < P:
        m = np.block([[4 * m, 4 * m + 2], [4 * m + 3, 4 * m + 1]])
    return m


def selector(kind: str, P: int, k: int = 1) -> tuple:
    """(vmap, n_variants) for a P x P tile."""
    if P == 1:
        return (0,), 1
    if kind == "bayer":
        return tuple(int(v) for v in bayer(P).ravel()), P * P
    yy, xx = np.mgrid[0:P, 0:P]  # 'dot': (x + k*y) mod P
    return tuple(int(v) for v in ((xx + k * yy) % P).ravel()), P


def variants(base: list, n_var: int, spread: float = 2 * math.pi) -> tuple:
    """n_var rotated copies of the tap set, evenly spread over `spread` radians."""
    return tuple(rotate(base, spread * v / n_var) for v in range(n_var))
