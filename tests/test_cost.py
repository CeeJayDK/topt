import dataclasses

from topt.cost import pipeline_cost
from topt.sim import Pass, Pipeline


def _pl(bpp):
    passes = [Pass(2, ((0.0, 0.0, 1.0),), bpp=bpp), Pass(2, ((0.0, 0.0, 1.0),), bpp=bpp), Pass(1, ((0.0, 0.0, 1.0),))]
    return Pipeline("t", {}, passes)


def test_smaller_intermediates_cost_less():
    rgb, r16, r8 = (pipeline_cost(_pl(b))["us"] for b in (4, 2, 1))
    assert rgb > r16 > r8 > 0


def test_default_bpp_matches_rgb10a2():
    pl = _pl(4)
    same = dataclasses.replace(pl, passes=[dataclasses.replace(p, bpp=4) for p in pl.passes])
    assert pipeline_cost(pl)["us"] == pipeline_cost(same)["us"]
