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
    # Per-pixel ("interleaved") sampling: output pixel (x, y) uses the tap set
    # variants[vmap[(y % tile) * tile + x % tile]]. All variants have len(taps) taps.
    variants: tuple | None = None
    tile: int = 1
    vmap: tuple | None = None

    def variant_of(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        idx = (y % self.tile) * self.tile + (x % self.tile)
        return np.asarray(self.vmap)[idx]


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
        """Period (full-res pixels) of the pipeline's shift variance."""
        return max(p.div * p.tile for p in self.passes)

    @property
    def interleaved(self) -> bool:
        return any(p.variants is not None for p in self.passes)


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


def _variant_matrix(p: Pass, hd: int, wd: int, hs: int, ws: int, address: str) -> sp.csr_matrix:
    """Sparse (hd*wd x hs*ws) matrix of a pass whose taps depend on the output pixel."""
    yy, xx = np.mgrid[0:hd, 0:wd]
    var = p.variant_of(xx.ravel(), yy.ravel())
    rows, cols, vals = [], [], []
    for v, taps in enumerate(p.variants):
        sel = np.nonzero(var == v)[0]
        if not len(sel):
            continue
        ox = (xx.ravel()[sel] + 0.5) * (ws / wd) - 0.5
        oy = (yy.ravel()[sel] + 0.5) * (hs / hd) - 0.5
        for dx, dy, w in taps:
            cx, cy = ox + dx, oy + dy
            x0, y0 = np.floor(cx).astype(np.int64), np.floor(cy).astype(np.int64)
            fx, fy = cx - x0, cy - y0
            for ax, ay, wt in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)),
                               (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
                c_x, c_y = x0 + ax, y0 + ay
                if address == "mirror":
                    c_x, c_y = _mirror(c_x, ws), _mirror(c_y, hs)
                else:
                    c_x, c_y = np.clip(c_x, 0, ws - 1), np.clip(c_y, 0, hs - 1)
                rows.append(sel)
                cols.append(c_y * ws + c_x)
                vals.append(w * wt)
    return sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                         shape=(hd * wd, hs * ws))


def run_pass(p: Pass, src: np.ndarray, full_shape: tuple, address: str = "mirror",
             subtexel_bits: int | None = None) -> np.ndarray:
    H, W = full_shape
    hd, wd = max(1, H // p.div), max(1, W // p.div)
    hs, ws = src.shape
    if p.variants is not None:
        return (_variant_matrix(p, hd, wd, hs, ws, address) @ src.ravel()).reshape(hd, wd)
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


def quantize(a: np.ndarray, fmt) -> np.ndarray:
    """Round to a storage format: int n = n-bit UNORM, 'f6' / 'f5' = unsigned small
    float with 5-bit exponent and 6 / 5 mantissa bits (R11G11B10F red,green / blue)."""
    if isinstance(fmt, int):
        q = float((1 << fmt) - 1)
        return np.round(np.clip(a, 0.0, 1.0) * q) / q
    m = {"f6": 6, "f5": 5}[fmt]
    a = np.clip(a, 0.0, None)
    e = np.floor(np.log2(np.maximum(a, 2.0 ** -14)))  # denormals below 2^-14
    step = 2.0 ** (e - m)
    return np.round(a / step) * step


def run(pl: Pipeline, img: np.ndarray, address: str = "mirror", quantize_bits=None,
        subtexel_bits: int | None = None) -> np.ndarray:
    """Run the pipeline on a single-channel image (the filter is linear per channel).
    quantize_bits: storage format of every intermediate (see `quantize`)."""
    bufs = []
    for i, p in enumerate(pl.passes):
        j = pl.src_index(i)
        src = img if j < 0 else bufs[j]
        out = run_pass(p, src, img.shape, address, subtexel_bits)
        if quantize_bits is not None and i < len(pl.passes) - 1:  # the last pass writes the screen
            out = quantize(out, quantize_bits)
        bufs.append(out)
    return bufs[-1]


def factor_taps(taps) -> tuple | None:
    """Split a pass's taps into 1D x and y tap lists if they form an outer product."""
    xs = sorted({float(dx) for dx, _, _ in taps})
    ys = sorted({float(dy) for _, dy, _ in taps})
    w2 = np.zeros((len(ys), len(xs)))
    for dx, dy, w in taps:
        w2[ys.index(float(dy)), xs.index(float(dx))] += w
    wx = w2.sum(0)
    wy = w2.sum(1) / w2.sum()
    if np.abs(np.outer(wy, wx) - w2).max() > 1e-12 * np.abs(w2).max():
        return None
    return tuple(zip(xs, wx)), tuple(zip(ys, wy))


def is_separable(pl: Pipeline) -> bool:
    return all(p.variants is None and factor_taps(p.taps) is not None for p in pl.passes)


def run_1d(pl: Pipeline, vec: np.ndarray, axis: int, address: str = "mirror") -> np.ndarray:
    """Run a separable pipeline along one axis (0 = x, 1 = y) of a 1D signal."""
    bufs = []
    for i, p in enumerate(pl.passes):
        j = pl.src_index(i)
        src = vec if j < 0 else bufs[j]
        nd = max(1, len(vec) // p.div)
        m = sum(w * interp_matrix(nd, len(src), o, p.warp, address) for o, w in factor_taps(p.taps)[axis])
        bufs.append(m @ src)
    return bufs[-1]
