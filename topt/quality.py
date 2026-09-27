"""Impulse-response quality metrics against an ideal Gaussian.

Multi-rate pipelines (down/up sampling) are shift-variant, so the impulse is
placed at several phases relative to the coarsest grid. Metrics:

sigma   RMS radius of the phase-averaged response (per axis, averaged)
aniso   sqrt(max/min) - 1 of the variance along x, y and both diagonals
tv      total-variation distance (0..1) to the Gaussian of the same sigma
leak    worst stop-band gain: max |H(f)| where the matched Gaussian is < 1 %.
        Truncation (boxiness) and blocky resampling show up here as sidelobes.
        For sigma < ~1.5 a sampled Gaussian itself aliases above 1 %; that excess
        is subtracted so small kernels are judged against what is attainable.
phase   mean TV distance of each phase's response to the phase average
        (shift variance -> visible blockiness / shimmering on motion)
curv    mean over phases of |lap(K_i) - lap(G_i)|_1 / |lap(G_i)|_1, G_i the
        Gaussian matched to that phase's response. Catches kinks: Mach bands
        from linear upsampling and the edge of truncated kernels. Responses are
        first box-binned to sigma ~4 so the value does not grow with sigma.
block   like curv, but of each phase's deviation from the phase average:
        kinks locked to the low-res grid (visible blockiness), zero for
        shift-invariant filters.
"""
from __future__ import annotations

import math

import numpy as np

from .sim import Pipeline, is_separable, run, run_1d

GAUSS_STOP = math.sqrt(math.log(100.0) / (2 * math.pi ** 2))  # |G(f)| = 1% at f = this / sigma


def support_radius(pl: Pipeline) -> int:
    r = 0.0
    for i, p in enumerate(pl.passes):
        ext = max(max(abs(dx), abs(dy)) for dx, dy, _ in p.taps)
        r += (ext + 1.0) * pl.src_div(i) + p.div
    return int(math.ceil(r))


def default_phases(F: int, n: int = 3) -> list:
    ph = sorted({int(round(v)) for v in np.linspace(0, F - 1, min(F, n))})
    return [(py, px) for py in ph for px in ph]


def eval_radius(sigma: float, F: int) -> int:
    """Window that holds all but ~1e-6 of a Gaussian-like response."""
    return int(math.ceil(5 * sigma)) + 2 * F + 4


def responses(pl: Pipeline, phases=None, radius: int | None = None) -> tuple:
    """Impulse responses (one per phase), cropped to +-R around the impulse."""
    F = pl.max_div
    R = support_radius(pl) if radius is None else min(radius, support_radius(pl))
    N = int(math.ceil((2 * R + 2 * F + 16) / F)) * F
    c0 = (N // 2) // F * F
    if phases is None:
        phases = default_phases(F)
    ks = []
    if is_separable(pl):  # two 1D runs per phase instead of one 2D run
        cache = {}

        def k1(p, axis):
            if (p, axis) not in cache:
                v = np.zeros(N)
                v[c0 + p] = 1.0
                cache[p, axis] = run_1d(pl, v, axis)[c0 + p - R:c0 + p + R + 1]
            return cache[p, axis]

        for py, px in phases:
            ks.append(np.outer(k1(py, 1), k1(px, 0)))
        return np.array(ks), R
    if N > 8192:
        raise ValueError(f"support radius {R} too large to simulate")
    for py, px in phases:
        img = np.zeros((N, N))
        img[c0 + py, c0 + px] = 1.0
        out = run(pl, img)
        ks.append(out[c0 + py - R:c0 + py + R + 1, c0 + px - R:c0 + px + R + 1])
    return np.array(ks), R


def measured_sigma(pl: Pipeline, phases=None, radius: int | None = None) -> float:
    ks, R = responses(pl, phases, radius)
    return _moments(ks.mean(0), R)[0]


def _moments(k: np.ndarray, R: int):
    k = k / k.sum()
    y, x = np.mgrid[-R:R + 1, -R:R + 1].astype(float)
    mx, my = (k * x).sum(), (k * y).sum()
    vx = (k * (x - mx) ** 2).sum()
    vy = (k * (y - my) ** 2).sum()
    cxy = (k * (x - mx) * (y - my)).sum()
    return math.sqrt((vx + vy) / 2), (mx, my), (vx, vy, cxy), (x, y)


def _lap(a: np.ndarray) -> np.ndarray:
    return a[1:-1, 2:] + a[1:-1, :-2] + a[2:, 1:-1] + a[:-2, 1:-1] - 4 * a[1:-1, 1:-1]


def _bin(k: np.ndarray, sig: float) -> np.ndarray:
    b = max(1, int(sig // 4))
    if b > 1:
        n = (k.shape[0] // b) * b
        k = k[:n, :n].reshape(n // b, b, n // b, b).sum((1, 3))
    return k


def _gauss_like(k: np.ndarray) -> np.ndarray:
    y, x = np.mgrid[0:k.shape[0], 0:k.shape[1]].astype(float)
    mx, my = (k * x).sum(), (k * y).sum()
    sig = math.sqrt(((k * (x - mx) ** 2).sum() + (k * (y - my) ** 2).sum()) / 2)
    g = np.exp(-((x - mx) ** 2 + (y - my) ** 2) / (2 * sig * sig))
    return g / g.sum()


def _block_err(k: np.ndarray, kbar: np.ndarray, sig: float) -> float:
    k, kbar = _bin(k, sig), _bin(kbar, sig)
    return float(np.abs(_lap(k - kbar)).sum() / np.abs(_lap(_gauss_like(kbar))).sum())


def _curv_err(k: np.ndarray, sig: float) -> float:
    k = _bin(k, sig)
    y, x = np.mgrid[0:k.shape[0], 0:k.shape[1]].astype(float)
    mx, my = (k * x).sum(), (k * y).sum()
    sig = math.sqrt(((k * (x - mx) ** 2).sum() + (k * (y - my) ** 2).sum()) / 2)
    g = np.exp(-((x - mx) ** 2 + (y - my) ** 2) / (2 * sig * sig))
    lg = _lap(g / g.sum())
    return float(np.abs(_lap(k) - lg).sum() / np.abs(lg).sum())


def metrics(pl: Pipeline, target_sigma: float | None = None, phases=None) -> dict:
    radius = eval_radius(target_sigma, pl.max_div) if target_sigma else None
    ks, R = responses(pl, phases, radius)
    return score(ks, R, target_sigma)


def score(ks: np.ndarray, R: int, target_sigma: float | None = None) -> dict:
    """Metrics from per-phase impulse responses cropped to +-R."""
    k = ks.mean(0)
    k = k / k.sum()
    sig, (mx, my), (vx, vy, cxy), (x, y) = _moments(k, R)
    vs = [vx, vy, (vx + vy) / 2 + cxy, (vx + vy) / 2 - cxy]
    g = np.exp(-((x - mx) ** 2 + (y - my) ** 2) / (2 * sig * sig))
    g /= g.sum()
    M = max(2 * R + 1, int(8 * sig), 64)
    H = np.abs(np.fft.fft2(k, s=(M, M)))
    f = np.fft.fftfreq(M)
    fr = np.sqrt(f[:, None] ** 2 + f[None, :] ** 2)
    stop = fr > GAUSS_STOP / sig
    alias = 0.0
    if stop.any():  # aliasing of the sampled Gaussian itself, above its nominal 1 %
        alias = max(0.0, float(np.abs(np.fft.fft2(g, s=(M, M)))[stop].max()) - 0.01)
    phase = float(np.mean([0.5 * np.abs(ki / ki.sum() - k).sum() for ki in ks]))
    curv = float(np.mean([_curv_err(ki / ki.sum(), sig) for ki in ks]))
    block = float(np.mean([_block_err(ki / ki.sum(), k, sig) for ki in ks]))
    out = {
        "sigma": sig,
        "aniso": math.sqrt(max(vs) / min(vs)) - 1.0,
        "tv": 0.5 * float(np.abs(k - g).sum()),
        "leak": max(0.0, float(H[stop].max()) - alias) if stop.any() else 0.0,
        "phase": phase,
        "curv": curv,
        "block": block,
        "shift": math.hypot(mx, my),
    }
    if target_sigma:
        out["sigma_err"] = sig / target_sigma - 1.0
    return out
