# Baseline sweep (GTX 1660 model, 1920x1080, RGB10A2)

Limits: leak <= 0.015, tv <= 0.055, curv <= 0.7, block <= 0.35, aniso <= 0.03, phase <= 0.1, sigma_err <= 0.02

| sigma | family | us | passes | fetch/px | leak | tv | aniso | phase | curv | params / status |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | direct2d | 216 | 1 | 16.00 | 0.014 | 0.002 | 0.000 | 0.000 | 0.01 | r=3 s=1 |
| 1 | sep_linear | 226 | 2 | 8.00 | 0.014 | 0.002 | 0.000 | 0.000 | 0.01 | r=3 s=1 |
| 1 | sep_bilinear | 226 | 2 | 4.00 | 0.002 | 0.048 | 0.000 | 0.000 | 0.22 | m=2 s=0.954 |
| 1 | kawase | 226 | 2 | 8.00 | 0.002 | 0.048 | 0.000 | 0.000 | 0.22 | 2 passes |
| 1 | dual_filter | 183 | 2 | 9.25 | 0.002 | 0.048 | 0.000 | 0.293 | 0.34 | levels=1 o=0.25 — best tried fails block,phase |
| 2 | sep_linear | 226 | 2 | 12.00 | 0.011 | 0.025 | 0.000 | 0.000 | 0.18 | r=5 s=2.06 |
| 2 | sep_bilinear | 226 | 2 | 10.00 | 0.010 | 0.032 | 0.000 | 0.000 | 0.23 | m=5 s=2.03 |
| 2 | direct2d | 480 | 1 | 36.00 | 0.011 | 0.025 | 0.000 | 0.000 | 0.17 | r=5 s=2.06 |
| 2 | dual_filter | 183 | 2 | 9.25 | 0.050 | 0.085 | 0.000 | 0.117 | 1.46 | levels=1 o=1.31 — best tried fails leak,tv,curv,block,phase |
| 2 | kawase | 339 | 3 | 12.00 | 0.064 | 0.117 | 0.000 | 0.000 | 1.23 | 3 passes — best tried fails leak,tv,curv |
| 3 | pyramid | 209 | 4 | 2.75 | 0.004 | 0.046 | 0.000 | 0.092 | 0.39 | k=1 m=3 s=1.5 up=chain |
| 3 | sep_linear | 226 | 2 | 16.00 | 0.015 | 0.050 | 0.000 | 0.000 | 0.57 | r=7 s=3.2 |
| 3 | sep_bilinear | 226 | 2 | 16.00 | 0.009 | 0.026 | 0.000 | 0.000 | 0.22 | m=8 s=3.06 |
| 3 | dual_filter | 236 | 4 | 11.56 | 0.004 | 0.024 | 0.001 | 0.159 | 0.24 | levels=2 o=0.658 — best tried fails block,phase,sigma_err |
| 3 | kawase | 339 | 3 | 12.00 | 0.171 | 0.203 | 0.000 | 0.000 | 3.68 | 3 passes — best tried fails leak,tv,curv |
| 3 | direct2d | 480 | 1 | 36.00 | 0.102 | 0.234 | 0.000 | 0.000 | 4.95 | r=5 s=6.13 — best tried fails leak,tv,curv |
| 4 | pyramid | 209 | 4 | 4.25 | 0.008 | 0.006 | 0.000 | 0.071 | 0.18 | k=1 m=6 s=1.88 up=chain |
| 4 | dual_filter | 236 | 4 | 11.56 | 0.010 | 0.043 | 0.010 | 0.028 | 0.40 | levels=2 o=1.12 |
| 4 | sep_bilinear | 274 | 2 | 20.00 | 0.013 | 0.044 | 0.000 | 0.000 | 0.46 | m=10 s=4.22 |
| 4 | sep_linear | 300 | 2 | 22.00 | 0.013 | 0.036 | 0.000 | 0.000 | 0.50 | r=10 s=4.18 |
| 4 | kawase | 452 | 4 | 16.00 | 0.119 | 0.138 | 0.000 | 0.000 | 3.93 | 4 passes — best tried fails leak,tv,curv |
| 4 | direct2d | ≥850 | | | | | | | | rejected (>3x cost) |
| 6 | pyramid | 214 | 4 | 5.75 | 0.008 | 0.009 | 0.000 | 0.047 | 0.14 | k=1 m=9 s=2.95 up=chain |
| 6 | sep_bilinear | 406 | 2 | 30.00 | 0.013 | 0.047 | 0.000 | 0.000 | 0.64 | m=15 s=6.37 |
| 6 | sep_linear | 459 | 2 | 34.00 | 0.012 | 0.026 | 0.000 | 0.000 | 0.48 | r=16 s=6.19 |
| 6 | dual_filter | 257 | 6 | 12.14 | 0.005 | 0.022 | 0.000 | 0.223 | 0.24 | levels=3 o=0.585 — best tried fails block,phase,sigma_err |
| 6 | kawase | 565 | 5 | 20.00 | 0.083 | 0.108 | 0.000 | 0.000 | 4.74 | 5 passes — best tried fails leak,tv,curv |
| 6 | direct2d | ≥1602 | | | | | | | | rejected (>3x cost) |
| 8 | pyramid | 212 | 6 | 2.31 | 0.009 | 0.005 | 0.000 | 0.085 | 0.20 | k=2 m=6 s=1.85 up=chain |
| 8 | dual_filter | 257 | 6 | 12.14 | 0.006 | 0.037 | 0.005 | 0.015 | 0.31 | levels=3 o=1.08 |
| 8 | sep_bilinear | 538 | 2 | 40.00 | 0.013 | 0.048 | 0.000 | 0.000 | 0.56 | m=20 s=8.52 |
| 8 | sep_linear | 591 | 2 | 44.00 | 0.010 | 0.031 | 0.000 | 0.000 | 0.36 | r=21 s=8.31 |
| 8 | kawase | ≥678 | | | | | | | | rejected (>3x cost) |
| 8 | direct2d | ≥2975 | | | | | | | | rejected (>3x cost) |
| 12 | pyramid | 182 | 5 | 2.44 | 0.008 | 0.008 | 0.000 | 0.056 | 0.27 | k=2 m=9 s=2.94 up=direct |
| 12 | dual_filter | 270 | 8 | 12.29 | 0.004 | 0.023 | 0.000 | 0.267 | 0.21 | levels=4 o=0.549 — best tried fails block,phase,sigma_err |
| 12 | sep_bilinear | ≥564 | | | | | | | | rejected (>3x cost) |
| 12 | sep_linear | ≥591 | | | | | | | | rejected (>3x cost) |
| 12 | kawase | ≥904 | | | | | | | | rejected (>3x cost) |
| 12 | direct2d | ≥6394 | | | | | | | | rejected (>3x cost) |
| 16 | pyramid | 187 | 5 | 2.81 | 0.008 | 0.010 | 0.000 | 0.042 | 0.10 | k=2 m=12 s=3.98 up=direct |
| 16 | dual_filter | 270 | 8 | 12.29 | 0.005 | 0.036 | 0.002 | 0.011 | 0.30 | levels=4 o=1.07 |
| 16 | sep_bilinear | ≥749 | | | | | | | | rejected (>3x cost) |
| 16 | sep_linear | ≥776 | | | | | | | | rejected (>3x cost) |
| 16 | kawase | ≥1130 | | | | | | | | rejected (>3x cost) |
| 16 | direct2d | ≥11107 | | | | | | | | rejected (>3x cost) |
| 24 | pyramid | 177 | 6 | 1.61 | 0.007 | 0.008 | 0.000 | 0.064 | 0.17 | k=3 m=9 s=2.93 up=direct |
| 24 | dual_filter | 281 | 10 | 12.32 | 0.003 | 0.025 | 0.000 | 0.296 | 0.19 | levels=5 o=0.531 — best tried fails block,phase,sigma_err |
| 24 | sep_bilinear | ≥1119 | | | | | | | | rejected (>3x cost) |
| 24 | sep_linear | ≥1145 | | | | | | | | rejected (>3x cost) |
| 24 | kawase | ≥1356 | | | | | | | | rejected (>3x cost) |
| 32 | pyramid | 178 | 6 | 1.70 | 0.006 | 0.010 | 0.000 | 0.048 | 0.08 | k=3 m=12 s=3.97 up=direct |
| 32 | dual_filter | 281 | 10 | 12.32 | 0.005 | 0.035 | 0.001 | 0.009 | 0.29 | levels=5 o=1.06 |
| 32 | sep_linear | ≥1489 | | | | | | | | rejected (>3x cost) |
| 32 | sep_bilinear | ≥1489 | | | | | | | | rejected (>3x cost) |
| 32 | kawase | ≥1695 | | | | | | | | rejected (>3x cost) |
| 48 | pyramid | 180 | 7 | 1.40 | 0.008 | 0.008 | 0.000 | 0.068 | 0.11 | k=4 m=9 s=2.92 up=direct |
| 48 | dual_filter | 291 | 12 | 12.33 | 0.002 | 0.026 | 0.000 | 0.313 | 0.17 | levels=6 o=0.521 — best tried fails block,phase,sigma_err |
| 48 | sep_linear | ≥2228 | | | | | | | | rejected (>3x cost) |
| 48 | sep_bilinear | ≥2228 | | | | | | | | rejected (>3x cost) |
| 48 | kawase | ≥2260 | | | | | | | | rejected (>3x cost) |
| 64 | pyramid | 180 | 7 | 1.43 | 0.005 | 0.010 | 0.000 | 0.051 | 0.07 | k=4 m=12 s=3.97 up=direct |
| 64 | dual_filter | 291 | 12 | 12.33 | 0.005 | 0.035 | 0.001 | 0.009 | 0.29 | levels=6 o=1.06 |
| 64 | kawase | ≥2712 | | | | | | | | rejected (>3x cost) |
| 64 | sep_bilinear | ≥2941 | | | | | | | | rejected (>3x cost) |
| 64 | sep_linear | ≥2967 | | | | | | | | rejected (>3x cost) |
| 100 | pyramid | 181 | 7 | 1.48 | 0.007 | 0.010 | 0.000 | 0.032 | 0.09 | k=4 m=19 s=6.28 up=direct |
| 100 | dual_filter | 301 | 14 | 12.33 | 0.005 | 0.023 | 0.000 | 0.185 | 0.32 | levels=7 o=0.585 — best tried fails block,phase,sigma_err |
| 100 | kawase | ≥3616 | | | | | | | | rejected (>3x cost) |
| 100 | sep_linear | ≥4604 | | | | | | | | rejected (>3x cost) |
| 100 | sep_bilinear | ≥4604 | | | | | | | | rejected (>3x cost) |
| 150 | pyramid | 184 | 8 | 1.36 | 0.008 | 0.011 | 0.000 | 0.044 | 0.09 | k=5 m=14 s=4.68 up=direct |
| 150 | dual_filter | 301 | 14 | 12.33 | 0.016 | 0.051 | 0.016 | 0.032 | 0.49 | levels=7 o=1.44 — best tried fails leak,sigma_err |
| 150 | kawase | ≥4633 | | | | | | | | rejected (>3x cost) |
| 150 | sep_bilinear | ≥6874 | | | | | | | | rejected (>3x cost) |
| 150 | sep_linear | ≥6901 | | | | | | | | rejected (>3x cost) |
| 200 | pyramid | 184 | 8 | 1.37 | 0.007 | 0.010 | 0.000 | 0.033 | 0.09 | k=5 m=19 s=6.27 up=direct |
| 200 | dual_filter | 311 | 16 | 12.33 | 0.004 | 0.024 | 0.000 | 0.176 | 0.33 | levels=8 o=0.584 — best tried fails block,phase,sigma_err |
| 200 | kawase | ≥5650 | | | | | | | | rejected (>3x cost) |
| 200 | sep_linear | ≥9171 | | | | | | | | rejected (>3x cost) |
| 200 | sep_bilinear | ≥9171 | | | | | | | | rejected (>3x cost) |
