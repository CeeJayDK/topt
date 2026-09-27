"""Impulse-response quality metrics against an ideal Gaussian.

Multi-rate pipelines (down/up sampling) are shift-variant, so the impulse is
placed at several phases relative to the coarsest grid. Metrics:

sigma   RMS radius of the phase-averaged response (per axis, averaged)
aniso   sqrt(max/min) - 1 of the variance along x, y and both diagonals
tv      total-variation distance (0..1) to the Gaussian of the same sigma
leak    worst stop-band gain: max |H(f)| where the matched Gaussian is < 1 %.
        Truncation (boxiness) and blocky resampling show up here as sidelobes.
phase   mean TV distance of each phase's response to the phase average
        (shift variance -> visible blockiness / shimmering on motion)
"""
from __future__ import annotations

import math

import numpy as np

from .sim import Pipeline, run

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


def responses(pl: Pipeline, phases=None) -> tuple:
    F = pl.max_div
    R = support_radius(pl)
    N = int(math.ceil((2 * R + 2 * F + 16) / F)) * F
    if N > 8192:
        raise ValueError(f"support radius {R} too large to simulate")
    c0 = (N // 2) // F * F
    if phases is None:
        phases = default_phases(F)
    ks = []
    for py, px in phases:
        img = np.zeros((N, N))
        img[c0 + py, c0 + px] = 1.0
        out = run(pl, img)
        ks.append(out[c0 + py - R:c0 + py + R + 1, c0 + px - R:c0 + px + R + 1])
    return np.array(ks), R


def measured_sigma(pl: Pipeline, phases=None) -> float:
    ks, R = responses(pl, phases)
    return _moments(ks.mean(0), R)[0]


def _moments(k: np.ndarray, R: int):
    k = k / k.sum()
    y, x = np.mgrid[-R:R + 1, -R:R + 1].astype(float)
    mx, my = (k * x).sum(), (k * y).sum()
    vx = (k * (x - mx) ** 2).sum()
    vy = (k * (y - my) ** 2).sum()
    cxy = (k * (x - mx) * (y - my)).sum()
    return math.sqrt((vx + vy) / 2), (mx, my), (vx, vy, cxy), (x, y)


def metrics(pl: Pipeline, target_sigma: float | None = None, phases=None) -> dict:
    ks, R = responses(pl, phases)
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
    phase = float(np.mean([0.5 * np.abs(ki / ki.sum() - k).sum() for ki in ks]))
    out = {
        "sigma": sig,
        "aniso": math.sqrt(max(vs) / min(vs)) - 1.0,
        "tv": 0.5 * float(np.abs(k - g).sum()),
        "leak": float(H[stop].max()) if stop.any() else 0.0,
        "phase": phase,
        "shift": math.hypot(mx, my),
    }
    if target_sigma:
        out["sigma_err"] = sig / target_sigma - 1.0
    return out
