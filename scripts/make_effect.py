"""Generate the research blur effect fx/TOPT_Blur.fx from the optimizer's designs (and fx/MovieNight.fx,
which uses the same blur: scripts/movienight.py; both include fx/TOPT_BlurTables.fxh, the size classes).

Structure per size class (downsample factor D): one wide box*binomial
downsample pass (x8 then the rest for D >= 16), one single-pass 2D Gaussian at
1/D resolution whose width is computed at runtime, and a pinwheel upsample (or,
in the "e" classes, one bilinear read) fused into the composite pass; the low-res blur is split into H + V passes where that
is clearly cheaper. Size 1 (sigma 0.7..1.3) is a single pinwheel pass. The
runtime kernels are emulated here to verify quality over each class's range.

    python -m scripts.make_effect             (class checks, per-GPU tables, all files; ~25 min)
    python -m scripts.make_effect --render    (re-render the files from results/topt_blur_tables.json)
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np

from topt import search as S
from topt.cost import pipeline_cost
from topt.quality import metrics
from topt.sim import Pass, Pipeline

ROOT = Path(__file__).resolve().parent.parent
SL_MIN, SL_MAX = 1.6, 3.4          # low-res sigma range that keeps medium quality (D >= 4)
TRUNC = 2.5                        # low-res kernel radius in low-res sigmas
# name: (down factors, down binomial e, up steps, up filter, lowest low-res sigma for medium quality)
CLASSES = {
    "2": ((2,), 3, (2,), "p4", 0.8),
    "4s": ((4,), 9, (2, 2), "e2", 0.35),  # two-step 2x2 upsample: smooth enough at small sl (tv fails at 0.33)
    "4": ((4,), 5, (4,), "p5", SL_MIN),
    "8": ((8,), 3, (8,), "p4", SL_MIN),
    # x16 and more: x8 first, then the rest (one x16 pass into a 1/16 target leaves the GPU under-filled at
    # 1080p and reads 144 taps per pixel: TexBench P13c)
    "16": ((8, 2), 3, (16,), "p4", 1.4),
    "32": ((8, 4), 3, (32,), "p4", 1.4),
    "64": ((8, 8), 3, (64,), "p4", 1.4),
    "128": ((8, 16), 3, (128,), "p4", 1.4),
    # one bilinear read to upsample (e1): medium quality from a wider low-res Gaussian (sl >= 2.0..2.6),
    # so a narrower sigma range, but 3 fewer full-resolution reads
    "8e": ((8,), 3, (8,), "e1", 2.5),   # blocky just above 2.4 (radius 7)
    "16e": ((8, 2), 3, (16,), "e1", 2.2),
    "32e": ((8, 4), 1, (32,), "e1", 2.6),
    "64e": ((8, 8), 1, (64,), "e1", 2.6),
    "128e": ((8, 16), 1, (128,), "e1", 2.6),
    # in-between factors, so the one-read classes also cover the sigmas between the ones above
    # (1/48 at 1080p is 40 x 22.5 texels: the target rounds to 22, 2 % off vertically)
    "6e": ((6,), 3, (6,), "e1", 2.45),  # r = ceil(2.5 sl) = 6 (sl <= 2.4) fails medium
    "12e": ((4, 3), 3, (12,), "e1", 2.4),
    "24e": ((8, 3), 3, (24,), "e1", 2.2),
    "48e": ((8, 6), 3, (48,), "e1", 2.05),  # blocky just above 2.0 (radius 6)
}


# Single-pass class for sigma 0.7..1.3 (BLUR_SIZE 1 at 1080p): a centre texel plus
# a 4-fold pinwheel of 2x2 texel blocks. A Gaussian is separable, so one bilinear
# fetch reproduces a block's four Gaussian weights exactly; offsets and weights
# are computed at runtime. Blocks (lower-left texel of one arm, the other three
# arms are its 90-degree rotations) nest: the first 2 give 9 fetches, 3 give 13, 4 give 17.
SMALL_ARM = [(1, -1), (2, 1), (3, -1), (3, -3)]
SMALL_STEPS = [(0.9, 2), (1.1, 3), (1.3, 4)]   # (max sigma at medium quality, arm blocks)


def small_blocks(sigma: float) -> int:
    return next((n for smax, n in SMALL_STEPS if sigma <= smax), SMALL_STEPS[-1][1])


def small_taps(sigma: float) -> tuple:
    g = lambda v: math.exp(-0.5 * (v / sigma) ** 2)
    t = [(0.0, 0.0, 1.0)]
    for x, y in SMALL_ARM[:small_blocks(sigma)]:
        wx, wy = g(x) + g(x + 1), g(y) + g(y + 1)
        ox, oy = x + g(x + 1) / wx, y + g(y + 1) / wy
        t += [(ox, oy, wx * wy), (-oy, ox, wx * wy), (-ox, -oy, wx * wy), (oy, -ox, wx * wy)]
    tot = sum(w for *_, w in t)
    return tuple((a, b, w / tot) for a, b, w in t)


def small_pipeline(sigma: float) -> Pipeline:
    return Pipeline("TOPT_Blur", {"class": "1", "sigma": sigma}, [Pass(1, small_taps(sigma))])


def up_taps(name: str) -> tuple:
    kind, n = name[0], int(name[1:])
    return tuple(S.UP_PIN[n]) if kind == "p" else S.outer(S.up_taps_1d(n))


def runtime_taps_1d(sl: float, rmax: int) -> list:
    """The shader's 1D low-res kernel: Gaussian(sl) over -r..r, r = min(rmax, ceil(TRUNC*sl)),
    centre tap + symmetric pairs merged into bilinear taps, as (offset, weight)."""
    r = min(rmax, max(1, math.ceil(TRUNC * sl)))
    g = lambda i: math.exp(-0.5 * (i / sl) ** 2) if i <= r else 0.0
    t1 = [(0.0, g(0))]
    for i in range(1, r + 1, 2):
        a, b = g(i), g(i + 1)
        o = i + b / (a + b)
        t1 += [(o, a + b), (-o, a + b)]
    tot = sum(w for _, w in t1)
    return [(o, w / tot) for o, w in t1]


def runtime_bottom(sl: float, rmax: int, sep: bool = False) -> list:
    """The low-res blur passes: one 2D (outer product) pass, or H then V."""
    t1 = runtime_taps_1d(sl, rmax)
    if sep:
        return [tuple((o, 0.0, w) for o, w in t1), tuple((0.0, o, w) for o, w in t1)]
    return [tuple((ox, oy, wx * wy) for ox, wx in t1 for oy, wy in t1)]


def pipeline(name: str, sl: float, rmax: int, sep: bool = False) -> Pipeline:
    down, e, ups, upf, _ = CLASSES[name]
    passes, div = [], 1
    for f in down:
        div *= f
        passes.append(Pass(div, S.outer(S.down_taps_1d(f, e))))
    passes += [Pass(div, t) for t in runtime_bottom(sl, rmax, sep)]
    for u in ups:
        div //= u
        passes.append(Pass(div, up_taps(upf)))
    return Pipeline("TOPT_Blur", {"class": name, "sl": sl, "sep": sep}, passes)


def chain_variance(name: str) -> tuple:
    """Blur (full-res px^2) added by the down/up chain alone: sigma^2 = C + B sl^2."""
    rmax = math.ceil(TRUNC * SL_MAX)
    s1, s2 = 1.6, 3.0
    g1 = metrics(pipeline(name, s1, rmax))["sigma"] ** 2
    g2 = metrics(pipeline(name, s2, rmax))["sigma"] ** 2
    b = (g2 - g1) / (s2 * s2 - s1 * s1)
    return g1 - b * s1 * s1, b


def _f(v: float) -> str:
    """A float literal in short form (1. not 1.0)."""
    s = f"{v:.9g}"
    return s if any(c in s for c in ".e") else s + "."


def _w(v: float) -> str:
    """A weight: as a fraction where it is one exactly (1. / 16), else a float."""
    from fractions import Fraction
    q = Fraction(v).limit_denominator(1 << 16)
    if abs(float(q) - v) > 1e-15 * max(1.0, abs(v)):
        return _f(v)
    return f"{q.numerator}." if q.denominator == 1 else f"{q.numerator}. / {q.denominator}"


_CTOR = re.compile(r"\bfloat[234]?\s*\($")
_WHOLE = re.compile(r"\s*-?\s*\d+\.\s*")


def short_floats(code: str) -> str:
    """1.0 -> 1., 2.0 -> 2. in generated code (not in exponents or longer decimals); a whole number that is
    a whole argument of a float / floatN constructor loses the point too: float2(1., 0.) -> float2(1, 0)
    (the constructor makes it a float; elsewhere it stays 1. so it is not read as an int)."""
    code = re.sub(r"(?<![\w.])(\d+)\.0(?![\d\w])", r"\1.", code)
    out, stack, arg = [], [], 0      # stack: is each open bracket a float constructor; arg: start of its argument
    for i, ch in enumerate(code):
        if ch in "([":
            stack.append((ch == "(" and bool(_CTOR.search(code[max(0, i - 12):i + 1])), len(out) + 1))
        elif ch in ",)]" and stack:
            ctor, start = stack[-1]
            if ctor and _WHOLE.fullmatch("".join(out[start:])):
                a = "".join(out[start:])
                out[start:] = list(a.replace(".", "", 1))
            if ch == ",":
                stack[-1] = (ctor, len(out) + 1)
            else:
                stack.pop()
        out.append(ch)
    return "".join(out)


def class_info(rmax: int) -> dict:
    """Per class: chain variance (C, B), low-res sigma range, screen sigma range, quality checks."""
    info = {}
    for name, (down, e, ups, upf, lo) in CLASSES.items():
        C, b = chain_variance(name)
        hi = SL_MAX if name != "4s" else 1.6
        smin, smax = math.sqrt(C + b * lo * lo), math.sqrt(C + b * hi * hi)
        checks = []
        for sl in np.linspace(lo, hi, 4):
            pl = pipeline(name, float(sl), rmax)
            q = metrics(pl)
            ok = [n for n, p in S.PROFILES.items()
                  if S.passes_profile({**q, "sigma_err": 0.0}, p) and q["block"] <= S.NOISE_BLOCK_MAX]
            qs = metrics(pipeline(name, float(sl), rmax, True))
            oks = [n for n, p in S.PROFILES.items()
                   if S.passes_profile({**qs, "sigma_err": 0.0}, p) and qs["block"] <= S.NOISE_BLOCK_MAX]
            checks.append((round(q["sigma"], 1), "/".join(ok) or "FAIL", round(pipeline_cost(pl)["us"]),
                           "sep:" + ("/".join(oks) or "FAIL"), round(pipeline_cost(pipeline(name, float(sl), rmax, True))["us"])))
        info[name] = (C, b, lo, hi, smin, smax, checks)
        print(f"{name:>4}: C={C:8.2f} B={b:8.1f} sigma {smin:6.1f}..{smax:6.1f}  {checks}", flush=True)
    return info


def options(info: dict, sig: int, rmax: int) -> list:
    """(class, separable, pipeline) candidates for an integer screen sigma."""
    out = []
    for name, (C, b, lo, hi, smin, smax, _) in info.items():
        if smin - 0.5 <= sig <= smax + 0.5:
            sl = min(hi, max(lo, math.sqrt(max(sig * sig - C, 0.0) / b)))
            out += [(name, sep, pipeline(name, sl, rmax, sep)) for sep in (False, True)]
    return out


# GPU families by PCI vendor / device id ranges (approximate, from the PCI id lists), each mapped to the
# profile (topt/gpu_profiles.json) of its architecture. Unlisted GPUs get the least-regret table.
FAMILIES = [
    (0x10DE, 0x1340, 0x17FF, "GTX 860M", "NVIDIA Maxwell"),
    (0x10DE, 0x1B00, 0x1DFF, "GTX 1080", "NVIDIA Pascal"),
    (0x10DE, 0x2180, 0x21FF, "GTX 1660", "NVIDIA Turing GTX 16 (TU116)"),
    (0x10DE, 0x1E00, 0x1FFF, "RTX 2070", "NVIDIA Turing (TU10x, TU117)"),
    (0x10DE, 0x2200, 0x25FF, "RTX 3060", "NVIDIA Ampere"),
    (0x10DE, 0x2600, 0x28FF, "RTX 4070", "NVIDIA Ada"),
    (0x10DE, 0x2900, 0x2FFF, "RTX 5070", "NVIDIA Blackwell"),
    (0x1002, 0x6700, 0x69FF, "RX 590", "AMD GCN (Polaris, Vega)"),
    (0x1002, 0x7310, 0x739F, "RX 5500 XT", "AMD RDNA 1"),
    (0x1002, 0x73A0, 0x743F, "RX 6600", "AMD RDNA 2"),
    (0x1002, 0x7440, 0x74FF, "RX 7900 XTX", "AMD RDNA 3"),
    (0x1002, 0x7500, 0x75FF, "RX 9070 XT", "AMD RDNA 4"),
    (0x1002, 0x1500, 0x19FF, "Radeon 680M", "AMD Ryzen iGPUs (RDNA 2 / 3)"),
    (0x8086, 0x1900, 0x193F, "UHD 630", "Intel Gen9 (Skylake)"),
    (0x8086, 0x5900, 0x59FF, "UHD 630", "Intel Gen9.5 (Kaby Lake)"),
    (0x8086, 0x3E90, 0x3EFF, "UHD 630", "Intel Gen9.5 (Coffee Lake)"),
    (0x8086, 0x9B00, 0x9BFF, "UHD 630", "Intel Gen9.5 (Comet Lake)"),
    (0x8086, 0x9A40, 0x9AFF, "Iris Xe", "Intel Gen12 (Tiger Lake)"),
    (0x8086, 0x4680, 0x46FF, "Iris Xe", "Intel Gen12 (Alder Lake)"),
    (0x8086, 0xA780, 0xA7FF, "Iris Xe", "Intel Gen12 (Raptor Lake)"),
    (0x8086, 0x5690, 0x56FF, "Arc B580", "Intel Arc (Alchemist)"),
    (0x8086, 0xE200, 0xE2FF, "Arc B580", "Intel Arc (Battlemage)"),
    (0x8086, 0x6400, 0x64FF, "Arc B580", "Intel Xe2 (Lunar Lake)"),
    (0x8086, 0x7D40, 0x7DFF, "Arc B580", "Intel Xe-LPG (Meteor Lake)"),
]
TABLE_RES = ("1080p", "4k")
SEP_MARGIN = 1.0   # % of a composite pass the separable variant must save (near-ties keep the 2D pass)


def gpu_tables(info: dict, rmax: int) -> tuple:
    """Per GPU profile the class choice for every integer screen sigma (least regret over 1080p and 4K,
    regret in % of that GPU's composite pass); profiles with the same choices share a table. Also the
    least mean regret over all profiles, for unknown GPUs."""
    import numpy as np
    from topt.cost import CORE as PROFILES, RESOLUTIONS, composite_baseline
    gpus = list(PROFILES)
    picks = {g: [] for g in gpus + [None]}
    for sig in range(2, 441):
        opts = options(info, sig, rmax)
        if not opts:
            for g in picks:
                picks[g].append(picks[g][-1])
            continue
        cost = np.array([[[pipeline_cost(p, *RESOLUTIONS[r], gpu=PROFILES[g])["us"] for r in TABLE_RES] for g in gpus]
                         for _, _, p in opts])
        base = np.array([[composite_baseline(*RESOLUTIONS[r], PROFILES[g]) * 1e6 for r in TABLE_RES] for g in gpus])
        regret = (100 * (cost - cost.min(0)) / base).mean(2)       # option x gpu
        regret[1::2] += SEP_MARGIN                                  # separable only for a clear win
        for j, g in enumerate(gpus + [None]):
            r = regret.mean(1) if g is None else regret[:, j]
            k = int(np.argmin(r))
            picks[g].append((opts[k][0], opts[k][1]))
    def intervals(choice):
        iv = [[1, 1, ("1", False)]]
        for sig, key in enumerate(choice, 2):
            if iv[-1][2] == key:
                iv[-1][1] = sig
            else:
                iv.append([sig, sig, key])
        return iv
    groups = {}
    for g in gpus:
        groups.setdefault(tuple(picks[g]), []).append(g)
    tables = [(gs, intervals(list(k))) for k, gs in groups.items()]
    return tables, intervals(picks[None])


def main():
    rmax = math.ceil(TRUNC * SL_MAX)
    info = class_info(rmax)
    small = []
    for sig in (0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3):
        q = metrics(small_pipeline(sig))
        ok = [n for n, p in S.PROFILES.items() if S.passes_profile({**q, "sigma_err": 0.0}, p)]
        small.append((round(q["sigma"], 2), "/".join(ok) or "FAIL", round(pipeline_cost(small_pipeline(sig))["us"])))
    print(f"   1: single pass {small}", flush=True)
    tables, default = gpu_tables(info, rmax)
    (ROOT / "results" / "topt_blur_tables.json").write_text(json.dumps({"info": info, "tables": tables, "default": default}))
    write(info, tables, default, rmax)


def write(info: dict, tables: list, default: list, rmax: int):
    for t, (gpus, iv) in enumerate(tables, 1):
        print(f"table {t} ({', '.join(gpus)}):", [(a, b, n) for a, b, n in iv])
    print("table 0 (unknown GPU):", [(a, b, n) for a, b, n in default])
    (ROOT / "fx" / "TOPT_BlurTables.fxh").write_text(render_tables(info, tables, default))
    (ROOT / "fx" / "TOPT_Blur.fx").write_text(render(info, tables, default, rmax))
    print("wrote fx/TOPT_BlurTables.fxh, fx/TOPT_Blur.fx")
    from scripts import movienight
    (ROOT / "fx" / "MovieNight.fx").write_text(render(info, tables, default, rmax, movienight.TEMPLATE))
    print("wrote fx/MovieNight.fx")


VENDOR_NAMES = {0x10DE: "NVIDIA", 0x1002: "AMD", 0x8086: "Intel"}


def render_tables(info: dict, tables: list, default: list) -> str:
    """fx/TOPT_BlurTables.fxh: the GPU's table, the size class for the blur size, the class constants."""
    ids = {n: i + 1 for i, n in enumerate(CLASSES)}
    ids["1"] = 0
    table_of = {g: t for t, (gs, _) in enumerate(tables, 1) for g in gs}
    out = [TABLES_HEAD, "#ifndef BLUR_GPU"]
    fams = [f for f in FAMILIES if f[3] in table_of]
    for i, vendor in enumerate(dict.fromkeys(f[0] for f in fams)):
        out.append(f"\t#{'if' if i == 0 else 'elif'} __VENDOR__ == 0x{vendor:04X} // {VENDOR_NAMES.get(vendor, '')}")
        for j, (_, lo, hi, prof, label) in enumerate(f for f in fams if f[0] == vendor):
            out.append(f"\t\t#{'if' if j == 0 else 'elif'} __DEVICE__ >= 0x{lo:04X} && __DEVICE__ <= 0x{hi:04X} "
                       f"// {prof} profile\n\t\t\t#define BLUR_GPU {table_of[prof]}\n\t\t\t#define BLUR_GPU_NAME \"{label}\"")
        out += [f"\t\t#else\n\t\t\t#define BLUR_GPU 0\n\t\t\t#define BLUR_GPU_NAME \"{VENDOR_NAMES.get(vendor, '')}, unknown model\"",
                "\t\t#endif"]
    out += ["\t#else\n\t\t#define BLUR_GPU 0 // unknown GPU: least regret over all profiles\n\t\t#define BLUR_GPU_NAME \"unknown\"",
            "\t#endif", "#endif", "#ifndef BLUR_GPU_NAME\n\t#define BLUR_GPU_NAME \"set by hand (BLUR_GPU)\"\n#endif", "",
            "// Per table: BLUR_CHOICE = 2 * class + separable, by the blur sigma on screen (px)."]
    for t, iv in [(t, iv) for t, (_, iv) in enumerate(tables, 1)] + [(0, default)]:
        gs = ", ".join(tables[t - 1][0]) if t else "unknown GPUs"
        out.append(f"#{'if' if t == 1 else 'elif'} BLUR_GPU == {t} // {gs}" if t else f"#else // {gs}")
        for i, (a, b, (name, sep)) in enumerate(iv):
            cond = "#if" if i == 0 else "#elif" if i < len(iv) - 1 else "#else"
            test = f" BLUR_SIGMA_SCREEN <= {b}" if i < len(iv) - 1 else ""
            out.append(f"\t{cond}{test} // '{name}'{' separable' if sep else ''}\n\t\t#define BLUR_CHOICE {2 * ids[name] + sep}")
        out.append("\t#endif")
    out += ["#endif", "#define BLUR_CLASS (BLUR_CHOICE / 2)", "#define BLUR_SEP (BLUR_CHOICE % 2)", ""]
    arm = ", ".join(f"float2({x}.0, {y}.0)" for x, y in SMALL_ARM)
    steps = " : ".join(f"sigma <= {_f(smax)} ? {n}" for smax, n in SMALL_STEPS[:-1]) + f" : {SMALL_STEPS[-1][1]}"
    out.append(f"#if BLUR_CLASS == 0 // '1': single pass, sigma 0.7..1.3 px\n\t#define BLUR_SMALL 1\n"
               f"\tstatic const float2 BLUR_ARM[{len(SMALL_ARM)}] = {{ {arm} }};\n"
               f"\t#define BLUR_ARM_BLOCKS(sigma) ({steps})")
    def arr(nm, t, what):  # the taps as (x, y offset); the weight once if all are equal, else per tap
        ws = {w for _, _, w in t}
        if len(ws) == 1:
            v = [f"float2({_f(x)}, {_f(y)})" for x, y, _ in t]
            head = [f"\t// {what}: {len(t)} bilinear reads at (x, y) offsets, each weighted {_w(ws.pop())}",
                    f"\t#define {nm}_W(i) ({_w(t[0][2])})", f"\tstatic const float2 {nm}[{len(t)}] = {{"]
        else:
            v = [f"float3({_f(x)}, {_f(y)}, {_w(w)})" for x, y, w in t]
            head = [f"\t// {what}: {len(t)} bilinear reads at (x, y) offsets, weight z",
                    f"\t#define {nm}_W(i) {nm}[i].z", f"\tstatic const float3 {nm}[{len(t)}] = {{"]
        return "\n".join(head) + "\n\t\t" + ",\n\t\t".join(", ".join(v[k:k + 4]) for k in range(0, len(v), 4)) + "\n\t};"
    up_name = lambda u: {"p": "Pinwheel", "e": "Binomial"}[u[0]] + u[1:]
    for i, (name, (down, e, ups, upf, lo)) in enumerate(CLASSES.items(), 1):
        C, b, lo, hi, smin, smax, _ = info[name]
        taps = [S.outer(S.down_taps_1d(f, e)) for f in down]
        up = up_taps(upf)
        divs = [math.prod(down[:k + 1]) for k in range(len(down))]
        div = divs[-1]
        upk = "one bilinear read" if upf == "e1" else f"{up_name(upf)}"
        lines = [f"#elif BLUR_CLASS == {i} // '{name}': sigma {smin:.1f}..{smax:.1f} px: downsample x{div}, Gaussian at 1/{div}, "
                 f"upsample {upk}",
                 "\t#define BLUR_SMALL 0",
                 f"\t#define BLUR_STEPS {len(down)}",
                 f"\t#define BLUR_F1 {down[0]}",
                 f"\t#define BLUR_F2 {down[1] if len(down) > 1 else 1}",
                 f"\t#define BLUR_UPSTEPS {len(ups)}",
                 f"\tstatic const float BLUR_C = {_f(C)};  // chain variance (px^2): sigma^2 = C + B * sl^2",
                 f"\tstatic const float BLUR_B = {_f(b)};",
                 f"\tstatic const float BLUR_SL_MIN = {_f(lo)}; // low-res Gaussian sigma range (texels)",
                 f"\tstatic const float BLUR_SL_MAX = {_f(hi)};",
                 "\t// the buffers, named after what they hold"]
        lines += [f"\t#define BLUR_tDown{k + 1} BLUR_Down{d}_Box{f}_Binomial{e}" for k, (d, f) in enumerate(zip(divs, down))]
        lines += [f"\t#define BLUR_tGaussH BLUR_GaussH_Div{div}", f"\t#define BLUR_tGauss BLUR_Gauss_Div{div}"]
        if len(ups) > 1:
            lines.append(f"\t#define BLUR_tUp BLUR_Up{div // ups[0]}_{up_name(upf)}")
        lines += [f"\t#define BLUR_ND1 {len(taps[0])}",
                  arr("BLUR_DOWN1", taps[0], f"x{down[0]} downsample of the screen, kernel box {down[0]} * binomial {e}")]
        if len(down) > 1:
            lines += [f"\t#define BLUR_ND2 {len(taps[1])}",
                      arr("BLUR_DOWN2", taps[1], f"x{down[1]} downsample of the x{down[0]} level, kernel box {down[1]} * binomial {e}")]
        what = ("upsample: one bilinear read" if upf == "e1" else
                f"upsample, pinwheel around the pixel (offsets in low-res texels)" if upf[0] == "p" else
                f"upsample: bilinear then binomial {upf[1:]}")
        lines += [f"\t#define BLUR_NUP {len(up)}", arr("BLUR_UP", up, what)]
        out.append("\n".join(lines))
    out.append("#endif")
    return short_floats("\n".join(out) + "\n")


def render(info: dict, tables: list, default: list, rmax: int, template: str | None = None) -> str:
    return short_floats((template or TEMPLATE).replace("{RMAX}", str(rmax)).replace("{NARM}", str(len(SMALL_ARM))) \
        .replace("{TRUNC}", _f(TRUNC)))


TABLES_HEAD = r"""/*
  TOPT_BlurTables.fxh: the size classes of the topt blur (TOPT_Blur.fx, MovieNight.fx), generated by
  scripts/make_effect.py.

  BLUR_GPU: the table of the GPU's family (PCI vendor / device id ranges), each made with the cost model
  calibrated on that architecture's TexBench report; 0 = unknown GPU (least regret over all of them).
  Define BLUR_GPU to force one. Each table gives the size class for the blur sigma on screen
  (BLUR_SIGMA_SCREEN, px), and the class block below its constants: downsample factors and taps, the
  low-res sigma range and the upsample taps.
*/
"""


# The effect = HEAD + BODY + TAIL. BODY (settings, size classes, the blur passes and BLUR_Resolve) is
# shared with other effects built on the blur (scripts/movienight.py).
HEAD = r"""/*------------------.
| :: TOPT Blur ::   |
'------------------*/
/*
  Fast Gaussian-like blur, generated by the topt texture-sample optimizer.

  One wide downsample pass (x8 then the rest for larger blurs), a Gaussian at
  low resolution whose width is computed at runtime (one 2D pass, or H + V),
  and a smooth "pinwheel" upsample (or one bilinear read, where the low-res
  Gaussian is wide enough) fused into the final pass. Cost is nearly
  independent of the blur size above sigma ~8. Size 1 is a single pass: an
  exact Gaussian pinwheel of 2x2 texel blocks (sigma 0.7..1.3).

  Use it as is, or call BLUR_Resolve(uv) from your own final pass after
  running the BLUR_Down / BLUR_Gauss (H/V) passes.
*/

"""

BODY = r"""#include "ReShade.fxh"

#ifndef BLUR_SIZE
	#define BLUR_SIZE 16 // blur sigma in pixels at 1080p (integer, 1..200; 1 = single pass, 0.7..1.3 with the fine-tune); scales with resolution
#endif
#ifndef BLUR_FORMAT
	#define BLUR_FORMAT RGB10A2 // intermediate format; R11G11B10F keeps HDR (> 1) values
#endif
#ifndef BLUR_LUMA
	#define BLUR_LUMA 0 // 1: blur brightness only (one-channel buffers); the composite keeps the colour detail
#endif
#ifndef BLUR_LUMA_FORMAT
	#define BLUR_LUMA_FORMAT R16F // brightness-only buffers: R16F or R8
#endif
#ifndef BLUR_FROST
	#define BLUR_FROST 0 // 1: scatter the final read inside a disk (frosted glass)
#endif
#ifndef BLUR_FROST_SHARE
	#define BLUR_FROST_SHARE 30 // frosted glass: % the blur is made narrower; the scatter makes up the width
#endif
#ifndef BLUR_DITHER
	#define BLUR_DITHER 1 // dither of the output against banding: 0 off, 1-12 methods (see the help in the UI)
#endif
#ifndef BLUR_DITHER_TEST
	#define BLUR_DITHER_TEST 0 // 1: show a grey gradient (0.25 to 0.75, left to right) over the top quarter of the screen, with the BLUR_DITHER method
#endif
#ifndef BLUR_NOISE
	#ifdef BLUR_FROST_NOISE // the earlier name
		#define BLUR_NOISE BLUR_FROST_NOISE
	#else
		#define BLUR_NOISE 0 // dither / frosted glass noise: 0 blue-noise texture (Textures/topt_bn64_RGBA8.png), 1 IGN
	#endif
#endif
#ifndef BLUR_BLEND
	#define BLUR_BLEND 0 // 1: blend with the screen by the output-merger blend state instead of in the shader
#endif

#define BLUR_STR2(x) #x
#define BLUR_STR(x) BLUR_STR2(x) // a definition's value as text (for the help in the UI)

#ifndef BLUR_NEED_TEX
	#define BLUR_NEED_TEX 0 // an effect built on the blur reads the blue-noise texture itself
#endif
#ifndef BLUR_NEED_NOISE
	#define BLUR_NEED_NOISE BLUR_FROST // the scatter noise (BLUR_Noise2) is used
#endif
#if BLUR_FROST
	#define BLUR_KEEP (100 - BLUR_FROST_SHARE) // % of the blur width the blur passes make
#else
	#define BLUR_KEEP 100
#endif
#define BLUR_SIGMA_SCREEN (BLUR_SIZE * BLUR_KEEP * BUFFER_HEIGHT / 108000)

uniform float BLUR_SizeTune <
	ui_type = "slider"; ui_min = 0.7; ui_max = 1.33;
	ui_label = "Size fine-tune";
	ui_tooltip = "Multiplies the blur size set by BLUR_SIZE.\nThe usable range of each size class is limited; the blur stops growing at its edges.";
> = 1.0;

// Size class: chosen at compile time from the blur size, the resolution and the GPU (BLUR_GPU forces a
// GPU's table), with its constants.
#include "TOPT_BlurTables.fxh"

sampler BLUR_sBackBuffer { Texture = ReShade::BackBufferTex; AddressU = MIRROR; AddressV = MIRROR; };
#ifndef BLUR_SRC_UV
	#define BLUR_SRC_UV(uv) (uv) // where the first downsample reads the screen (an effect can clamp it to a region)
#endif
#ifndef BLUR_LOW_UV
	#define BLUR_LOW_UV(uv, px) (uv) // where the later passes read a low-res level of texel size px (likewise)
#endif

static const float3 BLUR_LUMA_W = float3(0.2126, 0.7152, 0.0722); // Rec. 709 weights on the stored values
#if BLUR_LUMA && !BLUR_SMALL
	#define BLUR_FMT BLUR_LUMA_FORMAT
	#define BLUR_T float
	#define BLUR_CH r
	#define BLUR_TO_LOW(c) dot(c, BLUR_LUMA_W)
	#define BLUR_OUT(c) float4(c, 0.0, 0.0, 1.0)
#else
	#define BLUR_FMT BLUR_FORMAT
	#define BLUR_T float3
	#define BLUR_CH rgb
	#define BLUR_TO_LOW(c) c
	#define BLUR_OUT(c) float4(c, 1.0)
#endif

#if BLUR_SMALL
// Single pass: centre texel + 4-fold pinwheel of 2x2 texel blocks, each block's
// Gaussian weights reproduced exactly by one bilinear fetch.
float3 BLUR_Resolve(float2 uv)
{
	const float sigma = clamp(BLUR_SIZE * BLUR_KEEP * BLUR_SizeTune * BUFFER_HEIGHT / 108000.0, 0.7, 1.3);
	const float k = -0.5 / (sigma * sigma);
	const int n = BLUR_ARM_BLOCKS(sigma); // blocks per arm: the same for every pixel
	float3 c = tex2Dlod(BLUR_sBackBuffer, float4(uv, 0.0, 0.0)).rgb;
	float wsum = 1.0;
	[unroll] for (int i = 0; i < {NARM}; i++)
	{
		[branch] if (i < n)
		{
			const float2 b = BLUR_ARM[i];
			const float4 g = exp(k * float4(b.x, b.x + 1.0, b.y, b.y + 1.0) * float4(b.x, b.x + 1.0, b.y, b.y + 1.0));
			const float2 o = float2(b.x + g.y / (g.x + g.y), b.y + g.w / (g.z + g.w)); // pixels
			const float w = (g.x + g.y) * (g.z + g.w);
			c += w * (tex2Dlod(BLUR_sBackBuffer, float4(uv + o * BUFFER_PIXEL_SIZE, 0.0, 0.0)).rgb
			        + tex2Dlod(BLUR_sBackBuffer, float4(uv + float2(-o.y, o.x) * BUFFER_PIXEL_SIZE, 0.0, 0.0)).rgb
			        + tex2Dlod(BLUR_sBackBuffer, float4(uv - o * BUFFER_PIXEL_SIZE, 0.0, 0.0)).rgb
			        + tex2Dlod(BLUR_sBackBuffer, float4(uv + float2(o.y, -o.x) * BUFFER_PIXEL_SIZE, 0.0, 0.0)).rgb);
			wsum += 4.0 * w;
		}
	}
	return c / wsum;
}
#else
#define BLUR_RMAX {RMAX}   // low-res kernel radius limit (texels)
#define BLUR_NP ((BLUR_RMAX + 1) / 2) // max merged pairs per side

#define BLUR_DIV1 BLUR_F1
#define BLUR_DIV2 (BLUR_F1 * BLUR_F2)

texture BLUR_tDown1 { Width = BUFFER_WIDTH / BLUR_DIV1; Height = BUFFER_HEIGHT / BLUR_DIV1; Format = BLUR_FMT; };
sampler BLUR_sDown1 { Texture = BLUR_tDown1; AddressU = MIRROR; AddressV = MIRROR; };
#if BLUR_STEPS > 1
texture BLUR_tDown2 { Width = BUFFER_WIDTH / BLUR_DIV2; Height = BUFFER_HEIGHT / BLUR_DIV2; Format = BLUR_FMT; };
sampler BLUR_sDown2 { Texture = BLUR_tDown2; AddressU = MIRROR; AddressV = MIRROR; };
	#define BLUR_sLow BLUR_sDown2
	#define BLUR_DIVL BLUR_DIV2
#else
	#define BLUR_sLow BLUR_sDown1
	#define BLUR_DIVL BLUR_DIV1
#endif
#if BLUR_SEP
texture BLUR_tGaussH { Width = BUFFER_WIDTH / BLUR_DIVL; Height = BUFFER_HEIGHT / BLUR_DIVL; Format = BLUR_FMT; };
sampler BLUR_sGaussH { Texture = BLUR_tGaussH; AddressU = MIRROR; AddressV = MIRROR; };
#endif
texture BLUR_tGauss { Width = BUFFER_WIDTH / BLUR_DIVL; Height = BUFFER_HEIGHT / BLUR_DIVL; Format = BLUR_FMT; };
sampler BLUR_sGauss { Texture = BLUR_tGauss; AddressU = MIRROR; AddressV = MIRROR; };
#if BLUR_UPSTEPS > 1 // intermediate x2 upsample to 1/(DIVL/2) resolution
	#define BLUR_DIVU (BLUR_DIVL / 2)
texture BLUR_tUp { Width = BUFFER_WIDTH / BLUR_DIVU; Height = BUFFER_HEIGHT / BLUR_DIVU; Format = BLUR_FMT; };
sampler BLUR_sUp { Texture = BLUR_tUp; AddressU = MIRROR; AddressV = MIRROR; };
	#define BLUR_sFinal BLUR_sUp
	#define BLUR_DIVF BLUR_DIVU
#else
	#define BLUR_sFinal BLUR_sGauss
	#define BLUR_DIVF BLUR_DIVL
#endif

float4 BLUR_Down1PS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	const float2 px = BUFFER_PIXEL_SIZE;
	float3 c = 0.0; // backbuffer colour; converted to brightness once at the end (it is linear)
	[unroll] for (int i = 0; i < BLUR_ND1; i++)
		c += BLUR_DOWN1_W(i) * tex2Dlod(BLUR_sBackBuffer, float4(BLUR_SRC_UV(uv + BLUR_DOWN1[i].xy * px), 0.0, 0.0)).rgb;
	return BLUR_OUT(BLUR_TO_LOW(c));
}

#if BLUR_STEPS > 1
float4 BLUR_Down2PS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	const float2 px = 1.0 / float2(BUFFER_WIDTH / BLUR_DIV1, BUFFER_HEIGHT / BLUR_DIV1);
	BLUR_T c = 0.0;
	[unroll] for (int i = 0; i < BLUR_ND2; i++)
		c += BLUR_DOWN2_W(i) * tex2Dlod(BLUR_sDown1, float4(BLUR_LOW_UV(uv + BLUR_DOWN2[i].xy * px, px), 0.0, 0.0)).BLUR_CH;
	return BLUR_OUT(c);
}
#endif

// Low-res Gaussian: width from the requested blur size, pairs of texels merged
// into one bilinear fetch; one 2D pass (outer product) or H then V passes.
float BLUR_LowSigma()
{
	const float sigma = BLUR_SIZE * BLUR_KEEP * BLUR_SizeTune * BUFFER_HEIGHT / 108000.0;
	return clamp(sqrt(max(sigma * sigma - BLUR_C, 0.0) / BLUR_B), BLUR_SL_MIN, BLUR_SL_MAX);
}

// Pair m >= 1 of the 1D kernel (texels 2m-1 and 2m, the second only if within r)
// as (offset, weight); k = -1 / (2 sl^2).
float2 BLUR_Pair(int m, float k, int r)
{
	const float j = 2 * m - 1;
	const float a = exp(k * j * j);
	const float b = j + 1.0 <= r ? exp(k * (j + 1.0) * (j + 1.0)) : 0.0;
	return float2(j + b / (a + b), a + b);
}

float4 BLUR_GaussPS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	const float2 px = 1.0 / float2(BUFFER_WIDTH / BLUR_DIVL, BUFFER_HEIGHT / BLUR_DIVL);
	const float sl = BLUR_LowSigma();
	const int r = min(BLUR_RMAX, (int)ceil({TRUNC} * sl));
	const int np = (r + 1) / 2; // pairs used; the same for every pixel, so the branches never diverge
	const float k = -0.5 / (sl * sl);

	float2 t[BLUR_NP + 1];
	t[0] = float2(0.0, 1.0);
	float wsum = 1.0;
	[unroll] for (int m = 1; m <= BLUR_NP; m++)
	{
		t[m] = BLUR_Pair(m, k, r);
		wsum += m <= np ? 2.0 * t[m].y : 0.0;
	}

	BLUR_T c = 0.0;
	[unroll] for (int y = -BLUR_NP; y <= BLUR_NP; y++)
	{
		[branch] if (abs(y) <= np)
		{
			const float2 ty = t[abs(y)];
			[unroll] for (int x = -BLUR_NP; x <= BLUR_NP; x++)
			{
				[branch] if (abs(x) <= np)
				{
					const float2 tx = t[abs(x)];
					const float2 o = float2(x < 0 ? -tx.x : tx.x, y < 0 ? -ty.x : ty.x);
					c += tx.y * ty.y * tex2Dlod(BLUR_sLow, float4(BLUR_LOW_UV(uv + o * px, px), 0.0, 0.0)).BLUR_CH;
				}
			}
		}
	}
	return BLUR_OUT(c / (wsum * wsum));
}

#if BLUR_SEP
BLUR_T BLUR_Gauss1D(sampler s, float2 uv, float2 dir)
{
	const float2 d = dir / float2(BUFFER_WIDTH / BLUR_DIVL, BUFFER_HEIGHT / BLUR_DIVL);
	const float sl = BLUR_LowSigma();
	const int r = min(BLUR_RMAX, (int)ceil({TRUNC} * sl));
	const int np = (r + 1) / 2;
	const float k = -0.5 / (sl * sl);

	const float2 px = 1.0 / float2(BUFFER_WIDTH / BLUR_DIVL, BUFFER_HEIGHT / BLUR_DIVL);
	BLUR_T c = tex2Dlod(s, float4(BLUR_LOW_UV(uv, px), 0.0, 0.0)).BLUR_CH;
	float wsum = 1.0;
	[unroll] for (int m = 1; m <= BLUR_NP; m++)
	{
		[branch] if (m <= np)
		{
			const float2 p = BLUR_Pair(m, k, r);
			c += p.y * (tex2Dlod(s, float4(BLUR_LOW_UV(uv + p.x * d, px), 0.0, 0.0)).BLUR_CH
			          + tex2Dlod(s, float4(BLUR_LOW_UV(uv - p.x * d, px), 0.0, 0.0)).BLUR_CH);
			wsum += 2.0 * p.y;
		}
	}
	return c / wsum;
}

float4 BLUR_GaussHPS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	return BLUR_OUT(BLUR_Gauss1D(BLUR_sLow, uv, float2(1.0, 0.0)));
}

float4 BLUR_GaussVPS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	return BLUR_OUT(BLUR_Gauss1D(BLUR_sGaussH, uv, float2(0.0, 1.0)));
}
#endif

#if BLUR_UPSTEPS > 1
float4 BLUR_UpPS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	const float2 px = 1.0 / float2(BUFFER_WIDTH / BLUR_DIVL, BUFFER_HEIGHT / BLUR_DIVL);
	BLUR_T c = 0.0;
	[unroll] for (int i = 0; i < BLUR_NUP; i++)
		c += BLUR_UP_W(i) * tex2Dlod(BLUR_sGauss, float4(BLUR_LOW_UV(uv + BLUR_UP[i].xy * px, px), 0.0, 0.0)).BLUR_CH;
	return BLUR_OUT(c);
}
#endif

// The blurred image at uv (full resolution): smooth upsample of the low-res
// blur. Call this from your own composite pass.
float3 BLUR_Resolve(float2 uv)
{
	const float2 px = 1.0 / float2(BUFFER_WIDTH / BLUR_DIVF, BUFFER_HEIGHT / BLUR_DIVF);
	BLUR_T c = 0.0;
	[unroll] for (int i = 0; i < BLUR_NUP; i++)
		c += BLUR_UP_W(i) * tex2Dlod(BLUR_sFinal, float4(BLUR_LOW_UV(uv + BLUR_UP[i].xy * px, px), 0.0, 0.0)).BLUR_CH;
	return c; // brightness-only: the blurred luma in all three channels
}
#endif // BLUR_SMALL

// Noise for the dither and the frosted glass.
#define BLUR_NEED_BN ((BLUR_DITHER >= 1 && BLUR_DITHER <= 4) || BLUR_DITHER == 10 || (BLUR_NEED_NOISE && BLUR_NOISE == 0) || BLUR_NEED_TEX)
#if BLUR_NEED_BN
texture BLUR_tBN < source = "topt_bn64_RGBA8.png"; > { Width = 64; Height = 64; Format = RGBA8; };
sampler BLUR_sBN { Texture = BLUR_tBN; AddressU = WRAP; AddressV = WRAP; MagFilter = POINT; MinFilter = POINT; MipFilter = POINT; };
// Four independent blue-noise values in (0, 1) (64 x 64 void-and-cluster, one per channel), centred on
// the 256 levels so they are symmetric about 0.5.
float4 BLUR_BN(float2 pos) { return tex2Dlod(BLUR_sBN, float4((floor(pos) + 0.5) / 64.0, 0.0, 0.0)) * (255.0 / 256.0) + 0.5 / 256.0; }
#endif
// Interleaved gradient noise (Jimenez 2014), four decorrelated copies.
float BLUR_IGN(float2 p) { return frac(52.9829189 * frac(dot(p, float2(0.06711056, 0.00583715)))); }
float4 BLUR_IGN4(float2 pos)
{
	const float2 p = floor(pos);
	return float4(BLUR_IGN(p), BLUR_IGN(p + float2(47.0, 17.0)), BLUR_IGN(p + float2(13.0, 61.0)), BLUR_IGN(p + float2(71.0, 29.0)));
}
float2 BLUR_Noise2(float2 pos) // frosted glass
{
#if BLUR_NEED_NOISE && BLUR_NOISE == 0
	return BLUR_BN(pos).rg;
#else
	return BLUR_IGN4(pos).rg;
#endif
}

// Ordered dither: 8 x 8 Bayer threshold in [0, 1) from the pixel position (float-only, works on D3D9).
float BLUR_Bayer2(float2 p) { p = floor(p); return frac(p.x * 0.5 + p.y * p.y * 0.75); }
float BLUR_Bayer8(float2 p) { return BLUR_Bayer2(p * 0.25) * 0.0625 + BLUR_Bayer2(p * 0.5) * 0.25 + BLUR_Bayer2(p) + 0.0078125; }

// Uniform (0, 1) -> triangular in (-1, 1) by the inverse distribution: one value per channel keeps the
// noise's spectrum (blue stays blue).
float3 BLUR_Tri(float3 u)
{
	const float3 v = 2.0 * u - 1.0;
	return sign(v) * (1.0 - sqrt(1.0 - abs(v)));
}

#ifndef BUFFER_COLOR_BIT_DEPTH
	#define BUFFER_COLOR_BIT_DEPTH 8
#endif
// Dither, added before the output is rounded to the screen format (step = one level). Triangular noise
// of +-1 step removes the error's dependence on the signal; independent noise per channel: a one-step
// change of one channel is a third of a step in brightness and hard to see as colour, so the output
// gets ~3 x as many brightness levels.
//   1 blue noise, triangular, per channel (one texture read, remapped)
//   2 blue noise, triangular, per channel (two reads summed)
//   3 blue noise, rectangular (+-0.5 step), per channel
//   4 blue noise, triangular, the same in all channels
//   5 IGN, triangular, per channel (no texture)
//   6 Bayer 8 x 8 ordered, rectangular, per channel (shifted patterns, no texture)
// One value, rectangular, added to G and subtracted from R and B (-,+,-): the brightness steps get as
// small as with three independent channels for the price of one (the colour noise is harder to see):
//   7 plus dither, 5 levels: (x + 2y) mod 5 as a rank-1 lattice, frac(dot(pos, (1/5, 2/5)) + c)
//   8 SweetFX 1 ordered dither (CeeJay.dk 2012): frac(dot(pos, (1/16, 10/36)) + 1/4), 144 levels, (+,-,+)
//   9 IGN (no texture)
//  10 blue noise (one channel of the texture)
//  11 R2 ordered dither: frac(dot(pos, (0.7548777, 0.5698403))), the best of scripts.dither_lattice
//  12 rank-1 lattice of 32 levels, (8 x + 13 y) / 32 (Fibonacci-like), the best lattice there
// t - round(t): an ordered dither's value in (-0.5, 0.5). NVIDIA runs round / frac at a quarter rate
// (half on Turing), so there the add-round is cheaper: adding 1.5 * 2^23 rounds to an integer (|t| <=
// 2^22), precise keeps the compiler from folding it away; frac elsewhere (sopt's OpBench, see
// results/dither_lattice.md). The same values (the lattices never land on a tie).
float BLUR_Centre(float t)
{
#if __VENDOR__ == 0x10DE
	precise float r = (t + 12582912.0) - 12582912.0;
	return t - r;
#else
	return frac(t + 0.5) - 0.5;
#endif
}

float3 BLUR_DitherBy(float3 c, float2 pos, int method)
{
	pos += float2(32.0, 17.0); // away from the frosted-glass noise
	float3 d = 0.0;
#if BLUR_NEED_BN
	if (method == 1) d = BLUR_Tri(BLUR_BN(pos).rgb);
	if (method == 2) d = BLUR_BN(pos).rgb + BLUR_BN(pos + float2(11.0, 45.0)).rgb - 1.0;
	if (method == 3) d = BLUR_BN(pos).rgb - 0.5;
	if (method == 4) d = BLUR_Tri(BLUR_BN(pos).rrr);
#endif
	if (method == 5) d = BLUR_Tri(BLUR_IGN4(pos).rgb);
	if (method == 6) d = float3(BLUR_Bayer8(pos), BLUR_Bayer8(pos + float2(3.0, 5.0)), BLUR_Bayer8(pos + float2(6.0, 2.0))) - 0.5;
	const float2 pc = pos; // pixel centres: SV_Position plus whole offsets (no floor needed)
	if (method == 7) d = float3(-1.0, 1.0, -1.0) * (frac(dot(pc, float2(0.2, 0.4)) + 0.8) - 0.5); // levels (k + 0.5) / 5 - 0.5
	if (method == 8) d = float3(1.0, -1.0, 1.0) * (0.5 - frac(dot(pc, float2(1.0 / 16.0, 10.0 / 36.0)) + 0.25));
	if (method == 9) d = float3(-1.0, 1.0, -1.0) * (BLUR_IGN(floor(pos)) - 0.5);
	if (method == 11) d = float3(-1.0, 1.0, -1.0) * BLUR_Centre(dot(pc, float2(0.7548776662, 0.5698402910)));
	if (method == 12) d = float3(-1.0, 1.0, -1.0) * BLUR_Centre(dot(pc, float2(0.25, 0.40625)) + 0.1875); // levels (k + 0.5) / 32 - 0.5, exact
#if BLUR_NEED_BN
	if (method == 10) d = float3(-1.0, 1.0, -1.0) * (BLUR_BN(pos).r - 0.5);
#endif
	return c + d / (exp2(BUFFER_COLOR_BIT_DEPTH) - 1.0);
}
float3 BLUR_Dither(float3 c, float2 pos)
{
#if BLUR_DITHER
	return BLUR_DitherBy(c, pos, BLUR_DITHER);
#else
	return c;
#endif
}

// Dither test: over the top quarter of the screen, a grey gradient from 0.25 at the left to 0.75 at the
// right (bands of 15 px at 1080p on 8-bit screens) with the BLUR_DITHER method; returns from the pixel shader.
#if BLUR_DITHER_TEST
	#define BLUR_DITHER_TEST_AT(uv, pos) if (uv.y < 0.25) return float4(BLUR_Dither((uv.x * 0.5 + 0.25).xxx, pos), 1.0);
#else
	#define BLUR_DITHER_TEST_AT(uv, pos)
#endif
"""

TAIL = r"""
uniform int BLUR_Help <
	ui_type = "radio"; ui_label = " ";
	ui_category = "Help: preprocessor definitions"; ui_category_closed = true;
	ui_text =
		"Detected GPU architecture: " BLUR_GPU_NAME "\n\n"
		"Set with the preprocessor definitions below the effect's settings (current value after =).\n\n"
		"BLUR_SIZE = " BLUR_STR(BLUR_SIZE) "\n"
		"  Blur sigma in pixels at 1080p (1-200; scales with the resolution).\n"
		"BLUR_LUMA = " BLUR_STR(BLUR_LUMA) "\n"
		"  1: blur the brightness only (one-channel buffers, cheaper); the colour detail stays.\n"
		"BLUR_BLEND = " BLUR_STR(BLUR_BLEND) "\n"
		"  1: blend with the screen by the blend state instead of in the shader.\n"
		"BLUR_FROST = " BLUR_STR(BLUR_FROST) ", BLUR_FROST_SHARE = " BLUR_STR(BLUR_FROST_SHARE) "\n"
		"  Frosted glass: the blur is made SHARE % narrower and a random scatter of the\n"
		"  final read makes up the width.\n"
		"BLUR_DITHER = " BLUR_STR(BLUR_DITHER) "\n"
		"  Dither against banding: 0 off, 1 blue noise triangular per channel (one read),\n"
		"  2 blue noise triangular per channel (two reads), 3 blue noise rectangular per channel,\n"
		"  4 blue noise triangular same in all channels, 5 IGN triangular per channel (no texture),\n"
		"  6 Bayer 8x8 ordered per channel (no texture),\n"
		"  one value as (-,+,-) on R, G, B (no texture unless 10): 7 plus dither (5 levels),\n"
		"  8 SweetFX 1 ordered (+,-,+), 9 IGN rectangular, 10 blue noise rectangular,\n"
		"  11 R2 ordered (no texture), 12 lattice of 32 levels (8, 13) / 32 (no texture).\n"
		"BLUR_DITHER_TEST = " BLUR_STR(BLUR_DITHER_TEST) "\n"
		"  1: show a grey gradient (0.25 to 0.75, left to right) over the top quarter of the screen,\n"
		"  dithered with the BLUR_DITHER method.\n"
		"BLUR_NOISE = " BLUR_STR(BLUR_NOISE) "\n"
		"  Frosted-glass noise: 0 blue-noise texture, 1 IGN.\n"
		"BLUR_FORMAT = " BLUR_STR(BLUR_FORMAT) "\n"
		"  Format of the blur buffers; R11G11B10F keeps HDR (> 1) values.\n"
		"BLUR_GPU = " BLUR_STR(BLUR_GPU) "\n"
		"  The size-class table, picked from your GPU (0 = unknown GPU). Set it to force one.";
>;

uniform float BLUR_Strength <
	ui_type = "slider"; ui_min = 0.0; ui_max = 1.0;
	ui_label = "Strength";
> = 1.0;

#if BLUR_FROST
uniform float BLUR_FrostRadius <
	ui_type = "slider"; ui_min = 0.0; ui_max = 32.0;
	ui_label = "Extra frosted glass radius (px)";
	ui_tooltip = "Added to the radius that makes up the blur width BLUR_FROST_SHARE takes from the blur.";
> = 0.0;
#endif

uniform bool BLUR_ShowBlur <
	ui_label = "Show blur only";
> = false;


#if BLUR_FROST
// Frosted glass: move the final read to a random point in a disk. The blur passes make the blur
// BLUR_FROST_SHARE % narrower; a disk of radius R adds (R / 2)^2 to the variance on each axis, so
// R = 2 sqrt(sigma^2 - sigma_blur^2) gives the full width back (plus BLUR_FrostRadius).
float2 BLUR_Frost(float2 pos, float2 uv)
{
	const float sigma = BLUR_SIZE * BLUR_SizeTune * BUFFER_HEIGHT / 1080.0;
	const float keep = BLUR_KEEP / 100.0;
	const float radius = 2.0 * sigma * sqrt(1.0 - keep * keep) + BLUR_FrostRadius;
	const float2 u = BLUR_Noise2(pos);
	float2 cs; sincos(6.2831853 * u.x, cs.y, cs.x);
	return uv + cs * (sqrt(u.y) * radius) * BUFFER_PIXEL_SIZE;
}
#else
	#define BLUR_Frost(pos, uv) (uv)
#endif

#if BLUR_LUMA
// Brightness only: replace the pixel's luma with the blurred luma, keep its colour detail.
float4 BLUR_CompositePS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	BLUR_DITHER_TEST_AT(uv, pos.xy)
	const float yb = dot(BLUR_Resolve(BLUR_Frost(pos.xy, uv)), BLUR_LUMA_W);
	if (BLUR_ShowBlur)
		return float4(BLUR_Dither(yb.xxx, pos.xy), 1.0);
	const float3 o = tex2D(ReShade::BackBuffer, uv).rgb;
	return float4(BLUR_Dither(o + BLUR_Strength * (yb - dot(o, BLUR_LUMA_W)), pos.xy), 1.0);
}
#elif BLUR_BLEND
// The pass blends: screen = blur * a + screen * (1 - a). The shader neither reads
// the screen nor lerps. Blending uses the stored (non-sRGB) values, as the
// shader lerp below does, so the result is the same.
float4 BLUR_CompositePS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	BLUR_DITHER_TEST_AT(uv, pos.xy)
	return float4(BLUR_Dither(BLUR_Resolve(BLUR_Frost(pos.xy, uv)), pos.xy), BLUR_ShowBlur ? 1.0 : BLUR_Strength);
}
#else
float4 BLUR_CompositePS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	BLUR_DITHER_TEST_AT(uv, pos.xy)
	const float3 blur = BLUR_Resolve(BLUR_Frost(pos.xy, uv));
	if (BLUR_ShowBlur)
		return float4(BLUR_Dither(blur, pos.xy), 1.0);
	const float3 o = tex2D(ReShade::BackBuffer, uv).rgb;
	return float4(BLUR_Dither(lerp(o, blur, BLUR_Strength), pos.xy), 1.0);
}
#endif

technique TOPT_Blur < ui_tooltip = "Fast Gaussian-like blur (topt).\nSet the size with the BLUR_SIZE preprocessor definition (sigma in pixels at 1080p)."; >
{
#if !BLUR_SMALL
	pass Down1 { VertexShader = PostProcessVS; PixelShader = BLUR_Down1PS; RenderTarget = BLUR_tDown1; }
#if BLUR_STEPS > 1
	pass Down2 { VertexShader = PostProcessVS; PixelShader = BLUR_Down2PS; RenderTarget = BLUR_tDown2; }
#endif
#if BLUR_SEP
	pass GaussH { VertexShader = PostProcessVS; PixelShader = BLUR_GaussHPS; RenderTarget = BLUR_tGaussH; }
	pass GaussV { VertexShader = PostProcessVS; PixelShader = BLUR_GaussVPS; RenderTarget = BLUR_tGauss; }
#else
	pass Gauss { VertexShader = PostProcessVS; PixelShader = BLUR_GaussPS; RenderTarget = BLUR_tGauss; }
#endif
#if BLUR_UPSTEPS > 1
	pass Up { VertexShader = PostProcessVS; PixelShader = BLUR_UpPS; RenderTarget = BLUR_tUp; }
#endif
#endif
	pass Composite
	{
		VertexShader = PostProcessVS; PixelShader = BLUR_CompositePS;
#if BLUR_BLEND && !BLUR_LUMA
		BlendEnable = true; BlendOp = ADD; SrcBlend = SRCALPHA; DestBlend = INVSRCALPHA;
		RenderTargetWriteMask = 7; // keep the screen's alpha
#endif
	}
}
"""

TEMPLATE = HEAD + BODY + TAIL



if __name__ == "__main__":
    import sys
    if "--render" in sys.argv:  # templates changed only: the class checks and tables from the last full run
        c = json.loads((ROOT / "results" / "topt_blur_tables.json").read_text())
        tabs = [(gs, [(a, b, tuple(k)) for a, b, k in iv]) for gs, iv in c["tables"]]
        write(c["info"], tabs, [(a, b, tuple(k)) for a, b, k in c["default"]], math.ceil(TRUNC * SL_MAX))
    else:
        main()
