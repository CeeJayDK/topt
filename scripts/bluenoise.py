"""Blue-noise textures (void and cluster, Ulichney 1993) for the noise benchmarks.

    python -m scripts.bluenoise

Writes fx/Textures/topt_bn<size>_<format>.png:
  RG8   two independent blue-noise channels, sizes 4 .. 512
  R8    one channel, 64
  RGBA8 four channels, 64
  R8P   one byte holding two 4-bit values (high nibble x, low nibble y), 64
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "fx" / "Textures"
SIGMA = 1.5


def _kernel(n: int) -> tuple:
    r = min(n // 2, int(np.ceil(3.5 * SIGMA)))
    d = np.arange(-r, r + 1)
    k = np.exp(-(d[:, None] ** 2 + d[None, :] ** 2) / (2 * SIGMA ** 2))
    return d, k


def _splat(E, n, d, k, i, j, s):
    E[np.ix_((i + d) % n, (j + d) % n)] += s * k


def void_and_cluster(n: int, seed: int) -> np.ndarray:
    """Rank (0 .. n*n-1) of every texel; ranks spread as blue noise."""
    rng = np.random.default_rng(seed)
    d, k = _kernel(n)
    N = n * n
    ones = max(1, N // 10)
    B = np.zeros((n, n), bool)
    B.flat[rng.choice(N, ones, replace=False)] = True
    E = np.zeros((n, n))
    for p in np.flatnonzero(B):
        _splat(E, n, d, k, *divmod(p, n), 1.0)

    def tightest(B, E):
        return int(np.argmax(np.where(B, E, -np.inf)))

    def largest_void(B, E):
        return int(np.argmin(np.where(B, np.inf, E)))

    while True:  # relax the initial pattern
        c = tightest(B, E)
        B.flat[c] = False
        _splat(E, n, d, k, *divmod(c, n), -1.0)
        v = largest_void(B, E)
        B.flat[v] = True
        _splat(E, n, d, k, *divmod(v, n), 1.0)
        if v == c:
            break
    rank = np.zeros(N, np.int64)
    B1, E1 = B.copy(), E.copy()
    for r in range(ones - 1, -1, -1):  # phase 1: remove clusters
        c = tightest(B1, E1)
        B1.flat[c] = False
        _splat(E1, n, d, k, *divmod(c, n), -1.0)
        rank[c] = r
    for r in range(ones, N):  # phases 2 + 3: fill voids
        v = largest_void(B, E)
        B.flat[v] = True
        _splat(E, n, d, k, *divmod(v, n), 1.0)
        rank[v] = r
    return rank.reshape(n, n)


def to8(rank: np.ndarray, levels: int = 256) -> np.ndarray:
    return (rank * levels // rank.size).astype(np.uint8)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for n in (4, 8, 16, 32, 64, 128, 256, 512):
        rg = np.stack([to8(void_and_cluster(n, 2 * n)), to8(void_and_cluster(n, 2 * n + 1)),
                       np.zeros((n, n), np.uint8)], -1)
        Image.fromarray(rg, "RGB").save(OUT / f"topt_bn{n}_RG8.png", optimize=True)
        print("wrote", n, flush=True)
    n = 64
    ch = [to8(void_and_cluster(n, 100 + c)) for c in range(4)]
    Image.fromarray(ch[0], "L").save(OUT / "topt_bn64_R8.png", optimize=True)
    Image.fromarray(np.stack(ch, -1), "RGBA").save(OUT / "topt_bn64_RGBA8.png", optimize=True)
    packed = (to8(void_and_cluster(n, 200), 16) << 4) | to8(void_and_cluster(n, 201), 16)
    Image.fromarray(packed.astype(np.uint8), "L").save(OUT / "topt_bn64_R8P.png", optimize=True)
    print("wrote 64 R8 / RGBA8 / R8P")


if __name__ == "__main__":
    main()
