"""GPU profiles for the cost model from TexBench reports (CeeJayDK/sopt, docs/texbench).

    python -m scripts.gpu_profiles <sopt>/docs/texbench

For each card in CARDS, the newest report gives (all full-screen passes at 3840 x 2160):
  tex_rate      the report's texture rate (bilinear RGBA8)
  bandwidth     combined read + write traffic of the RGBA8 copy / half-size downsample (the larger)
  rop_rate      the report's pixel fill rate (formats without a write test)
  write_rate    per format, from the incompressible ("noise") write passes
  wide_filter   RGBA16F bilinear / RGBA8 bilinear (throughput test)
  pass_overhead from the dependent pass chains (TexBench 0.7.27+): time per extra pass (2 to 32) at 1/64 and
                1/256 of the screen, fitted as overhead + pixels * cost; cards without the chains get
                the median of the others
Writes topt/gpu_profiles.json (read by topt.cost.PROFILES).
"""
from __future__ import annotations

import csv
import json
import re
import statistics
import sys
from pathlib import Path

from topt.cost import FORMAT_BYTES

OUT = Path(__file__).resolve().parent.parent / "topt" / "gpu_profiles.json"
N = 3840 * 2160

# label: (architecture, report GPU name). One card per architecture, desktop where there is one.
CARDS = {
    "GTX 860M": ("NVIDIA Maxwell", "NVIDIA GeForce GTX 860M"),
    "GTX 1080": ("NVIDIA Pascal", "NVIDIA GeForce GTX 1080"),
    "GTX 1660": ("NVIDIA Turing", "NVIDIA GeForce GTX 1660"),
    "RTX 2070": ("NVIDIA Turing RTX", "NVIDIA GeForce RTX 2070"),
    "RTX 3060": ("NVIDIA Ampere", "NVIDIA GeForce RTX 3060"),
    "RTX 4070": ("NVIDIA Ada", "NVIDIA GeForce RTX 4070"),
    "RTX 5070": ("NVIDIA Blackwell", "NVIDIA GeForce RTX 5070"),
    "RX 590": ("AMD GCN 4", "Radeon RX 590 Series"),
    "RX 5500 XT": ("AMD RDNA 1", "Radeon RX 5500 XT"),
    "RX 6600": ("AMD RDNA 2", "AMD Radeon RX 6600"),
    "RX 7900 XTX": ("AMD RDNA 3", "AMD Radeon RX 7900 XTX"),
    "RX 9070 XT": ("AMD RDNA 4", "AMD Radeon RX 9070 XT"),
    "Radeon 610M": ("AMD RDNA 2 iGPU", "AMD Radeon(TM) Graphics"),
    "UHD 630": ("Intel Gen9.5", "Intel(R) UHD Graphics 630"),
    "Iris Xe": ("Intel Gen12", "Intel(R) Iris(R) Xe Graphics"),
    "Arc B580": ("Intel Xe2", "Intel(R) Arc(TM) B580 Graphics"),
}


def newest(folder: Path) -> dict:
    """GPU name -> (version, path) of its newest report."""
    out = {}
    for f in folder.glob("*.csv"):
        head = f.read_text(encoding="utf-8", errors="ignore").splitlines()[:2]
        if len(head) < 2 or not head[0].startswith("# TexBench"):
            continue
        v = tuple(int(x) for x in re.findall(r"\d+", head[0])[:3])
        g = head[1].split(":", 1)[1].strip()
        if g not in out or v > out[g][0]:
            out[g] = (v, f)
    return out


def read(path: Path) -> tuple:
    hdr, rows = {}, {}
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    for line in lines:
        if line.startswith("#") and ":" in line:
            k, v = line[1:].split(":", 1)
            hdr[k.strip()] = v.strip()
    for r in csv.reader(x for x in lines if not x.startswith("#")):
        if len(r) > 8 and r[0] != "config":
            rows[(r[0], r[1])] = r
    return hdr, rows


def ms(rows: dict, cfg: str, name: str) -> float | None:
    r = rows.get((cfg, name))
    return float(r[5]) * 1e-3 if r else None


def profile(path: Path) -> dict:
    hdr, rows = read(path)
    rate = lambda key: float(hdr[key].split()[0]) * 1e9
    p = {"tex_rate": rate("texture rate"), "rop_rate": rate("pixel fill rate")}
    bw = []
    if (t := ms(rows, "pass", "copy Sample RGBA8")):
        bw.append(8 * N / t)
    if (t := ms(rows, "pass", "half bilinear RGBA8")):
        bw.append(5 * N / t)
    p["bandwidth"] = max(bw)
    p["write_rate"] = {f: N / t for f in FORMAT_BYTES if (t := ms(rows, "write", f"{f} write noise"))}
    a, b = (rows.get(("tput", f"{f} bilinear")) for f in ("RGBA8", "RGBA16F"))
    p["wide_filter"] = round(max(1.0, float(b[7]) / float(a[7])), 2) if a and b else 2.0
    slopes = []
    for frac, px in (("1/64", 480 * 270), ("1/256", 240 * 135)):
        # from 2 passes on (a single pass times shorter than a pass inside a chain)
        t2, t32 = ms(rows, "pass", f"{frac}, 2 passes"), ms(rows, "pass", f"{frac}, 32 passes")
        if t2 is not None and t32 is not None:
            slopes.append((px, (t32 - t2) / 30))
    if len(slopes) == 2:
        (p1, s1), (p2, s2) = slopes
        c = (s1 - s2) / (p1 - p2)
        p["pass_overhead"] = max(0.2e-6, s2 - c * p2)
    p["report"] = f"{path.name} ({path.read_text(encoding='utf-8', errors='ignore').splitlines()[0][2:]})"
    return p


def main():
    reports = newest(Path(sys.argv[1]))
    profiles = {}
    for label, (arch, gpu) in CARDS.items():
        if gpu not in reports:
            print("no report:", gpu)
            continue
        profiles[label] = {"arch": arch, **profile(reports[gpu][1])}
    measured = [p["pass_overhead"] for p in profiles.values() if "pass_overhead" in p]
    med = statistics.median(measured)
    for p in profiles.values():
        p["overhead_measured"] = "pass_overhead" in p
        p.setdefault("pass_overhead", med)
    OUT.write_text(json.dumps(profiles, indent=1) + "\n")
    for k, p in profiles.items():
        w = p["write_rate"]
        print(f"{k:12s} {p['arch']:18s} tex {p['tex_rate'] / 1e9:6.0f} bw {p['bandwidth'] / 1e9:5.0f} "
              f"RGBA8 {w.get('RGBA8', 0) / 1e9:5.1f} R8 {w.get('R8', 0) / 1e9:5.1f} wide {p['wide_filter']:.2f} "
              f"overhead {p['pass_overhead'] * 1e6:5.2f} us{'' if p['overhead_measured'] else ' (median)'}  {p['report']}")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
