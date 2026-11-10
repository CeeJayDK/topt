"""Estimated cost of fx/TOPT_Clarity.fx (cost model, topt.cost), per core GPU: the blur passes on the whole
screen (two channels, RG16F: 4 bytes like the blur's RGB10A2) and the final pass (the upsample's reads, the
screen read, the base layer). Each GPU's class from TOPT_Blur's tables. Writes results/clarity_cost.md.

    python -m scripts.clarity_cost
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from scripts import make_effect as ME
from scripts.movienight_cost import class_for
from topt.cost import BYTES_PER_PIXEL, CORE, FORMAT_BYTES, SCREEN_FORMAT, _pass_time, pass_format

ROOT = Path(__file__).resolve().parent.parent


def cost(gpu, pl, W, H) -> float:
    total = 0.0
    last = len(pl.passes) - 1
    for i, p in enumerate(pl.passes):
        sd = pl.src_div(i)
        j = pl.src_index(i)
        sfmt = pass_format(pl.passes[j]) if j >= 0 else SCREEN_FORMAT
        taps = len(p.taps)
        nd = (W // p.div) * (H // p.div)
        ns = (W // sd) * (H // sd)
        if i < last:
            ns_read = min(ns, nd * taps * 4)
            total += _pass_time(max(1, nd), ns_read, taps, gpu, 4, ns_read * FORMAT_BYTES[sfmt], "RG16F")[0]
        else:  # final: the upsample's taps + the screen pixel, written to the screen
            rb = min(ns, nd * taps) * 4 + nd * BYTES_PER_PIXEL
            total += _pass_time(nd, 0, taps + 1, gpu, FORMAT_BYTES[SCREEN_FORMAT], rb, SCREEN_FORMAT)[0]
    return total * 1e6


def main():
    tables = json.loads((ROOT / "results" / "topt_blur_tables.json").read_text())
    rmax = math.ceil(ME.TRUNC * ME.SL_MAX)
    lines = ["# TOPT Clarity: cost (estimate)", "",
             "Cost model estimate (us) of the whole technique: blur passes on (brightness, square) in RG16F,",
             "then the final pass. Each GPU's class from TOPT_Blur's tables, by CLARITY_SIZE (sigma at 1080p).", ""]
    for res, (W, H) in (("1080p", (1920, 1080)), ("4K", (3840, 2160))):
        sizes = (8, 24, 64)
        lines += [f"## {res}", "", "| GPU | " + " | ".join(f"size {s}" for s in sizes) + " |", "|---|" + "---:|" * len(sizes)]
        for g, gpu in CORE.items():
            row = []
            for size in sizes:
                sig = round(size * H / 1080)
                name, sep, sl = class_for(g, sig, tables)
                row.append(f"{cost(gpu, ME.pipeline(name, sl, rmax, sep), W, H):.0f}")
            lines.append(f"| {g} | " + " | ".join(row) + " |")
        lines.append("")
    (ROOT / "results" / "clarity_cost.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
