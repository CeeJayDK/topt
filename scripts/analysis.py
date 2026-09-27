"""Cross-method summary: winners per sigma, pass-overhead sensitivity, compute
tile estimate and RGB10A2 quantization check.

    python -m scripts.analysis        (after scripts.baseline and scripts.hybrid)

Writes results/analysis.md.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from topt import methods as M
from topt import search as S
from topt.cost import GTX1660, cs_tile_sep_cost
from topt.quality import metrics
from topt.sim import run

from .common import parse_args

OUT = Path(__file__).resolve().parent.parent / "results"
OVERHEADS = (2, 5, 10, 20)  # us per pass
BASE_OVH = GTX1660.pass_overhead * 1e6


def candidates(s: str, hyb: dict, base: dict, W: int, H: int) -> list:
    """(name, us, passes, metrics, rebuild) for every candidate we know at sigma s."""
    out = []
    for r in hyb.get(s, []):
        p = r["params"]
        d = S.Design.from_params(p)
        out.append(("hybrid: " + r["design"], r["us"], r["passes"], r, (d, p["sl"])))
    for fam, r in base.get(s, {}).items():
        if "curv" in r:
            out.append((fam, r["us"], r["passes"], r, None))
    sigma = float(s)
    if sigma <= 8:  # compute-shader tile blur has the quality of sep_linear with the same r
        for pl in M.cand_sep_linear(sigma):
            r = pl.params["r"]
            c = cs_tile_sep_cost(r, W, H)
            if c is None or c["us"] > 2000:
                break
            out.append((f"cs_tile r={r} + composite (T={c['tile']}, {c['bound']}-bound)", c["us"], c["passes"],
                        metrics(pl, sigma), None))
    return out


def quant_error(d: S.Design, sl: float) -> tuple:
    """Max / RMS error in 10-bit LSBs when every pass is stored as RGB10A2."""
    pl = S.build(d, sl)
    n = 1024
    y, x = np.mgrid[0:n, 0:n] / n
    rng = np.random.default_rng(1)
    img = np.clip(0.5 + 0.3 * np.sin(6 * x) * np.cos(5 * y) + 0.05 * rng.standard_normal((n, n)), 0, 1)
    img = np.round(img * 1023) / 1023
    a, b = run(pl, img), run(pl, img, quantize_bits=10)
    e = np.abs(a - b)[n // 8:-n // 8, n // 8:-n // 8] * 1023
    return float(e.max()), float(np.sqrt((e ** 2).mean()))


def main():
    _, res, W, H, suffix = parse_args([])
    hyb = json.loads((OUT / f"hybrid{suffix}.json").read_text())
    bp = OUT / f"baseline{suffix}.json"
    base = json.loads(bp.read_text()) if bp.exists() else {}
    base = {f"{float(k):g}": v for k, v in base.items()}
    sigmas = sorted(set(hyb) | set(base), key=float)
    lines = [f"# Summary: cheapest method per sigma (GTX 1660 model, {W}x{H}, RGB10A2)", "",
             "us = marginal cost over a plain composite pass (blur fused into the consumer pass).", "",
             f"Quality profile: medium ({', '.join(f'{k}<={v}' for k, v in S.PROFILES['medium'].items())}).",
             f"Cost columns re-price every candidate with a different per-pass overhead (model default "
             f"{BASE_OVH:g} us).", "",
             "| sigma | winner @5us | us @2 | us @5 | us @10 | us @20 | winner @20us if different | "
             "10-bit err max/rms (LSB) |",
             "|---:|---|---:|---:|---:|---:|---|---|"]
    prof = S.PROFILES["medium"]
    for s in sigmas:
        cands = [c for c in candidates(s, hyb, base, W, H) if S.passes_profile(c[3], prof)]
        if not cands:
            lines.append(f"| {s} | none passes | | | | | | |")
            continue
        reprice = lambda c, o: c[1] + (c[2] - 1) * (o - BASE_OVH)  # composite pass not counted
        price = {o: sorted(cands, key=lambda c: reprice(c, o)) for o in OVERHEADS}
        w5 = price[5][0]
        cols = [f"{reprice(price[o][0], o):.0f}" for o in OVERHEADS]
        w20 = price[20][0][0] if price[20][0][0] != w5[0] else ""
        q = ""
        if w5[4] is not None:
            mx, rms = quant_error(*w5[4])
            q = f"{mx:.2f} / {rms:.2f}"
        lines.append(f"| {s} | {w5[0]} | " + " | ".join(cols) + f" | {w20} | {q} |")
    (OUT / f"analysis{suffix}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
