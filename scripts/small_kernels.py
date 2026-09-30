"""Single-pass small blurs with freely placed bilinear taps (fused into the composite).

Taps come in "pinwheel" groups of 4 rotated by 90 degrees (as LumaSharpen's
"Wider" pattern) plus an optional centre tap. For each fetch count we search
the largest sigma that still meets each quality profile.

    python -m scripts.small_kernels
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

from topt.cost import pipeline_cost
from topt.quality import GAUSS_STOP, metrics
from topt.search import PROFILES
from topt.sim import Pass, Pipeline, run

OUT = Path(__file__).resolve().parent.parent / "results"
CONFIGS = [(1, True), (2, False), (2, True), (3, True)]  # (groups, centre) -> 5, 8, 9, 13 fetches


def build(x: np.ndarray, groups: int, centre: bool) -> Pipeline:
    """x = [a_g, b_g]*groups + logits for group weights (+ centre)."""
    ab = x[:2 * groups].reshape(groups, 2)
    lw = x[2 * groups:]
    w = np.exp(lw - lw.max())
    w /= w.sum()
    taps = []
    for (a, b), wg in zip(ab, w):
        for ra, rb in ((a, b), (-b, a), (-a, -b), (b, -a)):
            taps.append((float(ra), float(rb), float(wg / 4)))
    if centre:
        taps.append((0.0, 0.0, float(w[-1])))
    return Pipeline("pinwheel", {"groups": groups, "centre": centre, "x": [float(v) for v in x]}, [Pass(1, tuple(taps))])


def score(q: dict, prof: dict) -> float:
    """Worst metric relative to its limit (<= 1 passes the profile)."""
    keys = ("leak", "tv", "curv", "aniso", "sigma_err")
    return max(abs(q[k]) / prof[k] for k in keys)


def kernel(pl: Pipeline, R: int) -> np.ndarray:
    n = 2 * R + 9
    img = np.zeros((n, n))
    img[n // 2, n // 2] = 1.0
    return run(pl, img)[n // 2 - R:n // 2 + R + 1, n // 2 - R:n // 2 + R + 1]


def fits(sigma: float, groups: int, centre: bool, starts: int = 16, seed: int = 0) -> list:
    """Least-squares fits of the tap pattern to a sampled Gaussian: [(pipeline, metrics)]."""
    rng = np.random.default_rng(seed)
    nw = groups + (1 if centre else 0)
    R = int(np.ceil(4 * sigma)) + 3
    y, x_ = np.mgrid[-R:R + 1, -R:R + 1]
    g = np.exp(-(x_ ** 2 + y ** 2) / (2 * sigma * sigma))
    g /= g.sum()
    M_ = 64
    f = np.fft.fftfreq(M_)
    stop = np.sqrt(f[:, None] ** 2 + f[None, :] ** 2) > GAUSS_STOP / sigma
    out = []
    for _ in range(starts):
        r = sigma * (0.5 + 1.5 * rng.random(groups))
        th = rng.random(groups) * np.pi / 2
        x0 = np.concatenate([np.stack([r * np.cos(th), r * np.sin(th)], 1).ravel(), rng.normal(0, 0.5, nw)])
        def resid(v):
            k = kernel(build(v, groups, centre), R)
            var = (k * (x_ ** 2 + y ** 2)).sum() / 2
            spec = np.abs(np.fft.fft2(k, s=(M_, M_)))[stop]  # stop-band leakage
            return np.concatenate([(k - g).ravel(), [0.5 * (np.sqrt(var) / sigma - 1.0)], 0.05 * spec])

        res = least_squares(resid, x0,
                            bounds=([-R + 2] * (2 * groups) + [-20] * nw, [R - 2] * (2 * groups) + [20] * nw))
        pl = build(res.x, groups, centre)
        out.append((pl, metrics(pl, sigma)))
    return out


def best_for(sigma: float, groups: int, centre: bool, prof: dict, starts: int = 16, seed: int = 0):
    pl, q = min(fits(sigma, groups, centre, starts, seed), key=lambda t: score(t[1], prof))
    return score(q, prof), None, pl


def main():
    sigmas = np.round(np.arange(0.5, 2.51, 0.1), 2)
    rows, report = [], {}
    for groups, centre in CONFIGS:
        n = 4 * groups + (1 if centre else 0)
        top = {p: None for p in PROFILES}
        misses = 0
        for s in sigmas:
            fl = fits(float(s), groups, centre, starts=24)
            any_ok = False
            for pname, prof in PROFILES.items():
                pl, q = min(fl, key=lambda t: score(t[1], prof))
                if score(q, prof) <= 1.0:
                    top[pname] = (float(s), pl, q)
                    any_ok = True
            print(f"{n:2d} fetches sigma {s:.1f}: " + ", ".join(
                f"{p} {'ok' if top[p] and top[p][0] == s else '-'}" for p in PROFILES), flush=True)
            misses = 0 if any_ok else misses + 1
            if misses >= 3:
                break
        for pname in PROFILES:
            if top[pname]:
                s, pl, q = top[pname]
                c = pipeline_cost(pl)
                rows.append(f"| {n} | {pname} | {s:.1f} | {c['us']:.0f} | {q['leak']:.3f} | {q['tv']:.3f} | "
                            f"{q['curv']:.2f} | " + "; ".join(f"({dx:.3f}, {dy:.3f}) w {w:.4f}"
                                                                for dx, dy, w in pl.passes[0].taps[::4]) + " |")
                report[f"{n}_{pname}"] = {"sigma": s, "taps": pl.passes[0].taps, **q, "us": c["us"]}
            else:
                rows.append(f"| {n} | {pname} | none | | | | | |")
    md = ["# Single-pass pinwheel blurs fused into the composite (1080p model)", "",
          "Largest sigma per fetch count that meets each profile. Taps: one per 90-degree",
          "group (the other three are its rotations) and the centre (if any) last.", "",
          "| fetches | profile | max sigma | marginal us | leak | tv | curv | taps (per group) |",
          "|---:|---|---:|---:|---:|---:|---:|---|"] + rows
    (OUT / "small_kernels.md").write_text("\n".join(md) + "\n")
    (OUT / "small_kernels.json").write_text(json.dumps(report, indent=1))
    print("\n".join(md))


if __name__ == "__main__":
    main()
