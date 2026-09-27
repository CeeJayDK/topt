"""Free-position upsample tap patterns ("pinwheel" upsamplers).

A set of bilinear taps at offsets o_i (source texels) with weights w_i
reconstructs the low-res image with the continuous kernel
    h(x, y) = sum_i w_i * tent(x + ox_i) * tent(y + oy_i).
Kinks in h (from the tents) sit at fixed positions relative to the low-res
grid and show up as blockiness. We fit h to a smooth Gaussian in value and
gradient (H1 norm), so the pattern is universal: independent of sigma and of
the upsampling factor. Taps come in 90-degree rotation groups (+ centre).

    python -m topt.uptaps     # refits and writes topt/up_taps.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

PATH = Path(__file__).with_name("up_taps.json")
STEP = 1.0 / 16
X = np.arange(-4.0, 4.0 + STEP / 2, STEP)
GX, GY = np.meshgrid(X, X)
CONFIGS = {4: (1, False), 5: (1, True), 8: (2, False), 9: (2, True)}


def tent(t: np.ndarray) -> np.ndarray:
    return np.clip(1.0 - np.abs(t), 0.0, None)


def expand(v: np.ndarray, groups: int, centre: bool) -> list:
    """Parameter vector -> [(dx, dy, w)]; last entry of v is log(sigma_u)."""
    ab = v[:2 * groups].reshape(groups, 2)
    lw = v[2 * groups:-1]
    w = np.exp(lw - lw.max())
    w /= w.sum()
    taps = []
    for (a, b), wg in zip(ab, w):
        for ra, rb in ((a, b), (-b, a), (-a, -b), (b, -a)):
            taps.append((float(ra), float(rb), float(wg / 4)))
    if centre:
        taps.append((0.0, 0.0, float(w[-1])))
    return taps


def recon(taps: list) -> np.ndarray:
    return sum(w * tent(GX + dx) * tent(GY + dy) for dx, dy, w in taps)


def h1_residual(h: np.ndarray, g: np.ndarray, lam: float = 1.0) -> np.ndarray:
    gy_h, gx_h = np.gradient(h, STEP)
    gy_g, gx_g = np.gradient(g, STEP)
    return np.concatenate([(h - g).ravel(), lam * (gx_h - gx_g).ravel(), lam * (gy_h - gy_g).ravel()]) * STEP


def gauss2(s: float) -> np.ndarray:
    return np.exp(-(GX ** 2 + GY ** 2) / (2 * s * s)) / (2 * np.pi * s * s)


def fit(n: int, starts: int = 20, seed: int = 0) -> dict:
    groups, centre = CONFIGS[n]
    nw = groups + (1 if centre else 0)
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(starts):
        r = 0.3 + 1.2 * rng.random(groups)
        th = rng.random(groups) * np.pi / 2
        v0 = np.concatenate([np.stack([r * np.cos(th), r * np.sin(th)], 1).ravel(),
                             rng.normal(0, 0.5, nw), [np.log(0.6)]])
        res = least_squares(lambda v: h1_residual(recon(expand(v, groups, centre)), gauss2(np.exp(v[-1]))), v0,
                            bounds=([-2.5] * (2 * groups) + [-20] * nw + [np.log(0.3)],
                                    [2.5] * (2 * groups) + [20] * nw + [np.log(1.5)]))
        if best is None or res.cost < best.cost:
            best = res
    taps = expand(best.x, groups, centre)
    return {"taps": taps, "sigma_u": float(np.exp(best.x[-1])), "h1_err": rel_err(taps, float(np.exp(best.x[-1])))}


def rel_err(taps: list, s: float) -> float:
    g = gauss2(s)
    return float(np.linalg.norm(h1_residual(recon(taps), g)) / np.linalg.norm(h1_residual(0 * g, g)))


def load() -> dict:
    """{n_taps: [(dx, dy, w)]} from the cached fit."""
    return {int(k): [tuple(t) for t in v["taps"]] for k, v in json.loads(PATH.read_text()).items()}


def main():
    out = {}
    for n in CONFIGS:
        r = fit(n)
        out[str(n)] = r
        print(f"{n} taps: sigma_u {r['sigma_u']:.3f}, H1 error {r['h1_err']:.3f}, "
              + "; ".join(f"({dx:.3f},{dy:.3f}) w {w:.4f}" for dx, dy, w in r["taps"][::4]))
    # reference: the binomial upsamplers already in the search (fit sigma_u only)
    for e, taps in ((1, [(0.0, 0.0, 1.0)]), (2, [(sx * .5, sy * .5, .25) for sx in (-1, 1) for sy in (-1, 1)])):
        s = min(np.linspace(0.3, 1.5, 121), key=lambda s: rel_err(taps, s))
        print(f"binomial e{e} ({len(taps)} taps): best-fit sigma_u {s:.3f}, H1 error {rel_err(taps, s):.3f}")
    PATH.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
