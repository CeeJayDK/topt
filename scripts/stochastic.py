"""Search stochastic / interleaved sparse blurs.

F1  one interleaved pass inside the composite (small sigma)
F2  down (box*binomial) -> interleaved sparse blur at low res -> upsample in the
    composite; the upsample footprint spans several pattern variants and so
    averages the pattern noise.

    python -m scripts.stochastic [sigma ...]

Writes results/stochastic.json and results/stochastic.md.
"""
from __future__ import annotations

import itertools
import json
import math
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

from topt import patterns as P
from topt import search as S
from topt.cost import pipeline_cost
from topt.methods import bisect
from topt.quality import default_phases, eval_radius, measured_sigma, metrics
from topt.sim import Pass, Pipeline

OUT = Path(__file__).resolve().parent.parent / "results"
SIGMAS = [1, 1.5, 2, 3, 4, 6, 8, 12, 16]
_BASE = {}


def base_points(gen: str, n: int):
    if (gen, n) not in _BASE:
        _BASE[(gen, n)] = P.GENERATORS[gen](n)
    return _BASE[(gen, n)]


def interleaved(gen, n, mapping, k, tile, sel, s, div) -> Pass:
    base = P.to_gaussian(base_points(gen, n), s, k, mapping)
    vmap, nv = P.selector(sel, tile)
    var = P.variants(base, nv)
    return Pass(div, var[0], variants=var, tile=tile, vmap=vmap, sel=sel)


def build(cfg: dict, s: float) -> Pipeline:
    if cfg["fam"] == "F1":
        passes = [interleaved(cfg["gen"], cfg["n"], cfg["map"], cfg["k"], cfg["tile"], cfg["sel"], s, 1)]
    else:
        f = cfg["f"]
        up = tuple(S.UP_PIN[cfg["up"]]) if cfg["up"] > 3 else S.outer(S.up_taps_1d(cfg["up"]))
        passes = [Pass(f, S.outer(S.down_taps_1d(f, cfg["e"]))),
                  interleaved(cfg["gen"], cfg["n"], cfg["map"], cfg["k"], cfg["tile"], cfg["sel"], s, f),
                  Pass(1, up)]
    return Pipeline("stochastic", {**cfg, "s": s}, passes)


def label(c: dict) -> str:
    pat = f"{c['gen']} {c['n']} {c['map'][:3]} k{c['k']:g} tile {c['tile']}{c['sel'][0]}"
    if c["fam"] == "F1":
        return f"single pass: {pat}"
    u = f"p{c['up']}" if c["up"] > 3 else f"e{c['up']}"
    return f"down {c['f']} e{c['e']} | {pat} | up {c['f']} {u}"


def configs(sigma: float):
    gens, maps = ("vogel", "sot", "r2"), ("importance", "weighted")
    if sigma <= 4:
        for gen, n, mp, tile in itertools.product(gens, (4, 6, 8), maps, (2, 4)):
            yield {"fam": "F1", "gen": gen, "n": n, "map": mp, "k": 3.0, "tile": tile, "sel": "bayer"}
    for f in (2, 4, 8):
        if not 1.0 <= sigma / f <= 6:
            continue
        for gen, n, mp, tile, up in itertools.product(gens, (4, 8, 12, 16), maps, (2, 4), (2, 4, 8, 9)):
            yield {"fam": "F2", "f": f, "e": 3, "gen": gen, "n": n, "map": mp, "k": 3.0, "tile": tile,
                   "sel": "bayer", "up": up}


def fit(cfg: dict, sigma: float):
    F = build(cfg, 1.0).max_div
    ph, rad = default_phases(F, min(F, 4)), eval_radius(sigma, F)
    div = 1 if cfg["fam"] == "F1" else cfg["f"]
    s = bisect(lambda s: measured_sigma(build(cfg, s), ph, rad), sigma, 0.05, 3.0 * sigma / div + 2, 22)
    if s is None:
        return None
    pl = build(cfg, s)
    return pl, metrics(pl, sigma)


def run_sigma(sigma: float) -> list:
    out = []
    for cfg in configs(sigma):
        r = fit(cfg, sigma)
        if r is None:
            continue
        pl, q = r
        c = pipeline_cost(pl)
        out.append({"design": label(cfg), "params": pl.params, "us": c["us"], "passes": c["passes"], **q})
    return out


def _run(s):
    return s, run_sigma(s)


def write_md(allrecs: dict):
    hyb = json.loads((OUT / "hybrid.json").read_text()) if (OUT / "hybrid.json").exists() else {}
    lines = ["# Stochastic / interleaved sparse blurs (GTX 1660 model, 1080p)", "",
             "us = marginal cost over a plain composite pass. 'noise-blind' ignores the",
             "shift-variance metrics (phase, block) that measure the static pattern noise.", "",
             "| sigma | profile | us | design | phase | block | leak | tv | iso | best non-stochastic |",
             "|---:|---|---:|---|---:|---:|---:|---:|---:|---|"]
    blind = {n: {k: v for k, v in p.items() if k not in ("phase", "block")} for n, p in S.PROFILES.items()}
    for s in sorted(allrecs, key=float):
        recs = allrecs[s]
        for name, prof in list(S.PROFILES.items()) + [(f"{n} noise-blind", p) for n, p in blind.items()]:
            ok = [r for r in recs if S.passes_profile(r, prof)
                  and ("blind" in name or r["block"] <= S.NOISE_BLOCK_MAX)]
            ref = [r for r in hyb.get(s, []) if S.passes_profile(r, S.PROFILES[name.split()[0]])]
            refs = f"{min(r['us'] for r in ref):.0f} us" if ref else "-"
            if ok:
                r = min(ok, key=lambda r: r["us"])
                lines.append(f"| {s} | {name} | {r['us']:.0f} | {r['design']} | {r['phase']:.3f} | {r['block']:.2f} | "
                             f"{r['leak']:.3f} | {r['tv']:.3f} | {r['iso']:.3f} | {refs} |")
            else:
                lines.append(f"| {s} | {name} | | none | | | | | | {refs} |")
    (OUT / "stochastic.md").write_text("\n".join(lines) + "\n")


def main():
    sigmas = [float(a) for a in sys.argv[1:]] or SIGMAS
    path = OUT / "stochastic.json"
    allrecs = json.loads(path.read_text()) if path.exists() else {}
    t0 = time.time()
    with Pool(min(len(sigmas), os.cpu_count() or 1)) as pool:
        for s, recs in pool.imap_unordered(_run, sigmas):
            allrecs[f"{s:g}"] = recs
            print(f"sigma {s:g}: {len(recs)} evaluated ({time.time() - t0:.0f}s)", file=sys.stderr, flush=True)
            path.write_text(json.dumps(allrecs, default=str))
    write_md(allrecs)


if __name__ == "__main__":
    main()
