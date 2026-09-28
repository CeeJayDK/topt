# Hybrid down/blur/up search (GTX 1660 model, 3840x2160, RGB10A2)

us = marginal cost over a plain composite pass (the last pass is the composite).

Profiles: **strict** leak<=0.01, tv<=0.02, curv<=0.2, block<=0.1, aniso<=0.03, phase<=0.01, iso<=0.01, sigma_err<=0.02; **medium** leak<=0.012, tv<=0.032, curv<=0.4, block<=0.35, aniso<=0.03, phase<=0.1, iso<=0.032, sigma_err<=0.02; **loose** leak<=0.015, tv<=0.055, curv<=0.7, block<=0.45, aniso<=0.05, phase<=0.15, iso<=0.04, sigma_err<=0.03

## Cheapest design per profile

| sigma | profile | us | passes | leak | tv | phase | curv | design | best baseline |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| 2 | strict | | | | | | | none found | none |
| 2 | medium | 453 | 3 | 0.012 | 0.008 | 0.023 | 0.35 | down 2 e3 | direct 2s | up 2 p4 | none |
| 2 | loose | 453 | 3 | 0.012 | 0.008 | 0.023 | 0.38 | down 2 e3 | direct 2s | up 2 e1 | none |
| 3 | strict | | | | | | | none found | none |
| 3 | medium | 545 | 3 | 0.006 | 0.021 | 0.093 | 0.25 | down 2 e1 | direct 2s | up 2 e2 | none |
| 3 | loose | 545 | 3 | 0.009 | 0.037 | 0.092 | 0.38 | down 2 e1 | direct 2s | up 2 e1 | none |
| 4 | strict | | | | | | | none found | none |
| 4 | medium | 393 | 4 | 0.004 | 0.013 | 0.023 | 0.29 | down 4 e9 | direct 2s | up 2x2 e2 | none |
| 4 | loose | 312 | 4 | 0.005 | 0.027 | 0.026 | 0.49 | down 4 e9 | sep 2s | up 4 p5 | none |
| 6 | strict | 577 | 4 | 0.008 | 0.008 | 0.001 | 0.11 | down 2 e3 | sep 3s | up 2 p5 | none |
| 6 | medium | 306 | 3 | 0.006 | 0.026 | 0.025 | 0.40 | down 4 e5 | direct 2s | up 4 p5 | none |
| 6 | loose | 306 | 3 | 0.006 | 0.029 | 0.045 | 0.47 | down 4 e3 | direct 2s | up 4 p4 | none |
| 8 | strict | 425 | 5 | 0.007 | 0.011 | 0.005 | 0.11 | down 4 e9 | sep 2.5s | up 2x2 e2 | none |
| 8 | medium | 283 | 5 | 0.002 | 0.027 | 0.055 | 0.36 | down 8 e9 | sep 3s | up 2x4 p5 | none |
| 8 | loose | 272 | 4 | 0.007 | 0.009 | 0.040 | 0.45 | down 4x2 e3 | direct 2s | up 8 p5 | none |
| 12 | strict | 317 | 4 | 0.008 | 0.008 | 0.004 | 0.07 | down 4 e9 | sep 3s | up 4 e1 | none |
| 12 | medium | 246 | 3 | 0.005 | 0.028 | 0.059 | 0.34 | down 8 e3 | direct 2s | up 8 p4 | none |
| 12 | loose | 246 | 3 | 0.005 | 0.029 | 0.128 | 0.32 | down 8 e1 | direct 2s | up 8 p5 | none |
| 16 | strict | 326 | 5 | 0.010 | 0.009 | 0.008 | 0.10 | down 4x2 e5 | direct 2.5s | up 2x4 e1 | none |
| 16 | medium | 248 | 5 | 0.005 | 0.027 | 0.064 | 0.35 | down 16 e9 | sep 2s | up 2x8 p5 | none |
| 16 | loose | 241 | 4 | 0.010 | 0.009 | 0.054 | 0.45 | down 8x2 e3 | direct 2s | up 16 p5 | none |
| 24 | strict | 275 | 5 | 0.007 | 0.011 | 0.007 | 0.18 | down 4x4 e9 | direct 2s | up 2x8 e2 | none |
| 24 | medium | 231 | 3 | 0.005 | 0.028 | 0.067 | 0.34 | down 16 e3 | direct 2s | up 16 p4 | none |
| 24 | loose | 231 | 3 | 0.005 | 0.028 | 0.067 | 0.34 | down 16 e3 | direct 2s | up 16 p4 | none |
| 32 | strict | 258 | 4 | 0.006 | 0.010 | 0.009 | 0.07 | down 8 e9 | sep 3s | up 8 e1 | none |
| 32 | medium | 235 | 3 | 0.008 | 0.014 | 0.049 | 0.16 | down 16 e3 | direct 2.5s | up 16 p4 | none |
| 32 | loose | 233 | 3 | 0.007 | 0.039 | 0.100 | 0.42 | down 16 e1 | direct 2s | up 16 e2 | none |
| 48 | strict | 246 | 5 | 0.006 | 0.011 | 0.010 | 0.10 | down 8x4 e9 | direct 2s | up 2x16 e2 | none |
| 48 | medium | 234 | 4 | 0.006 | 0.022 | 0.038 | 0.34 | down 16x2 e3 | direct 2s | up 32 p4 | none |
| 48 | loose | 234 | 4 | 0.006 | 0.022 | 0.038 | 0.34 | down 16x2 e3 | direct 2s | up 32 p4 | none |
| 64 | strict | 247 | 5 | 0.008 | 0.012 | 0.007 | 0.12 | down 8x4 e9 | direct 2.5s | up 2x16 e1 | none |
| 64 | medium | 235 | 4 | 0.005 | 0.026 | 0.014 | 0.23 | down 16x2 e9 | direct 2s | up 32 p4 | none |
| 64 | loose | 233 | 4 | 0.010 | 0.008 | 0.048 | 0.45 | down 16x4 e5 | direct 2s | up 64 p5 | none |
| 100 | strict | 237 | 4 | 0.007 | 0.016 | 0.009 | 0.12 | down 16x2 e9 | direct 2.5s | up 32 e1 | none |
| 100 | medium | 233 | 4 | 0.006 | 0.032 | 0.012 | 0.34 | down 16x4 e9 | direct 2s | up 64 p4 | none |
| 100 | loose | 233 | 4 | 0.007 | 0.037 | 0.037 | 0.38 | down 16x4 e3 | direct 2s | up 64 p4 | none |
| 150 | strict | 233 | 4 | 0.009 | 0.014 | 0.007 | 0.11 | down 16x4 e9 | direct 2.5s | up 64 p4 | none |
| 150 | medium | 233 | 4 | 0.005 | 0.015 | 0.091 | 0.17 | down 16x4 e1 | direct 2.5s | up 64 p4 | none |
| 150 | loose | 233 | 4 | 0.005 | 0.023 | 0.056 | 0.39 | down 16x8 e3 | direct 2s | up 128 p5 | none |
| 200 | strict | 234 | 4 | 0.006 | 0.003 | 0.010 | 0.05 | down 16x4 e5 | direct 3s | up 64 e1 | none |
| 200 | medium | 233 | 4 | 0.008 | 0.007 | 0.039 | 0.29 | down 16x8 e3 | direct 2.5s | up 128 p4 | none |
| 200 | loose | 233 | 4 | 0.006 | 0.037 | 0.038 | 0.38 | down 16x8 e3 | direct 2s | up 128 p4 | none |

## Cost vs shift-variance Pareto front (candidates also meeting the other 'medium' limits)

**sigma 2**: 453 us / phase 0.018 (down 2 e5 | direct 2s | up 2 p4), 502 us / phase 0.017 (down 2 e9 | direct 2s | up 2 p5)

**sigma 3**: 545 us / phase 0.004 (down 2 e5 | direct 2s | up 2 p5), 555 us / phase 0.004 (down 2 e5 | sep 2s | up 2 p5)

**sigma 4**: 393 us / phase 0.023 (down 4 e9 | direct 2s | up 2x2 e2), 425 us / phase 0.023 (down 4 e9 | sep 2s | up 2x2 p5 rot45), 506 us / phase 0.008 (down 2x2 e5 | direct 2s | up 2x2 e2), 555 us / phase 0.002 (down 2 e5 | sep 2.5s | up 2 p5), 724 us / phase 0.001 (down 2 e9 | direct 2s | up 2 p5)

**sigma 6**: 306 us / phase 0.010 (down 4 e9 | direct 2s | up 4 p5), 317 us / phase 0.010 (down 4 e9 | pw9x2 | up 4 p5), 419 us / phase 0.004 (down 2x2 e5 | direct 2s | up 4 p5), 425 us / phase 0.004 (down 2x2 e5 | sep 2s | up 4 p5), 532 us / phase 0.001 (down 2x2 e5 | direct 2s | up 2x2 e2), 538 us / phase 0.001 (down 2x2 e5 | sep 2s | up 2x2 e2)

**sigma 8**: 283 us / phase 0.055 (down 8 e9 | sep 3s | up 2x4 p5), 303 us / phase 0.019 (down 4x2 e5 | direct 2s | up 2x4 e2), 307 us / phase 0.011 (down 4x2 e9 | direct 3s | up 2x4 p5), 312 us / phase 0.006 (down 4 e9 | sep 2.5s | up 4 p5), 425 us / phase 0.005 (down 4 e9 | sep 2.5s | up 2x2 e2), 425 us / phase 0.002 (down 2x2 e5 | sep 2.5s | up 4 p5)

**sigma 12**: 246 us / phase 0.030 (down 8 e9 | direct 2s | up 8 p5), 253 us / phase 0.030 (down 8 e9 | pw9x2 | up 8 p5), 278 us / phase 0.012 (down 4x2 e5 | direct 2s | up 8 p5), 282 us / phase 0.005 (down 4x2 e9 | direct 2s | up 8 p5), 287 us / phase 0.005 (down 4x2 e9 | sep 2s | up 8 p5), 288 us / phase 0.005 (down 4x2 e9 | pw9x2 | up 8 p5)

**sigma 16**: 248 us / phase 0.064 (down 16 e9 | sep 2s | up 2x8 p5), 251 us / phase 0.020 (down 8 e9 | sep 2.5s | up 8 p5), 273 us / phase 0.020 (down 4x4 e9 | direct 2s | up 2x8 e2), 280 us / phase 0.020 (down 4x4 e9 | sep 3s | up 2x8 p4 rot45), 283 us / phase 0.008 (down 4x2 e5 | sep 2.5s | up 8 p5), 287 us / phase 0.003 (down 4x2 e9 | sep 2.5s | up 8 p5)

**sigma 24**: 231 us / phase 0.037 (down 16 e9 | direct 2s | up 16 p5), 236 us / phase 0.037 (down 16 e9 | pw9x2 | up 16 p5), 243 us / phase 0.022 (down 8x2 e5 | direct 2s | up 16 p5), 244 us / phase 0.014 (down 8x2 e9 | direct 2s | up 16 p5), 249 us / phase 0.013 (down 8x2 e9 | sep 2s | up 16 p5), 249 us / phase 0.013 (down 8x2 e9 | pw9x2 | up 16 p5)

**sigma 32**: 235 us / phase 0.026 (down 16 e9 | direct 2.5s | up 16 p5), 236 us / phase 0.026 (down 16 e9 | sep 2.5s | up 16 p5), 243 us / phase 0.026 (down 16 e9 | pw9x3 | up 16 p5), 245 us / phase 0.026 (down 16 e9 | direct 2s | up 2x8 e2), 245 us / phase 0.024 (down 8x4 e9 | direct 2s | up 2x16 p5), 246 us / phase 0.010 (down 8x2 e9 | direct 2s | up 16 p5)

**sigma 48**: 234 us / phase 0.027 (down 16x2 e5 | direct 2s | up 32 p5), 234 us / phase 0.019 (down 16x2 e9 | direct 2s | up 32 p5), 236 us / phase 0.016 (down 16 e9 | sep 2.5s | up 16 p5), 239 us / phase 0.011 (down 8x4 e9 | direct 2s | up 32 p5), 244 us / phase 0.010 (down 8x4 e9 | sep 2s | up 32 p5), 244 us / phase 0.010 (down 8x4 e9 | pw9x2 | up 32 p5)

**sigma 64**: 235 us / phase 0.014 (down 16x2 e9 | direct 2s | up 32 p5), 238 us / phase 0.012 (down 16 e9 | sep 3s | up 16 p5), 240 us / phase 0.007 (down 8x4 e9 | direct 2.5s | up 32 p5), 244 us / phase 0.007 (down 8x4 e9 | sep 2.5s | up 32 p5), 246 us / phase 0.006 (down 8x4 e9 | direct 2s | up 2x16 e2), 247 us / phase 0.005 (down 8x2x2 e9 | direct 2s | up 32 p5)

**sigma 100**: 233 us / phase 0.012 (down 16x4 e9 | direct 2s | up 64 p5), 237 us / phase 0.009 (down 16x2 e9 | direct 2.5s | up 32 p5), 241 us / phase 0.008 (down 16 e9 | sep 3s | up 16 p5), 242 us / phase 0.004 (down 8x4 e9 | direct 2.5s | up 32 p5)

**sigma 150**: 233 us / phase 0.091 (down 16x4 e1 | direct 2.5s | up 64 p5), 233 us / phase 0.007 (down 16x4 e9 | direct 2.5s | up 64 p5)

**sigma 200**: 233 us / phase 0.019 (down 16x8 e9 | direct 2.5s | up 128 p5), 234 us / phase 0.005 (down 16x4 e9 | direct 2.5s | up 64 p5), 234 us / phase 0.005 (down 16x4 e9 | direct 3s | up 64 p5)

