"""Baseline sweep: cheapest candidate per method family that meets quality limits.

    python -m scripts.baseline [sigma ...]

Writes results/baseline.md and results/baseline.json.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from topt import methods as M
from topt.cost import pipeline_cost
from topt.quality import metrics
from topt.search import PROFILES

from .common import parse_args

# Provisional limits (the search's 'medium' profile), to be calibrated by eye.
LIMITS = PROFILES["medium"]
SIGMAS = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 100, 150, 200]
REJECT_FACTOR = 3.0  # skip candidates costing more than this x the best passing one


def failures(q: dict) -> list:
    return [k for k, lim in LIMITS.items() if abs(q[k]) > lim]


def sweep(sigma: float, W: int = 1920, H: int = 1080) -> dict:
    cands = []
    for fam, gen in M.FAMILIES.items():
        try:
            for p in gen(sigma):
                cands.append((pipeline_cost(p, W, H)["us"], fam, p))
        except ValueError as e:  # too large to simulate
            print(f"  {fam}: {e}", file=sys.stderr)
    cands.sort(key=lambda c: c[0])
    best_us, done, rows = None, set(), {}
    for us, fam, p in cands:
        if fam in done:
            continue
        if best_us is not None and us > REJECT_FACTOR * best_us:
            rows.setdefault(fam, {"status": f"rejected (>{REJECT_FACTOR:g}x cost)", "us": us})
            continue
        try:
            q = metrics(p, sigma)
        except ValueError:
            continue
        fail = failures(q)
        if not fail:
            done.add(fam)
            best_us = us if best_us is None else min(best_us, us)
            rows[fam] = {"status": "ok", **pipeline_cost(p, W, H), **q, "params": p.params}
        elif fam not in rows or rows[fam]["status"] != "ok":
            rows[fam] = {"status": "best tried fails " + ",".join(fail), **pipeline_cost(p, W, H), **q,
                         "params": p.params}
    return rows


def fmt_params(pr: dict) -> str:
    out = []
    for k, v in pr.items():
        if k == "offsets":
            out.append(f"{len(v)} passes")
        elif isinstance(v, float):
            out.append(f"{k}={v:.3g}")
        elif v is not None:
            out.append(f"{k}={v}")
    return " ".join(out)


def main():
    sigmas, res, W, H, suffix = parse_args(SIGMAS)
    results = {}
    lines = [f"# Baseline sweep (GTX 1660 model, {W}x{H}, RGB10A2)", "",
             "us = marginal cost over a plain composite pass (the last pass is the composite).", "",
             "Limits: " + ", ".join(f"{k} <= {v}" for k, v in LIMITS.items()), "",
             "| sigma | family | us | passes | fetch/px | leak | tv | aniso | phase | curv | params / status |",
             "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for s in sigmas:
        t0 = time.time()
        rows = sweep(s, W, H)
        results[s] = rows
        order = sorted(rows.items(), key=lambda kv: (kv[1]["status"] != "ok", kv[1]["us"]))
        for fam, r in order:
            if "leak" in r:
                lines.append(f"| {s:g} | {fam} | {r['us']:.0f} | {r['passes']} | {r['fetch_per_px']:.2f} | "
                             f"{r['leak']:.3f} | {r['tv']:.3f} | {r['aniso']:.3f} | {r['phase']:.3f} | {r['curv']:.2f} | "
                             f"{fmt_params(r['params'])}{'' if r['status'] == 'ok' else ' — ' + r['status']} |")
            else:
                lines.append(f"| {s:g} | {fam} | ≥{r['us']:.0f} | | | | | | | | {r['status']} |")
        print(f"sigma {s:g}: {time.time() - t0:.1f}s", file=sys.stderr)
    out = Path(__file__).resolve().parent.parent / "results"
    out.mkdir(exist_ok=True)
    (out / f"baseline{suffix}.md").write_text("\n".join(lines) + "\n")
    (out / f"baseline{suffix}.json").write_text(json.dumps(results, indent=1, default=str))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
