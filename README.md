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

| sigma | 1080p winner (medium quality) | 1080p us | 4K us |
|---:|---|---:|---:|
| 1 | single-pass 16-fetch 2D kernel in the composite | 116 | 466 |
| 2-3 | x2 down, small blur, x2 up in the composite | 121-144 | 453-545 |
| 4-8 | one x4 / x8 down pass (wide filter), blur, pinwheel up | 84-110 | 283-393 |
| 12-16 | one x8 down pass, one-pass blur, x8 4-tap pinwheel up | 69-73 | 246-248 |
| 24-200 | one x16 down pass (+ x2/x4), one-pass blur, direct up | 65-70 | 231-234 |

* **Every pass has a free fetch budget** in the model: the first downsample is
  memory-bound (reads the full frame, writes 1/64-1/256 of it), tiny passes are
  overhead-bound and the composite is memory-bound (~7 free taps). So the
  optimizer spends taps on wide single-step x8/x16 downsamples (fewer passes)
  and on free-position "pinwheel" upsamplers in the composite
  (`topt/uptaps.py`: the 4-tap version is ~3x smoother than bilinear), which
  keep the direct x8-x64 upsample from looking blocky.
* **Pinwheel chains and rotation** (`iso` metric, `results/calib/isotropy.png`):
  a 2-pass pinwheel chain whose 2nd pass is rotated 45 degrees is ~23x rounder
  than repeating the same pinwheel; a 3-pass 9-tap chain at the bottom level
  reaches iso 0.002 (exact Gaussian ~0.0002). In the model they cost 8-12 us
  more than the winners at sigma 16 because of the extra passes; they are in
  the benchmark so hardware can decide. A single C4 pinwheel is not round
  (9-fetch sigma-1 pinwheel: iso 0.046, fails the calibrated profiles).
* **Full-res traffic sets the floor.** A 1080p RGB10A2 read is ~55 us on a 1660
  at 80 % of peak bandwidth; passes with fewer than ~6 taps are memory-bound,
  so extra taps there are free. Above sigma ~8 the cost is ~1 full-res read
  plus a few small passes, flat up to sigma 200.
* Compute shaders must be followed by a pixel shader. A compute blur whose
  output the composite reads costs the same as the pixel-shader separable blur
  (~167 us at 1080p, sigma 1-2); doing the composite in the compute shader and
  only copying in the pixel shader is modelled at ~113 us; compute H + pixel V
  fused with the composite wins at sigma ~4 (167 vs 204 us). To be timed.
* Strict quality costs little extra (sigma 16: 96 vs 83 us; sigma >= 64 the same).
* Tiny blurs: a single pass inside the composite with <= ~8 fetches is free
  (the composite is memory-bound). Optimised 4-fold "pinwheel" tap patterns
  (generalising LumaSharpen's "Wider") reach medium quality at sigma 0.8 with 5
  fetches (0 us), 1.0 with 9 (24 us), 1.3 with 13 (77 us); see
  `results/small_kernels.md`.
* Stochastic / interleaved sampling (Vogel, R2, jittered and optimal-transport
  point sets, per-pixel rotation by Bayer index) was a bust without temporal
  accumulation: most variants fail on static pattern noise, and the one that
  passed by eye (sigma 2) is slower than the hybrid (131 vs 121 us). Parked
  for temporal use; see `results/stochastic.md`.
* iq's smoothstep trick hurts blur upsampling (terracing, blockiness).
* RGB10A2 intermediates add <= 0.17 8-bit levels of error on smooth ramps.
  R11G11B10F gives up to 1.1 (R, G) / 2.0 (B) levels on mid/bright ramps:
  banding and hue shift unless dithered, so use it only for HDR (> 1) data.
* FFT and full-res IIR/moving-average methods need >= 2 full-res read+write
  passes, so they cannot beat the hybrid in this sigma range.

## The research effect

`fx/TOPT_Blur.fx` combines the winners into one effect with a size class per
downsample factor, so they can be timed and compared on hardware. It is a test
bed, not a release shader: the plan is to split the best methods into small
reference effects afterwards. See `fx/README.md` for settings and modelled cost.

## Status / next

* Quality profiles in `topt/search.py` are calibrated by eye with
  `scripts/calibrate.py` renders (truncation, blockiness, motion, isotropy,
  noise).
* Next: hardware timing (`fx/README.md`), then refit the cost model (per-pass
  overhead, memory-bound claim) and re-run the searches.
* Open: sigma 2.5-3 and 9-12 cost more than their neighbours (the runtime
  kernel grows in whole 2D pair steps at low resolution); a separable low-res
  blur would make sigma 2.5-6 ~150 us at x2. Temporal stochastic sampling (Movie Night) and extra
  downsample/upsample variants are parked.
