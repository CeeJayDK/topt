"""Check the cost model against TexBench full-screen pass timings, for every GPU profile.

    python -m scripts.texbench_check <sopt>/docs/texbench

TexBench (CeeJayDK/sopt, tools/windows/texbench) times whole passes at 3840 x 2160: render-target
writes per format, copies, half-size downsamples, N bilinear reads per pixel, strided downsamples
into smaller targets, dependent pass chains and the quad-exchange test. For each profile in
topt/gpu_profiles.json, measured vs model (ms), from the report the profile was made from.
Writes results/calibration.md.
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

from scripts.gpu_profiles import ms, read
from topt.cost import FORMAT_BYTES, PROFILES, _pass_time

ROOT = Path(__file__).resolve().parent.parent
W, H = 3840, 2160
N = W * H


def tests(gpu) -> list:
    """(section, TexBench test, row config, model ms)."""
    out = []
    for f, b in FORMAT_BYTES.items():
        out.append(("write", f"{f} write noise", "write", _pass_time(N, 0, 0, gpu, b, 0, f)[0]))
    for f in ("RGBA8", "RGB10A2", "RGBA16F", "RGBA32F"):
        b, wide = FORMAT_BYTES[f], gpu.wide_filter if FORMAT_BYTES[f] >= 8 else 1.0
        out.append(("copy", f"copy Sample {f}", "pass", _pass_time(N, N, 1, gpu, b, N * b, f)[0]))
        out.append(("half", f"half bilinear {f}", "pass", _pass_time(N // 4, N, wide, gpu, b, N * b, f)[0]))
    for n in (1, 2, 3, 4, 6, 8, 10, 12, 16, 24):
        out.append(("reads", f"{n} read{'s' if n > 1 else ''}", "pass", _pass_time(N, N, n, gpu, 4, 4 * N, "RGBA8")[0]))
    for name, dw, dh in (("1/4 (1920 x 1080)", 1920, 1080), ("1/16 (960 x 540)", 960, 540),
                         ("1/64 (480 x 270)", 480, 270), ("1/256 (240 x 135)", 240, 135),
                         ("1/1024 (120 x 67)", 120, 67)):
        nd = dw * dh
        ns = min(N, nd * 16)
        ns = min(N, ns * gpu.sparse_waste) if ns < N else ns
        out.append(("size", name, "pass", _pass_time(nd, ns, 4, gpu, 4, 4 * ns, "RGBA8", src_bytes=4 * N)[0]))
    for frac, dw, dh in (("1/64", 480, 270), ("1/256", 240, 135)):
        for k in (2, 8, 32):
            t = k * _pass_time(dw * dh, dw * dh, 1, gpu, 4, 4 * dw * dh, "RGBA8")[0]
            out.append(("chain", f"{frac}, {k} passes", "pass", t))
    out.append(("quad", "4 reads + 12 exchanges", "pass", _pass_time(N, N, 4, gpu, 4, 4 * N, "RGBA8", 12)[0]))
    out.append(("quad", "16 reads", "pass", _pass_time(N, N, 16, gpu, 4, 4 * N, "RGBA8")[0]))
    for name, dw, dh in (("120 x 67", 120, 67), ("240 x 135", 240, 135), ("480 x 270", 480, 270)):
        ns = 1920 * 1080  # 64 bilinear reads (a 16 x 16 block) per pixel of a 1920 x 1080 area
        out.append(("underfill", f"64 reads into {name}", "pass", _pass_time(dw * dh, ns, 64, gpu, 4, 4 * ns, "RGBA8")[0]))
    for f in ("RGBA8", "RGB10A2", "RG11B10F", "RGBA16F", "RGBA32F", "R8", "R16F", "R32F", "RG16F", "RG32F"):
        if f in FORMAT_BYTES:
            b = FORMAT_BYTES[f]
            out.append(("blend", f"{f} add blend", "blend", _pass_time(N, 0, 0, gpu, b, 0, f, blend=True)[0]))
    return out


def main():
    folder = Path(sys.argv[1])
    meta = json.loads((ROOT / "topt" / "gpu_profiles.json").read_text())
    lines = ["# Cost model vs TexBench", "",
             "Model (topt/cost.py, profile from topt/gpu_profiles.json) against the TexBench report the profile",
             "was made from, 3840 x 2160, ms. err = model / measured - 1.", ""]
    summary = ["| GPU | core | report | tests | median abs err | worst |", "|---|---|---|---|---|---|"]
    for name, gpu in PROFILES.items():
        report = meta[name]["report"].split()[0]
        _, rows = read(folder / report)
        got = []
        for sec, test, cfg, model in tests(gpu):
            m = ms(rows, cfg, test)
            if m:
                got.append((sec, test, m * 1e3, model * 1e3))
        if not got:
            continue
        errs = [(mod / mea - 1, t) for _, t, mea, mod in got]
        worst = max(errs, key=lambda e: abs(e[0]))
        summary.append(f"| {name} | {'yes' if meta[name].get('core') else ''} | {report} | {len(got)} | {100 * statistics.median(abs(e) for e, _ in errs):.0f} % "
                       f"| {100 * worst[0]:+.0f} % ({worst[1]}) |")
        lines += [f"## {name} ({meta[name]['arch']})", "", "| section | test | measured | model | err |",
                  "|---|---|---:|---:|---:|"]
        lines += [f"| {s} | {t} | {a:.4f} | {b:.4f} | {100 * (b / a - 1):+.0f} % |" for s, t, a, b in got]
        lines.append("")
    text = "\n".join(lines[:5] + summary + [""] + lines[5:]) + "\n"
    (ROOT / "results" / "calibration.md").write_text(text)
    print("\n".join(summary))


if __name__ == "__main__":
    main()
