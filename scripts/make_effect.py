"""Generate the shippable blur effect fx/TOPT_Blur.fx from the optimizer's designs.

Structure per size class (downsample factor D): one wide box*binomial
downsample pass (two for D >= 32), one single-pass 2D Gaussian at 1/D
resolution whose width is computed at runtime, and a pinwheel upsample fused
into the composite pass. The runtime Gaussian is emulated here to verify
quality over each class's range.

    python -m scripts.make_effect
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from topt import search as S
from topt.cost import pipeline_cost
from topt.quality import metrics
from topt.sim import Pass, Pipeline

ROOT = Path(__file__).resolve().parent.parent
SL_MIN, SL_MAX = 1.6, 3.4          # low-res sigma range that keeps medium quality (D >= 4)
TRUNC = 2.5                        # low-res kernel radius in low-res sigmas
# name: (down factors, down binomial e, up steps, up filter, lowest low-res sigma for medium quality)
CLASSES = {
    "2": ((2,), 3, (2,), "p4", 0.8),
    "4s": ((4,), 9, (2, 2), "e2", 0.3),   # two-step 2x2 upsample: smooth enough at small sl
    "4": ((4,), 5, (4,), "p5", SL_MIN),
    "8": ((8,), 3, (8,), "p4", SL_MIN),
    "16": ((16,), 3, (16,), "p4", SL_MIN),
    "32": ((16, 2), 9, (32,), "p4", 1.2),
    "64": ((16, 4), 3, (64,), "p4", SL_MIN),
    "128": ((16, 8), 3, (128,), "p4", SL_MIN),
}


def up_taps(name: str) -> tuple:
    kind, n = name[0], int(name[1:])
    return tuple(S.UP_PIN[n]) if kind == "p" else S.outer(S.up_taps_1d(n))


def runtime_bottom(sl: float, rmax: int) -> tuple:
    """The shader's low-res kernel: Gaussian(sl) over -r..r, r = min(rmax, ceil(TRUNC*sl)),
    centre tap + symmetric pairs merged into bilinear taps, 2D outer product."""
    r = min(rmax, max(1, math.ceil(TRUNC * sl)))
    g = lambda i: math.exp(-0.5 * (i / sl) ** 2) if i <= r else 0.0
    t1 = [(0.0, g(0))]
    for i in range(1, r + 1, 2):
        a, b = g(i), g(i + 1)
        o = i + b / (a + b)
        t1 += [(o, a + b), (-o, a + b)]
    tot = sum(w for _, w in t1)
    t1 = [(o, w / tot) for o, w in t1]
    return tuple((ox, oy, wx * wy) for ox, wx in t1 for oy, wy in t1)


def pipeline(name: str, sl: float, rmax: int) -> Pipeline:
    down, e, ups, upf, _ = CLASSES[name]
    passes, div = [], 1
    for f in down:
        div *= f
        passes.append(Pass(div, S.outer(S.down_taps_1d(f, e))))
    passes.append(Pass(div, runtime_bottom(sl, rmax)))
    for u in ups:
        div //= u
        passes.append(Pass(div, up_taps(upf)))
    return Pipeline("TOPT_Blur", {"class": name, "sl": sl}, passes)


def chain_variance(name: str) -> tuple:
    """Blur (full-res px^2) added by the down/up chain alone: sigma^2 = C + B sl^2."""
    rmax = math.ceil(TRUNC * SL_MAX)
    s1, s2 = 1.6, 3.0
    g1 = metrics(pipeline(name, s1, rmax))["sigma"] ** 2
    g2 = metrics(pipeline(name, s2, rmax))["sigma"] ** 2
    b = (g2 - g1) / (s2 * s2 - s1 * s1)
    return g1 - b * s1 * s1, b


def _f(v: float) -> str:
    s = f"{v:.9g}"
    return s if any(c in s for c in ".e") else s + ".0"


def main():
    rmax = math.ceil(TRUNC * SL_MAX)
    info = {}
    for name, (down, e, ups, upf, lo) in CLASSES.items():
        C, b = chain_variance(name)
        hi = SL_MAX if name != "4s" else 1.6
        smin, smax = math.sqrt(C + b * lo * lo), math.sqrt(C + b * hi * hi)
        checks = []
        for sl in np.linspace(lo, hi, 4):
            pl = pipeline(name, float(sl), rmax)
            q = metrics(pl)
            ok = [n for n, p in S.PROFILES.items()
                  if S.passes_profile({**q, "sigma_err": 0.0}, p) and q["block"] <= S.NOISE_BLOCK_MAX]
            checks.append((round(q["sigma"], 1), "/".join(ok) or "FAIL", round(pipeline_cost(pl)["us"])))
        info[name] = (C, b, lo, hi, smin, smax, checks)
        print(f"{name:>4}: C={C:8.2f} B={b:8.1f} sigma {smin:6.1f}..{smax:6.1f}  {checks}", flush=True)
    # cheapest valid class for every integer screen sigma
    choice = []
    for sig in range(2, 441):
        best = None
        for name, (C, b, lo, hi, smin, smax, _) in info.items():
            if not smin - 0.5 <= sig <= smax + 0.5:
                continue
            sl = min(hi, max(lo, math.sqrt(max(sig * sig - C, 0.0) / b)))
            us = pipeline_cost(pipeline(name, sl, rmax))["us"]
            if best is None or us < best[1]:
                best = (name, us)
        choice.append((sig, best[0] if best else choice[-1][1] if choice else "2"))
    intervals = []
    for sig, name in choice:
        if intervals and intervals[-1][2] == name:
            intervals[-1][1] = sig
        else:
            intervals.append([sig, sig, name])
    print("selection:", [(a, b, n) for a, b, n in intervals])
    (ROOT / "fx" / "TOPT_Blur.fx").write_text(render(info, intervals, rmax))
    print("wrote fx/TOPT_Blur.fx")


def render(info: dict, intervals: list, rmax: int) -> str:
    ids = {n: i for i, n in enumerate(CLASSES)}
    sel = []
    for i, (a, b, name) in enumerate(intervals):
        cond = "#if" if i == 0 else "#elif"
        if i < len(intervals) - 1:
            sel.append(f"{cond} TOPT_SIGMA_SCREEN <= {b}\n\t#define TOPT_CLASS {ids[name]} // '{name}'")
        else:
            sel.append(f"#else\n\t#define TOPT_CLASS {ids[name]} // '{name}'")
    sel.append("#endif")
    blocks = []
    for i, (name, (down, e, ups, upf, lo)) in enumerate(CLASSES.items()):
        C, b, lo, hi, smin, smax, _ = info[name]
        taps = [S.outer(S.down_taps_1d(f, e)) for f in down]
        up = up_taps(upf)
        arr = lambda nm, t: (f"\tstatic const float3 {nm}[{len(t)}] = {{\n\t\t" +
                             ",\n\t\t".join(f"float3({_f(x)}, {_f(y)}, {_f(w)})" for x, y, w in t) + "\n\t};")
        lines = [f"{'#if' if i == 0 else '#elif'} TOPT_CLASS == {i} // '{name}': sigma {smin:.1f}..{smax:.1f} px",
                 f"\t#define TOPT_STEPS {len(down)}",
                 f"\t#define TOPT_F1 {down[0]}",
                 f"\t#define TOPT_F2 {down[1] if len(down) > 1 else 1}",
                 f"\t#define TOPT_UPSTEPS {len(ups)}",
                 f"\tstatic const float TOPT_C = {_f(C)};  // chain variance (px^2): sigma^2 = C + B * sl^2",
                 f"\tstatic const float TOPT_B = {_f(b)};",
                 f"\tstatic const float TOPT_SL_MIN = {_f(lo)};",
                 f"\tstatic const float TOPT_SL_MAX = {_f(hi)};",
                 f"\t#define TOPT_ND1 {len(taps[0])}", arr("TOPT_DOWN1", taps[0])]
        if len(down) > 1:
            lines += [f"\t#define TOPT_ND2 {len(taps[1])}", arr("TOPT_DOWN2", taps[1])]
        lines += [f"\t#define TOPT_NUP {len(up)}", arr("TOPT_UP", up)]
        blocks.append("\n".join(lines))
    blocks.append("#endif")
    return TEMPLATE.replace("{SELECT}", "\n".join(sel)).replace("{CLASSES}", "\n".join(blocks)) \
        .replace("{RMAX}", str(rmax)).replace("{TRUNC}", _f(TRUNC))


TEMPLATE = r"""/*------------------.
| :: TOPT Blur ::   |
'------------------*/
/*
  Fast Gaussian-like blur, generated by the topt texture-sample optimizer.

  One wide downsample pass (two for very large blurs), one Gaussian pass at
  low resolution whose width is computed at runtime, and a smooth "pinwheel"
  upsample fused into the final pass. Cost is nearly independent of the blur
  size above sigma ~8.

  Use it as is, or call TOPT_BlurResolve(uv) from your own final pass after
  running the TOPT_Down / TOPT_Blur passes.
*/

#include "ReShade.fxh"

#ifndef TOPT_BLUR_SIZE
	#define TOPT_BLUR_SIZE 16 // blur sigma in pixels at 1080p (integer, 2..200); scales with resolution
#endif
#ifndef TOPT_BLUR_FORMAT
	#define TOPT_BLUR_FORMAT RGB10A2 // intermediate format; R11G11B10F keeps HDR (> 1) values
#endif

#define TOPT_SIGMA_SCREEN (TOPT_BLUR_SIZE * BUFFER_HEIGHT / 1080)

uniform float TOPT_SizeTune <
	ui_type = "slider"; ui_min = 0.75; ui_max = 1.33;
	ui_label = "Size fine-tune";
	ui_tooltip = "Multiplies the blur size set by TOPT_BLUR_SIZE.\nThe usable range of each size class is limited; the blur stops growing at its edges.";
> = 1.0;

uniform float TOPT_Strength <
	ui_type = "slider"; ui_min = 0.0; ui_max = 1.0;
	ui_label = "Strength";
> = 1.0;

uniform bool TOPT_ShowBlur <
	ui_label = "Show blur only";
> = false;

// ---- size class (chosen at compile time from the blur size and the resolution)
{SELECT}

{CLASSES}

#define TOPT_RMAX {RMAX}   // low-res kernel radius limit (texels)
#define TOPT_NP ((TOPT_RMAX + 1) / 2) // max merged pairs per side

#define TOPT_DIV1 TOPT_F1
#define TOPT_DIV2 (TOPT_F1 * TOPT_F2)

texture TOPT_tDown1 { Width = BUFFER_WIDTH / TOPT_DIV1; Height = BUFFER_HEIGHT / TOPT_DIV1; Format = TOPT_BLUR_FORMAT; };
sampler TOPT_sDown1 { Texture = TOPT_tDown1; AddressU = MIRROR; AddressV = MIRROR; };
#if TOPT_STEPS > 1
texture TOPT_tDown2 { Width = BUFFER_WIDTH / TOPT_DIV2; Height = BUFFER_HEIGHT / TOPT_DIV2; Format = TOPT_BLUR_FORMAT; };
sampler TOPT_sDown2 { Texture = TOPT_tDown2; AddressU = MIRROR; AddressV = MIRROR; };
	#define TOPT_sLow TOPT_sDown2
	#define TOPT_DIVL TOPT_DIV2
#else
	#define TOPT_sLow TOPT_sDown1
	#define TOPT_DIVL TOPT_DIV1
#endif
texture TOPT_tBlur { Width = BUFFER_WIDTH / TOPT_DIVL; Height = BUFFER_HEIGHT / TOPT_DIVL; Format = TOPT_BLUR_FORMAT; };
sampler TOPT_sBlur { Texture = TOPT_tBlur; AddressU = MIRROR; AddressV = MIRROR; };
#if TOPT_UPSTEPS > 1 // intermediate x2 upsample to 1/(DIVL/2) resolution
	#define TOPT_DIVU (TOPT_DIVL / 2)
texture TOPT_tUp { Width = BUFFER_WIDTH / TOPT_DIVU; Height = BUFFER_HEIGHT / TOPT_DIVU; Format = TOPT_BLUR_FORMAT; };
sampler TOPT_sUp { Texture = TOPT_tUp; AddressU = MIRROR; AddressV = MIRROR; };
	#define TOPT_sFinal TOPT_sUp
	#define TOPT_DIVF TOPT_DIVU
#else
	#define TOPT_sFinal TOPT_sBlur
	#define TOPT_DIVF TOPT_DIVL
#endif
sampler TOPT_sBackBuffer { Texture = ReShade::BackBufferTex; AddressU = MIRROR; AddressV = MIRROR; };

float4 TOPT_Down1PS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	const float2 px = BUFFER_PIXEL_SIZE;
	float3 c = 0.0;
	[unroll] for (int i = 0; i < TOPT_ND1; i++)
		c += TOPT_DOWN1[i].z * tex2Dlod(TOPT_sBackBuffer, float4(uv + TOPT_DOWN1[i].xy * px, 0.0, 0.0)).rgb;
	return float4(c, 1.0);
}

#if TOPT_STEPS > 1
float4 TOPT_Down2PS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	const float2 px = 1.0 / float2(BUFFER_WIDTH / TOPT_DIV1, BUFFER_HEIGHT / TOPT_DIV1);
	float3 c = 0.0;
	[unroll] for (int i = 0; i < TOPT_ND2; i++)
		c += TOPT_DOWN2[i].z * tex2Dlod(TOPT_sDown1, float4(uv + TOPT_DOWN2[i].xy * px, 0.0, 0.0)).rgb;
	return float4(c, 1.0);
}
#endif

// Low-res Gaussian: width from the requested blur size, pairs of texels merged
// into one bilinear fetch, 2D (outer product) in a single pass.
float4 TOPT_BlurPS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	const float2 px = 1.0 / float2(BUFFER_WIDTH / TOPT_DIVL, BUFFER_HEIGHT / TOPT_DIVL);
	const float sigma = TOPT_BLUR_SIZE * TOPT_SizeTune * BUFFER_HEIGHT / 1080.0;
	const float sl = clamp(sqrt(max(sigma * sigma - TOPT_C, 0.0) / TOPT_B), TOPT_SL_MIN, TOPT_SL_MAX);
	const int r = min(TOPT_RMAX, (int)ceil({TRUNC} * sl));
	const float k = -0.5 / (sl * sl);

	// 1D taps: centre + symmetric pairs of texels merged into one bilinear fetch
	// t[m] = (offset, weight) of pair m (texels 2m-1, 2m); only np pairs are used.
	const int np = (r + 1) / 2;
	float2 t[TOPT_NP + 1];
	t[0] = float2(0.0, 1.0);
	float wsum = 1.0;
	[unroll] for (int m = 1; m <= TOPT_NP; m++)
	{
		const float j = 2 * m - 1;
		const float a = exp(k * j * j);
		const float b = j + 1.0 <= r ? exp(k * (j + 1.0) * (j + 1.0)) : 0.0;
		t[m] = float2(j + b / (a + b), a + b);
		wsum += m <= np ? 2.0 * (a + b) : 0.0;
	}

	// np is the same for every pixel, so these branches never diverge
	float3 c = 0.0;
	[unroll] for (int y = -TOPT_NP; y <= TOPT_NP; y++)
	{
		[branch] if (abs(y) <= np)
		{
			const float2 ty = t[abs(y)];
			[unroll] for (int x = -TOPT_NP; x <= TOPT_NP; x++)
			{
				[branch] if (abs(x) <= np)
				{
					const float2 tx = t[abs(x)];
					const float2 o = float2(x < 0 ? -tx.x : tx.x, y < 0 ? -ty.x : ty.x);
					c += tx.y * ty.y * tex2Dlod(TOPT_sLow, float4(uv + o * px, 0.0, 0.0)).rgb;
				}
			}
		}
	}
	return float4(c / (wsum * wsum), 1.0);
}

#if TOPT_UPSTEPS > 1
float4 TOPT_UpPS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	const float2 px = 1.0 / float2(BUFFER_WIDTH / TOPT_DIVL, BUFFER_HEIGHT / TOPT_DIVL);
	float3 c = 0.0;
	[unroll] for (int i = 0; i < TOPT_NUP; i++)
		c += TOPT_UP[i].z * tex2Dlod(TOPT_sBlur, float4(uv + TOPT_UP[i].xy * px, 0.0, 0.0)).rgb;
	return float4(c, 1.0);
}
#endif

// The blurred image at uv (full resolution): smooth upsample of the low-res
// blur. Call this from your own composite pass.
float3 TOPT_BlurResolve(float2 uv)
{
	const float2 px = 1.0 / float2(BUFFER_WIDTH / TOPT_DIVF, BUFFER_HEIGHT / TOPT_DIVF);
	float3 c = 0.0;
	[unroll] for (int i = 0; i < TOPT_NUP; i++)
		c += TOPT_UP[i].z * tex2Dlod(TOPT_sFinal, float4(uv + TOPT_UP[i].xy * px, 0.0, 0.0)).rgb;
	return c;
}

float4 TOPT_CompositePS(float4 pos : SV_Position, float2 uv : TEXCOORD) : SV_Target
{
	const float3 blur = TOPT_BlurResolve(uv);
	if (TOPT_ShowBlur)
		return float4(blur, 1.0);
	const float3 o = tex2D(ReShade::BackBuffer, uv).rgb;
	return float4(lerp(o, blur, TOPT_Strength), 1.0);
}

technique TOPT_Blur < ui_tooltip = "Fast Gaussian-like blur (topt).\nSet the size with the TOPT_BLUR_SIZE preprocessor definition (sigma in pixels at 1080p)."; >
{
	pass Down1 { VertexShader = PostProcessVS; PixelShader = TOPT_Down1PS; RenderTarget = TOPT_tDown1; }
#if TOPT_STEPS > 1
	pass Down2 { VertexShader = PostProcessVS; PixelShader = TOPT_Down2PS; RenderTarget = TOPT_tDown2; }
#endif
	pass Blur { VertexShader = PostProcessVS; PixelShader = TOPT_BlurPS; RenderTarget = TOPT_tBlur; }
#if TOPT_UPSTEPS > 1
	pass Up { VertexShader = PostProcessVS; PixelShader = TOPT_UpPS; RenderTarget = TOPT_tUp; }
#endif
	pass Composite { VertexShader = PostProcessVS; PixelShader = TOPT_CompositePS; }
}
"""


if __name__ == "__main__":
    main()
