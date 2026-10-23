"""TOPT_Blur's class choice across GPU architectures.

    python -m scripts.multi_gpu

For every integer screen sigma 2..200 and every candidate (class, separable), the cost on each
GPU profile (topt/gpu_profiles.json) at 1080p and 4K. Regret = extra time over the cheapest
candidate on that GPU, in percent of its plain composite pass (so cards of every speed count the
same). The robust choice minimises the mean regret over GPUs and resolutions; it is compared with
the effect's current choice (GTX 1660 model) and each GPU's own best.

Writes results/multi_gpu.json and results/multi_gpu.md.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from scripts import make_effect as ME
from topt.cost import PROFILES, RESOLUTIONS, composite_baseline, pipeline_cost

OUT = Path(__file__).resolve().parent.parent / "results"
RES = ("1080p", "4k")
SIGMAS = range(2, 201)


def label(name: str, sep: bool) -> str:
    return name + (" sep" if sep else "")


def main():
    rmax = math.ceil(ME.TRUNC * ME.SL_MAX)
    info = ME.class_info(rmax)
    gpus = list(PROFILES)
    rows = {}
    for sig in SIGMAS:
        opts = ME.options(info, sig, rmax)
        cost = np.array([[[pipeline_cost(p, *RESOLUTIONS[r], gpu=PROFILES[g])["us"] for r in RES] for g in gpus]
                         for _, _, p in opts])            # option x gpu x resolution
        base = np.array([[composite_baseline(*RESOLUTIONS[r], PROFILES[g]) * 1e6 for r in RES] for g in gpus])
        regret = 100 * (cost - cost.min(0)) / base
        mean = regret.mean((1, 2))
        # current rule (GTX 1660 model): separable only when >= 3 us cheaper
        cur = None
        for i in range(0, len(opts), 2):
            us2d, ussep = (pipeline_cost(opts[j][2])["us"] for j in (i, i + 1))
            k, us = (i + 1, ussep) if ussep < us2d - 3.0 else (i, us2d)
            if cur is None or us < cur[1]:
                cur = (k, us)
        rob = int(np.argmin(mean))
        rows[sig] = {
            "current": label(*opts[cur[0]][:2]), "robust": label(*opts[rob][:2]),
            "current_mean": float(mean[cur[0]]), "current_max": float(regret[cur[0]].max()),
            "robust_mean": float(mean[rob]), "robust_max": float(regret[rob].max()),
            "per_gpu_best": {g: label(*opts[int(np.argmin(cost[:, j, 0]))][:2]) for j, g in enumerate(gpus)},
            "current_regret": {g: [round(float(x), 1) for x in regret[cur[0], j]] for j, g in enumerate(gpus)},
        }
        print(sig, rows[sig]["current"], "->", rows[sig]["robust"],
              f"mean {rows[sig]['current_mean']:.1f} -> {rows[sig]['robust_mean']:.1f} %", flush=True)
    (OUT / "multi_gpu.json").write_text(json.dumps(rows, indent=1))
    write_md(rows, gpus)


def intervals(rows: dict, key) -> list:
    out = []
    for sig, r in rows.items():
        k = key(r)
        if out and out[-1][2] == k:
            out[-1][1] = sig
        else:
            out.append([sig, sig, k])
    return out


def write_md(rows: dict, gpus: list):
    from topt.cost import PROFILES as P
    rows = {int(k): v for k, v in rows.items()}
    lines = ["# TOPT_Blur class choice across GPU architectures", "",
             "Regret = extra time over the cheapest candidate on that GPU, in % of its plain composite pass",
             "(1080p and 4K). Current = the effect's choice (GTX 1660 model); robust = least mean regret over",
             "the GPUs below. Profiles from TexBench reports (`python -m scripts.gpu_profiles`).", "",
             "| sigma | current | robust | mean regret current -> robust | worst GPU regret current -> robust |",
             "|---|---|---|---|---|"]
    for a, b, (cur, rob) in intervals(rows, lambda r: (r["current"], r["robust"])):
        rs = [rows[s] for s in range(a, b + 1)]
        cm, rm = max(r["current_mean"] for r in rs), max(r["robust_mean"] for r in rs)
        cx, rx = max(r["current_max"] for r in rs), max(r["robust_max"] for r in rs)
        lines.append(f"| {a}–{b} | {cur} | {rob} | {cm:.1f} -> {rm:.1f} % | {cx:.0f} -> {rx:.0f} % |")
    lines += ["", "Worst regret of the current choice per GPU (1080p / 4K, % of a composite pass), and the sigma:", "",
              "| GPU | architecture | worst 1080p | worst 4K | pass overhead |", "|---|---|---|---|---|"]
    for g in gpus:
        w = [max((rows[s]["current_regret"][g][i], s) for s in rows) for i in (0, 1)]
        lines.append(f"| {g} | {json.loads((Path(__file__).resolve().parent.parent / 'topt' / 'gpu_profiles.json').read_text())[g]['arch']} "
                     f"| {w[0][0]:.0f} % (sigma {w[0][1]}) | {w[1][0]:.0f} % (sigma {w[1][1]}) "
                     f"| {P[g].pass_overhead * 1e6:.1f} us |")
    (OUT / "multi_gpu.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    import sys
    if "--md" in sys.argv:
        write_md(json.loads((OUT / "multi_gpu.json").read_text()), list(PROFILES))
    else:
        main()
