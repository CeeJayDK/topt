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

## Status / next

* Quality limits in `scripts/baseline.py` are provisional and need to be
  calibrated by eye.
* Planned: generic search over pass sequences, compute-shader (groupshared)
  cost model, stochastic methods, FFT for the largest radii, and `.fx`
  generators for hardware timing.
