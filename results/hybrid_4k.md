# Hybrid down/blur/up search (GTX 1660 model, 3840x2160, RGB10A2)

us = marginal cost over a plain composite pass (the last pass is the composite).

Profiles: **strict** leak<=0.01, tv<=0.02, curv<=0.2, block<=0.1, aniso<=0.03, phase<=0.01, sigma_err<=0.02; **medium** leak<=0.015, tv<=0.055, curv<=0.7, block<=0.35, aniso<=0.03, phase<=0.1, sigma_err<=0.02; **loose** leak<=0.02, tv<=0.1, curv<=1.7, block<=0.45, aniso<=0.05, phase<=0.15, sigma_err<=0.03

## Cheapest design per profile

| sigma | profile | us | passes | leak | tv | phase | curv | design | best baseline |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| 2 | strict | | | | | | | none found | none |
| 2 | medium | 484 | 3 | 0.005 | 0.024 | 0.022 | 0.38 | down 2 e3 | direct 2s | up 2 e3 | sep_linear 653 us |
| 2 | loose | 453 | 3 | 0.012 | 0.008 | 0.023 | 0.38 | down 2 e3 | direct 2s | up 2 e1 | sep_linear 653 us |
| 3 | strict | | | | | | | none found | none |
| 3 | medium | 545 | 3 | 0.009 | 0.037 | 0.092 | 0.38 | down 2 e1 | direct 2s | up 2 e1 | pyramid 555 us |
| 3 | loose | 545 | 3 | 0.009 | 0.037 | 0.092 | 0.38 | down 2 e1 | direct 2s | up 2 e1 | pyramid 555 us |
| 4 | strict | | | | | | | none found | none |
| 4 | medium | 396 | 4 | 0.005 | 0.012 | 0.047 | 0.30 | down 4 e5 | direct 2s | up 2x2 e2 | dual_filter 512 us |
| 4 | loose | 396 | 4 | 0.005 | 0.011 | 0.075 | 0.30 | down 4 e3 | direct 2s | up 2x2 e2 | dual_filter 512 us |
| 6 | strict | | | | | | | none found | none |
| 6 | medium | 419 | 4 | 0.008 | 0.027 | 0.045 | 0.31 | down 4 e3 | direct 2s | up 2x2 e1 | pyramid 577 us |
| 6 | loose | 419 | 4 | 0.008 | 0.030 | 0.111 | 0.34 | down 4 e1 | direct 2s | up 2x2 e1 | pyramid 577 us |
| 8 | strict | 538 | 6 | 0.007 | 0.010 | 0.001 | 0.07 | down 2x2 e3 | sep 2.5s | up 2x2 e2 | none |
| 8 | medium | 312 | 4 | 0.005 | 0.050 | 0.033 | 0.48 | down 4 e3 | sep 2s | up 4 e2 | pyramid 538 us |
| 8 | loose | 312 | 4 | 0.006 | 0.053 | 0.081 | 0.52 | down 4 e1 | sep 2s | up 4 e2 | pyramid 538 us |
| 12 | strict | 425 | 5 | 0.009 | 0.020 | 0.002 | 0.14 | down 2x2 e3 | sep 2.5s | up 4 e1 | none |
| 12 | medium | 312 | 4 | 0.010 | 0.022 | 0.055 | 0.17 | down 4 e1 | sep 2.5s | up 4 e1 | pyramid 430 us |
| 12 | loose | 312 | 4 | 0.010 | 0.022 | 0.055 | 0.17 | down 4 e1 | sep 2.5s | up 4 e1 | pyramid 430 us |
| 16 | strict | 337 | 4 | 0.008 | 0.010 | 0.008 | 0.07 | down 4 e5 | sep 3s | up 4 e1 | none |
| 16 | medium | 283 | 5 | 0.003 | 0.044 | 0.017 | 0.40 | down 4x2 e3 | sep 2s | up 8 e2 | pyramid 450 us |
| 16 | loose | 283 | 5 | 0.008 | 0.015 | 0.096 | 0.26 | down 4x2 e1 | sep 2.5s | up 8 e2 | pyramid 450 us |
| 24 | strict | 283 | 5 | 0.007 | 0.018 | 0.006 | 0.13 | down 4x2 e5 | sep 2.5s | up 8 e1 | none |
| 24 | medium | 283 | 5 | 0.008 | 0.021 | 0.063 | 0.23 | down 4x2 e1 | sep 2.5s | up 8 e1 | pyramid 398 us |
| 24 | loose | 283 | 5 | 0.008 | 0.021 | 0.063 | 0.23 | down 4x2 e1 | sep 2.5s | up 8 e1 | pyramid 398 us |
| 32 | strict | 290 | 5 | 0.006 | 0.010 | 0.008 | 0.06 | down 4x2 e3 | sep 3s | up 8 e1 | none |
| 32 | medium | 265 | 4 | 0.010 | 0.053 | 0.013 | 0.50 | down 4x4 e5 | direct 2s | up 16 e1 | pyramid 403 us |
| 32 | loose | 265 | 4 | 0.007 | 0.039 | 0.100 | 0.39 | down 4x4 e1 | direct 2s | up 16 e2 | pyramid 403 us |
| 48 | strict | 268 | 5 | 0.006 | 0.017 | 0.007 | 0.14 | down 4x4 e5 | sep 2.5s | up 16 e2 | none |
| 48 | medium | 268 | 5 | 0.007 | 0.021 | 0.067 | 0.19 | down 4x4 e1 | sep 2.5s | up 16 e1 | pyramid 393 us |
| 48 | loose | 268 | 5 | 0.007 | 0.021 | 0.067 | 0.19 | down 4x4 e1 | sep 2.5s | up 16 e1 | pyramid 393 us |
| 64 | strict | 270 | 5 | 0.010 | 0.010 | 0.005 | 0.07 | down 4x4 e5 | sep 3s | up 16 e1 | none |
| 64 | medium | 266 | 5 | 0.009 | 0.048 | 0.013 | 0.43 | down 4x4x2 e3 | direct 2s | up 32 e1 | pyramid 394 us |
| 64 | loose | 266 | 5 | 0.006 | 0.039 | 0.103 | 0.37 | down 4x4x2 e1 | direct 2s | up 32 e2 | pyramid 394 us |
| 100 | strict | 269 | 5 | 0.005 | 0.018 | 0.008 | 0.13 | down 4x4x2 e3 | direct 2.5s | up 32 e2 | none |
| 100 | medium | 268 | 5 | 0.007 | 0.043 | 0.065 | 0.39 | down 4x4x2 e1 | direct 2s | up 32 e2 | pyramid 396 us |
| 100 | loose | 268 | 5 | 0.019 | 0.081 | 0.004 | 0.74 | down 4x4x2 e5 | direct 2s | up 32 e2 | pyramid 396 us |
| 150 | strict | 272 | 6 | 0.008 | 0.011 | 0.005 | 0.08 | down 4x4x2 e3 | sep 3s | up 32 e1 | none |
| 150 | medium | 265 | 5 | 0.012 | 0.049 | 0.013 | 0.48 | down 4x4x4 e3 | direct 2s | up 64 e1 | pyramid 396 us |
| 150 | loose | 265 | 5 | 0.008 | 0.038 | 0.089 | 0.37 | down 4x4x4 e1 | direct 2s | up 64 e2 | pyramid 396 us |
| 200 | strict | 266 | 5 | 0.006 | 0.019 | 0.009 | 0.14 | down 4x4x4 e3 | direct 2.5s | up 64 e2 | none |
| 200 | medium | 266 | 5 | 0.010 | 0.043 | 0.066 | 0.39 | down 4x4x4 e1 | direct 2s | up 64 e2 | pyramid 397 us |
| 200 | loose | 266 | 5 | 0.012 | 0.050 | 0.066 | 0.57 | down 4x4x4 e1 | direct 2s | up 64 e1 | pyramid 397 us |

## Cost vs shift-variance Pareto front (candidates also meeting the other 'medium' limits)

**sigma 2**: 484 us / phase 0.022 (down 2 e3 | direct 2s | up 2 e3), 555 us / phase 0.017 (down 2 e5 | sep 3s | up 2 e1)

**sigma 3**: 545 us / phase 0.005 (down 2 e5 | direct 2s | up 2 e1), 555 us / phase 0.005 (down 2 e5 | sep 2s | up 2 e1)

**sigma 4**: 396 us / phase 0.047 (down 4 e5 | direct 2s | up 2x2 e2), 506 us / phase 0.008 (down 2x2 e5 | direct 2s | up 2x2 e2), 555 us / phase 0.002 (down 2 e5 | sep 2s | up 2 e2), 664 us / phase 0.002 (down 2 e5 | direct 2s | up 2 e2)

**sigma 6**: 419 us / phase 0.025 (down 4 e5 | direct 2s | up 2x2 e2), 425 us / phase 0.025 (down 4 e5 | sep 2s | up 2x2 e1), 532 us / phase 0.001 (down 2x2 e5 | direct 2s | up 2x2 e2), 538 us / phase 0.001 (down 2x2 e5 | sep 2s | up 2x2 e2), 555 us / phase 0.001 (down 2 e5 | sep 2.5s | up 2 e2)

**sigma 8**: 312 us / phase 0.018 (down 4 e5 | sep 2.5s | up 4 e2), 416 us / phase 0.018 (down 4x2 e5 | direct 2s | up 2x2x2 e2), 425 us / phase 0.017 (down 4 e5 | sep 2s | up 2x2 e2), 425 us / phase 0.005 (down 2x2 e5 | sep 2s | up 4 e1), 538 us / phase 0.000 (down 2x2 e5 | sep 2s | up 2x2 e2)

**sigma 12**: 312 us / phase 0.011 (down 4 e5 | sep 2.5s | up 4 e2), 395 us / phase 0.011 (down 4 e5 | sep 2.5s | up 4 e3), 423 us / phase 0.011 (down 4x2 e5 | direct 2s | up 2x2x2 e2), 425 us / phase 0.002 (down 2x2 e5 | sep 2.5s | up 4 e1)

**sigma 16**: 283 us / phase 0.010 (down 4x2 e5 | sep 2s | up 8 e2), 324 us / phase 0.008 (down 4 e5 | sep 2.5s | up 4 e2)

**sigma 24**: 283 us / phase 0.006 (down 4x2 e5 | sep 2.5s | up 8 e1)

**sigma 32**: 265 us / phase 0.012 (down 4x4 e5 | direct 2s | up 16 e2), 277 us / phase 0.007 (down 4x2x2 e5 | direct 2s | up 16 e1), 286 us / phase 0.004 (down 4x2 e5 | sep 2.5s | up 8 e2)

**sigma 48**: 268 us / phase 0.007 (down 4x4 e5 | sep 2.5s | up 16 e2)

**sigma 64**: 266 us / phase 0.007 (down 4x4x2 e5 | direct 2s | up 32 e2), 269 us / phase 0.005 (down 4x4 e5 | sep 2.5s | up 16 e2)

**sigma 100**: 268 us / phase 0.065 (down 4x4x2 e1 | direct 2s | up 32 e2), 268 us / phase 0.004 (down 4x4x2 e5 | direct 2s | up 32 e1), 269 us / phase 0.004 (down 4x4x2 e5 | direct 2.5s | up 32 e2), 271 us / phase 0.004 (down 4x4x2 e5 | sep 2.5s | up 32 e2), 271 us / phase 0.003 (down 4x4 e5 | sep 2.5s | up 16 e2)

**sigma 150**: 265 us / phase 0.007 (down 4x4x4 e5 | direct 2s | up 64 e2), 270 us / phase 0.007 (down 4x4x4 e5 | sep 2s | up 64 e2), 271 us / phase 0.002 (down 4x4x2 e5 | sep 2.5s | up 32 e2), 275 us / phase 0.002 (down 4x4 e5 | sep 2.5s | up 16 e2), 277 us / phase 0.002 (down 4x4 e5 | sep 3s | up 16 e2)

**sigma 200**: 266 us / phase 0.066 (down 4x4x4 e1 | direct 2s | up 64 e2), 266 us / phase 0.004 (down 4x4x4 e5 | direct 2s | up 64 e2), 270 us / phase 0.004 (down 4x4x4 e5 | sep 2s | up 64 e2)

