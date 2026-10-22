# TexBench / OpBench requests from topt (blur optimizer)

topt's cost model (GTX 1660 profile) is calibrated against TexBench writes,
copies and half-size downsamples. These tests would replace the remaining
guesses. Priority order. All passes are full-screen pixel shaders at
3840x2160 unless stated; report ms per pass (median of several runs).

## P1. Per-pass overhead
Chain of K dependent passes, each reading the previous pass's output:
K = 1, 2, 4, 8, 16, 32. Target sizes 1/64 (480x270) and 1/256 (240x135) of
the screen, RGBA8, 1 point read + write per pixel.
Report: total ms per K. The slope (ms per extra pass) is the overhead
(topt assumes 5 us). Also one variant where consecutive passes alternate
between two render targets (A->B->A) instead of K distinct targets.

## P2. Derivative mode (fine or coarse) per API
Output = ddx(f) and ddy(f) for f = pixel index (x + 1000*y), written as
float. Check the bottom-right pixel of each 2x2 quad: fine derivatives give
values from its own row/column, coarse ones repeat the top row / left column.
Test ddx/ddy and ddx_fine/ddy_fine (ReShade emits plain ddx for SM3/SM4) on
D3D9, D3D10, D3D11, D3D12, OpenGL, Vulkan.
Report per API: fine / coarse for each intrinsic.

## P3. "Free" fetches in a memory-bound pass
One full-screen pass, RGBA8 source (a full-res texture, not the backbuffer)
and RGBA8 target, N bilinear reads per pixel at fractional offsets within
+-3 texels, N = 1, 2, 3, 4, 6, 8, 10, 12, 16, 24.
Report: ms per N. The flat part = fetches hidden behind memory time; the
slope after the knee = cost per fetch. topt assumes the knee at ~7.

## P4. Pass time vs render-target size
Same shader (1 bilinear read of a full-res source with 4 taps averaging a
2x2 block, write RGBA8) into targets of 1/4, 1/16, 1/64, 1/256, 1/1024 of
the screen (source read at the matching stride).
Report: ms per size. Shows where small targets stop scaling (under-utilised
GPU) - decides x8 vs x16 vs x32 downsampling.

## P5. Quad exchange vs a fetch
In a texture-bound pass (16 bilinear reads per pixel), replace 3 of every
4 reads with values obtained from 2x2 quad neighbours:
v_x = v + s*ddx_fine(v), v_y = v + s*ddy_fine(v), v_xy = v_x + s*ddy_fine(v_x)
(s = +1 on even, -1 on odd pixel coordinates), on float3.
Report: ms for 16 reads vs 4 reads + exchange, and fma-unit cost of one
float3 exchange (ddx_fine + ddy_fine + diagonal).

## P6. Noise sources (one 2D random value per pixel, 8 per pixel in a stress variant)
- blue-noise texture lookups (tex2D point, WRAP) at 4^2, 8^2 ... 512^2 texels,
  RG8; at 64^2 also R8, RGBA8 (two values per read), R8 with two packed 4-bit
  values; tex2D vs tex2Dfetch
- static const float2 table[16] indexed by (x&3) + 4*(y&3)
- ALU: interleaved gradient noise, R2 (frac(dot(p, (0.7548777, 0.5698403)))),
  hash without sine (Dave Hoskins)
Report: fma units per lookup. Texture versions: does the size change the
cost (cache)?

## P7. Fetch order
Same 25 bilinear taps (5x5 grid, 2 texels apart) and 81 taps (x16 downsample,
18x18 texels) fetched in row, serpentine, Morton (Z-order), spiral and
random order.
Report: ms per order (check in the ISA that the driver keeps the order).

## P8. Uniform vs divergent branches
Loop over 0..16 taps with [branch] if (i < n): n from a uniform (same for
the whole wave) vs n from the pixel position (varies within the wave).
Report: ms for both, vs the same loop fully unrolled with no branch.

## P9. Compute (lower priority)
Dispatch overhead (chain of K small dispatches, as P1) and groupshared read
rate (fma units per float4 LDS read). Note: a compute pass in ReShade must be
followed by a pixel-shader pass.

## P10. Partial-screen draws (lower priority)
Writing only 25% of the screen (two bands top/bottom) with a heavy shader:
custom vertex shader drawing only the bands (TRIANGLELIST, SV_VertexID) vs
full-screen draw + stencil vs full-screen + discard.
Report: ms for each.

## P11. Scatter rate: blended points (vertex-shader histogram) and splats
Vertex-shader scatter, the no-compute way to build a histogram: POINTLIST,
VertexCount = number of source pixels used, the vertex shader takes its pixel
from SV_VertexID, reads it with tex2Dlod and places the point in its bin;
additive blending (BlendOp ADD, SrcBlend ONE, DestBlend ONE) counts.
Source: a 1920x1080 RGBA8 texture with varied content.

a) Contention: every point to 1 pixel; to 16 bins; to 256 bins (256x1
   target, luma histogram); every point to its own pixel (full-res target,
   no contention).
b) Subsampling: every pixel, every 4th, every 16th (the usual histogram trick).
c) Target format: R32F, R16F, RGBA16F, RGBA8.
d) APIs: D3D9 (vs_3_0 vertex texture fetch: the case without compute),
   D3D11, Vulkan.
e) Reference: the same 256-bin histogram as a compute shader (InterlockedAdd
   in groupshared per thread group, then one atomic add per bin to a global
   buffer), and the same with global atomics only.
f) Splats (bokeh-style scatter): one 2-triangle quad per source pixel of a
   1/8- and a 1/16-size source, quad size 4x4, 8x8, 16x16 pixels, additive
   blending into RGBA16F at full res.

Report: ms per variant, plus points/s (a-e) and blended pixels/s (f). The
point is the blend rate under contention versus the uncontended write rate;
f decides whether scatter-based blur (bokeh) can ever compete with gather.
