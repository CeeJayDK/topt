"""Estimated cost of fx/MovieNight.fx's soft glow options (cost model, topt.cost).

    python -m scripts.movienight_cost

2.39:1 video on a 16:9 screen (top and bottom bars), MOVIENIGHT_BLUR_SIZE 32, each core GPU's class from
TOPT_Blur's tables (results/topt_blur_tables.json). The blur passes draw only the strips the bars show
plus the reach (MN_StripVS), so their pixels and reads are scaled by the strips' share of the screen; the
bars pass draws the bars only. Options: no soft glow, 1 ring (8 more bilinear reads per bar pixel),
2 frosted-glass scatter (one more noise read), and 0.4f's second blur level (three extra passes at 4 x
coarser resolution over strips widened by its reach). Writes results/movienight_cost.md.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from scripts import make_effect as ME
from topt.cost import BYTES_PER_PIXEL, CORE, FORMAT_BYTES, SCREEN_FORMAT, _pass_time, pass_format

ROOT = Path(__file__).resolve().parent.parent
SIZE = 32
ASPECT = 2.39


def class_for(gpu: str, sig: int, tables: dict) -> tuple:
    table = next((t for names, t in tables["tables"] if gpu in names), tables["default"])
    name, sep = next(c for a, b, c in table if a <= sig <= b)
    C, B, lo, hi = tables["info"][name][:4]
    return name, sep, min(hi, max(lo, math.sqrt(max(sig * sig - C, 0.0) / B)))


def strips(W: int, H: int, T: int, reach: float) -> float:
    """Share of the screen the strip passes draw (top + bottom strips, cut to the picture)."""
    d = 2 * T / H
    shown = T * (1 - d)                  # picture strip a bar shows (px)
    return min(H - 2 * T, 2 * (shown + reach)) * W / (W * H)


def cost(gpu, pl, W, H, T, frac, extra_taps=0.0, soft_old=None) -> float:
    """us of the Movie Night technique: blur passes on the strips, then the bars pass."""
    total = 0.0
    last = len(pl.passes) - 1
    for i, p in enumerate(pl.passes):
        sd = pl.src_div(i)
        j = pl.src_index(i)
        sfmt = pass_format(pl.passes[j]) if j >= 0 else SCREEN_FORMAT
        taps = len(p.taps)
        if i < last:
            nd = (W // p.div) * (H // p.div) * frac
            ns = (W // sd) * (H // sd) * frac
            ns_read = min(ns, nd * taps * 4)
            wfmt = pass_format(p)
            total += _pass_time(max(1, int(nd)), ns_read, taps, gpu, FORMAT_BYTES[wfmt],
                                ns_read * FORMAT_BYTES[sfmt], wfmt)[0]
        else:  # bars: the final upsample + the screen + the dither noise + the soft glow's reads
            nd = 2 * T * W
            taps += 2 + extra_taps
            rb = min((W // sd) * (H // sd) * frac, nd * taps) * FORMAT_BYTES[sfmt] + nd * BYTES_PER_PIXEL
            total += _pass_time(nd, 0, taps, gpu, FORMAT_BYTES[SCREEN_FORMAT], rb, SCREEN_FORMAT)[0]
    if soft_old:  # 0.4f: 4x4 box, H and V Gaussians (9 taps each) at 4 x the low level's division
        div, sfrac = soft_old
        nd = (W // div) * (H // div) * sfrac
        for taps in (4, 9, 9):
            total += _pass_time(max(1, int(nd)), nd * taps, taps, gpu, 4, nd * 4 * min(taps, 4), "RGB10A2")[0]
    return total * 1e6


def main():
    tables = json.loads((ROOT / "results" / "topt_blur_tables.json").read_text())
    rmax = math.ceil(ME.TRUNC * ME.SL_MAX)
    lines = ["# Movie Night: soft glow cost (estimate)", "",
             f"Cost model estimate, 2.39:1 video on 16:9 (top and bottom bars), MOVIENIGHT_BLUR_SIZE {SIZE},",
             "Soft glow 1, each GPU's class from TOPT_Blur's tables. us for the whole technique (blur passes on",
             "the strips + the bars pass); in brackets the extra over no soft glow. Ring: 8 more bilinear reads",
             "per bar pixel (the upsample's reads skipped from 27 % into the bar on); frost: one noise read and the scattered read (TOPT_BlurResolve as before); 0.4f:",
             "the earlier second blur level (three passes at 4 x coarser resolution, strips widened by its reach).",
             "Both new options also widen the strips by their radius (2.5 sigma).", ""]
    for res, (W, H) in (("1080p", (1920, 1080)), ("4K", (3840, 2160))):
        T = round(H * (1 - 16 / 9 / ASPECT) / 2)
        sig = round(SIZE * H / 1080)
        lines += [f"## {res} (bars {T} px, sigma {sig} px)", "",
                  "| GPU | class | no soft glow | 1 ring | 2 frost | 0.4f second level |", "|---|---|---:|---:|---:|---:|"]
        for g, gpu in CORE.items():
            name, sep, sl = class_for(g, sig, tables)
            pl = ME.pipeline(name, sl, rmax, sep)
            divl = max(p.div for p in pl.passes)
            reach = 3 * sig + 2 * divl
            base = cost(gpu, pl, W, H, T, strips(W, H, T, reach))
            # the ring takes over from the upsample (skipped) once its radius is sigma / 2: 27 % into the bar
            ring = cost(gpu, pl, W, H, T, strips(W, H, T, reach + 2.5 * sig), 8 - 0.73 * len(pl.passes[-1].taps))
            frost = cost(gpu, pl, W, H, T, strips(W, H, T, reach + 2.5 * sig), 1)
            sdiv = 4 * divl
            soft = math.sqrt(sig ** 2 + (sdiv * 2.5) ** 2)
            sreach = 3 * soft + 2 * sdiv
            old = cost(gpu, pl, W, H, T, strips(W, H, T, sreach), 1, (sdiv, strips(W, H, T, sreach)))
            lines.append(f"| {g} | {name}{' sep' if sep else ''} | {base:.0f} | {ring:.0f} (+{ring - base:.0f}) "
                         f"| {frost:.0f} (+{frost - base:.0f}) | {old:.0f} (+{old - base:.0f}) |")
        lines.append("")
    (ROOT / "results" / "movienight_cost.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
