"""Exact linear simulator for multi-pass bilinear texture filters.

Conventions
-----------
* Texel k of a texture covers [k-0.5, k+0.5] in texel space (its centre is k).
* A pass renders a target of size (H // div, W // div). Output pixel i maps to
  source texel coordinate (i + 0.5) * n_src / n_dst - 0.5, then each tap adds its
  (dx, dy) offset, given in *source* texels.
* Every tap is one hardware bilinear fetch. Addressing mode defaults to MIRROR
  (D3D semantics: texel -1 -> 0, -2 -> 1, ...), since clamping would vignette.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

import numpy as np
import scipy.sparse as sp


@dataclass(frozen=True)
class Pass:
    div: int                 # output size = full size // div
    taps: tuple              # ((dx, dy, weight), ...) in source texels
    src: int | None = None   # index of source pass; None = previous pass, -1 = input
    warp: str | None = None  # 'iq' = smoothstep on the bilinear fraction (magnification only)


@dataclass
class Pipeline:
    method: str
    params: dict
    passes: list = field(default_factory=list)

    def src_index(self, i: int) -> int:
        s = self.passes[i].src
        return i - 1 if s is None else s

    def src_div(self, i: int) -> int:
        j = self.src_index(i)
        return 1 if j < 0 else self.passes[j].div

    @property
    def max_div(self) -> int:
        return max(p.div for p in self.passes)


def _mirror(idx: np.ndarray, n: int) -> np.ndarray:
    m = np.mod(idx, 2 * n)
    return np.where(m < n, m, 2 * n - 1 - m)


def _warp(f: np.ndarray, warp: str | None) -> np.ndarray:
    if warp is None:
        return f
    if warp == "iq":
        return f * f * (3.0 - 2.0 * f)
    if warp == "quintic":
        return f * f * f * (f * (f * 6.0 - 15.0) + 10.0)
    raise ValueError(warp)


@lru_cache(maxsize=4096)
def interp_matrix(n_dst: int, n_src: int, offset: float, warp: str | None = None,
                  address: str = "mirror", subtexel_bits: int | None = None) -> sp.csr_matrix:
    """Sparse (n_dst x n_src) matrix of 1D linear-filter weights for one tap offset."""
    c = (np.arange(n_dst) + 0.5) * (n_src / n_dst) - 0.5 + offset
    x0 = np.floor(c)
    f = _warp(c - x0, warp)
    if subtexel_bits is not None:  # hardware filter-weight precision
        q = float(1 << subtexel_bits)
        f = np.round(f * q) / q
    x0 = x0.astype(np.int64)
    rows = np.repeat(np.arange(n_dst), 2)
    cols = np.stack([x0, x0 + 1], 1).ravel()
    vals = np.stack([1.0 - f, f], 1).ravel()
    if address == "mirror":
        cols = _mirror(cols, n_src)
    elif address == "clamp":
        cols = np.clip(cols, 0, n_src - 1)
    elif address == "border":
        keep = (cols >= 0) & (cols < n_src)
        rows, cols, vals = rows[keep], cols[keep], vals[keep]
    else:
        raise ValueError(address)
    return sp.csr_matrix((vals, (rows, cols)), shape=(n_dst, n_src))


def run_pass(p: Pass, src: np.ndarray, full_shape: tuple, address: str = "mirror",
             subtexel_bits: int | None = None) -> np.ndarray:
    H, W = full_shape
    hd, wd = max(1, H // p.div), max(1, W // p.div)
    hs, ws = src.shape
    out = np.zeros((hd, wd))
    # Group taps by dy so each row-resample of the source is done once.
    by_dy: dict = {}
    for dx, dy, w in p.taps:
        by_dy.setdefault(float(dy), []).append((float(dx), float(w)))
    for dy, row in by_dy.items():
        t = interp_matrix(hd, hs, dy, p.warp, address, subtexel_bits) @ src
        m = sum(w * interp_matrix(wd, ws, dx, p.warp, address, subtexel_bits) for dx, w in row)
        out += (m @ t.T).T
    return out


def run(pl: Pipeline, img: np.ndarray, address: str = "mirror", quantize_bits: int | None = None,
        subtexel_bits: int | None = None) -> np.ndarray:
    """Run the pipeline on a single-channel image (the filter is linear per channel)."""
    bufs = []
    for i, p in enumerate(pl.passes):
        j = pl.src_index(i)
        src = img if j < 0 else bufs[j]
        out = run_pass(p, src, img.shape, address, subtexel_bits)
        if quantize_bits is not None:
            q = float((1 << quantize_bits) - 1)
            out = np.round(np.clip(out, 0.0, 1.0) * q) / q
        bufs.append(out)
    return bufs[-1]
