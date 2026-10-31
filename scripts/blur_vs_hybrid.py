"""TOPT_Blur's per-GPU class choice against the per-GPU hybrid search winners.

    python -m scripts.blur_vs_hybrid

For every sigma of results/hybrid_gpu_best.json and every GPU profile / resolution there: the class
TOPT_Blur picks for that GPU (scripts.make_effect's rule: least regret over 1080p and 4K, the separable
variant only when it saves SEP_MARGIN), its cost, and the cheapest hybrid design that meets the same
quality profile (medium, the classes' target), rebuilt from its parameters and priced with the current
profiles (the search ran on earlier ones). Writes results/blur_vs_hybrid.md.
"""
from __future__ import annotations

import json
import math
import statistics
from pathlib import Path

import numpy as np

from scripts import make_effect as ME
from topt import search as S
from topt.cost import CORE as PROFILES, RESOLUTIONS, composite_baseline, pipeline_cost

OUT = Path(__file__).resolve().parent.parent / "results"
RES = ME.TABLE_RES


def pick(opts: list, g: str) -> int:
    cost = np.array([[pipeline_cost(p, *RESOLUTIONS[r], gpu=PROFILES[g])["us"] for r in RES] for _, _, p in opts])
    base = np.array([composite_baseline(*RESOLUTIONS[r], PROFILES[g]) * 1e6 for r in RES])
    regret = (100 * (cost - cost.min(0)) / base).mean(1)
    regret[1::2] += ME.SEP_MARGIN
    return int(np.argmin(regret))


def main():
    rmax = math.ceil(ME.TRUNC * ME.SL_MAX)
    info = ME.class_info(rmax)
    best = json.loads((OUT / "hybrid_gpu_best.json").read_text())
    rows = []
    for s in sorted(best, key=float):
        opts = ME.options(info, int(float(s)), rmax)
        hyb = best[s]["medium"]
        if not opts or not hyb:
            continue
        for g in PROFILES:
            k = pick(opts, g)
            name, sep, pl = opts[k]
            for r in RES:
                h = hyb.get(f"{g}@{r}")
                if h:
                    d = next(x for x in S.designs(float(s)) if x.label() == h["design"])
                    hus = pipeline_cost(S.build(d, h["params"]["sl"]), *RESOLUTIONS[r], gpu=PROFILES[g])["us"]
                    us = pipeline_cost(pl, *RESOLUTIONS[r], gpu=PROFILES[g])["us"]
                    base = composite_baseline(*RESOLUTIONS[r], PROFILES[g]) * 1e6
                    rows.append((float(s), g, r, name + (" sep" if sep else ""), us, h["design"], hus, base))
    write_md(rows)


def write_md(rows: list):
    lines = ["# TOPT_Blur against the hybrid search, per GPU", "",
             "TOPT_Blur's class for each GPU profile (its per-GPU table rule) against the cheapest hybrid design",
             "meeting the medium profile on that GPU (results/hybrid_gpu_best.json). us = marginal cost over the",
             "GPU's plain composite pass; gain = (TOPT_Blur - hybrid) in % of the composite pass.", ""]
    for r in RES:
        lines += [f"## {r}", "", "| sigma | median gain | worst GPU for TOPT_Blur | TOPT_Blur us | hybrid us | hybrid design |",
                  "|---:|---:|---|---:|---:|---|"]
        for s in sorted({x[0] for x in rows}):
            sel = [x for x in rows if x[0] == s and x[2] == r]
            gains = [100 * (x[4] - x[6]) / x[7] for x in sel]
            w = sel[int(np.argmax(gains))]
            lines.append(f"| {s:g} | {statistics.median(gains):+.1f} % | {w[1]} ({w[3]}): {max(gains):+.1f} % "
                         f"| {w[4]:.0f} | {w[6]:.0f} | {w[5].replace(' | ', ' / ')} |")
        lines.append("")
    lines += ["## Every GPU", "", "| sigma | res | GPU | TOPT_Blur class | TOPT_Blur us | hybrid us | gain | hybrid design |",
              "|---:|---|---|---|---:|---:|---:|---|"]
    for s, g, r, cls, us, d, hus, base in rows:
        lines.append(f"| {s:g} | {r} | {g} | {cls} | {us:.0f} | {hus:.0f} | {100 * (us - hus) / base:+.1f} % "
                     f"| {d.replace(' | ', ' / ')} |")
    (OUT / "blur_vs_hybrid.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:60]))


if __name__ == "__main__":
    main()
