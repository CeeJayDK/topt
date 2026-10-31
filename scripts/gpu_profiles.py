"""GPU profiles for the cost model from TexBench reports (CeeJayDK/sopt, docs/texbench).

    python -m scripts.gpu_profiles <sopt>/docs/texbench

Every GPU (PCI vendor / device id) with a report gets a profile from its newest report; the cards in
CARDS are the core set (one per architecture) the searches and TOPT_Blur's tables are made for.
Each profile (all full-screen passes at 3840 x 2160):
  tex_rate      the report's texture rate (bilinear RGBA8)
  bandwidth     combined read + write traffic of the RGBA8 copy
  rop_rate      the report's pixel fill rate (formats without a write test)
  write_rate    per format, from the incompressible ("noise") write passes
  wide_filter   RGBA16F bilinear / RGBA8 bilinear (throughput test)
  px_rate       pixels / s of work every pass pays besides its reads, and tex_rate refitted, from the
                N-reads passes: time = N / px_rate + reads / tex_rate past the knee (TexBench 0.8+)
  exchange_rate ddx_fine / ddy_fine exchanges of a float3 per second (quad-sharing test)
  sparse_waste  bytes moved / bytes used by strided x8 / x16 downsample reads
  cache_bandwidth  traffic / s of passes whose reads and writes fit in the last-level cache
                (cache_bytes, spec sheets), from the pass chains below
  fill_px       a pass with fewer pixels leaves the GPU part idle: its work takes fill_px / pixels
                longer (from the under-filled passes, 64 reads into 120 x 67, TexBench 0.9.2+; else
                the 1/1024 strided downsample)
  blend_rate    per format, pixels / s of additive blending (TexBench 0.9.2+)
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

import numpy as np

from topt.cost import FORMAT_BYTES

OUT = Path(__file__).resolve().parent.parent / "topt" / "gpu_profiles.json"
N = 3840 * 2160

# The core set, label: (architecture, report GPU name[, PCI device id], last-level GPU cache in MB from
# the spec sheets: L2, or AMD's Infinity Cache, or Intel's L3 / LLC share). One card per architecture,
# desktop where there is one. Other GPUs: label from the report's name, architecture from
# make_effect.FAMILIES, 2 MB cache (the cache rule is capped at 2 MB anyway).
CARDS = {
    "GTX 860M": ("NVIDIA Maxwell", "NVIDIA GeForce GTX 860M", 2),
    "GTX 1080": ("NVIDIA Pascal", "NVIDIA GeForce GTX 1080", 2),
    "GTX 1660": ("NVIDIA Turing", "NVIDIA GeForce GTX 1660", 1.5),
    "RTX 2070": ("NVIDIA Turing RTX", "NVIDIA GeForce RTX 2070", 4),
    "RTX 3060": ("NVIDIA Ampere", "NVIDIA GeForce RTX 3060", 3),
    "RTX 4070": ("NVIDIA Ada", "NVIDIA GeForce RTX 4070", 36),
    "RTX 5070": ("NVIDIA Blackwell", "NVIDIA GeForce RTX 5070", 48),
    "RX 590": ("AMD GCN 4", "Radeon RX 590 Series", 2),
    "RX 5500 XT": ("AMD RDNA 1", "Radeon RX 5500 XT", 2),
    "RX 6600": ("AMD RDNA 2", "AMD Radeon RX 6600", 32),
    "RX 7900 XTX": ("AMD RDNA 3", "AMD Radeon RX 7900 XTX", 96),
    "RX 9070 XT": ("AMD RDNA 4", "AMD Radeon RX 9070 XT", 64),
    "Radeon 680M": ("AMD RDNA 2 iGPU", "AMD Radeon(TM) Graphics", "0x1681", 2),
    "UHD 630": ("Intel Gen9.5", "Intel(R) UHD Graphics 630", 4),
    "Iris Xe": ("Intel Gen12", "Intel(R) Iris(R) Xe Graphics", 4),
    "Arc B580": ("Intel Xe2", "Intel(R) Arc(TM) B580 Graphics", 18),
}


def newest(folder: Path) -> dict:
    """(GPU name, device id) -> (version, path) of its newest report."""
    out = {}
    for f in folder.glob("*.csv"):
        head = f.read_text(encoding="utf-8", errors="ignore").splitlines()[:8]
        if len(head) < 2 or not head[0].startswith("# TexBench"):
            continue
        v = tuple(int(x) for x in re.findall(r"\d+", head[0])[:3])
        g = head[1].split(":", 1)[1].strip()
        dev = next((h.split(":", 1)[1].strip().upper().replace("0X", "0x") for h in head if h.startswith("# device:")), "")
        if (g, dev) not in out or v > out[(g, dev)][0]:
            out[(g, dev)] = (v, f)
    return out


VENDORS = {"0x10DE": "NVIDIA", "0x1002": "AMD", "0x8086": "Intel"}


def auto_label(gpu: str, vendor: str, dev: str) -> str:
    s = re.sub(r"\((R|TM)\)", "", gpu)
    for pre in ("NVIDIA GeForce ", "NVIDIA ", "AMD Radeon ", "AMD ", "Intel ", "Radeon "):
        if s.startswith(pre):
            s = s[len(pre):]
            break
    s = " ".join(s.replace("Graphics", "").split())
    if s in ("", "Radeon"):
        return f"{VENDORS.get(vendor, vendor)} {dev}"
    if vendor == "0x1002" and not s.startswith(("RX", "HD", "R")):
        s = "Radeon " + s
    return s


def family(vendor: str, dev: str) -> str:
    from scripts.make_effect import FAMILIES
    try:
        d = int(dev, 16)
    except ValueError:
        return VENDORS.get(vendor, "unknown")
    return next((name for v, lo, hi, _, name in FAMILIES if f"0x{v:04X}" == vendor and lo <= d <= hi),
                VENDORS.get(vendor, "unknown"))


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
    # DRAM traffic from the copy (the half-size downsample reads a 33 MB source that stays in a big L2 /
    # Infinity Cache between runs, so it overstates DRAM on those cards)
    t = ms(rows, "pass", "copy Sample RGBA8")
    p["bandwidth"] = 8 * N / t if t else 5 * N / ms(rows, "pass", "half bilinear RGBA8")
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
        if c > 0:  # the chain passes (4 B read + 4 B written per pixel) stay in the cache
            p["cache_bandwidth"] = 8 / c
    over = p.get("pass_overhead", 1e-6)
    # Pixel floor and texture rate from N bilinear reads per pixel (TexBench 0.8+): past the knee a pass
    # takes a + N * b, a = per-pixel work every pass pays besides its reads (the knee of the "free"
    # fetches: memory time = a + knee * b).
    pts = [(n, t) for n in (8, 10, 12, 16, 24) if (t := ms(rows, "pass", f"{n} reads"))]
    if len(pts) >= 3:
        b, a = np.polyfit(*zip(*pts), 1)
        p["tex_rate"] = N / b
        if a > 0:
            p["px_rate"] = N / a
        # quad sharing: 4 reads + 12 ddx_fine / ddy_fine exchanges of a float3
        if (t := ms(rows, "pass", "4 reads + 12 exchanges")):
            p["exchange_rate"] = N / max((t - max(a, 0.0) - 4 * b) / 12, 0.02 * b)
    # Sparse reads: x8 / x16 strided 4-tap downsamples (1/64, 1/256 of the screen) move this many times
    # the bytes of the texels they use (cache-line granularity).
    waste = [((t - over) * p["bandwidth"] - dw * dh * 4) / (dw * dh * 16 * 4)
             for name, dw, dh in (("1/64 (480 x 270)", 480, 270), ("1/256 (240 x 135)", 240, 135))
             if (t := ms(rows, "pass", name))]
    if waste:
        p["sparse_waste"] = round(min(4.0, max(1.0, statistics.median(waste))), 2)
    p["blend_rate"] = {f: N / t for f in FORMAT_BYTES if (t := ms(rows, "blend", f"{f} add blend"))}
    p["vendor"], p["device"] = hdr.get("vendor"), hdr.get("device")
    p["report"] = f"{path.name} ({path.read_text(encoding='utf-8', errors='ignore').splitlines()[0][2:]})"
    return p


def fit_fill(p: dict, path: Path):
    """Too few pixels to fill the GPU: the under-filled pass (64 bilinear reads, a 16 x 16 block, per
    pixel of 120 x 67 covering a 1920 x 1080 area), or else the 1/1024 strided downsample (120 x 67),
    against the model."""
    from topt.cost import GPU, _pass_time
    _, rows = read(path)
    over = p.get("pass_overhead", 1e-6)
    g = GPU("fit", p["tex_rate"], p["bandwidth"], p["rop_rate"], over, write_rate=tuple(p["write_rate"].items()),
            px_rate=p.get("px_rate", 0.0), sparse_waste=p.get("sparse_waste", 1.0),
            cache_bytes=p["cache_bytes"], cache_bandwidth=p.get("cache_bandwidth", 0.0))
    nd = 120 * 67
    if (t := ms(rows, "pass", "64 reads into 120 x 67")):
        ns = 1920 * 1080
        work = _pass_time(nd, ns, 64, g, 4, 4 * ns, "RGBA8")[0] - over
    elif (t := ms(rows, "pass", "1/1024 (120 x 67)")):
        ns = min(N, nd * 16 * g.sparse_waste)
        work = _pass_time(nd, ns, 4, g, 4, 4 * ns, "RGBA8", src_bytes=4 * N)[0] - over
    else:
        return
    if t - over > work > 0:
        p["fill_px"] = round(nd * (t - over) / work)


def main():
    reports = newest(Path(sys.argv[1]))
    core = {}
    for label, (arch, gpu, *dev, cache) in CARDS.items():
        keys = [k for k in reports if k[0] == gpu and (not dev or k[1] == dev[0])]
        if not keys:
            print("no report:", label, gpu)
        else:
            core[max(keys, key=lambda k: reports[k][0])] = (label, arch, cache)
    profiles = {}
    for key in [k for k in reports if not ms(read(reports[k][1])[1], "pass", "copy Sample RGBA8")]:
        print("no pass tests (TexBench too old):", key[0], reports.pop(key)[1].name)
    for key in sorted(reports, key=lambda k: (k not in core, VENDORS.get(read(reports[k][1])[0].get("vendor"), "~"), k[0], k[1])):
        hdr = read(reports[key][1])[0]
        label, arch, cache = core.get(key) or (auto_label(key[0], hdr.get("vendor", ""), key[1]),
                                               family(hdr.get("vendor", ""), key[1]), 2)
        while label in profiles:
            label += f" {key[1]}"
        # cache rule only as far as measured: the chains move 1 MB per pass; whole-screen writes into
        # a big L2 / Infinity Cache still run at DRAM rate
        profiles[label] = {"arch": arch, "core": key in core, "cache_bytes": min(cache, 2) * 2 ** 20,
                           **profile(reports[key][1])}
        fit_fill(profiles[label], reports[key][1])
    measured = [p["pass_overhead"] for p in profiles.values() if "pass_overhead" in p]
    med = statistics.median(measured)
    for p in profiles.values():
        p["overhead_measured"] = "pass_overhead" in p
        p.setdefault("pass_overhead", med)
    OUT.write_text(json.dumps(profiles, indent=1) + "\n")
    for k, p in profiles.items():
        w = p["write_rate"]
        print(f"{k:22s} {p['arch'][:18]:18s} tex {p['tex_rate'] / 1e9:6.0f} bw {p['bandwidth'] / 1e9:5.0f} "
              f"RGBA8 {w.get('RGBA8', 0) / 1e9:5.1f} R8 {w.get('R8', 0) / 1e9:5.1f} wide {p['wide_filter']:.2f} "
              f"overhead {p['pass_overhead'] * 1e6:5.2f} us{'' if p['overhead_measured'] else ' (median)'} "
              f"px {p.get('px_rate', 0) / 1e9:5.1f} xch {p.get('exchange_rate', 0) / 1e9:6.0f} "
              f"waste {p.get('sparse_waste', 1):.2f} fill {p.get('fill_px', 0):6.0f}{' core' if p['core'] else ''}")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
