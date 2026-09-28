"""Re-price the 1080p hybrid search at another resolution.

Quality metrics do not depend on the screen size, only the cost model does, so
the candidates evaluated at 1080p are rebuilt and re-costed:

    python -m scripts.reprice --res 4k      # results/hybrid.json -> results/hybrid_4k.json
"""
from __future__ import annotations

import json
from pathlib import Path

from topt import search as S
from topt.cost import pipeline_cost

from .common import parse_args
from .hybrid import write_md

OUT = Path(__file__).resolve().parent.parent / "results"


def main():
    _, res, W, H, suffix = parse_args([])
    recs = json.loads((OUT / "hybrid.json").read_text())
    for s, rows in recs.items():
        for r in rows:
            pl = S.build(S.Design.from_params(r["params"]), r["params"]["sl"])
            c = pipeline_cost(pl, W, H)
            r.update({k: c[k] for k in ("us", "passes", "fetch_per_px")})
    (OUT / f"hybrid{suffix}.json").write_text(json.dumps(recs, default=str))
    write_md(recs, W, H, suffix)
    print(f"re-priced {sum(len(v) for v in recs.values())} candidates at {W}x{H}")


if __name__ == "__main__":
    main()
