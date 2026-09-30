# Baseline sweep (GTX 1660 model, 1920x1080, RGB10A2)

us = marginal cost over a plain composite pass (the last pass is the composite).

Limits: leak <= 0.012, tv <= 0.032, curv <= 0.4, block <= 0.35, aniso <= 0.03, phase <= 0.1, iso <= 0.032, sigma_err <= 0.02

| sigma | family | us | passes | fetch/px | leak | tv | aniso | phase | curv | params / status |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | direct2d | 116 | 1 | 17.00 | 0.009 | 0.002 | 0.000 | 0.000 | 0.01 | r=3 s=1 |
| 1 | sep_linear | 167 | 2 | 9.00 | 0.009 | 0.002 | 0.000 | 0.000 | 0.01 | r=3 s=1 |
| 1 | sep_bilinear | 167 | 2 | 7.00 | 0.001 | 0.014 | 0.000 | 0.000 | 0.06 | m=3 s=0.868 |
| 1 | dual_filter | 86 | 2 | 10.25 | 0.000 | 0.048 | 0.000 | 0.293 | 0.34 | levels=1 o=0.25 — best tried fails tv,block,phase |
| 1 | kawase | 167 | 2 | 9.00 | 0.000 | 0.048 | 0.000 | 0.000 | 0.22 | 2 passes — best tried fails tv |
| 2 | sep_linear | 167 | 2 | 13.00 | 0.011 | 0.025 | 0.000 | 0.000 | 0.18 | r=5 s=2.06 |
| 2 | sep_bilinear | 167 | 2 | 11.00 | 0.010 | 0.032 | 0.000 | 0.000 | 0.23 | m=5 s=2.03 |
| 2 | direct2d | 380 | 1 | 37.00 | 0.011 | 0.025 | 0.000 | 0.000 | 0.17 | r=5 s=2.06 |
| 2 | dual_filter | 86 | 2 | 10.25 | 0.050 | 0.085 | 0.000 | 0.117 | 1.46 | levels=1 o=1.31 — best tried fails leak,tv,curv,block,phase |
| 2 | kawase | 280 | 3 | 13.00 | 0.064 | 0.117 | 0.000 | 0.000 | 1.23 | 3 passes — best tried fails leak,tv,curv,iso |
| 3 | pyramid | 150 | 4 | 4.75 | 0.008 | 0.003 | 0.000 | 0.095 | 0.25 | k=1 m=5 s=1.32 up=chain |
| 3 | sep_bilinear | 167 | 2 | 17.00 | 0.009 | 0.026 | 0.000 | 0.000 | 0.22 | m=8 s=3.06 |
| 3 | sep_linear | 178 | 2 | 19.00 | 0.010 | 0.020 | 0.000 | 0.000 | 0.21 | r=8 s=3.07 |
| 3 | dual_filter | 139 | 4 | 12.56 | 0.004 | 0.024 | 0.001 | 0.159 | 0.24 | levels=2 o=0.658 — best tried fails block,phase,sigma_err |
| 3 | kawase | 280 | 3 | 13.00 | 0.171 | 0.203 | 0.000 | 0.000 | 3.68 | 3 passes — best tried fails leak,tv,curv,iso |
| 3 | direct2d | 380 | 1 | 37.00 | 0.098 | 0.234 | 0.000 | 0.000 | 4.95 | r=5 s=6.13 — best tried fails leak,tv,curv,iso |
| 4 | pyramid | 150 | 4 | 5.25 | 0.008 | 0.006 | 0.000 | 0.071 | 0.18 | k=1 m=6 s=1.88 up=chain |
| 4 | sep_bilinear | 204 | 2 | 23.00 | 0.010 | 0.023 | 0.000 | 0.000 | 0.22 | m=11 s=4.09 |
| 4 | sep_linear | 227 | 2 | 25.00 | 0.009 | 0.018 | 0.000 | 0.000 | 0.23 | r=11 s=4.09 |
| 4 | dual_filter | 139 | 4 | 12.56 | 0.010 | 0.043 | 0.010 | 0.028 | 0.40 | levels=2 o=1.12 — best tried fails tv |
| 4 | kawase | 393 | 4 | 17.00 | 0.119 | 0.138 | 0.000 | 0.000 | 3.93 | 4 passes — best tried fails leak,tv,curv,iso |
| 4 | direct2d | ≥750 | | | | | | | | rejected (>3x cost) |
| 6 | pyramid | 155 | 4 | 6.75 | 0.008 | 0.009 | 0.000 | 0.047 | 0.14 | k=1 m=9 s=2.95 up=chain |
| 6 | sep_bilinear | 333 | 2 | 33.00 | 0.011 | 0.031 | 0.000 | 0.000 | 0.39 | m=16 s=6.22 |
| 6 | sep_linear | 385 | 2 | 37.00 | 0.010 | 0.016 | 0.000 | 0.000 | 0.28 | r=17 s=6.12 |
| 6 | dual_filter | 160 | 6 | 13.14 | 0.005 | 0.022 | 0.000 | 0.223 | 0.24 | levels=3 o=0.585 — best tried fails block,phase,sigma_err |
| 6 | kawase | ≥506 | | | | | | | | rejected (>3x cost) |
| 6 | direct2d | ≥1503 | | | | | | | | rejected (>3x cost) |
| 8 | pyramid | 153 | 6 | 3.31 | 0.009 | 0.005 | 0.000 | 0.085 | 0.20 | k=2 m=6 s=1.85 up=chain |
| 8 | dual_filter | 160 | 6 | 13.14 | 0.006 | 0.037 | 0.005 | 0.015 | 0.31 | levels=3 o=1.08 — best tried fails tv |
| 8 | sep_bilinear | 438 | 2 | 41.00 | 0.013 | 0.048 | 0.000 | 0.000 | 0.56 | m=20 s=8.52 — best tried fails leak,tv,curv |
| 8 | sep_linear | 438 | 2 | 41.00 | 0.015 | 0.060 | 0.000 | 0.000 | 0.75 | r=19 s=8.65 — best tried fails leak,tv,curv,iso |
| 8 | kawase | ≥619 | | | | | | | | rejected (>3x cost) |
| 8 | direct2d | ≥2875 | | | | | | | | rejected (>3x cost) |
| 12 | pyramid | 123 | 5 | 3.44 | 0.008 | 0.008 | 0.000 | 0.056 | 0.27 | k=2 m=9 s=2.94 up=direct |
| 12 | dual_filter | 173 | 8 | 13.29 | 0.004 | 0.023 | 0.000 | 0.267 | 0.21 | levels=4 o=0.549 — best tried fails block,phase,sigma_err |
| 12 | sep_bilinear | ≥465 | | | | | | | | rejected (>3x cost) |
| 12 | sep_linear | ≥491 | | | | | | | | rejected (>3x cost) |
| 12 | kawase | ≥845 | | | | | | | | rejected (>3x cost) |
| 12 | direct2d | ≥6294 | | | | | | | | rejected (>3x cost) |
| 16 | pyramid | 128 | 5 | 3.81 | 0.008 | 0.010 | 0.000 | 0.042 | 0.10 | k=2 m=12 s=3.98 up=direct |
| 16 | dual_filter | 173 | 8 | 13.29 | 0.005 | 0.036 | 0.002 | 0.011 | 0.30 | levels=4 o=1.07 — best tried fails tv |
| 16 | sep_bilinear | ≥649 | | | | | | | | rejected (>3x cost) |
| 16 | sep_linear | ≥676 | | | | | | | | rejected (>3x cost) |
| 16 | kawase | ≥1071 | | | | | | | | rejected (>3x cost) |
| 16 | direct2d | ≥11007 | | | | | | | | rejected (>3x cost) |
| 24 | pyramid | 118 | 6 | 2.61 | 0.007 | 0.008 | 0.000 | 0.064 | 0.17 | k=3 m=9 s=2.93 up=direct |
| 24 | dual_filter | 183 | 10 | 13.32 | 0.003 | 0.025 | 0.000 | 0.296 | 0.19 | levels=5 o=0.531 — best tried fails block,phase,sigma_err |
| 24 | sep_bilinear | ≥1019 | | | | | | | | rejected (>3x cost) |
| 24 | sep_linear | ≥1045 | | | | | | | | rejected (>3x cost) |
| 24 | kawase | ≥1297 | | | | | | | | rejected (>3x cost) |
| 32 | pyramid | 119 | 6 | 2.70 | 0.006 | 0.010 | 0.000 | 0.048 | 0.08 | k=3 m=12 s=3.97 up=direct |
| 32 | dual_filter | 183 | 10 | 13.32 | 0.005 | 0.035 | 0.001 | 0.009 | 0.29 | levels=5 o=1.06 — best tried fails tv |
| 32 | sep_linear | ≥1389 | | | | | | | | rejected (>3x cost) |
| 32 | sep_bilinear | ≥1389 | | | | | | | | rejected (>3x cost) |
| 32 | kawase | ≥1636 | | | | | | | | rejected (>3x cost) |
| 48 | pyramid | 121 | 7 | 2.40 | 0.008 | 0.008 | 0.000 | 0.068 | 0.11 | k=4 m=9 s=2.92 up=direct |
| 48 | dual_filter | 194 | 12 | 13.33 | 0.002 | 0.026 | 0.000 | 0.313 | 0.17 | levels=6 o=0.521 — best tried fails block,phase,sigma_err |
| 48 | sep_linear | ≥2128 | | | | | | | | rejected (>3x cost) |
| 48 | sep_bilinear | ≥2128 | | | | | | | | rejected (>3x cost) |
| 48 | kawase | ≥2201 | | | | | | | | rejected (>3x cost) |
| 64 | pyramid | 121 | 7 | 2.43 | 0.005 | 0.010 | 0.000 | 0.051 | 0.07 | k=4 m=12 s=3.97 up=direct |
| 64 | dual_filter | 194 | 12 | 13.33 | 0.005 | 0.035 | 0.001 | 0.009 | 0.29 | levels=6 o=1.06 — best tried fails tv |
| 64 | kawase | ≥2653 | | | | | | | | rejected (>3x cost) |
| 64 | sep_bilinear | ≥2841 | | | | | | | | rejected (>3x cost) |
| 64 | sep_linear | ≥2867 | | | | | | | | rejected (>3x cost) |
| 100 | pyramid | 122 | 7 | 2.48 | 0.007 | 0.010 | 0.000 | 0.032 | 0.09 | k=4 m=19 s=6.28 up=direct |
| 100 | dual_filter | 204 | 14 | 13.33 | 0.005 | 0.023 | 0.000 | 0.185 | 0.32 | levels=7 o=0.585 — best tried fails block,phase,sigma_err |
| 100 | kawase | ≥3557 | | | | | | | | rejected (>3x cost) |
| 100 | sep_linear | ≥4504 | | | | | | | | rejected (>3x cost) |
| 100 | sep_bilinear | ≥4504 | | | | | | | | rejected (>3x cost) |
| 150 | pyramid | 125 | 8 | 2.36 | 0.008 | 0.011 | 0.000 | 0.044 | 0.09 | k=5 m=14 s=4.68 up=direct |
| 150 | dual_filter | 204 | 14 | 13.33 | 0.016 | 0.051 | 0.016 | 0.032 | 0.49 | levels=7 o=1.44 — best tried fails leak,tv,curv,sigma_err |
| 150 | kawase | ≥4574 | | | | | | | | rejected (>3x cost) |
| 150 | sep_bilinear | ≥6775 | | | | | | | | rejected (>3x cost) |
| 150 | sep_linear | ≥6801 | | | | | | | | rejected (>3x cost) |
| 200 | pyramid | 125 | 8 | 2.37 | 0.007 | 0.010 | 0.000 | 0.033 | 0.09 | k=5 m=19 s=6.27 up=direct |
| 200 | dual_filter | 214 | 16 | 13.33 | 0.004 | 0.024 | 0.000 | 0.176 | 0.33 | levels=8 o=0.584 — best tried fails block,phase,sigma_err |
| 200 | kawase | ≥5591 | | | | | | | | rejected (>3x cost) |
| 200 | sep_linear | ≥9072 | | | | | | | | rejected (>3x cost) |
| 200 | sep_bilinear | ≥9072 | | | | | | | | rejected (>3x cost) |
