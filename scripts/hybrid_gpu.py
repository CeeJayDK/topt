"""The hybrid down/blur/up search on every GPU profile at once (1080p and 4K).

    python -m scripts.hybrid_gpu [sigma ...]

Quality does not depend on the GPU, so each design is fitted once and priced on every profile
(topt/gpu_profiles.json) at both resolutions; the search goes on until every GPU / resolution has
found its cheapest strict design (topt.search.search_multi). Writes results/hybrid_gpu.json (every
evaluated candidate, cost per target) and results/hybrid_gpu.md (the cheapest design per profile).
"""
from __future__ import annotations

import json
import os
import sys
import time
from multiprocessing import Pool
from pathlib import Path

from topt.cost import PROFILES as GPUS, RESOLUTIONS
from topt.search import PROFILES, passes_profile, search_multi

from .common import parse_args
from .hybrid import SIGMAS

OUT = Path(__file__).resolve().parent.parent / "results"
RES = ("1080p", "4k")


def targets() -> list:
    return [(f"{g}@{r}", GPUS[g], *RESOLUTIONS[r]) for g in GPUS for r in RES]


def _run(s):
    return s, search_multi(s, targets())


def main():
    sigmas = parse_args(SIGMAS)[0]
    path = OUT / "hybrid_gpu.json"
    allrecs = json.loads(path.read_text()) if path.exists() else {}
    t0 = time.time()
    with Pool(min(len(sigmas), os.cpu_count() or 1)) as pool:
        for s, recs in pool.imap_unordered(_run, sigmas):
            allrecs[f"{s:g}"] = recs
            print(f"sigma {s:g}: {len(recs)} evaluated ({time.time() - t0:.0f}s elapsed)", file=sys.stderr, flush=True)
            path.write_text(json.dumps(allrecs, default=str))
    write_md(allrecs)


def write_md(allrecs: dict):
    lines = ["# Hybrid search per GPU profile", "",
             "Cheapest design per GPU that meets the profile; us = marginal cost over that GPU's plain",
             "composite pass. GPUs with the same winner are listed together.", ""]
    for prof in ("medium", "strict"):
        for res in RES:
            lines += [f"## {prof}, {res}", "", "| sigma | design | GPUs (us) |", "|---:|---|---|"]
            for s in sorted(allrecs, key=float):
                ok = [r for r in allrecs[s] if passes_profile(r, PROFILES[prof])]
                if not ok:
                    lines.append(f"| {s} | none found | |")
                    continue
                win = {}
                for g in GPUS:
                    r = min(ok, key=lambda r: r["us_by"][f"{g}@{res}"])
                    win.setdefault(r["design"], []).append(f"{g} {r['us_by'][f'{g}@{res}']:.0f}")
                for i, (d, gs) in enumerate(sorted(win.items(), key=lambda kv: -len(kv[1]))):
                    lines.append(f"| {s if i == 0 else ''} | {d} | {', '.join(gs)} |")
            lines.append("")
    (OUT / "hybrid_gpu.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    if "--md" in sys.argv:
        write_md(json.loads((OUT / "hybrid_gpu.json").read_text()))
    else:
        main()
