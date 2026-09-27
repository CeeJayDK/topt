# Baseline sweep (GTX 1660 model, 1920x1080, RGB10A2)

Limits: leak <= 0.015, tv <= 0.055, curv <= 0.7, aniso <= 0.03, phase <= 0.03, sigma_err <= 0.02

| sigma | family | us | passes | fetch/px | leak | tv | aniso | phase | curv | params / status |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | direct2d | 216 | 1 | 16.00 | 0.014 | 0.002 | 0.000 | 0.000 | 0.01 | r=3 s=1 |
| 1 | sep_linear | 226 | 2 | 8.00 | 0.014 | 0.002 | 0.000 | 0.000 | 0.01 | r=3 s=1 |
| 1 | sep_bilinear | 226 | 2 | 4.00 | 0.002 | 0.048 | 0.000 | 0.000 | 0.22 | m=2 s=0.954 |
| 1 | kawase | 226 | 2 | 8.00 | 0.002 | 0.048 | 0.000 | 0.000 | 0.22 | 2 passes |
| 1 | dual_filter | 183 | 2 | 9.25 | 0.002 | 0.048 | 0.000 | 0.293 | 0.34 | levels=1 o=0.25 — best tried fails phase |
| 2 | sep_linear | 226 | 2 | 12.00 | 0.011 | 0.025 | 0.000 | 0.000 | 0.18 | r=5 s=2.06 |
| 2 | sep_bilinear | 226 | 2 | 10.00 | 0.010 | 0.032 | 0.000 | 0.000 | 0.23 | m=5 s=2.03 |
| 2 | direct2d | 480 | 1 | 36.00 | 0.011 | 0.025 | 0.000 | 0.000 | 0.17 | r=5 s=2.06 |
| 2 | dual_filter | 183 | 2 | 9.25 | 0.050 | 0.085 | 0.000 | 0.117 | 1.46 | levels=1 o=1.31 — best tried fails leak,tv,curv,phase |
| 2 | kawase | 339 | 3 | 12.00 | 0.064 | 0.117 | 0.000 | 0.000 | 1.23 | 3 passes — best tried fails leak,tv,curv |
| 3 | sep_linear | 226 | 2 | 16.00 | 0.015 | 0.050 | 0.000 | 0.000 | 0.57 | r=7 s=3.2 |
| 3 | sep_bilinear | 226 | 2 | 16.00 | 0.009 | 0.026 | 0.000 | 0.000 | 0.22 | m=8 s=3.06 |
| 3 | pyramid | 209 | 4 | 3.75 | 0.008 | 0.003 | 0.000 | 0.095 | 0.25 | k=1 m=5 s=1.32 up=direct — best tried fails phase |
| 3 | dual_filter | 236 | 4 | 11.56 | 0.004 | 0.024 | 0.001 | 0.159 | 0.24 | levels=2 o=0.658 — best tried fails phase,sigma_err |
| 3 | kawase | 339 | 3 | 12.00 | 0.171 | 0.203 | 0.000 | 0.000 | 3.68 | 3 passes — best tried fails leak,tv,curv |
| 3 | direct2d | 652 | 1 | 49.00 | 0.037 | 0.111 | 0.000 | 0.000 | 1.62 | r=6 s=3.59 — best tried fails leak,tv,curv |
| 4 | dual_filter | 236 | 4 | 11.56 | 0.010 | 0.043 | 0.010 | 0.028 | 0.40 | levels=2 o=1.12 |
| 4 | sep_bilinear | 274 | 2 | 20.00 | 0.013 | 0.044 | 0.000 | 0.000 | 0.46 | m=10 s=4.22 |
| 4 | sep_linear | 300 | 2 | 22.00 | 0.013 | 0.036 | 0.000 | 0.000 | 0.50 | r=10 s=4.18 |
| 4 | pyramid | 209 | 4 | 4.25 | 0.008 | 0.006 | 0.000 | 0.071 | 0.18 | k=1 m=6 s=1.88 up=direct — best tried fails phase |
| 4 | kawase | 452 | 4 | 16.00 | 0.119 | 0.138 | 0.000 | 0.000 | 3.93 | 4 passes — best tried fails leak,tv,curv |
| 4 | direct2d | ≥850 | | | | | | | | rejected (>3x cost) |
| 6 | sep_bilinear | 406 | 2 | 30.00 | 0.013 | 0.047 | 0.000 | 0.000 | 0.64 | m=15 s=6.37 |
| 6 | sep_linear | 459 | 2 | 34.00 | 0.012 | 0.026 | 0.000 | 0.000 | 0.48 | r=16 s=6.19 |
| 6 | pyramid | 214 | 4 | 5.75 | 0.008 | 0.009 | 0.000 | 0.047 | 0.14 | k=1 m=9 s=2.95 up=direct — best tried fails phase |
| 6 | dual_filter | 257 | 6 | 12.14 | 0.005 | 0.022 | 0.000 | 0.223 | 0.24 | levels=3 o=0.585 — best tried fails phase,sigma_err |
| 6 | kawase | 565 | 5 | 20.00 | 0.083 | 0.108 | 0.000 | 0.000 | 4.74 | 5 passes — best tried fails leak,tv,curv |
| 6 | direct2d | ≥1602 | | | | | | | | rejected (>3x cost) |
| 8 | dual_filter | 257 | 6 | 12.14 | 0.006 | 0.037 | 0.005 | 0.015 | 0.31 | levels=3 o=1.08 |
| 8 | sep_bilinear | 538 | 2 | 40.00 | 0.013 | 0.048 | 0.000 | 0.000 | 0.56 | m=20 s=8.52 |
| 8 | sep_linear | 591 | 2 | 44.00 | 0.010 | 0.031 | 0.000 | 0.000 | 0.36 | r=21 s=8.31 |
| 8 | pyramid | 234 | 4 | 7.25 | 0.008 | 0.010 | 0.000 | 0.035 | 0.08 | k=1 m=12 s=3.99 up=direct — best tried fails phase |
| 8 | kawase | 678 | 6 | 24.00 | 0.064 | 0.085 | 0.000 | 0.000 | 2.78 | 6 passes — best tried fails leak,tv,curv |
| 8 | direct2d | ≥2975 | | | | | | | | rejected (>3x cost) |
| 12 | pyramid | 274 | 4 | 10.25 | 0.007 | 0.011 | 0.000 | 0.023 | 0.11 | k=1 m=18 s=6.04 up=chain |
| 12 | dual_filter | 270 | 8 | 12.29 | 0.004 | 0.023 | 0.000 | 0.267 | 0.21 | levels=4 o=0.549 — best tried fails phase,sigma_err |
| 12 | sep_linear | 776 | 2 | 58.00 | 0.016 | 0.070 | 0.000 | 0.000 | 1.23 | r=28 s=13.2 — best tried fails leak,tv,curv |
| 12 | sep_bilinear | 802 | 2 | 60.00 | 0.011 | 0.050 | 0.000 | 0.000 | 0.79 | m=30 s=12.8 — best tried fails curv |
| 12 | kawase | ≥904 | | | | | | | | rejected (>3x cost) |
| 12 | direct2d | ≥6394 | | | | | | | | rejected (>3x cost) |
| 16 | dual_filter | 270 | 8 | 12.29 | 0.005 | 0.036 | 0.002 | 0.011 | 0.30 | levels=4 o=1.07 |
| 16 | pyramid | 313 | 4 | 13.25 | 0.009 | 0.012 | 0.000 | 0.017 | 0.11 | k=1 m=24 s=8.09 up=chain |
| 16 | sep_linear | 776 | 2 | 58.00 | 0.103 | 0.269 | 0.000 | 0.000 | 5.48 | r=28 s=44.2 — best tried fails leak,tv,curv |
| 16 | sep_bilinear | 802 | 2 | 60.00 | 0.072 | 0.213 | 0.000 | 0.000 | 3.07 | m=30 s=27.7 — best tried fails leak,tv,curv |
| 16 | kawase | ≥1130 | | | | | | | | rejected (>3x cost) |
| 16 | direct2d | ≥11107 | | | | | | | | rejected (>3x cost) |
| 24 | pyramid | 196 | 5 | 3.56 | 0.009 | 0.011 | 0.000 | 0.028 | 0.10 | k=2 m=18 s=6.04 up=direct |
| 24 | dual_filter | 281 | 10 | 12.32 | 0.003 | 0.025 | 0.000 | 0.296 | 0.19 | levels=5 o=0.531 — best tried fails phase,sigma_err |
| 24 | sep_bilinear | ≥1119 | | | | | | | | rejected (>3x cost) |
| 24 | sep_linear | ≥1145 | | | | | | | | rejected (>3x cost) |
| 24 | kawase | ≥1356 | | | | | | | | rejected (>3x cost) |
| 32 | pyramid | 206 | 5 | 4.31 | 0.007 | 0.012 | 0.000 | 0.021 | 0.12 | k=2 m=24 s=8.08 up=direct |
| 32 | dual_filter | 281 | 10 | 12.32 | 0.005 | 0.035 | 0.001 | 0.009 | 0.29 | levels=5 o=1.06 |
| 32 | sep_linear | ≥1489 | | | | | | | | rejected (>3x cost) |
| 32 | sep_bilinear | ≥1489 | | | | | | | | rejected (>3x cost) |
| 32 | kawase | ≥1695 | | | | | | | | rejected (>3x cost) |
| 48 | kawase | 2260 | 20 | 80.00 | 0.002 | 0.016 | 0.000 | 0.000 | 0.11 | 20 passes |
| 48 | sep_bilinear | 3152 | 2 | 238.00 | 0.014 | 0.054 | 0.000 | 0.000 | 0.68 | m=119 s=51.5 |
| 48 | sep_linear | 3337 | 2 | 252.00 | 0.013 | 0.038 | 0.000 | 0.000 | 0.50 | r=125 s=50.3 |
| 48 | pyramid | 240 | 12 | 1.67 | 0.009 | 0.013 | 0.000 | 0.149 | 1.31 | k=5 m=5 s=1.26 up=chain warp=iq — best tried fails curv,phase |
| 48 | dual_filter | 291 | 12 | 12.33 | 0.002 | 0.026 | 0.000 | 0.313 | 0.17 | levels=6 o=0.521 — best tried fails phase,sigma_err |
| 64 | pyramid | 183 | 6 | 2.08 | 0.007 | 0.012 | 0.000 | 0.024 | 0.11 | k=3 m=24 s=8.08 up=direct |
| 64 | dual_filter | 291 | 12 | 12.33 | 0.005 | 0.035 | 0.001 | 0.009 | 0.29 | levels=6 o=1.06 |
| 64 | kawase | ≥2712 | | | | | | | | rejected (>3x cost) |
| 64 | sep_bilinear | ≥2941 | | | | | | | | rejected (>3x cost) |
| 64 | sep_linear | ≥2967 | | | | | | | | rejected (>3x cost) |
| 100 | kawase | 3616 | 32 | 128.00 | 0.006 | 0.010 | 0.000 | 0.000 | 0.07 | 32 passes |
| 100 | sep_linear | 6901 | 2 | 522.00 | 0.013 | 0.039 | 0.000 | 0.000 | 0.46 | r=260 s=105 |
| 100 | sep_bilinear | 6901 | 2 | 522.00 | 0.013 | 0.038 | 0.000 | 0.000 | 0.47 | m=261 s=105 |
| 100 | pyramid | 250 | 14 | 1.67 | 0.008 | 0.013 | 0.000 | 0.145 | 1.17 | k=6 m=5 s=1.33 up=chain warp=iq — best tried fails curv,phase |
| 100 | dual_filter | 301 | 14 | 12.33 | 0.005 | 0.023 | 0.000 | 0.185 | 0.32 | levels=7 o=0.585 — best tried fails phase,sigma_err |
| 150 | kawase | 4633 | 41 | 164.00 | 0.006 | 0.007 | 0.000 | 0.000 | 0.05 | 41 passes |
| 150 | sep_bilinear | 9805 | 2 | 742.00 | 0.014 | 0.055 | 0.000 | 0.000 | 0.69 | m=371 s=161 |
| 150 | sep_linear | 9831 | 2 | 744.00 | 0.014 | 0.054 | 0.000 | 0.000 | 0.67 | r=371 s=161 |
| 150 | pyramid | 250 | 14 | 1.67 | 0.008 | 0.010 | 0.000 | 0.094 | 0.57 | k=6 m=7 s=2.21 up=chain warp=iq — best tried fails phase |
| 150 | dual_filter | 301 | 14 | 12.33 | 0.016 | 0.051 | 0.016 | 0.032 | 0.49 | levels=7 o=1.44 — best tried fails leak,phase,sigma_err |
| 200 | kawase | 5650 | 50 | 200.00 | 0.007 | 0.006 | 0.000 | 0.000 | 0.04 | 50 passes |
| 200 | sep_linear | 13765 | 2 | 1042.00 | 0.013 | 0.039 | 0.000 | 0.000 | 0.49 | r=520 s=210 |
| 200 | sep_bilinear | 13792 | 2 | 1044.00 | 0.013 | 0.038 | 0.000 | 0.000 | 0.46 | m=522 s=210 |
| 200 | pyramid | 260 | 16 | 1.67 | 0.008 | 0.013 | 0.000 | 0.146 | 1.13 | k=7 m=5 s=1.33 up=chain warp=iq — best tried fails curv,phase |
| 200 | dual_filter | 311 | 16 | 12.33 | 0.004 | 0.024 | 0.000 | 0.176 | 0.33 | levels=8 o=0.584 — best tried fails phase,sigma_err |
