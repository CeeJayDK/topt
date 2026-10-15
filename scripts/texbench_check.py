"""Check the cost model against TexBench full-screen pass timings.

    python -m scripts.texbench_check path/to/texbench-report.csv

TexBench (CeeJayDK/sopt, tools/windows/texbench) times whole passes at 3840 x 2160:
render-target writes per format, copies, half-size downsamples. Prints measured vs
model (GTX 1660 profile) in ms.
"""
from __future__ import annotations

import csv
import sys

from topt.cost import FORMAT_BYTES, GTX1660, GTX1660_V1, _pass_time

W, H = 3840, 2160
N = W * H


def model(kind: str, fmt: str, gpu) -> float:
    b = FORMAT_BYTES[fmt]
    wide = gpu.wide_filter if b >= 8 else 1.0
    if kind == "write":     # write only, no reads
        t = _pass_time(N, 0, 0, gpu, b, 0, fmt)[0]
    elif kind == "copy":    # full-size copy, one point read
        t = _pass_time(N, N, 1, gpu, b, N * b, fmt)[0]
    else:                   # half-size, one bilinear read of 2 x 2
        t = _pass_time(N // 4, N, wide, gpu, b, N * b, fmt)[0]
    return t * 1e3


def main():
    rows = list(csv.reader(line for line in open(sys.argv[1]) if not line.startswith("#")))
    print(f"{'test':28s} {'measured':>9s} {'model':>7s} {'old model':>9s}")
    for r in rows:
        if len(r) < 6 or r[0] not in ("write", "pass"):
            continue
        name, ms = r[1], r[5]
        parts = name.split()
        if r[0] == "write" and parts[-1] == "noise" and parts[0] in FORMAT_BYTES:
            kind, fmt = "write", parts[0]
        elif r[0] == "pass" and parts[0] == "copy" and parts[1] == "Sample" and parts[-1] in FORMAT_BYTES:
            kind, fmt = "copy", parts[-1]
        elif r[0] == "pass" and parts[0] == "half" and parts[1] == "bilinear" and parts[-1] in FORMAT_BYTES:
            kind, fmt = "half", parts[-1]
        else:
            continue
        print(f"{name:28s} {float(ms):9.3f} {model(kind, fmt, GTX1660):7.3f} {model(kind, fmt, GTX1660_V1):9.3f}")


if __name__ == "__main__":
    main()
