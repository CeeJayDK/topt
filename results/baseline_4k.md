# Baseline sweep (GTX 1660 model, 3840x2160, RGB10A2)

us = marginal cost over a plain composite pass (the last pass is the composite).

Limits: leak <= 0.012, tv <= 0.032, curv <= 0.4, block <= 0.35, aniso <= 0.03, phase <= 0.1, iso <= 0.032, sigma_err <= 0.02

| sigma | family | us | passes | fetch/px | leak | tv | aniso | phase | curv | params / status |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | direct2d | 466 | 1 | 17.00 | 0.009 | 0.002 | 0.000 | 0.000 | 0.01 | r=3 s=1 |
| 1 | sep_linear | 653 | 2 | 9.00 | 0.009 | 0.002 | 0.000 | 0.000 | 0.01 | r=3 s=1 |
| 1 | sep_bilinear | 653 | 2 | 7.00 | 0.001 | 0.014 | 0.000 | 0.000 | 0.06 | m=3 s=0.868 |
| 1 | dual_filter | 329 | 2 | 10.25 | 0.000 | 0.048 | 0.000 | 0.293 | 0.34 | levels=1 o=0.25 — best tried fails tv,block,phase |
| 1 | kawase | 653 | 2 | 9.00 | 0.000 | 0.048 | 0.000 | 0.000 | 0.22 | 2 passes — best tried fails tv |
| 2 | sep_linear | 653 | 2 | 13.00 | 0.011 | 0.025 | 0.000 | 0.000 | 0.18 | r=5 s=2.06 |
| 2 | sep_bilinear | 653 | 2 | 11.00 | 0.010 | 0.032 | 0.000 | 0.000 | 0.23 | m=5 s=2.03 |
| 2 | direct2d | 1522 | 1 | 37.00 | 0.011 | 0.025 | 0.000 | 0.000 | 0.17 | r=5 s=2.06 |
| 2 | dual_filter | 329 | 2 | 10.25 | 0.050 | 0.085 | 0.000 | 0.117 | 1.46 | levels=1 o=1.31 — best tried fails leak,tv,curv,block,phase |
| 2 | kawase | 1090 | 3 | 13.00 | 0.064 | 0.117 | 0.000 | 0.000 | 1.23 | 3 passes — best tried fails leak,tv,curv,iso |
| 3 | pyramid | 555 | 4 | 4.75 | 0.008 | 0.003 | 0.000 | 0.095 | 0.25 | k=1 m=5 s=1.32 up=chain |
| 3 | sep_bilinear | 653 | 2 | 17.00 | 0.009 | 0.026 | 0.000 | 0.000 | 0.22 | m=8 s=3.06 |
| 3 | sep_linear | 696 | 2 | 19.00 | 0.010 | 0.020 | 0.000 | 0.000 | 0.21 | r=8 s=3.07 |
| 3 | dual_filter | 512 | 4 | 12.56 | 0.004 | 0.024 | 0.001 | 0.159 | 0.24 | levels=2 o=0.658 — best tried fails block,phase,sigma_err |
| 3 | kawase | 1090 | 3 | 13.00 | 0.171 | 0.203 | 0.000 | 0.000 | 3.68 | 3 passes — best tried fails leak,tv,curv,iso |
| 3 | direct2d | 1522 | 1 | 37.00 | 0.098 | 0.234 | 0.000 | 0.000 | 4.95 | r=5 s=6.13 — best tried fails leak,tv,curv,iso |
| 4 | pyramid | 555 | 4 | 5.25 | 0.008 | 0.006 | 0.000 | 0.071 | 0.18 | k=1 m=6 s=1.88 up=chain |
| 4 | sep_bilinear | 802 | 2 | 23.00 | 0.010 | 0.023 | 0.000 | 0.000 | 0.22 | m=11 s=4.09 |
| 4 | sep_linear | 893 | 2 | 25.00 | 0.009 | 0.018 | 0.000 | 0.000 | 0.23 | r=11 s=4.09 |
| 4 | dual_filter | 512 | 4 | 12.56 | 0.010 | 0.043 | 0.010 | 0.028 | 0.40 | levels=2 o=1.12 — best tried fails tv |
| 4 | kawase | 1527 | 4 | 17.00 | 0.119 | 0.138 | 0.000 | 0.000 | 3.93 | 4 passes — best tried fails leak,tv,curv,iso |
| 4 | direct2d | ≥3000 | | | | | | | | rejected (>3x cost) |
| 6 | pyramid | 577 | 4 | 6.75 | 0.008 | 0.009 | 0.000 | 0.047 | 0.14 | k=1 m=9 s=2.95 up=chain |
| 6 | sep_bilinear | 1316 | 2 | 33.00 | 0.011 | 0.031 | 0.000 | 0.000 | 0.39 | m=16 s=6.22 |
| 6 | sep_linear | 1527 | 2 | 37.00 | 0.010 | 0.016 | 0.000 | 0.000 | 0.28 | r=17 s=6.12 |
| 6 | dual_filter | 565 | 6 | 13.14 | 0.005 | 0.022 | 0.000 | 0.223 | 0.24 | levels=3 o=0.585 — best tried fails block,phase,sigma_err |
| 6 | kawase | ≥1964 | | | | | | | | rejected (>3x cost) |
| 6 | direct2d | ≥6010 | | | | | | | | rejected (>3x cost) |
| 8 | pyramid | 538 | 6 | 3.31 | 0.009 | 0.005 | 0.000 | 0.085 | 0.20 | k=2 m=6 s=1.85 up=chain |
| 8 | dual_filter | 565 | 6 | 13.14 | 0.006 | 0.037 | 0.005 | 0.015 | 0.31 | levels=3 o=1.08 — best tried fails tv |
| 8 | sep_bilinear | 1527 | 2 | 37.00 | 0.024 | 0.088 | 0.000 | 0.000 | 1.18 | m=18 s=9.15 — best tried fails leak,tv,curv,iso |
| 8 | sep_linear | 1527 | 2 | 37.00 | 0.031 | 0.110 | 0.000 | 0.000 | 3.32 | r=17 s=9.46 — best tried fails leak,tv,curv,iso |
| 8 | kawase | ≥2401 | | | | | | | | rejected (>3x cost) |
| 8 | direct2d | ≥11502 | | | | | | | | rejected (>3x cost) |
| 12 | pyramid | 430 | 5 | 3.44 | 0.008 | 0.008 | 0.000 | 0.056 | 0.27 | k=2 m=9 s=2.94 up=direct |
| 12 | dual_filter | 586 | 8 | 13.29 | 0.004 | 0.023 | 0.000 | 0.267 | 0.21 | levels=4 o=0.549 — best tried fails block,phase,sigma_err |
| 12 | sep_bilinear | ≥1844 | | | | | | | | rejected (>3x cost) |
| 12 | sep_linear | ≥1949 | | | | | | | | rejected (>3x cost) |
| 12 | kawase | ≥3275 | | | | | | | | rejected (>3x cost) |
| 12 | direct2d | ≥25178 | | | | | | | | rejected (>3x cost) |
| 16 | pyramid | 450 | 5 | 3.81 | 0.008 | 0.010 | 0.000 | 0.042 | 0.10 | k=2 m=12 s=3.98 up=direct |
| 16 | dual_filter | 586 | 8 | 13.29 | 0.005 | 0.036 | 0.002 | 0.011 | 0.30 | levels=4 o=1.07 — best tried fails tv |
| 16 | sep_bilinear | ≥2583 | | | | | | | | rejected (>3x cost) |
| 16 | sep_linear | ≥2688 | | | | | | | | rejected (>3x cost) |
| 16 | kawase | ≥4149 | | | | | | | | rejected (>3x cost) |
| 16 | direct2d | ≥44029 | | | | | | | | rejected (>3x cost) |
| 24 | pyramid | 398 | 6 | 2.61 | 0.007 | 0.008 | 0.000 | 0.064 | 0.17 | k=3 m=9 s=2.93 up=direct |
| 24 | dual_filter | 599 | 10 | 13.32 | 0.003 | 0.025 | 0.000 | 0.296 | 0.19 | levels=5 o=0.531 — best tried fails block,phase,sigma_err |
| 24 | sep_bilinear | ≥4061 | | | | | | | | rejected (>3x cost) |
| 24 | sep_linear | ≥4167 | | | | | | | | rejected (>3x cost) |
| 24 | kawase | ≥5023 | | | | | | | | rejected (>3x cost) |
| 32 | pyramid | 403 | 6 | 2.70 | 0.006 | 0.010 | 0.000 | 0.048 | 0.08 | k=3 m=12 s=3.97 up=direct |
| 32 | dual_filter | 599 | 10 | 13.32 | 0.005 | 0.035 | 0.001 | 0.009 | 0.29 | levels=5 o=1.06 — best tried fails tv |
| 32 | sep_linear | ≥5540 | | | | | | | | rejected (>3x cost) |
| 32 | sep_bilinear | ≥5540 | | | | | | | | rejected (>3x cost) |
| 32 | kawase | ≥6334 | | | | | | | | rejected (>3x cost) |
| 48 | pyramid | 393 | 7 | 2.40 | 0.008 | 0.008 | 0.000 | 0.068 | 0.11 | k=4 m=9 s=2.92 up=direct |
| 48 | dual_filter | 610 | 12 | 13.33 | 0.002 | 0.026 | 0.000 | 0.313 | 0.17 | levels=6 o=0.521 — best tried fails block,phase,sigma_err |
| 48 | sep_linear | ≥8497 | | | | | | | | rejected (>3x cost) |
| 48 | sep_bilinear | ≥8497 | | | | | | | | rejected (>3x cost) |
| 48 | kawase | ≥8519 | | | | | | | | rejected (>3x cost) |
| 64 | pyramid | 394 | 7 | 2.43 | 0.005 | 0.010 | 0.000 | 0.051 | 0.07 | k=4 m=12 s=3.97 up=direct |
| 64 | dual_filter | 610 | 12 | 13.33 | 0.005 | 0.035 | 0.001 | 0.009 | 0.29 | levels=6 o=1.06 — best tried fails tv |
| 64 | kawase | ≥10267 | | | | | | | | rejected (>3x cost) |
| 64 | sep_bilinear | ≥11348 | | | | | | | | rejected (>3x cost) |
| 64 | sep_linear | ≥11454 | | | | | | | | rejected (>3x cost) |
| 100 | pyramid | 396 | 8 | 2.35 | 0.007 | 0.004 | 0.000 | 0.068 | 0.06 | k=5 m=10 s=3.04 up=direct |
| 100 | dual_filter | 620 | 14 | 13.33 | 0.005 | 0.023 | 0.000 | 0.185 | 0.32 | levels=7 o=0.585 — best tried fails block,phase,sigma_err |
| 100 | kawase | ≥13763 | | | | | | | | rejected (>3x cost) |
| 100 | sep_linear | ≥18001 | | | | | | | | rejected (>3x cost) |
| 100 | sep_bilinear | ≥18001 | | | | | | | | rejected (>3x cost) |
| 150 | pyramid | 396 | 8 | 2.36 | 0.008 | 0.011 | 0.000 | 0.044 | 0.09 | k=5 m=14 s=4.68 up=direct |
| 150 | dual_filter | 620 | 14 | 13.33 | 0.016 | 0.051 | 0.016 | 0.032 | 0.49 | levels=7 o=1.44 — best tried fails leak,tv,curv,sigma_err |
| 150 | kawase | ≥17696 | | | | | | | | rejected (>3x cost) |
| 150 | sep_bilinear | ≥27084 | | | | | | | | rejected (>3x cost) |
| 150 | sep_linear | ≥27189 | | | | | | | | rejected (>3x cost) |
| 200 | pyramid | 397 | 8 | 2.37 | 0.007 | 0.010 | 0.000 | 0.033 | 0.09 | k=5 m=19 s=6.27 up=direct |
| 200 | dual_filter | 630 | 16 | 13.33 | 0.004 | 0.024 | 0.000 | 0.176 | 0.33 | levels=8 o=0.584 — best tried fails block,phase,sigma_err |
| 200 | kawase | ≥21629 | | | | | | | | rejected (>3x cost) |
| 200 | sep_linear | ≥36272 | | | | | | | | rejected (>3x cost) |
| 200 | sep_bilinear | ≥36272 | | | | | | | | rejected (>3x cost) |
