"""Model brightness-only blurs and a brightness/colour split (colour one level
lower) against the RGB effect, per size class (GTX 1660 model, 1080p).

    python -m scripts.luma_split
"""
import math, re, dataclasses
from scripts import make_effect as M
from topt.cost import pipeline_cost, _pass_time, composite_baseline, GTX1660 as g
W, H = 1920, 1080
N = W * H
fx = open("fx/TOPT_Blur.fx").read()
sel = re.findall(r"(?:TOPT_SIGMA_SCREEN <= (\d+)|#else)\n\t#define TOPT_CLASS \d+ // '(\w+)'( separable)?", fx)
def cls(s):
    for b, n, sep in sel:
        if not b or s <= int(b): return n, bool(sep)
def sl_for(n, s):
    C, B = M.chain_variance(n); d = M.CLASSES[n]
    hi = 1.6 if n == "4s" else M.SL_MAX
    return min(hi, max(d[4], math.sqrt(max(s * s - C, 0) / B)))
def with_bpp(pl, bpp):
    ps = [dataclasses.replace(p, bpp=bpp) for p in pl.passes[:-1]] + [pl.passes[-1]]
    return dataclasses.replace(pl, passes=ps)
def split_cost(n, sl, sep, lbpp=1, cbpp=2):
    """Down1 writes luma + chroma (MRT, same size); chroma is halved again and blurred there;
    the composite upsamples both. Luma blur as in the class; chroma blur at half its sigma."""
    pl = M.pipeline(n, sl, 9, sep)
    down = M.CLASSES[n][0]
    D = 1
    t = 0.0
    for k, f in enumerate(down):
        D *= f
        nd = (W // D) * (H // D); ns = N if k == 0 else (W // (D // f)) * (H // (D // f))
        taps = len(pl.passes[k].taps)
        rb = ns * (4 if k == 0 else lbpp + cbpp)
        t += _pass_time(nd, min(ns, nd * taps * 4), taps, g, lbpp + cbpp, rb)[0]
    nl = (W // D) * (H // D)
    blur = pl.passes[len(down):len(pl.passes) - 1]
    nblur = len(blur) - (len(M.CLASSES[n][2]) - 1)   # blur passes (the rest are extra up passes)
    for p in blur:
        t += _pass_time(nl, nl, len(p.taps), g, lbpp, nl * lbpp)[0]
    # chroma: x2 down (4 taps) + one 2D blur at 1/(2D) with ~ (np)^2 taps of half the sigma
    nc = (W // (2 * D)) * (H // (2 * D))
    t += _pass_time(nc, nl, 4, g, cbpp, nl * cbpp)[0]
    t += _pass_time(nc, nc, 9, g, cbpp, nc * cbpp)[0]
    up = len(pl.passes[-1].taps)
    t += _pass_time(N, N, up + 4 + 1, g, 4, N * 4 + nl * lbpp + nc * cbpp)[0]
    return (t - composite_baseline(W, H, g)) * 1e6
print("sigma  class        RGB10A2  luma R16F  luma R8   split Y8+C(RG8, 2x lower)")
for s in (2, 3, 4, 6, 8, 12, 16, 32, 64):
    n, sep = cls(s); sl = sl_for(n, s)
    pl = M.pipeline(n, sl, 9, sep)
    rgb = pipeline_cost(pl)["us"]
    l16 = pipeline_cost(with_bpp(pl, 2))["us"]; l8 = pipeline_cost(with_bpp(pl, 1))["us"]
    print(f"{s:5d}  {n:>3}{' sep' if sep else '    '}   {rgb:8.0f} {l16:9.0f} {l8:9.0f} {split_cost(n, sl, sep):12.0f}")
