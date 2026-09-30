"""Free-position "pinwheel" downsample filters.

A downsample by an even factor f puts the output centre on a texel corner, so
source texel centres sit at half-integer offsets. A tap at offset o spreads its
weight over the 4 nearest texel centres (bilinear). We fit 90-degree rotation
groups of taps so the resulting discrete kernel matches a sampled Gaussian
(its width sigma_d is fitted too) and leaks little above the Gaussian's 1 %
frequency: a round anti-aliasing filter with few fetches.

    python -m topt.downtaps     # refits and writes topt/down_taps.json
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

from .quality import GAUSS_STOP

PATH = Path(__file__).with_name("down_taps.json")
FACTORS = (2, 4, 8, 16)
COUNTS = (8, 16)  # taps = 4 * groups


def tent(t: np.ndarray) -> np.ndarray:
    return np.clip(1.0 - np.abs(t), 0.0, None)


def expand(v: np.ndarray, groups: int) -> list:
    ab = v[:2 * groups].reshape(groups, 2)
    lw = v[2 * groups:3 * groups]
    w = np.exp(lw - lw.max())
    w /= w.sum()
    taps = []
    for (a, b), wg in zip(ab, w):
        for ra, rb in ((a, b), (-b, a), (-a, -b), (b, -a)):
            taps.append((float(ra), float(rb), float(wg / 4)))
    return taps


def kernel(taps: list, cx: np.ndarray, cy: np.ndarray) -> np.ndarray:
    return sum(w * tent(dx - cx) * tent(dy - cy) for dx, dy, w in taps)


def fit(f: int, n: int, starts: int = 24, seed: int = 0) -> dict:
    groups = n // 4
    R = 2 * f + 2
    c = np.arange(-R, R) + 0.5  # texel centres relative to the output centre
    cx, cy = np.meshgrid(c, c)
    M = 128
    fr = np.fft.fftfreq(M)
    frr = np.sqrt(fr[:, None] ** 2 + fr[None, :] ** 2)
    rng = np.random.default_rng(seed)

    def resid(v):
        taps = expand(v, groups)
        s = math.exp(v[-1])
        k = kernel(taps, cx, cy)
        g = np.exp(-(cx ** 2 + cy ** 2) / (2 * s * s))
        g /= g.sum()
        mask = 1.0 / (1.0 + np.exp(-(frr - GAUSS_STOP / s) / 0.005))  # soft stop-band, fixed size
        spec = np.abs(np.fft.fft2(k, s=(M, M))) * mask
        return np.concatenate([(k - g).ravel(), 0.05 * spec.ravel()])

    best = None
    for _ in range(starts):
        r = f * (0.15 + 0.5 * rng.random(groups))
        th = rng.random(groups) * np.pi / 2
        v0 = np.concatenate([np.stack([r * np.cos(th), r * np.sin(th)], 1).ravel(),
                             rng.normal(0, 0.5, groups), [math.log(0.5 * f)]])
        lo = [-(f + 1)] * (2 * groups) + [-20] * groups + [math.log(0.3 * f)]
        hi = [f + 1] * (2 * groups) + [20] * groups + [math.log(0.9 * f)]
        res = least_squares(resid, v0, bounds=(lo, hi))
        if best is None or res.cost < best.cost:
            best = res
    return {"taps": expand(best.x, groups), "sigma_d": math.exp(best.x[-1]), "cost": float(best.cost)}


def load() -> dict:
    """{(factor, taps): [(dx, dy, w)]}"""
    d = json.loads(PATH.read_text())
    return {tuple(map(int, k.split("x"))): [tuple(t) for t in v["taps"]] for k, v in d.items()}


def main():
    out = {}
    for f in FACTORS:
        for n in COUNTS:
            r = fit(f, n)
            out[f"{f}x{n}"] = r
            print(f"down x{f}, {n} taps: sigma_d {r['sigma_d']:.3f} ({r['sigma_d'] / f:.2f} f), cost {r['cost']:.2e}",
                  flush=True)
    PATH.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
