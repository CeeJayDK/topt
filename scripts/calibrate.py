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
    for k in (2.0, 2.25, 2.5, 2.75, 3.0):
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


def isotropy(sigma: float = 16.0):
    """Kernels with a range of 'iso' scores (4-fold / square shapes)."""
    from topt import search as S
    W, H = 768, 256
    img = scene(W, H, sigma / 2)
    ref_img = run(reference(sigma), img)
    items = [("dual filter L=4", next(iter(M.cand_dual_filter(sigma))))]
    for k in (3.0, 2.5, 2.25):
        items.append((f"truncated Gaussian, radius {k:g} sigma", sep_bilinear_trunc(sigma, k)))
    for d in (S.Design((8,), 3, "direct", 2.0, (8,), 4, None, True),
              S.Design((8,), 1, "pw9x3", 0.0, (8,), 4, None, True),
              S.Design((8,), 1, "pw9x2", 0.0, (8,), 4, None, True)):
        r = S.fit(d, sigma)
        if r:
            items.append((d.label(), r[0]))
    rows = [(n, pl, metrics(pl, sigma)) for n, pl in items]
    rows.sort(key=lambda t: t[2]["iso"])
    panels = [panel(ref_img, f"reference Gaussian sigma={sigma:g}  iso 0.000\n(rows: normal, x8 exposure, |error| x16)",
                    ref_img)]
    for name, pl, q in rows:
        panels.append(panel(run(pl, img), f"{name}\niso {q['iso']:.3f}  block {q['block']:.2f}  leak {q['leak']:.3f}",
                            ref_img))
    grid(panels, 2).save(OUT / "isotropy.png")


def detail_scene(w: int, h: int, dx: int = 0, seed: int = 3) -> np.ndarray:
    """Fine-detail test content, panned right by dx pixels."""
    W = w + 64
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:h, 0:W].astype(float)
    tex = np.zeros((h, W))
    for octave in range(1, 6):  # multi-octave value noise
        s = 2 ** octave
        g = rng.random((h // s + 2, W // s + 2))
        tex += np.kron(g, np.ones((s, s)))[:h, :W] / 2 ** (6 - octave)
    tex = 0.06 * tex / tex.max()  # dark, so the x8 view stays informative
    im = Image.fromarray((tex * 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for i in range(12):  # 1 px lines
        x0 = 40 + 22 * i
        d.line([x0, 10, x0 + 60, h - 10], fill=255, width=1)
    f = ImageFont.truetype(FONT, 11)
    for i in range(6):
        d.text((W // 2, 8 + 18 * i), "Fine text 0123", fill=255, font=f)
    a = np.asarray(im, float) / 255.0
    cb = ((x // 2 + y // 2) % 2)[: h // 3, : W // 5]  # 2 px checkerboard
    a[h - h // 3:, W - W // 5:] = cb
    stars = rng.random((h, W)) > 0.996  # 1 px bright points
    a[stars] = 1.0
    return a[:, 32 - dx:32 - dx + w]


def motion(sigma: float = 16.0, frames: int = 16):
    """Fine detail panning 1 px/frame: blockiness, aliasing and flicker."""
    from topt import search as S
    W, H = 512, 256
    methods = {"reference Gaussian": reference(sigma), **{
        k: v for k, v in shift_methods(sigma).items()
        if k in ("dual filter L=4", "pyramid k=3 up=chain", "pyramid k=3 up=direct")}}
    for lab, d in {"hybrid 4x2 e5 | up 8": S.Design((4, 2), 5, "direct", 3.0, (8,), 1, None),
                   "hybrid 4x2 e5 | up 2x4 e2": S.Design((4, 2), 5, "direct", 3.0, (2, 4), 2, None),
                   "hybrid 4x2 e1 (box down) | up 2x4 e2": S.Design((4, 2), 1, "direct", 3.0, (2, 4), 2, None),
                   }.items():
        methods[lab] = S.fit(d, sigma)[0]
    outs = {n: [] for n in methods}
    for t in range(frames):
        img = detail_scene(W, H, t)
        for n, pl in methods.items():
            outs[n].append(run(pl, img))
    ref = outs["reference Gaussian"]
    stats = {}
    for n in methods:
        e = np.array([o - r for o, r in zip(outs[n], ref)])[:, 32:-32, 32:-32] * 255
        # flicker: temporal std of the error at each scene point (error follows the pan)
        al = np.array([np.roll(e[t], -t, axis=1) for t in range(frames)])[:, :, frames:-frames]
        stats[n] = (float(np.sqrt((e ** 2).mean())), float(al.std(0).mean()))
    src = Image.fromarray((np.clip(detail_scene(W, H, 0), 0, 1) ** (1 / 2.2) * 255).astype(np.uint8))
    src.save(OUT / "motion_source.png")
    gif = []
    for t in range(frames):
        ps = []
        for n in methods:
            rms, fl = stats[n]
            ps.append(panel(outs[n][t], f"{n}\nerr rms {rms:.2f}  flicker {fl:.2f} (8-bit levels)", ref[t]))
        g = grid(ps, 2)
        if t == 0:
            g.save(OUT / "motion.png")
        gif.append(g.resize((g.width // 2, g.height // 2)).convert("P"))
    gif[0].save(OUT / "motion.gif", save_all=True, append_images=gif[1:], duration=120, loop=0)
    for n, (rms, fl) in stats.items():
        print(f"{n:40s} err rms {rms:5.2f}  flicker {fl:5.2f}")


if __name__ == "__main__":
    import sys
    OUT.mkdir(parents=True, exist_ok=True)
    for name in sys.argv[1:] or ["truncation", "shift", "upsample", "motion", "isotropy"]:
        globals()[name]()
