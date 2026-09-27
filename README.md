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

See `results/analysis.md` (winners), `results/hybrid.md`, `results/baseline.md`.

* **Full-res traffic sets the floor.** One 1080p RGB10A2 read + write is ~110 us
  on a 1660 at 80 % of peak bandwidth; a full-res pass with fewer than ~6 taps is
  memory-bound, so extra taps there are free.
* **sigma 1-3:** a single compute dispatch (tile + halo in groupshared, separable
  kernel in LDS) is estimated at ~113-126 us vs ~205-226 us for the best
  pixel-shader methods (two full-res passes).
* **sigma >= 4:** a hybrid wins: one pass reads full res once and goes straight
  to 1/4 with a wide box*binomial filter (free, memory-bound), optional further
  x2/x4 steps, a small fitted blur at the bottom, and a bilinear upsample.
  Cost is ~140 us and nearly flat from sigma 16 to 200, vs ~180-215 us for the
  best classic pyramid / dual filter at the same quality.
* Strict quality costs little extra (e.g. sigma 16: 155 vs 142 us; sigma >= 48
  about the same).
* iq's smoothstep trick hurts blur upsampling (terracing, blockiness).
* Storing every pass as RGB10A2 adds <= 1.4 LSB (10-bit) error, ~0.35 LSB RMS.
* FFT and full-res IIR/moving-average methods need >= 2 full-res read+write
  passes (>= ~220 us), so they cannot beat the hybrid in this sigma range.

## Status / next

* Quality profiles in `topt/search.py` are calibrated by eye with
  `scripts/calibrate.py` renders (truncation, blockiness, motion).
* The per-pass overhead (5 us) and the memory-bound claim need hardware timing.
* Planned: generic search over pass sequences, compute-shader (groupshared)
  cost model, stochastic methods, FFT for the largest radii, and `.fx`
  generators for hardware timing.
