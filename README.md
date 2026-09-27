# topt — texture-sample optimizer

A search tool for the cheapest way to build GPU post-process filters out of
hardware bilinear fetches. First target: Gaussian(-like) blur for ReShade,
sigma 1–200 px at 1920x1080, RGB10A2 buffers, GTX 1660 as the reference GPU.

## How it works

* **Simulator** (`topt/sim.py`): exact linear model of multi-pass pipelines.
  Each pass renders a target at `full // div` and each tap is one bilinear
  fetch at an offset in source texels. Addressing is MIRROR (clamping would
  vignette). Sampling is done with sparse matrices, so it is exact and fast.
* **Cost model** (`topt/cost.py`): per pass `overhead + max(TMU, DRAM, ROP)`.
  At 1080p a full-res RGB10A2 pass moves ~16.6 MB (read + write), about 90 us
  on a 1660, so up to ~6 taps per pixel are "free" and full-res passes are what
  cost. The per-pass overhead (5 us) is a placeholder until measured.
* **Quality** (`topt/quality.py`): impulse responses at several phases of the
  coarsest grid, compared to a Gaussian of the same sigma:
  `leak` (stop-band sidelobes: truncation/boxiness), `tv` (shape distance),
  `aniso` (x/y/diagonal variance ratio), `phase` (shift variance: blockiness
  and shimmer from down/up-sampling).
* **Methods** (`topt/methods.py`): direct single pass, separable linear,
  separable 2xN bilinear (Day 2012 / CeeJay), Kawase, dual filter (Bjørge
  2015), and down/blur/up pyramids (optionally with iq's smoothstep upsample).
  Each is fitted to hit the target sigma exactly.

## Usage

    pip install -r requirements.txt
    python -m pytest -q tests
    python -m scripts.baseline            # or: python -m scripts.baseline 4 16 64

Results go to `results/baseline.md`.

## Findings so far (model estimates, not yet timed on hardware)

Target: the blur feeds the final composite pass (reads the backbuffer, writes
the screen); costs are the marginal cost over a plain composite pass.
See `results/analysis.md` / `results/analysis_4k.md` (winners), `results/hybrid*.md`.

| sigma | 1080p winner | 1080p us | 4K us |
|---:|---|---:|---:|
| 1 | single-pass 2D fused into the composite | 116 | 466 |
| 2-3 | x2 down, small blur, x2 up in the composite | 129-144 | 484-545 |
| 4-6 | x4 down (wide filter), blur, 2x2 up | 110-116 | 396-419 |
| 8-12 | x4 down, blur, x4 up in the composite | 89 | 312 |
| 16-200 | x4 x2..x4 down, one-pass blur, one direct up in the composite | 77-86 | 265-283 |

* **Full-res traffic sets the floor.** A 1080p RGB10A2 read is ~55 us on a 1660
  at 80 % of peak bandwidth; passes with fewer than ~6 taps are memory-bound,
  so extra taps there are free. Above sigma ~8 the cost is ~1 full-res read
  plus a few small passes, flat up to sigma 200.
* Compute shaders must be followed by a pixel shader. A compute blur whose
  output the composite reads costs the same as the pixel-shader separable blur
  (~167 us at 1080p, sigma 1-2); doing the composite in the compute shader and
  only copying in the pixel shader is modelled at ~113 us; compute H + pixel V
  fused with the composite wins at sigma ~4 (167 vs 204 us). To be timed.
* Strict quality costs little extra (e.g. sigma 16: 155 vs 142 us; sigma >= 48
  about the same).
* iq's smoothstep trick hurts blur upsampling (terracing, blockiness).
* RGB10A2 intermediates add <= 0.17 8-bit levels of error on smooth ramps.
  R11G11B10F gives up to 1.1 (R, G) / 2.0 (B) levels on mid/bright ramps:
  banding and hue shift unless dithered, so use it only for HDR (> 1) data.
* FFT and full-res IIR/moving-average methods need >= 2 full-res read+write
  passes, so they cannot beat the hybrid in this sigma range.

## Status / next

* Quality profiles in `topt/search.py` are calibrated by eye with
  `scripts/calibrate.py` renders (truncation, blockiness, motion).
* The per-pass overhead (5 us) and the memory-bound claim need hardware timing:
  see `fx/README.md`.
* Planned: generic search over pass sequences, compute-shader (groupshared)
  cost model, stochastic methods, FFT for the largest radii, and `.fx`
  generators for hardware timing.
