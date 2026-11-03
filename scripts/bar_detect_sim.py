"""Movie Night bar detection: six methods compared on real and synthetic frames.

    python -m scripts.bar_detect_sim <frames folder>

Each method finds, per screen edge (top, bottom, left, right), the pure black bar (lines whose pixels are
all 0) and the bar with the near-black fringe next to the picture: lines below LEVEL and below half the
picture line just inside (a step, not a dark plateau), at most fringe_max lines more (4 at 1080p). Reads
are simulated like the shader's: a corner read is the bilinear mean of 2 x 2 pixels (any light above 0 in
4 pixels), a point read one pixel.

A  current: per edge a binary search over lines; a probe = 16 corner reads along two lines. Top across the
   whole width, then left / right on the rows between the top bar and its mirror, then the bottom in the
   outer 1/16 of the picture's width at each end (subtitles). Fringe: binary search over 32 point reads per line.
B  diagonal (CeeJay's idea): centre read (black: skip the frame), binary search along the diagonal to a top
   corner, alternating left / right corners; then which edge it hit (two reads), the exact edge along that
   axis, the other axis at the row / column just inside (alternating sides), then the bottom and the other
   side from the mirrored guess (verify, else step 8 lines, then halve). One corner read per probe; the
   bottom probes near the picture's sides. Fringe: point reads stepping inward from the edge.
C  sparse profile: per line the brightest of 64 point reads in each of 32 segments (rows and columns), in one
   parallel pass; one pixel then scans the profile inward from each edge (top: all segments; left / right:
   the segments between the top bar and its mirror; bottom: the outer 1/16 of the picture's width at each end).
D  exact profile (CeeJay's max-pyramid): the same, but each segment's maximum over all its pixels.
E  exact profile, inside-out: from the screen centre outward to the first black line (CeeJay's start at the
   centre: the picture is connected around it, so subtitles further out in a bar do not count); left / right
   on the middle quarter of the rows, then top / bottom on the outer 1/16 of the picture's width at each end,
   then left / right again on the picture's rows.
F  the same on the sparse profile.
Over a run of frames A and B keep the smallest bars seen, C and D the brightest value per line and segment.
Writes results/bar_detect.md.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
LEVEL = 16 / 255          # Edge feather default
SEG = 64                  # profile segments per line
CPTS = 128                # sparse profile: point reads per line
OUTER = 1 / 16            # the bottom is read in this share of the picture's width at each end (subtitles)


def fringe_thr(ref: float, level=LEVEL) -> float:
    """A fringe line is below the level and below half the picture line just inside the fringe (ref), so a
    dark picture edge (a plateau, not a step) is not taken for a fringe."""
    return min(level, 0.5 * ref)


def fringe_max(H: int) -> int:
    """The fringe is 0-2 lines in the real frames (codec padding, the player's scaling); more would eat into
    dark picture edges."""
    return round(4 * H / 1080)


class Img:
    """A frame (max of R, G, B in 0..1) with read counting."""

    def __init__(self, a: np.ndarray):
        self.a, self.H, self.W, self.reads = a, a.shape[0], a.shape[1], 0

    def px(self, x: int, y: int) -> float:
        return self.a[min(max(y, 0), self.H - 1), min(max(x, 0), self.W - 1)]

    def corner(self, x: float, y: float) -> float:
        """Bilinear read at pixel coordinates (centres at n + 0.5); at a corner the mean of 4 pixels."""
        self.reads += 1
        x0, y0 = math.floor(x - 0.5), math.floor(y - 0.5)
        fx, fy = x - 0.5 - x0, y - 0.5 - y0
        return ((1 - fx) * (1 - fy) * self.px(x0, y0) + fx * (1 - fy) * self.px(x0 + 1, y0)
                + (1 - fx) * fy * self.px(x0, y0 + 1) + fx * fy * self.px(x0 + 1, y0 + 1))

    def point(self, x: int, y: int) -> float:
        self.reads += 1
        return self.px(x, y)


# ---------------------------------------------------------------- A: line probes, binary search
def method_a(im: Img, level=LEVEL, K=16):
    W, H = im.W, im.H
    seq = 0

    def along(i, n, span, outer):
        t = (i + 0.5) / n
        if not outer:
            return span[0] + (span[1] - span[0]) * t
        w = OUTER * (span[1] - span[0])
        return span[0] + w * 2 * t if t < 0.5 else span[1] - w * 2 * (1 - t)

    def pt(e, l, v):
        return [(v, l), (v, H - l), (l, v), (W - l, v)][e]

    def lit(e, l, span):
        nonlocal seq
        seq += 1
        return any(im.corner(*pt(e, l, math.floor(along(i, K, span, e == 1)))) > 0 for i in range(K))

    def line_max(e, n, span):
        nonlocal seq
        seq += 1
        v = 0.0
        for i in range(2 * K):
            x, y = pt(e, n + 0.5, math.floor(along(i, 2 * K, span, e == 1)) + 0.5)
            v = max(v, im.point(math.floor(x), math.floor(y)))
        return v

    def dark(e, n, span, thr):
        return line_max(e, n, span) < thr

    def search(e, guess, lmax, span):
        if lit(e, 1.0, span):
            return 0 if lit(e, 0.5, span) else 1
        lo, hi = 2.0, lmax + 1.0
        probe = min(max(guess, lo), hi - 1)
        for _ in range(16):
            if lo >= hi:
                break
            if lit(e, probe, span):
                hi = probe
            else:
                lo = probe + 1
            probe = math.floor((lo + hi) / 2)
        return int(lo)

    def refine(e, e0, span):
        if e0 <= 0:
            return e0
        thr = fringe_thr(line_max(e, e0 + fringe_max(H), span), level)
        lo, hi = e0, e0 + fringe_max(H)
        for _ in range(8):
            if lo >= hi:
                break
            n = math.floor((lo + hi) / 2)
            if dark(e, n, span, thr):
                lo = n + 1
            else:
                hi = n
        return int(lo)

    t0 = search(0, round(max(H - W / 2.35, 4) / 2), H // 2, (0, W)); t = refine(0, t0, (0, W))
    rows = (t, H - t)
    l0 = search(2, round(max(W - H * 4 / 3, 4) / 2), W // 2, rows); r0 = search(3, max(l0, 2), W // 2, rows)
    l, r = refine(2, l0, rows), refine(3, r0, rows)
    cols = (l, W - r)
    b0 = search(1, max(t0, 2), H // 2, cols); b = refine(1, b0, cols)
    return (t0, b0, l0, r0), (t, b, l, r), seq


# ---------------------------------------------------------------- B: diagonal search (CeeJay)
def method_b(im: Img, level=LEVEL):
    W, H = im.W, im.H
    seq = 0

    def rd(x, y):  # a corner read at integer corner (x, y): pixels x-1..x, y-1..y
        nonlocal seq
        seq += 1
        return im.corner(float(x), float(y)) > 0

    cx, cy = W // 2, H // 2
    if not rd(cx, cy):
        return None, None, seq                      # black centre: a black frame, or unlucky
    # top corners: (1, 1) and (W - 1, 1) cover the corner pixels
    tl, tr = rd(1, 1), rd(W - 1, 1)
    if tl and tr:
        top0 = left0 = right0 = 0
    else:
        # binary search on s in [0, 1]: point = centre + s * (corner - centre), alternating corners
        lo, hi, side = 0.0, 1.0, 0
        while (hi - lo) * max(cx, cy) > 0.5:
            s = (lo + hi) / 2
            x = round(cx - s * (cx - 1)) if side == 0 else round(cx + s * (W - 1 - cx))
            y = round(cy - s * (cy - 1))
            if rd(x, y):
                lo = s
            else:
                hi = s
            side ^= 1
        # the lit point and the black point next to it (on the left diagonal)
        yl, yb = round(cy - lo * (cy - 1)), round(cy - hi * (cy - 1))
        xl, xb = round(cx - lo * (cx - 1)), round(cx - hi * (cx - 1))
        # which edge: black above the lit point means a top edge, black left of it a side edge
        top_edge = not rd(xl, yb)
        # exact edge along that axis (corner reads cover two lines: first lit line = edge)
        if top_edge:
            a, b = yb, yl                               # black at a, lit at b
            while b - a > 1:
                m = (a + b) // 2
                if rd(xl, m):
                    b = m
                else:
                    a = m
            top0 = a                                    # lines 0..a-1 black (read at a covers a-1, a)
            yin = top0 + 2
            # sides at the row just inside: is there a side bar at all?
            if rd(1, yin):
                left0 = right0 = 0
            else:
                lo2, hi2, side = 1, cx, 0               # black at lo2, lit at hi2 (distance from the side)
                while hi2 - lo2 > 1:
                    m = (lo2 + hi2) // 2
                    if rd(m if side == 0 else W - m, yin):
                        hi2 = m
                    else:
                        lo2 = m
                    side ^= 1
                left0 = right0 = lo2
                left0 = _verify(rd, lambda d: (d, yin), left0, cx)
                right0 = _verify(rd, lambda d: (W - d, yin), left0, cx)
        else:
            a, b = xb, xl
            while b - a > 1:
                m = (a + b) // 2
                if rd(m, yl):
                    b = m
                else:
                    a = m
            left0 = a
            xin = left0 + 2
            if rd(xin, 1):
                top0 = 0
            else:
                lo2, hi2 = 1, cy
                while hi2 - lo2 > 1:
                    m = (lo2 + hi2) // 2
                    if rd(xin, m):
                        hi2 = m
                    else:
                        lo2 = m
                top0 = lo2
            right0 = _verify(rd, lambda d: (W - d, cy), left0, cx)
    # bottom: from the mirrored guess, read near the picture's side (no subtitles)
    xb_ = left0 + max(2, round((W - left0 - right0) * OUTER / 2))
    bottom0 = _verify(rd, lambda d: (xb_, H - d), top0, cy) if not rd(xb_, H - 1) else 0
    pure = (top0, bottom0, left0, right0)
    # fringe: step inward from each edge with point reads while below the level
    fm = fringe_max(H)

    def fringe(e, n0, at):
        nonlocal seq
        pos = lambda n: [(at, n), (at, H - 1 - n), (n, at), (W - 1 - n, at)][e]
        thr = fringe_thr(im.point(*pos(n0 + fm)), level)
        n = n0
        while n < n0 + fm:
            seq += 1
            if im.point(*pos(n)) >= thr:
                break
            n += 1
        return n if n0 > 0 else 0
    xin_ = left0 + max(2, round((W - left0 - right0) * OUTER / 2))
    full = (fringe(0, top0, xin_), fringe(1, bottom0, xin_), fringe(2, left0, cy), fringe(3, right0, cy))
    return pure, full, seq


def _verify(rd, at, guess, lmax):
    """Edge (black lines from the screen edge) near a guess: check the guess, else step 8 lines, then halve.
    at(d) gives the corner read covering lines d - 1 and d."""
    def black(d):
        return d <= 0 or not rd(*at(d))
    g = max(1, guess)
    if black(g) and not black(g + 1):
        return g
    if black(g):                                        # edge further in
        a, b = g, g + 8
        while black(b) and b < lmax:
            a, b = b, b + 8
    else:                                               # edge further out
        a, b = max(0, g - 8), g
        while a > 0 and not black(a):
            a, b = max(0, a - 8), a
    while b - a > 1:                                    # black at a, lit at b
        m = (a + b) // 2
        if black(m):
            a = m
        else:
            b = m
    return a


# ---------------------------------------------------------------- C / D: profiles
def profiles(im: Img, exact: bool):
    """Per row and per column the brightest value in each of SEG segments: exact (every pixel) or from
    CPTS point reads per line."""
    a, H, W = im.a, im.H, im.W
    if exact:
        im.reads += 2 * H * W
        rows = np.stack([s.max(1) for s in np.array_split(a, SEG, axis=1)], 1)      # H x SEG
        cols = np.stack([s.max(0) for s in np.array_split(a, SEG, axis=0)], 1)      # W x SEG
    else:
        xs = ((np.arange(CPTS) + 0.5) * W / CPTS).astype(int)
        ys = ((np.arange(CPTS) + 0.5) * H / CPTS).astype(int)
        im.reads += CPTS * (H + W)
        rows = a[:, xs].reshape(H, SEG, CPTS // SEG).max(2)
        cols = a[ys, :].T.reshape(W, SEG, CPTS // SEG).max(2)
    return rows, cols


def scan_profiles(rows: np.ndarray, cols: np.ndarray, H: int, W: int, level=LEVEL, inside_out=False):
    """Outside-in: the black lines from the screen edge until the first lit one. Inside-out: from the screen
    centre outward to the first black line (the picture is connected around the centre, so subtitles further
    out in a bar do not count); left / right on the middle half of the rows, then top / bottom on the outer
    1/16 of the picture's width at each end."""
    fm = fringe_max(H)
    if inside_out:
        def out(prof):  # black lines from the edge (index 0) inward up to the first black line seen from the centre
            lit = np.nonzero(prof > 0)[0]
            if not len(lit):
                return None
            c = lit[np.argmin(np.abs(lit - len(prof) // 2))]   # the lit line nearest the centre
            i = c
            while i > 0 and prof[i - 1] > 0:
                i -= 1
            return i

        def edge_io(p, n_max):
            e0 = out(p)
            if e0 is None or e0 > n_max:
                return None, None
            e1, thr = e0, fringe_thr(p[min(e0 + fm, len(p) - 1)], level)
            while e0 > 0 and e1 < e0 + fm and p[e1] < thr:
                e1 += 1
            return e0, e1

        def segs_io(lo, hi, n):
            e = np.linspace(0, n, SEG + 1)
            return [k for k in range(SEG) if e[k + 1] > lo and e[k] < hi] or list(range(SEG))
        def sides(r_lo, r_hi):
            pc = cols[:, segs_io(r_lo, r_hi, H)].max(1)
            return edge_io(pc, W // 2), edge_io(pc[::-1], W // 2)
        # sides on the middle quarter of the rows (clear of subtitles in a bottom bar), top / bottom on the
        # picture's outer columns, then the sides again on the picture's rows
        (l0, l), (r0, r) = sides(3 * H / 8, 5 * H / 8)
        if l0 is None or r0 is None:
            return None, None
        pw = W - l - r
        osel = sorted(set(segs_io(l, l + OUTER * pw, W)) | set(segs_io(W - r - OUTER * pw, W - r, W)))
        pr = rows[:, osel].max(1)
        t0, t = edge_io(pr, H // 2)
        b0, b = edge_io(pr[::-1], H // 2)
        if t0 is None or b0 is None:
            return None, None
        (l0, l), (r0, r) = sides(t, H - b)
        if l0 is None or r0 is None:
            return None, None
        return tuple(map(int, (t0, b0, l0, r0))), tuple(map(int, (t, b, l, r)))

    def first(prof, thr, start=0, stop=None):
        """Number of lines from the start that stay at or below thr (pure: thr 0 -> == 0)."""
        n = len(prof) if stop is None else stop
        for i in range(start, n):
            if (prof[i] > thr if thr == 0 else prof[i] >= thr):
                return i
        return n

    def segs(lo, hi, n):  # segments overlapping [lo, hi) of a line of n pixels
        e = np.linspace(0, n, SEG + 1)
        return [k for k in range(SEG) if e[k + 1] > lo and e[k] < hi] or list(range(SEG))

    def edge(prof_lines, sel, n_max):
        p = prof_lines[:, sel].max(1)
        e0 = first(p, 0, 0, n_max)
        e1 = first(p, fringe_thr(p[min(e0 + fm, len(p) - 1)], level), e0, min(n_max, e0 + fm)) if e0 > 0 else 0
        return e0, e1

    t0, t = edge(rows, segs(0, W, W), H // 2)
    rsel = segs(t, H - t, H)
    l0, l = edge(cols, rsel, W // 2)
    r0, r = edge(cols[::-1], rsel, W // 2)
    pw = W - l - r
    bsel = sorted(set(segs(l, l + OUTER * pw, W)) | set(segs(W - r - OUTER * pw, W - r, W)))
    b0, b = edge(rows[::-1], bsel, H // 2)
    return tuple(map(int, (t0, b0, l0, r0))), tuple(map(int, (t, b, l, r)))


# ---------------------------------------------------------------- runs over frames
def run_sequence(frames: list, method: str):
    """Detection over a run of frames; returns (pure, with fringe, reads per frame, sequential depth)."""
    reads = depth = 0
    if method in "AB":
        best = None
        for f in frames:
            im = Img(f)
            pure, full, seq = (method_a if method == "A" else method_b)(im)
            reads, depth = max(reads, im.reads), max(depth, seq)
            if pure is None:
                continue
            H, W = f.shape
            if pure[0] + pure[1] >= 0.9 * H or pure[2] + pure[3] >= 0.9 * W:
                continue                                # almost all black: skip
            best = (pure, full) if best is None else (tuple(map(min, best[0], pure)), tuple(map(min, best[1], full)))
        if best is None:
            return None, None, reads, depth
        return best[0], best[1], reads, depth
    acc = None
    for f in frames:
        im = Img(f)
        rows, cols = profiles(im, method in "DE")
        reads = max(reads, im.reads)
        acc = (rows, cols) if acc is None else (np.maximum(acc[0], rows), np.maximum(acc[1], cols))
    H, W = frames[0].shape
    pure, full = scan_profiles(acc[0], acc[1], H, W, inside_out=method in "EF")
    return pure, full, reads, 3


# ---------------------------------------------------------------- test frames
def load_frame(p: Path) -> np.ndarray:
    from PIL import Image
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float64).max(2) / 255.0


def truth_of(a: np.ndarray):
    """The answer on a real frame, from every pixel: inside-out (the picture is connected around the centre;
    subtitles further out in a bar are not picture), sides on the middle half of the rows, top / bottom on
    the picture's outer 1/16 columns. Checked by eye on a contact sheet."""
    H, W = a.shape
    fm = fringe_max(H)

    def out(prof):
        lit = np.nonzero(prof > 0)[0]
        i = lit[np.argmin(np.abs(lit - len(prof) // 2))]
        while i > 0 and prof[i - 1] > 0:
            i -= 1
        e1, thr = i, fringe_thr(prof[min(i + fm, len(prof) - 1)])
        while i > 0 and e1 < i + fm and prof[e1] < thr:
            e1 += 1
        return int(i), int(e1)
    col = a[H // 4: 3 * H // 4].max(0)
    (l0, l), (r0, r) = out(col), out(col[::-1])
    o = max(1, round((W - l - r) * OUTER))
    row = np.maximum(a[:, l:l + o].max(1), a[:, W - r - o:W - r].max(1))
    (t0, t), (b0, b) = out(row), out(row[::-1])
    return (t0, b0, l0, r0), (t, b, l, r)


def synthetic(pictures: list, rng) -> list:
    """(name, frames, truth pure, truth with fringe) with known bars."""
    W, H = 1920, 1080
    out = []

    def place(pic, T, B, L, R, fringe=0, subs=False, dark=1.0, vignette=False, sub_w=700, sub_y=None):
        f = np.zeros((H, W))
        ph, pw = H - T - B, W - L - R
        ys = (np.arange(ph) * pic.shape[0] / ph).astype(int)
        xs = (np.arange(pw) * pic.shape[1] / pw).astype(int)
        p = pic[ys][:, xs] * dark
        if vignette:
            yy, xx = np.mgrid[0:ph, 0:pw]
            d = np.hypot((xx - pw / 2) / (pw / 2), (yy - ph / 2) / (ph / 2)) / math.sqrt(2)
            p = p * np.clip(1.3 - 1.3 * d, 0, 1) ** 2
        f[T:H - B, L:W - R] = p
        for k in range(fringe):                     # compression fringe: near black, patchy, fading out
            amp = (k + 1) / (fringe + 1) * 12 / 255
            if T: f[T - 1 - k, L:W - R] = amp * rng.random(pw) * (rng.random(pw) < 0.7)
            if B: f[H - B + k, L:W - R] = amp * rng.random(pw) * (rng.random(pw) < 0.7)
            if L: f[T:H - B, L - 1 - k] = amp * rng.random(ph) * (rng.random(ph) < 0.7)
            if R: f[T:H - B, W - R + k] = amp * rng.random(ph) * (rng.random(ph) < 0.7)
        if subs:                                    # white text, grey outline, near-black shadow, centred
            y0 = sub_y if sub_y is not None else (H - max(B, 60) + 10 if B > 70 else H - 110)
            for j in range(2):
                yy = y0 + j * 45
                x0 = W // 2 - sub_w // 2 - 20 + j * 40
                f[yy + 4:yy + 38, x0 + 4:x0 + sub_w + 4] = np.maximum(f[yy + 4:yy + 38, x0 + 4:x0 + sub_w + 4], 3 / 255)  # shadow
                f[yy:yy + 34, x0:x0 + sub_w] = 0.5                                                                     # outline
                f[yy + 3:yy + 31, x0 + 3:x0 + sub_w - 3] = 0.95 * (rng.random((28, sub_w - 6)) < 0.5)               # glyphs
        return f

    def add(name, T, B, L, R, n=1, fringe=0, **kw):
        frames = [place(pictures[k % len(pictures)], T, B, L, R, fringe, **kw.get("kw", {})) for k in range(n)]
        out.append((name, frames, (T, B, L, R), (T, B, L, R)))

    out_pure = []
    for name, T, B, L, R, fr, extra in [
            ("2.39:1", 138, 138, 0, 0, 0, {}), ("2.39:1 + subtitles in the bar", 138, 138, 0, 0, 0, {"subs": True}),
            ("4:3 pillarbox", 0, 0, 240, 240, 0, {}), ("windowbox", 270, 270, 480, 480, 0, {"subs": True}),
            ("uneven 1.85 + subs", 40, 160, 0, 0, 0, {"subs": True}), ("2.39:1 fringe 4", 138, 138, 0, 0, 4, {}),
            ("windowbox fringe 3 + subs", 200, 200, 300, 300, 3, {"subs": True}), ("no bars", 0, 0, 0, 0, 0, {}),
            ("windowbox, subtitles wider than the picture", 300, 300, 640, 640, 0, {"subs": True, "sub_w": 1100}),
            ("2.39:1, subtitles over the picture's edge", 138, 138, 0, 0, 0, {"subs": True, "sub_y": 1080 - 138 - 20}),
            ("small windowbox, wide subtitles at the screen bottom", 380, 380, 700, 700, 0,
             {"subs": True, "sub_w": 1300, "sub_y": 990})]:
        f = place(pictures[len(out) % len(pictures)], T, B, L, R, fr, **extra)
        # the fringe lies in the bars next to the picture: pure black ends fr lines earlier
        out_pure.append((name, [f], tuple(v - fr if v else 0 for v in (T, B, L, R)), (T, B, L, R)))
    # dark scenes: one frame alone, and a 1 s run where the light comes back
    for name, T, B, L, R in [("2.39:1 dark vignetted scene", 138, 138, 0, 0), ("windowbox dark vignetted scene", 270, 270, 480, 480)]:
        d = place(pictures[0], T, B, L, R, dark=0.25, vignette=True)
        out_pure.append((name + " (one frame)", [d], (T, B, L, R), (T, B, L, R)))
        seq = [d] * 20 + [np.zeros((H, W))] * 5 + [place(pictures[1 % len(pictures)], T, B, L, R)] * 5
        out_pure.append((name + " + black frames + a lit frame (run)", seq, (T, B, L, R), (T, B, L, R)))
    return out_pure


def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    rng = np.random.default_rng(3)
    real = []
    if folder:
        for p in sorted(folder.iterdir()):
            if p.suffix.lower() in (".png", ".webp", ".jpg", ".bmp"):
                real.append((p.name, load_frame(p)))
    pictures = []
    for _, a in real:                                   # picture crops for the synthetic frames
        tb = truth_of(a)[1]
        pic = a[tb[0]:a.shape[0] - tb[1], tb[2]:a.shape[1] - tb[3]]
        if pic.size:
            pictures.append(pic)
    if not pictures:
        pictures = [np.clip(rng.random((400, 700)) * 0.8 + 0.1, 0, 1)]
    pictures.sort(key=lambda p: -p.mean())             # the brightest first: only the darkness tests are dark
    cases = [(name, [a], *truth_of(a)) for name, a in real] + synthetic(pictures, rng)
    lines = ["# Movie Night bar detection: methods compared", "",
             "Generated by `python -m scripts.bar_detect_sim <frames>`; methods in the script's docstring.",
             "Bars as (top, bottom, left, right) in pixels; ok = exactly right; pure = the black bar, full = with",
             f"the near-black fringe below {round(LEVEL * 255)}/255. reads = per frame; seq = dependent probes (latency).", ""]
    score = {m: [0, 0, 0, 0] for m in "ABCDEF"}
    for name, frames, tp, tf in cases:
        lines += [f"## {name}", "", f"truth: pure {tp}, full {tf}", "",
                  "| method | pure | full | reads | seq |", "|---|---|---|---:|---:|"]
        for m in "ABCDEF":
            pure, full, reads, seq = run_sequence(frames, m)
            okp, okf = pure == tuple(tp), full == tuple(tf)
            near = full is not None and max(abs(a - b) for a, b in zip(full, tf)) <= 1
            score[m][0] += okp; score[m][1] += okf; score[m][2] += near; score[m][3] += 1
            mark = lambda v, ok: f"{v} {'ok' if ok else '**wrong**'}" if v is not None else "**skipped**"
            lines.append(f"| {m} | {mark(pure, okp)} | {mark(full, okf)} | {reads} | {seq} |")
        lines.append("")
    summary = ["## Summary", "", "| method | pure exact | full exact | full within 1 line |", "|---|---:|---:|---:|"]
    summary += [f"| {m} | {s[0]} / {s[3]} | {s[1]} / {s[3]} | {s[2]} / {s[3]} |" for m, s in score.items()]
    lines[6:6] = summary + [""]
    (ROOT / "results" / "bar_detect.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
