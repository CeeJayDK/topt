"""Render calibration images for judging quality limits by eye.

    python -m scripts.calibrate

results/calib/truncation.png  same effective sigma, kernels from boxy to Gaussian
results/calib/shift.png       multi-rate methods vs reference (blockiness)
results/calib/shift.gif       a square moving 1 px/frame (shimmer)
Each panel's lower half shows the same result at x8 exposure to reveal tails.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from topt import methods as M
from topt.quality import metrics
from topt.sim import run

OUT = Path(__file__).resolve().parent.parent / "results" / "calib"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def scene(w: int, h: int, scale: float, dx: int = 0) -> np.ndarray:
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    s = scale
    d.rectangle([dx + 0.08 * w, 0.15 * h, dx + 0.08 * w + 12 * s, 0.15 * h + 12 * s], fill=255)
    d.text((0.45 * w, 0.12 * h), "Blur", fill=255, font=ImageFont.truetype(FONT, int(9 * s)))
    for i in range(6):  # small bright points
        x, y = 0.12 * w + i * 0.14 * w, 0.72 * h
        d.rectangle([x, y, x + max(1, s // 2), y + max(1, s // 2)], fill=255)
    for i in range(4):  # thin lines
        x = 0.5 * w + i * 3 * s
        d.line([x, 0.55 * h, x + 6 * s, 0.9 * h], fill=255, width=1)
    return np.asarray(im, float) / 255.0


def to_img(a: np.ndarray, gain: float = 1.0) -> Image.Image:
    a = np.clip(a * gain, 0, 1) ** (1 / 2.2)  # treat values as linear light
    return Image.fromarray((a * 255 + 0.5).astype(np.uint8))


def panel(img: np.ndarray, label: str, ref: np.ndarray | None = None) -> Image.Image:
    h, w = img.shape
    rows = 2 if ref is None else 3
    p = Image.new("L", (w, rows * h + 34), 40)
    p.paste(to_img(img), (0, 34))
    p.paste(to_img(img, 8.0), (0, 34 + h))
    if ref is not None:  # error vs reference, x16, shown linearly
        e = np.clip(np.abs(img - ref) * 16, 0, 1)
        p.paste(Image.fromarray((e * 255 + 0.5).astype(np.uint8)), (0, 34 + 2 * h))
    d = ImageDraw.Draw(p)
    f = ImageFont.truetype(FONT, 12)
    for i, line in enumerate(label.split("\n")):
        d.text((4, 2 + 15 * i), line, fill=255, font=f)
    return p


def grid(panels: list, cols: int) -> Image.Image:
    pw, ph = panels[0].size
    rows = math.ceil(len(panels) / cols)
    g = Image.new("L", (cols * (pw + 6), rows * (ph + 6)), 0)
    for i, p in enumerate(panels):
        g.paste(p, ((i % cols) * (pw + 6), (i // cols) * (ph + 6)))
    return g


def sep_bilinear_trunc(sigma: float, k: float):
    """sep_bilinear with radius m = k * sigma, s fitted to the same effective sigma."""
    m = max(1, round(k * sigma))
    pos = np.arange(-m, m, dtype=float)
    s = M.bisect(lambda s: M.var1d(pos, M.gauss(pos + 0.5, s)), sigma ** 2 - 0.25, 1e-3, 1e6)
    return None if s is None else M.sep_bilinear(m, s)


def reference(sigma: float):
    r = math.ceil(4 * sigma)
    return M.sep_linear(r, sigma)


def truncation(sigma: float = 6.0):
    img = scene(512, 256, sigma)
    panels = [panel(run(reference(sigma), img), f"reference Gaussian\nsigma={sigma:g}")]
    for k in (1.75, 2.0, 2.25, 2.5, 3.0):
        pl = sep_bilinear_trunc(sigma, k)
        if pl is None:
            continue
        q = metrics(pl, sigma)
        m, s = pl.params["m"], pl.params["s"]
        panels.append(panel(run(pl, img),
                            f"radius {k:g} sigma ({m}px), s = {100 * s / m:.0f}% of radius, "
                            f"{2 * m} fetches\nleak {q['leak']:.3f}  tv {q['tv']:.3f}"))
    grid(panels, 2).save(OUT / "truncation.png")


def shift_methods(sigma: float):
    fams = {}
    for p in M.cand_dual_filter(sigma):
        fams.setdefault(f"dual filter L={p.params['levels']}", p)
    for p in M.cand_pyramid(sigma, truncs=(3.0,)):
        pr = p.params
        name = f"pyramid k={pr['k']} up={pr['up']}{' iq' if pr['warp'] else ''}"
        fams.setdefault(name, p)
    return fams


def shift(sigma: float = 16.0):
    W, H = 768, 384
    img = scene(W, H, sigma / 2)
    ref = reference(sigma)
    methods = {"reference Gaussian": ref, **shift_methods(sigma)}
    panels = []
    for name, pl in methods.items():
        q = metrics(pl, sigma)
        panels.append(panel(run(pl, img), f"{name}\nphase {q['phase']:.3f}  leak {q['leak']:.3f}"))
    grid(panels, 2).save(OUT / "shift.png")

    # Animation: square moving 1 px per frame; shimmer shows as pulsing / wobbling.
    frames = []
    names = list(methods)[:4]
    for t in range(16):
        im = scene(W, H, sigma / 2, dx=t)
        row = [panel(run(methods[n], im)[:H // 2, :W // 2], n) for n in names]
        frames.append(grid(row, len(row)).convert("P"))
    frames[0].save(OUT / "shift.gif", save_all=True, append_images=frames[1:], duration=120, loop=0)


def upsample(sigma: float = 16.0):
    """Mach bands / kinks from the upsampling path of down/blur/up designs."""
    from topt import search as S
    W, H = 768, 256
    img = scene(W, H, sigma / 2)
    ref_img = run(reference(sigma), img)
    designs = [
        ("dual filter", next(iter(M.cand_dual_filter(sigma)))),
        *[(None, S.fit(S.Design((4, 2), 5, "direct", 2.0, up, e, w), sigma)[0])
          for up, e, w in [((8,), 1, None), ((8,), 2, None), ((8,), 1, "iq"),
                           ((2, 2, 2), 1, None), ((2, 2, 2), 2, None), ((2, 4), 2, None)]],
    ]
    panels = [panel(ref_img, f"reference Gaussian sigma={sigma:g}\n(rows: normal, x8 exposure, |error| x16)",
                    ref_img)]
    for name, pl in designs:
        q = metrics(pl, sigma)
        name = name or pl.params["label"]
        panels.append(panel(run(pl, img), f"{name}\ncurv {q['curv']:.2f}  phase {q['phase']:.3f}  "
                                          f"leak {q['leak']:.3f}", ref_img))
    grid(panels, 2).save(OUT / "upsample.png")


if __name__ == "__main__":
    import sys
    OUT.mkdir(parents=True, exist_ok=True)
    for name in sys.argv[1:] or ["truncation", "shift", "upsample"]:
        globals()[name]()
