"""Roofline-style GPU time estimate for a pipeline of full-screen passes.

Per pass:  overhead + max(texture-unit time, DRAM time, ROP time)
* texture-unit time: one bilinear fetch per tap per output pixel (32 bpp is full
  rate on Turing).
* DRAM time: write every output pixel once + read each source texel at most
  once (texture cache assumed to catch the overlap between neighbouring pixels).
* overhead: fixed per-pass cost (pipeline drain between dependent passes, render
  target switch, small-target under-utilisation). Placeholder until calibrated.
"""
from __future__ import annotations

from dataclasses import dataclass

from .sim import Pipeline


@dataclass(frozen=True)
class GPU:
    name: str
    tex_rate: float        # bilinear fetches / s
    bandwidth: float       # effective DRAM bytes / s
    rop_rate: float        # pixels written / s
    pass_overhead: float   # s per pass (to calibrate on hardware)


# GTX 1660: 88 TMUs, 48 ROPs, ~1.785 GHz boost, 192-bit GDDR5 @ 8 Gbps = 192 GB/s.
GTX1660 = GPU("GTX 1660", 88 * 1.785e9, 0.8 * 192e9, 48 * 1.785e9, 5e-6)

BYTES_PER_PIXEL = 4  # RGB10A2


def pipeline_cost(pl: Pipeline, W: int = 1920, H: int = 1080, gpu: GPU = GTX1660) -> dict:
    total = fetches = dram = 0.0
    bounds = []
    for i, p in enumerate(pl.passes):
        sd = pl.src_div(i)
        nd = (W // p.div) * (H // p.div)
        ns = (W // sd) * (H // sd)
        taps = len(p.taps)
        t_tex = nd * taps / gpu.tex_rate
        bytes_ = (nd + min(ns, nd * taps * 4)) * BYTES_PER_PIXEL
        t_mem = bytes_ / gpu.bandwidth
        t_rop = nd / gpu.rop_rate
        t = max(t_tex, t_mem, t_rop)
        bounds.append("tex" if t == t_tex else "mem" if t == t_mem else "rop")
        total += gpu.pass_overhead + t
        fetches += nd * taps
        dram += bytes_
    return {
        "us": total * 1e6,
        "passes": len(pl.passes),
        "fetch_per_px": fetches / (W * H),   # fetches normalised to full-res pixels
        "dram_mb": dram / 1e6,
        "bounds": bounds,
    }
