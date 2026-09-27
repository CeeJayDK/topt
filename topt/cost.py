"""Roofline-style GPU time estimate for a pipeline of full-screen passes.

Per pass:  overhead + max(texture-unit time, DRAM time, ROP time)
* texture-unit time: one bilinear fetch per tap per output pixel (32 bpp is full
  rate on Turing).
* DRAM time: write every output pixel once + read each source texel at most
  once (texture cache assumed to catch the overlap between neighbouring pixels).
* overhead: fixed per-pass cost (pipeline drain between dependent passes, render
  target switch, small-target under-utilisation). Placeholder until calibrated.

Target use: the blur feeds a consumer (composite) pass that writes the screen.
The pipeline's last pass *is* that pass: it also reads the backbuffer (+1 fetch,
+1 full-res read). `us` is the marginal cost over a plain composite pass
(read backbuffer + write screen); `us_total` includes it.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .sim import Pipeline


@dataclass(frozen=True)
class GPU:
    name: str
    tex_rate: float        # bilinear fetches / s
    bandwidth: float       # effective DRAM bytes / s
    rop_rate: float        # pixels written / s
    pass_overhead: float   # s per pass (to calibrate on hardware)
    lds_rate: float = 0.0  # groupshared texel reads / s (compute shaders)
    lds_bytes: int = 32768 # groupshared memory per thread group (D3D11 limit)


# GTX 1660: 22 SMs, 88 TMUs, 48 ROPs, ~1.785 GHz boost, 192-bit GDDR5 @ 8 Gbps
# = 192 GB/s (80 % assumed achievable). LDS: 128 B/clk/SM, texel stored as
# fp16x4 (8 B) -> 16 texel reads/clk/SM.
GTX1660 = GPU("GTX 1660", 88 * 1.785e9, 0.8 * 192e9, 48 * 1.785e9, 5e-6, 22 * 16 * 1.785e9)

BYTES_PER_PIXEL = 4  # RGB10A2 / R11G11B10F / RGBA8 backbuffer
RESOLUTIONS = {"1080p": (1920, 1080), "1440p": (2560, 1440), "4k": (3840, 2160)}


def _pass_time(nd: int, ns_read: int, taps: int, gpu: GPU) -> tuple:
    t_tex = nd * taps / gpu.tex_rate
    t_mem = (nd + ns_read) * BYTES_PER_PIXEL / gpu.bandwidth
    t_rop = nd / gpu.rop_rate
    t = max(t_tex, t_mem, t_rop)
    return gpu.pass_overhead + t, ("tex" if t == t_tex else "mem" if t == t_mem else "rop")


def composite_baseline(W: int, H: int, gpu: GPU) -> float:
    """A plain full-screen pass: read the backbuffer once, write the screen."""
    return _pass_time(W * H, W * H, 1, gpu)[0]


def pipeline_cost(pl: Pipeline, W: int = 1920, H: int = 1080, gpu: GPU = GTX1660,
                  composite: bool = True) -> dict:
    total = fetches = dram = 0.0
    bounds = []
    last = len(pl.passes) - 1
    for i, p in enumerate(pl.passes):
        sd = pl.src_div(i)
        nd = (W // p.div) * (H // p.div)
        ns = (W // sd) * (H // sd)
        taps = len(p.taps)
        ns_read = min(ns, nd * taps * 4)
        if composite and i == last:
            taps += 1
            ns_read += W * H
        t, b = _pass_time(nd, ns_read, taps, gpu)
        bounds.append(b)
        total += t
        fetches += nd * taps
        dram += (nd + ns_read) * BYTES_PER_PIXEL
    base = composite_baseline(W, H, gpu) if composite else 0.0
    return {
        "us": (total - base) * 1e6,
        "us_total": total * 1e6,
        "passes": len(pl.passes),
        "fetch_per_px": fetches / (W * H),   # fetches normalised to full-res pixels
        "dram_mb": dram / 1e6,
        "bounds": bounds,
    }


def cs_tile_sep_cost(r: int, W: int = 1920, H: int = 1080, gpu: GPU = GTX1660) -> dict:
    """Single compute dispatch for a separable (2r+1)-tap kernel on a TxT tile,
    followed by the mandatory composite pixel shader (compute cannot write the
    screen), which here also has to read the compute output.

    'lds'  : load tile + halo into groupshared (1 point fetch per texel), then
             run H and V in groupshared memory.
    'texH' : H pass straight from the texture with linear-pair taps ((r+1) per
             output, over the halo rows), store to groupshared, V pass there.
    T is the best power of two whose groupshared tile fits (8 B per texel).
    """
    n = W * H
    t_mem = 2 * n * BYTES_PER_PIXEL / gpu.bandwidth
    final = _pass_time(n, 2 * n, 2, gpu)[0]  # composite reading CS output + backbuffer
    best = None
    for T in (8, 16, 32, 64, 128):
        side = T + 2 * r
        opts = []
        if side * side * 8 <= gpu.lds_bytes:
            opts.append(("lds", n * (side / T) ** 2 / gpu.tex_rate,
                         n * (2 * r + 1) * (2 + 2 * r / T) / gpu.lds_rate))
        if side * T * 8 <= gpu.lds_bytes:
            opts.append(("texH", n * (r + 1) * (side / T) / gpu.tex_rate,
                         n * (2 * r + 1) / gpu.lds_rate))
        for kind, t_tex, t_lds in opts:
            t = gpu.pass_overhead + max(t_tex, t_mem, t_lds) + final
            us = (t - composite_baseline(W, H, gpu)) * 1e6
            if best is None or us < best["us"]:
                best = {"us": us, "us_total": t * 1e6, "passes": 2, "tile": T, "kind": kind,
                        "bound": ("tex", "mem", "lds")[int(np.argmax([t_tex, t_mem, t_lds]))]}
    return best
