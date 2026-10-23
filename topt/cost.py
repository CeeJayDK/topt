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


# Render-target formats: bytes per pixel.
FORMAT_BYTES = {"R8": 1, "RG8": 2, "R16F": 2, "RGBA8": 4, "RGB10A2": 4, "RG11B10F": 4, "RG16F": 4,
                "R32F": 4, "RGBA16F": 8, "RGBA32F": 16}
BPP_FORMAT = {1: "R8", 2: "R16F", 4: "RGB10A2", 8: "RGBA16F", 16: "RGBA32F"}


@dataclass(frozen=True)
class GPU:
    name: str
    tex_rate: float        # bilinear fetches / s (32-bit formats)
    bandwidth: float       # effective DRAM bytes / s
    rop_rate: float        # pixels written / s (formats missing from write_rate)
    pass_overhead: float   # s per pass (to calibrate on hardware)
    lds_rate: float = 0.0  # groupshared texel reads / s (compute shaders)
    lds_bytes: int = 32768 # groupshared memory per thread group (D3D11 limit)
    write_rate: tuple = () # ((format, pixels written / s), ...): render-target write limit per format
    wide_filter: float = 1.0  # bilinear cost factor for 64-bit formats (2 = half rate)
    px_rate: float = 0.0   # pixels / s of per-pixel work added to the texture time (0 = none)
    exchange_rate: float = 0.0  # quad exchanges (ddx_fine / ddy_fine of a float3) / s
    sparse_waste: float = 1.0   # bytes moved / bytes used by strided (sparse) downsample reads
    cache_bytes: float = 0.0    # last-level cache: a pass whose reads + writes fit runs from it
    cache_bandwidth: float = 0.0  # bytes / s of such a pass (no write-rate limit, no pixel floor)
    fill_px: float = 0.0   # a pass with fewer pixels cannot fill the GPU: its work takes fill_px / nd longer

    def writes(self, fmt: str) -> float:
        return dict(self.write_rate).get(fmt, self.rop_rate)


# GTX 1660: 22 SMs, 88 TMUs, 48 ROPs, ~1.785 GHz boost, 192-bit GDDR5 @ 8 Gbps.
# Calibrated against TexBench 0.6.0 (CeeJayDK/sopt, docs/texbench/nvidia-gtx-1660-v9.csv,
# full-screen passes at 3840 x 2160): texture rate 155 GTexel/s; copy and half-size
# downsample passes give ~160 GB/s of combined read + write traffic; render-target
# writes are limited per format (noise, incompressible): RGBA8 28.7, R16F 29.7, R8 / RG8
# 24.6, RGB10A2 / RG11B10F / RG16F / R32F 23.0, RGBA16F 18.9 Gpixel/s; 64-bit formats
# filter at half rate. LDS: 128 B/clk/SM, texel stored as fp16x4 (8 B) -> 16 texel
# reads/clk/SM. Per-pass overhead still a placeholder (not measured by TexBench).
GTX1660 = GPU("GTX 1660", 155e9, 160e9, 63.5e9, 5e-6, 22 * 16 * 1.785e9,
              write_rate=(("RGBA8", 28.7e9), ("R16F", 29.7e9), ("R8", 24.6e9), ("RG8", 24.6e9),
                          ("RGB10A2", 23.0e9), ("RG11B10F", 23.0e9), ("RG16F", 23.0e9), ("R32F", 23.0e9),
                          ("RGBA16F", 18.9e9)),
              wide_filter=2.0)
# The model before the TexBench calibration (kept to compare old results).
GTX1660_V1 = GPU("GTX 1660 (v1)", 88 * 1.785e9, 0.8 * 192e9, 48 * 1.785e9, 5e-6, 22 * 16 * 1.785e9)



def _load_profiles() -> dict:
    """One GPU per architecture, from TexBench reports (scripts/gpu_profiles.py)."""
    import json
    from pathlib import Path
    path = Path(__file__).with_name("gpu_profiles.json")
    if not path.exists():
        return {}
    out = {}
    for name, p in json.loads(path.read_text()).items():
        out[name] = GPU(name, p["tex_rate"], p["bandwidth"], p["rop_rate"], p["pass_overhead"],
                        write_rate=tuple(p["write_rate"].items()), wide_filter=p["wide_filter"],
                        px_rate=p.get("px_rate", 0.0), exchange_rate=p.get("exchange_rate", 0.0),
                        sparse_waste=p.get("sparse_waste", 1.0), cache_bytes=p.get("cache_bytes", 0.0),
                        cache_bandwidth=p.get("cache_bandwidth", 0.0), fill_px=p.get("fill_px", 0.0))
    return out


PROFILES = _load_profiles()
# The default model: the GTX 1660 profile from its newest TexBench report (pass chains, N-reads
# and strided-read tests); GTX1660_V2 is the hand calibration against TexBench 0.6.0.
GTX1660_V2 = GTX1660
GTX1660 = PROFILES.get("GTX 1660", GTX1660_V2)

BYTES_PER_PIXEL = 4  # RGB10A2 / R11G11B10F / RGBA8 backbuffer
SCREEN_FORMAT = "RGBA8"  # the backbuffer the composite writes
RESOLUTIONS = {"1080p": (1920, 1080), "1440p": (2560, 1440), "4k": (3840, 2160)}


def _pass_time(nd: int, ns_read: int, taps: float, gpu: GPU, wbytes: float = BYTES_PER_PIXEL,
               rbytes: float | None = None, wfmt: str | None = None, exchanges: float = 0,
               src_bytes: float | None = None) -> tuple:
    """rbytes: bytes read in total (default ns_read texels of BYTES_PER_PIXEL);
    wfmt: written format (write-rate limit), default from wbytes;
    exchanges: quad exchanges (ddx_fine / ddy_fine of a float3) per pixel;
    src_bytes: size of the source texture(s) (default rbytes): the pass runs from the cache when
    its sources and target fit."""
    rb = ns_read * BYTES_PER_PIXEL if rbytes is None else rbytes
    traffic = nd * wbytes + rb
    cached = gpu.cache_bandwidth and nd * wbytes + (rb if src_bytes is None else src_bytes) <= gpu.cache_bytes
    t_tex = nd * taps / gpu.tex_rate
    if gpu.px_rate and not cached:
        t_tex += nd / gpu.px_rate
    if exchanges and gpu.exchange_rate:
        t_tex += nd * exchanges / gpu.exchange_rate
    if cached:
        t_mem, t_rop = traffic / gpu.cache_bandwidth, 0.0
    else:
        t_mem = traffic / gpu.bandwidth
        t_rop = nd / gpu.writes(wfmt or BPP_FORMAT.get(int(wbytes), "RGB10A2"))
    t = max(t_tex, t_mem, t_rop) * max(1.0, gpu.fill_px / max(nd, 1))
    return gpu.pass_overhead + t, ("tex" if t == t_tex else "mem" if t == t_mem else "rop")


def composite_baseline(W: int, H: int, gpu: GPU) -> float:
    """A plain full-screen pass: read the backbuffer once, write the screen."""
    return _pass_time(W * H, W * H, 1, gpu, wfmt=SCREEN_FORMAT)[0]


def pass_format(p) -> str:
    return p.fmt or BPP_FORMAT.get(p.bpp, "RGB10A2")


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
        if ns_read < ns:  # sparse reads move whole cache lines
            ns_read = min(ns, ns_read * gpu.sparse_waste)
        j = pl.src_index(i)
        sfmt = pass_format(pl.passes[j]) if j >= 0 else SCREEN_FORMAT
        rbytes = ns_read * FORMAT_BYTES[sfmt]
        wfmt = pass_format(p)
        ftaps = taps * (gpu.wide_filter if FORMAT_BYTES[sfmt] >= 8 else 1.0)
        src = ns * FORMAT_BYTES[sfmt]
        if composite and i == last:
            taps += 1
            ftaps += 1
            wfmt = SCREEN_FORMAT
            if j >= 0:  # else the blur already reads the backbuffer
                ns_read += W * H
                rbytes += W * H * BYTES_PER_PIXEL
                src += W * H * BYTES_PER_PIXEL
        wbytes = FORMAT_BYTES[wfmt]
        t, b = _pass_time(nd, ns_read, ftaps, gpu, wbytes, rbytes, wfmt, getattr(p, "exchanges", 0), src)
        bounds.append(b)
        total += t
        fetches += nd * taps
        dram += nd * wbytes + rbytes
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
    final = _pass_time(n, 2 * n, 2, gpu, wfmt=SCREEN_FORMAT)[0]  # composite reading CS output + backbuffer
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
