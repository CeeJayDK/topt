"""Shared command-line handling: `--res 1080p|1440p|4k` plus sigma values."""
from __future__ import annotations

import sys

from topt.cost import RESOLUTIONS


def parse_args(default_sigmas: list) -> tuple:
    args, res = list(sys.argv[1:]), "1080p"
    if "--res" in args:
        i = args.index("--res")
        res = args[i + 1].lower()
        del args[i:i + 2]
    W, H = RESOLUTIONS[res]
    sigmas = [float(a) for a in args] or default_sigmas
    suffix = "" if res == "1080p" else f"_{res}"
    return sigmas, res, W, H, suffix
