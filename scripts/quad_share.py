"""Quad sharing: a single-pass blur where the four pixels of a 2 x 2 quad share
their texture reads through the fine derivatives.

Each pixel makes N bilinear reads; ddx_fine / ddy_fine give it the values its
three quad neighbours read (v_x = v +- ddx(v), v_y = v +- ddy(v), the diagonal
one = v_x +- ddy(v_x)), so every pixel blends 4N samples for N reads. The
neighbours mirror the read positions about the quad centre, so the four pixel
positions see the same samples from different sides; each weights them for its
own position (by symmetry one weight set, mirrored). The response differs per
position in the quad (shift variance); the metrics measure how much.

For each sigma and N: read positions by Nelder-Mead on the least-squares error
to the sampled Gaussian (weights solved exactly for given positions), then the
usual metrics against the single-pass pinwheel class of TOPT_Blur.

    python -m scripts.quad_share

Writes results/quad_share.json and results/quad_share.md.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

from scripts import make_effect as ME
from topt import search as S
from topt.cost import pipeline_cost
from topt.quality import metrics
from topt.sim import Pass, Pipeline

OUT = Path(__file__).resolve().parent.parent / "results"
R = 5  # half-width of the texel window the fit looks at
SIGMAS = (0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5)
READS = (2, 3, 4, 5, 6)


def samples(s: np.ndarray) -> list:
    """Sample positions seen by the quad pixel at (0, 0) and the member each came from:
    member (a, b) reads at its own offset s mirrored, i.e. at (a + (-1)^a s.x, b + (-1)^b s.y)."""
    out = []
    for a in (0, 1):
        for b in (0, 1):
            for k in range(len(s)):
                out.append(((a + (1 - 2 * a) * s[k, 0], b + (1 - 2 * b) * s[k, 1]), a, b, k))
    return out


def footprint(x: float, y: float) -> np.ndarray:
    """Bilinear weights of a read at (x, y) on the texel grid -R..R."""
    f = np.zeros((2 * R + 1, 2 * R + 1))
    x0, y0 = math.floor(x), math.floor(y)
    fx, fy = x - x0, y - y0
    for ax, ay, w in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
        i, j = y0 + ay + R, x0 + ax + R
        if 0 <= i <= 2 * R and 0 <= j <= 2 * R:
            f[i, j] += w
    return f


def gauss(sigma: float) -> np.ndarray:
    t = np.arange(-R, R + 1)
    g = np.exp(-0.5 * (t / sigma) ** 2)
    g = np.outer(g, g)
    return g / g.sum()


def fit_weights(s: np.ndarray, sigma: float) -> tuple:
    """Least-squares weights (sum = 1) of the samples seen by pixel (0, 0)."""
    sm = samples(s)
    A = np.stack([footprint(*p).ravel() for p, *_ in sm], 1)
    g = gauss(sigma).ravel()
    A2 = np.vstack([A, 1e3 * np.ones(A.shape[1])])
    g2 = np.concatenate([g, [1e3]])
    w, *_ = np.linalg.lstsq(A2, g2, rcond=None)
    return w, float(np.sum((A @ w - g) ** 2))


def best_positions(n: int, sigma: float, tries: int = 24) -> np.ndarray:
    rng = np.random.default_rng(n * 1000 + int(sigma * 100))
    best = None
    for _ in range(tries):
        x0 = rng.uniform(-2.0 * sigma - 0.5, 0.5, size=2 * n)
        r = minimize(lambda v: fit_weights(v.reshape(n, 2), sigma)[1], x0, method="Nelder-Mead",
                     options={"maxiter": 3000, "xatol": 1e-4, "fatol": 1e-12})
        if best is None or r.fun < best.fun:
            best = r
    return best.x.reshape(n, 2)


def quad_pass(s: np.ndarray, w: np.ndarray) -> Pass:
    """Variant v = (y % 2) * 2 + (x % 2): pixel (ra, rb) sees pixel (0, 0)'s samples mirrored."""
    sm = samples(s)
    variants = []
    for rb in (0, 1):
        for ra in (0, 1):
            sx, sy = 1 - 2 * ra, 1 - 2 * rb
            variants.append(tuple((sx * p[0], sy * p[1], float(wt)) for (p, *_), wt in zip(sm, w)))
    return Pass(1, variants[0], variants=tuple(variants), tile=2, vmap=(0, 1, 2, 3), sel="quad")


def main():
    rows = {}
    for sigma in SIGMAS:
        for n in READS:
            s = best_positions(n, sigma)
            w, err = fit_weights(s, sigma)
            p = quad_pass(s, w)
            pl = Pipeline("quad", {"n": n, "sigma": sigma}, [p])
            q = metrics(pl, sigma)
            ok = [k for k, pr in S.PROFILES.items() if S.passes_profile(q, pr) and q["block"] <= S.NOISE_BLOCK_MAX]
            cost = pipeline_cost(Pipeline("quad", {}, [Pass(1, p.taps[:n])]))["us"]
            rows[f"{sigma}_{n}"] = {"target": sigma, "reads": n, "samples": 4 * n, "us": cost,
                                    "positions": s.tolist(), "weights": w.tolist(), "ok": ok,
                                    **{k: q[k] for k in ("sigma", "tv", "leak", "iso", "phase", "block", "curv")}}
            print(f"sigma {sigma:3.1f} reads {n} ({4 * n:2d} samples): {cost:5.1f} us {'/'.join(ok) or 'FAIL':20s} "
                  f"tv {q['tv']:.3f} iso {q['iso']:.3f} phase {q['phase']:.3f} block {q['block']:.2f} "
                  f"leak {q['leak']:.3f}", flush=True)
    (OUT / "quad_share.json").write_text(json.dumps(rows, indent=1))
    write_md(rows)


def write_md(rows: dict):
    for key, r in rows.items():  # target sigma from the key (older files stored the measured one only)
        r.setdefault("target", float(key.split("_")[0]))
    lines = ["# Quad sharing (ddx_fine / ddy_fine) vs the single-pass pinwheel (GTX 1660 model, 1080p)", "",
             "us = marginal cost over a plain composite pass (texture reads only). The exchange costs",
             "12 scalar derivatives per pixel whatever the read count, plus 12 MAD per read; the",
             "composite is memory-bound, so this ALU is expected to hide. 'pinwheel' = TOPT_Blur size 1.", "",
             "| sigma | quad: reads (samples) | quality | us | phase | block | pinwheel reads | pinwheel us |",
             "|---:|---|---|---:|---:|---:|---:|---:|"]
    for t in sorted({r["target"] for r in rows.values()}):
        ok = [r for r in rows.values() if r["target"] == t and "medium" in r["ok"]]
        if 0.7 <= t <= 1.3:
            pp = ME.small_pipeline(t)
            pin = f"{len(pp.passes[0].taps)} | {pipeline_cost(pp)['us']:.0f}"
        else:
            pin = "- | -"
        if ok:
            r = min(ok, key=lambda r: r["reads"])
            q = "strict" if "strict" in r["ok"] else "medium"
            lines.append(f"| {t} | {r['reads']} ({4 * r['reads']}) | {q} | {r['us']:.0f} | {r['phase']:.3f} | "
                         f"{r['block']:.2f} | {pin} |")
        else:
            lines.append(f"| {t} | none up to {max(READS)} reads | | | | | {pin} |")
    (OUT / "quad_share.md").write_text("\n".join(lines) + "\n")

if __name__ == "__main__":
    import sys
    if "--md" in sys.argv:
        write_md(json.loads((OUT / "quad_share.json").read_text()))
    else:
        main()
