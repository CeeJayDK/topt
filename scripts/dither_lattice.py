"""Dither pattern optimizer: SweetFX-style ordered dithers frac(dot(pos, a) + c), scored and priced.

    python -m scripts.dither_lattice <sopt>/docs/opbench

The dither is one value d in (-0.5, 0.5) (rectangular, in steps of the screen format) per pixel, used as
it is in all three channels ("same") or added to green and subtracted from red and blue ("-+-", CeeJay's
trick: the brightness steps get as small as with three independent channels for the price of one).

Patterns:
* lattice N p q: d = frac((p x + q y) / N + c) - 0.5 on the pixel indices x, y: a rank-1 lattice of N
  levels (k + 0.5) / N - 0.5. CeeJay's plus dither is N 5 p 1 q 2, SweetFX 1 is N 144 p 9 q 40
  (1/16, 10/36). All N <= 64 (every p, q up to the mirror symmetries), N 65..256 with p = 1.
* real a b: d = frac(a x + b y + c) - 0.5 for real a, b (R2 / golden-ratio generators, random ones).
* scrambled a b k: d = frac(k frac(a x + b y)) - 0.5 (IGN: a, b = 0.06711056, 0.00583715, k = 52.98).

Quality (simulated, a gradient quantized to the screen's steps): on flat fields at 64 levels between two
steps, the output's brightness error (Rec. 709 luma) after a Gaussian of 1 px (the eye, roughly):
grain = its spread around the mean, band = the largest mean error (the banding left: N levels leave
contours of up to 1 / (2N) step), colour = the largest channel's error against the luma (-+- only).
vis = sqrt(grain^2 + band^2).

Cost (sopt's OpBench measurements, units of one mad = 1, per core GPU) of the formulations of
frac(t) - 0.5 after t = dot(pos, a) + c (two mads):
* frac: frac(t) - 0.5
* add-round: t - round(t) with round(t) = (t + 12582912) - 12582912 (1.5 * 2^23; needs `precise`, fxc
  folds it otherwise; |t| <= 2^22): 3 adds, and the offset c absorbs the 0.5. Exact on the lattices.
* uint: t - float(uint(t)) (t >= 0)
Writes results/dither_lattice.md and results/dither_lattice.json (the best of each kind).
"""
from __future__ import annotations

import csv
import io
import json
import math
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter

ROOT = Path(__file__).resolve().parent.parent
T, CROP = 96, 8                               # simulated tile, border dropped after the Gaussian
FS = (np.arange(64) + 0.5) / 64               # flat-field levels between two steps
LW = np.array([0.2126, 0.7152, 0.0722])       # Rec. 709 luma
EYE = 1.0
Y, X = np.mgrid[0:T, 0:T].astype(np.float64)


def frac(v):
    return v - np.floor(v)


def lattice(N, p, q):
    return frac((p * X + q * Y) / N + 0.5 / N) - 0.5


def real(a, b):
    return frac(a * X + b * Y + 0.5) - 0.5


def scrambled(a, b, k):
    return frac(k * frac(a * X + b * Y)) - 0.5


def score(d: np.ndarray) -> dict:
    f = FS[:, None, None]
    ep = np.round(f + d) - f                  # error of a channel that adds d
    em = np.round(f - d) - f                  # ... that subtracts d
    gp = gaussian_filter(ep, (0, EYE, EYE), mode="reflect")[:, CROP:-CROP, CROP:-CROP]
    gm = gaussian_filter(em, (0, EYE, EYE), mode="reflect")[:, CROP:-CROP, CROP:-CROP]
    out = {}
    for name, l in (("same", gp), ("-+-", LW[1] * gp + (LW[0] + LW[2]) * gm)):
        m = l.mean((1, 2))
        grain = float((l - m[:, None, None]).std((1, 2)).mean())
        band = float(np.abs(m).max())
        out[name] = {"grain": grain, "band": band, "vis": math.hypot(grain, band)}
    out["-+-"]["colour"] = float(max(LW[1], 1 - LW[1]) * (gp - gm).std((1, 2)).mean())
    out["same"]["colour"] = 0.0
    return out


def canon(N, p, q):
    p, q = min(p % N, (-p) % N), min(q % N, (-q) % N)
    return (N,) + tuple(sorted((p, q)))


NAMED = {"plus dither (CeeJay)": ("lattice", (5, 1, 2)), "SweetFX 1": ("lattice", (144, 9, 40)),
         "IGN": ("scrambled", (0.06711056, 0.00583715, 52.9829189)),
         "R2": ("real", (1 / 1.32471795724474602596, 1 / 1.32471795724474602596 ** 2))}


def candidates():
    seen = set()
    for kind, args in NAMED.values():
        if kind == "lattice":
            seen.add(args)
        yield kind, args
    for N in range(2, 257):
        for p in (range(1, N) if N <= 64 else (1,)):
            for q in range(0, N):
                if math.gcd(math.gcd(p, q), N) != 1:
                    continue
                c = canon(N, p, q)
                if c not in seen:
                    seen.add(c)
                    yield ("lattice", c)
    phi2 = 1.32471795724474602596                       # plastic number: R2
    phi = (1 + 5 ** 0.5) / 2
    for a, b in ((1 / phi2, 1 / phi2 ** 2), (phi - 1, (phi - 1) ** 2), (1 / 16, 10 / 36), (0.06711056, 0.00583715)):
        yield ("real", (a, b))
    rng = np.random.default_rng(1)
    for a, b in rng.random((3000, 2)):
        yield ("real", (float(a), float(b)))
    for a, b, k in zip(rng.random(3000), rng.random(3000), rng.uniform(2, 100, 3000)):
        yield ("scrambled", (float(a), float(b), float(k)))


def run(c):
    kind, args = c
    d = {"lattice": lattice, "real": real, "scrambled": scrambled}[kind](*args)
    return kind, args, score(d)


# ---- cost (OpBench) ----
CORE = {"GTX 1080": "NVIDIA GeForce GTX 1080", "GTX 1660": "NVIDIA GeForce GTX 1660", "RTX 2070": "NVIDIA GeForce RTX 2070",
        "RTX 3060": "NVIDIA GeForce RTX 3060", "RTX 4070": "NVIDIA GeForce RTX 4070", "RTX 5070": "NVIDIA GeForce RTX 5070",
        "RX 590": "Radeon RX 590 Series", "RX 5500 XT": "Radeon RX 5500 XT", "RX 6600": "AMD Radeon RX 6600",
        "RX 7900 XTX": "AMD Radeon RX 7900 XTX", "RX 9070 XT": "AMD Radeon RX 9070 XT",
        "UHD 630": "Intel(R) UHD Graphics 630", "Iris Xe": "Intel(R) Iris(R) Xe Graphics", "Arc B580": "Intel(R) Arc(TM) B580 Graphics"}
FORMS = {  # ops after the two mads of t = dot(pos, a) + c
    "frac": {"mad": 2, "frac": 1, "add": 1},
    "add-round": {"mad": 2, "add": 3},
    "uint": {"mad": 2, "ftou": 1, "utof": 1, "add": 1},
    "scrambled, frac": {"mad": 2, "frac": 2, "mul": 1, "add": 1},
    "scrambled, add-round": {"mad": 2, "mul": 1, "add": 6},
}


def load_opbench(folder: Path) -> dict:
    best = {}
    for f in folder.glob("*.csv"):
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        gpu = next((l.split(":", 1)[1].strip() for l in lines if l.startswith("# gpu:")), None)
        rows = list(csv.DictReader(io.StringIO("\n".join(l for l in lines if not l.startswith("#")))))
        if gpu is None and rows and "gpu" in rows[0]:
            gpu = rows[0]["gpu"]
        t = {}
        for r in rows:
            if r.get("config") == "tput":
                try:
                    t[r["test"]] = float(r["units_vs_base"]) / 4.0
                except (KeyError, TypeError, ValueError):
                    pass
        if gpu and (gpu not in best or len(t) > len(best[gpu])):
            best[gpu] = t
    return best


def costs(folder: Path) -> dict:
    ob = load_opbench(folder)
    out = {}
    for short, name in CORE.items():
        t = ob.get(name)
        if not t:
            continue
        out[short] = {k: sum(n * max(t.get(op, 1.0), 0.0) for op, n in ops.items()) for k, ops in FORMS.items()}
    return out


def label(kind, args):
    if kind == "lattice":
        N, p, q = args
        return f"lattice N {N} ({p}, {q}) / {N}"
    if kind == "real":
        return "real ({:.8f}, {:.8f})".format(*args)
    return "scrambled ({:.8f}, {:.8f}) k {:.4f}".format(*args)


def main():
    """argv: the OpBench folder; --rows <file>: keep / reuse every candidate's score there (not in the repo)."""
    args = sys.argv[1:]
    store = Path(args.pop(args.index("--rows") + 1)) if "--rows" in args else None
    if "--rows" in args:
        args.remove("--rows")
    opbench = Path(args[0]) if args else None
    if store and store.exists():
        rows = json.loads(store.read_text())
    else:
        cands = list(candidates())
        print(len(cands), "candidates", flush=True)
        with Pool() as pool:
            res = pool.map(run, cands, chunksize=64)
        rows = [{"kind": k, "args": list(a), "label": label(k, a), **{f"{s}_{m}": v for s, d in sc.items() for m, v in d.items()}}
                for k, a, sc in res]
        if store:
            store.write_text(json.dumps(rows))
    named = NAMED

    def fmt(r, s="-+-"):
        return (f"| {r['label']} | {r[s + '_vis']:.4f} | {r[s + '_grain']:.4f} | {r[s + '_band']:.4f} | "
                f"{r[s + '_colour']:.4f} | {r['same_vis']:.4f} |")
    head = ["| pattern | vis | grain | band | colour | vis (same) |", "|---|---:|---:|---:|---:|---:|"]
    lines = ["# Dither pattern optimizer", "", "Generated by `python -m scripts.dither_lattice <sopt>/docs/opbench`; see the",
             "script's docstring for the patterns, the simulation and the cost. One value, -+- (added to",
             "green, subtracted from red and blue) unless noted; errors in steps of the screen format.", "",
             "## Named patterns", ""] + head
    for n, (k, a) in named.items():
        r = next(x for x in rows if x["kind"] == k and tuple(x["args"]) == tuple(a))
        lines.append(fmt({**r, "label": f"{n}: {r['label']}"}))
    best = []
    for kind in ("lattice", "real", "scrambled"):
        sel = sorted((r for r in rows if r["kind"] == kind), key=lambda r: r["-+-_vis"])[:15]
        best += sel
        lines += ["", f"## Best {kind} patterns (by vis, -+-)", ""] + head + [fmt(r) for r in sel]
    lat = [r for r in rows if r["kind"] == "lattice"]
    lines += ["", "## Best lattice per level count N", "", "| N | pattern | vis | grain | band |", "|---:|---|---:|---:|---:|"]
    for N in (2, 3, 4, 5, 6, 7, 8, 10, 12, 13, 16, 21, 24, 32, 34, 48, 55, 64, 89, 128, 144, 233, 256):
        sel = [r for r in lat if r["args"][0] == N]
        if sel:
            r = min(sel, key=lambda r: r["-+-_vis"])
            lines.append(f"| {N} | {r['label']} | {r['-+-_vis']:.4f} | {r['-+-_grain']:.4f} | {r['-+-_band']:.4f} |")
    if opbench:
        c = costs(opbench)
        forms = list(FORMS)
        lines += ["", "## Cost per pixel (mads, OpBench)", "",
                  "Ops after t = dot(pos, a) + c (two mads); the -+- signs and the step scale are the same for all.", "",
                  "| GPU | " + " | ".join(forms) + " |", "|---|" + "---:|" * len(forms)]
        for g, v in c.items():
            lines.append(f"| {g} | " + " | ".join(f"{v[f]:.1f}" for f in forms) + " |")
    (ROOT / "results" / "dither_lattice.json").write_text(json.dumps(best, indent=0))
    (ROOT / "results" / "dither_lattice.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
