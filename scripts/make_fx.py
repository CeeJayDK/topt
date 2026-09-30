"""Write the hardware-timing effects to fx/.

    python -m scripts.make_fx [--repeat N]

TOPT_Bench_Micro.fx  cost-model calibration (composite baseline, fetch sweep,
                     pass overhead chain, first-downsample variants)
TOPT_Bench_Blur.fx   optimizer winners and classic methods, blur fused into
                     the composite pass
TOPT_Bench_CS.fx     compute tile blur + mandatory composite pixel shader
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import numpy as np

from topt import methods as M
from topt import search as S
from topt.fxgen import HEADER, effect
from topt.quality import metrics
from topt.sim import Pass, Pipeline

ROOT = Path(__file__).resolve().parent.parent
FX = ROOT / "fx"
ONE = ((0.0, 0.0, 1.0),)


def composite_from(src_passes: list, up_taps=ONE) -> Pipeline:
    return Pipeline("bench", {}, src_passes + [Pass(1, up_taps)])


def micro() -> list:
    items = [(Pipeline("bench", {}, [Pass(1, ONE)]), "TOPT_M_Composite",
              "Baseline: composite only (read backbuffer, write screen)")]
    for n in (1, 2, 4, 6, 8, 12, 16, 24, 32):
        # n bilinear taps on a ring of radius ~3 px with fractional offsets
        taps = tuple((3.3 * math.cos(2 * math.pi * (i + 0.5) / n) + 0.25,
                      3.3 * math.sin(2 * math.pi * (i + 0.5) / n) + 0.25, 1.0 / n) for i in range(n))
        items.append((composite_from([Pass(1, taps)]), f"TOPT_M_Taps{n:02d}",
                      f"Full-res pass with {n} bilinear taps into an intermediate, then composite"))
    for k in (1, 8, 32):
        passes = [Pass(64, ONE, src=-1 if i == 0 else None) for i in range(k)]
        items.append((composite_from(passes), f"TOPT_M_Chain{k:02d}",
                      f"{k} tiny 1/64-res passes, then composite (slope = per-pass overhead)"))
    for f, e, lab in ((2, 1, "x2 box, 1 tap"), (4, 1, "x4 box, 4 taps"), (4, 3, "x4 box*[1 2 1], 9 taps"),
                      (4, 5, "x4 box*[1 4 6 4 1], 16 taps"), (8, 1, "x8 box, 16 taps")):
        p = Pass(f, S.outer(S.down_taps_1d(f, e)))
        items.append((composite_from([p]), f"TOPT_M_Down{f}e{e}",
                      f"First downsample {lab}, then composite (1-tap upsample)"))
    return items


def load_winners(path: Path) -> list:
    """Hybrid designs to time: medium and strict winners at a few sigmas."""
    if not path.exists():
        return []
    recs = json.loads(path.read_text())
    out = []
    for s in ("4", "16", "64", "200"):
        for prof in ("medium", "strict"):
            ok = [r for r in recs.get(s, []) if S.passes_profile(r, S.PROFILES[prof])]
            if not ok:
                continue
            r = min(ok, key=lambda r: r["us"])
            p = r["params"]
            d = S.Design.from_params(p)
            out.append((S.build(d, p["sl"]), f"TOPT_B_Hybrid_s{s}_{prof}",
                        f"sigma {s} {prof} hybrid: {r['design']} (model {r['us']:.0f} us marginal @1080p)"))
    # pinwheel-chain variants at sigma 16 (more passes; hardware decides whether they pay off)
    rows = [r for r in recs.get("16", []) if S.passes_profile(r, S.PROFILES["medium"])]
    for tag, cond in (("pwchain", lambda r: r["params"]["bottom"].startswith("pw")),
                      ("pindown", lambda r: r["params"].get("down_pin", 0) > 0),
                      ("rot45", lambda r: r["params"].get("rot", False))):
        c = [r for r in rows if cond(r)]
        if c:
            r = min(c, key=lambda r: r["us"])
            out.append((S.build(S.Design.from_params(r["params"]), r["params"]["sl"]), f"TOPT_B_Hybrid_s16_{tag}",
                        f"sigma 16 medium, {tag}: {r['design']} (model {r['us']:.0f} us marginal @1080p)"))
    return out


def pinwheels(path: Path) -> list:
    """Single-pass pinwheel blurs from scripts.small_kernels (medium profile)."""
    if not path.exists():
        return []
    rep = json.loads(path.read_text())
    out = []
    for n in (5, 9, 13):
        r = rep.get(f"{n}_medium")
        if r:
            taps = tuple(tuple(t) for t in r["taps"])
            out.append((Pipeline("pinwheel", {}, [Pass(1, taps)]), f"TOPT_B_pinwheel{n}",
                        f"sigma {r['sigma']} single-pass pinwheel, {n} fetches (model {r['us']:.0f} us marginal @1080p)"))
    return out


def luma_patterns() -> list:
    """LumaSharpen's Fast and Normal sample patterns used as single-pass blurs."""
    t = 1.0 / 3.0
    quad = lambda o, w: tuple((sx * o, sy * o, w) for sx in (-1, 1) for sy in (-1, 1))
    pats = [
        ("TOPT_B_luma_fast", ((t, t, 0.5), (-t, -t, 0.5)), "LumaSharpen Fast: 2 taps at +-(1/3,1/3), sigma 0.58 (diagonal only)"),
        ("TOPT_B_luma_fast_c", ((t, t, 0.4), (-t, -t, 0.4), (0.0, 0.0, 0.2)), "LumaSharpen Fast + centre 0.2, 3 fetches, sigma 0.52"),
        ("TOPT_B_luma_normal", quad(0.5, 0.25), "LumaSharpen Normal: 4 taps at (+-0.5,+-0.5) = 3x3 binomial, sigma 0.71"),
        ("TOPT_B_luma_normal_034", quad(0.34, 0.25), "LumaSharpen Normal with offset 0.34, sigma 0.60 (best 4-fetch Gaussian fit)"),
    ]
    return [(Pipeline("luma", {}, [Pass(1, taps)]), name, label) for name, taps, label in pats]


def classic() -> list:
    out = []
    for sigma in (2, 4):
        for fam in ("sep_linear", "sep_bilinear"):
            for p in M.FAMILIES[fam](sigma):
                if S.passes_profile(metrics(p, sigma), S.PROFILES["medium"]):
                    out.append((p, f"TOPT_B_{fam}_s{sigma}", f"sigma {sigma} {fam} {p.params}"))
                    break
    for p in M.cand_direct2d(1):
        if S.passes_profile(metrics(p, 1), S.PROFILES["medium"]):
            out.append((p, "TOPT_B_direct2d_s1", f"sigma 1 single pass {p.params}"))
            break
    for sigma, L in ((16, 4), (64, 6)):
        p = next(q for q in M.cand_dual_filter(sigma) if q.params["levels"] == L)
        out.append((p, f"TOPT_B_dual_s{sigma}", f"sigma {sigma} dual filter L={L} o={p.params['o']:.3f}"))
    for p in M.cand_pyramid(16, truncs=(3.0,)):
        if p.params["k"] == 2 and p.params["up"] == "chain" and p.params["warp"] is None:
            out.append((p, "TOPT_B_pyramid_s16", f"sigma 16 classic pyramid k=2 chain m={p.params['m']}"))
            break
    return out


CS_TEMPLATE = """// Auto-generated by topt - compute tile blur (separable Gaussian in groupshared memory).
// Compute shaders cannot write the screen, so a composite pixel shader follows.
#include "ReShade.fxh"

#if __RENDERER__ >= 0xb000

#ifndef TOPT_FORMAT
	#define TOPT_FORMAT RGB10A2
#endif

uniform float TOPT_Strength < ui_type = "slider"; ui_min = 0.0; ui_max = 1.0; > = 1.0;

{BLOCKS}
#endif
"""

CS_BLOCK = """// ---- {NAME}: sigma {SIGMA}, radius {R}, {T}x{T} tile
texture {NAME}_tOut {{ Width = BUFFER_WIDTH; Height = BUFFER_HEIGHT; Format = TOPT_FORMAT; }};
storage2D {NAME}_stOut {{ Texture = {NAME}_tOut; }};
sampler {NAME}_sOut {{ Texture = {NAME}_tOut; }};
static const float {NAME}_w[{R1}] = {{ {W} }};
groupshared float3 {NAME}_tile[{S} * {S}];
groupshared float3 {NAME}_row[{S} * {T}];

void {NAME}_CS(uint3 gid : SV_GroupID, uint3 tid : SV_GroupThreadID)
{{
	const int2 size = int2(BUFFER_WIDTH, BUFFER_HEIGHT);
	const int2 origin = int2(gid.xy) * {T} - {R};
	const uint lin = tid.y * {T} + tid.x;
	for (uint i = lin; i < {S} * {S}; i += {T} * {T})
	{{
		int2 p = origin + int2(i % {S}, i / {S});
		p = max(p, -1 - p);            // mirror addressing
		p = min(p, 2 * size - 1 - p);
		{NAME}_tile[i] = tex2Dfetch(ReShade::BackBuffer, p).rgb;
	}}
	barrier();
	for (uint j = lin; j < {S} * {T}; j += {T} * {T})
	{{
		const uint b = (j / {T}) * {S} + (j % {T}) + {R};
		float3 c = {NAME}_w[0] * {NAME}_tile[b];
		[unroll] for (int k = 1; k <= {R}; k++)
			c += {NAME}_w[k] * ({NAME}_tile[b - k] + {NAME}_tile[b + k]);
		{NAME}_row[j] = c;
	}}
	barrier();
	const uint b = (tid.y + {R}) * {T} + tid.x;
	float3 c = {NAME}_w[0] * {NAME}_row[b];
	[unroll] for (int k = 1; k <= {R}; k++)
		c += {NAME}_w[k] * ({NAME}_row[b - k * {T}] + {NAME}_row[b + k * {T}]);
	const int2 o = int2(gid.xy) * {T} + int2(tid.xy);
	if (all(o < size))
		tex2Dstore({NAME}_stOut, o, float4(c, 1.0));
}}

float4 {NAME}_PS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{{
	const float3 o = tex2D(ReShade::BackBuffer, uv).rgb;
	return float4(lerp(o, tex2D({NAME}_sOut, uv).rgb, TOPT_Strength), 1.0);
}}

technique {NAME} < ui_tooltip = "Compute tile blur sigma {SIGMA} (r={R}) + composite pixel shader"; >
{{
	pass {{ ComputeShader = {NAME}_CS<{T}, {T}>; DispatchSizeX = (BUFFER_WIDTH + {T} - 1) / {T}; DispatchSizeY = (BUFFER_HEIGHT + {T} - 1) / {T}; }}
	pass {{ VertexShader = PostProcessVS; PixelShader = {NAME}_PS; }}
}}
"""


CS_SPLIT_BLOCK = """// ---- {NAME}: sigma {SIGMA}, radius {R}. Compute: horizontal pass in groupshared
// memory ({T}x{T} tile + {R} px row halo). Pixel shader: vertical pass ({NV} linear
// taps, accumulated in fp32) fused with the composite.
texture {NAME}_tH {{ Width = BUFFER_WIDTH; Height = BUFFER_HEIGHT; Format = TOPT_FORMAT; }};
storage2D {NAME}_stH {{ Texture = {NAME}_tH; }};
sampler {NAME}_sH {{ Texture = {NAME}_tH; AddressU = MIRROR; AddressV = MIRROR; }};
static const float {NAME}_w[{R1}] = {{ {W} }};
static const float2 {NAME}_v[{NV}] = {{ {V} }};
groupshared float3 {NAME}_tile[{T} * {S}];

void {NAME}_CS(uint3 gid : SV_GroupID, uint3 tid : SV_GroupThreadID)
{{
	const int2 size = int2(BUFFER_WIDTH, BUFFER_HEIGHT);
	const int2 origin = int2(gid.xy) * {T} - int2({R}, 0);
	const uint lin = tid.y * {T} + tid.x;
	for (uint i = lin; i < {S} * {T}; i += {T} * {T})
	{{
		int2 p = origin + int2(i % {S}, i / {S});
		p = max(p, -1 - p);            // mirror addressing
		p = min(p, 2 * size - 1 - p);
		{NAME}_tile[i] = tex2Dfetch(ReShade::BackBuffer, p).rgb;
	}}
	barrier();
	const uint b = tid.y * {S} + tid.x + {R};
	float3 c = {NAME}_w[0] * {NAME}_tile[b];
	[unroll] for (int k = 1; k <= {R}; k++)
		c += {NAME}_w[k] * ({NAME}_tile[b - k] + {NAME}_tile[b + k]);
	const int2 o = int2(gid.xy) * {T} + int2(tid.xy);
	if (all(o < size))
		tex2Dstore({NAME}_stH, o, float4(c, 1.0));
}}

float4 {NAME}_PS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{{
	float3 c = 0.0;
	[unroll] for (int i = 0; i < {NV}; i++)
		c += {NAME}_v[i].y * tex2Dlod({NAME}_sH, float4(uv.x, uv.y + {NAME}_v[i].x * BUFFER_RCP_HEIGHT, 0.0, 0.0)).rgb;
	const float3 o = tex2D(ReShade::BackBuffer, uv).rgb;
	return float4(lerp(o, c, TOPT_Strength), 1.0);
}}

technique {NAME} < ui_tooltip = "Compute horizontal pass + pixel-shader vertical pass fused with the composite, sigma {SIGMA} (r={R})"; >
{{
	pass {{ ComputeShader = {NAME}_CS<{T}, {T}>; DispatchSizeX = (BUFFER_WIDTH + {T} - 1) / {T}; DispatchSizeY = (BUFFER_HEIGHT + {T} - 1) / {T}; }}
	pass {{ VertexShader = PostProcessVS; PixelShader = {NAME}_PS; }}
}}
"""


CS_COMP_BLOCK = (CS_BLOCK
    .replace("// ---- {NAME}: sigma {SIGMA}, radius {R}, {T}x{T} tile",
             "// ---- {NAME}: sigma {SIGMA}, radius {R}, {T}x{T} tile. The compute shader also does the\n"
             "// composite (the original pixel is already in its tile); the pixel shader only copies.")
    .replace("\t\ttex2Dstore({NAME}_stOut, o, float4(c, 1.0));",
             "\t\ttex2Dstore({NAME}_stOut, o, float4(lerp({NAME}_tile[(tid.y + {R}) * {S} + tid.x + {R}], c, TOPT_Strength), 1.0));")
    .replace("""	const float3 o = tex2D(ReShade::BackBuffer, uv).rgb;
	return float4(lerp(o, tex2D({NAME}_sOut, uv).rgb, TOPT_Strength), 1.0);""",
             """	return float4(tex2Dfetch({NAME}_sOut, int2(pos.xy)).rgb, 1.0);""")
    .replace("Compute tile blur sigma {SIGMA} (r={R}) + composite pixel shader",
             "Compute tile blur + composite sigma {SIGMA} (r={R}), pixel shader copy"))


def cs_effect() -> str:
    blocks = []
    for sigma in (1, 2, 4):
        pl = next(p for p in M.cand_sep_linear(sigma)
                  if S.passes_profile(metrics(p, sigma), S.PROFILES["medium"]))
        r, s = pl.params["r"], pl.params["s"]
        w = M.gauss(np.arange(-r, r + 1, dtype=float), s)[r:]
        T = 16
        W = ", ".join(f"{v:.9g}" for v in w)
        blocks.append(CS_BLOCK.format(NAME=f"TOPT_C_Tile_s{sigma}", SIGMA=sigma, R=r, R1=r + 1, T=T, S=T + 2 * r, W=W))
        blocks.append(CS_COMP_BLOCK.format(NAME=f"TOPT_C_TileComp_s{sigma}", SIGMA=sigma, R=r, R1=r + 1, T=T,
                                           S=T + 2 * r, W=W))
        pos = np.arange(-r, r + 1, dtype=float)
        v = M.pair_taps(pos, M.gauss(pos, s))
        blocks.append(CS_SPLIT_BLOCK.format(NAME=f"TOPT_C_SplitHV_s{sigma}", SIGMA=sigma, R=r, R1=r + 1, T=T,
                                            S=T + 2 * r, W=W, NV=len(v),
                                            V=", ".join(f"float2({o:.9g}, {w_:.9g})" for o, w_ in v)))
    return CS_TEMPLATE.replace("{BLOCKS}", "\n".join(blocks))


def main():
    repeat = int(sys.argv[sys.argv.index("--repeat") + 1]) if "--repeat" in sys.argv else 1
    FX.mkdir(exist_ok=True)
    (FX / "TOPT_Bench_Micro.fx").write_text(effect(micro(), repeat))
    (FX / "TOPT_Bench_Blur.fx").write_text(effect(load_winners(ROOT / "results" / "hybrid.json")
                                                  + luma_patterns()
                                                  + pinwheels(ROOT / "results" / "small_kernels.json")
                                                  + classic(), repeat))
    (FX / "TOPT_Bench_CS.fx").write_text(cs_effect())
    csv = FX / "timings_template.csv"
    # TOPT_Blur.fx is timed per TOPT_BLUR_SIZE: keep its hand-written rows
    blur_rows = [r for r in csv.read_text().splitlines() if r.startswith("TOPT_Blur ")] if csv.exists() else []
    rows = ["technique,resolution,gpu_us,notes"]
    for f in sorted(FX.glob("TOPT_Bench_*.fx")):
        names = re.findall(r"^technique (\w+)", f.read_text(), re.M)
        rows += [f"{n},,," for n in names]
        print(f, len(names), "techniques")
    csv.write_text("\n".join(rows + blur_rows) + "\n")


if __name__ == "__main__":
    main()
