import numpy as np
from scipy.ndimage import convolve

from topt import methods as M
from topt.quality import metrics
from topt.sim import run

rng = np.random.default_rng(0)
IMG = rng.random((48, 48))


def ref(k1d):
    return convolve(IMG, np.outer(k1d, k1d), mode="reflect")  # == D3D MIRROR


def test_sep_bilinear_is_exact_binomial_7x7():
    b6 = np.array([1, 5, 10, 10, 5, 1], float) / 32
    pos = np.arange(-3, 3, dtype=float)
    taps = M.pair_taps(pos, b6)
    pl = M.sep_bilinear(3, 1.0)
    pl.passes[0] = pl.passes[0].__class__(1, tuple((o, -0.5, w) for o, w in taps))
    pl.passes[1] = pl.passes[1].__class__(1, tuple((0.5, o + 1.0, w) for o, w in taps))
    b7 = np.array([1, 6, 15, 20, 15, 6, 1], float) / 64
    # shifted passes + mirror differ from a symmetric reflect only at the border
    assert np.abs(run(pl, IMG) - ref(b7))[4:-4, 4:-4].max() < 1e-12
    assert sum(len(p.taps) for p in pl.passes) == 6


def test_sep_linear_matches_convolution():
    pl = M.sep_linear(4, 1.7)
    pos = np.arange(-4, 5, dtype=float)
    assert np.abs(run(pl, IMG) - ref(M.gauss(pos, 1.7))).max() < 1e-12


def test_direct2d_matches_sep_linear():
    assert np.abs(run(M.direct2d(3, 1.2), IMG) - run(M.sep_linear(3, 1.2), IMG)).max() < 1e-12


def test_fitted_sigma():
    for fam in ("sep_bilinear", "kawase", "dual_filter"):
        p = next(iter(M.FAMILIES[fam](4.0)))
        assert abs(metrics(p, 4.0)["sigma_err"]) < 0.02, fam
