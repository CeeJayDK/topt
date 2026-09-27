"""Hybrid down/blur/up search over sigma, with cost/quality Pareto output.

    python -m scripts.hybrid [sigma ...]

Writes results/hybrid.json (every evaluated candidate) and results/hybrid.md.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from topt.search import PROFILES, pareto, search

SIGMAS = [2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 100, 150, 200]
OUT = Path(__file__).resolve().parent.parent / "results"


def log(msg: str):
    print(msg, file=sys.stderr, flush=True)


def load_baseline() -> dict:
    """Cheapest baseline row per sigma that passes each profile (from baseline.json)."""
    from topt.search import passes_profile
    p = OUT / "baseline.json"
    if not p.exists():
        return {}
    best = {}
    for s, rows in json.loads(p.read_text()).items():
        for fam, r in rows.items():
            if "curv" not in r:
                continue
            for name, prof in PROFILES.items():
                if passes_profile(r, prof):
                    cur = best.setdefault(float(s), {}).get(name)
                    if cur is None or r["us"] < cur[1]:
                        best[float(s)][name] = (fam, r["us"])
    return best


def main():
    sigmas = [float(a) for a in sys.argv[1:]] or SIGMAS
    path = OUT / "hybrid.json"
    allrecs = json.loads(path.read_text()) if path.exists() else {}
    for s in sigmas:
        t0 = time.time()
        allrecs[f"{s:g}"] = search(s, log=log)
        log(f"sigma {s:g}: {len(allrecs[f'{s:g}'])} evaluated in {time.time() - t0:.0f}s")
        path.write_text(json.dumps(allrecs, default=str))
    write_md(allrecs)


def write_md(allrecs: dict):
    base = load_baseline()
    lines = ["# Hybrid down/blur/up search (GTX 1660 model, 1920x1080, RGB10A2)", "",
             "Profiles: " + "; ".join(f"**{n}** " + ", ".join(f"{k}<={v}" for k, v in p.items())
                                      for n, p in PROFILES.items()), "",
             "## Cheapest design per profile", "",
             "| sigma | profile | us | passes | leak | tv | phase | curv | design | best baseline |",
             "|---:|---|---:|---:|---:|---:|---:|---:|---|---|"]
    for s in sorted(allrecs, key=float):
        recs = allrecs[s]
        for name in PROFILES:
            ok = [r for r in recs if name in r["profiles"]]
            b = base.get(float(s), {}).get(name)
            bs = f"{b[0]} {b[1]:.0f} us" if b else "none"
            if ok:
                r = min(ok, key=lambda r: r["us"])
                lines.append(f"| {s} | {name} | {r['us']:.0f} | {r['passes']} | {r['leak']:.3f} | {r['tv']:.3f} | "
                             f"{r['phase']:.3f} | {r['curv']:.2f} | {r['design']} | {bs} |")
            else:
                lines.append(f"| {s} | {name} | | | | | | | none found | {bs} |")
    lines += ["", "## Cost vs shift-variance Pareto front (candidates also meeting the other 'medium' limits)", ""]
    med = PROFILES["medium"]
    for s in sorted(allrecs, key=float):
        recs = [r for r in allrecs[s] if all(abs(r[k]) <= med[k] for k in ("leak", "tv", "aniso", "curv", "block", "sigma_err"))]
        lines.append(f"**sigma {s}**: " + ", ".join(
            f"{r['us']:.0f} us / phase {r['phase']:.3f} ({r['design']})" for r in pareto(recs)[:6]))
        lines.append("")
    (OUT / "hybrid.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
