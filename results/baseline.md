# Baseline sweep (GTX 1660 model, 1920x1080, RGB10A2)

Limits: leak <= 0.02, tv <= 0.05, aniso <= 0.03, phase <= 0.03, sigma_err <= 0.02

| sigma | family | us | passes | fetch/px | leak | tv | aniso | phase | params / status |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | direct2d | 216 | 1 | 16.00 | 0.014 | 0.002 | 0.000 | 0.000 | r=3 s=1 |
| 1 | sep_linear | 226 | 2 | 8.00 | 0.014 | 0.002 | 0.000 | 0.000 | r=3 s=1 |
| 1 | sep_bilinear | 226 | 2 | 4.00 | 0.002 | 0.048 | 0.000 | 0.000 | m=2 s=0.954 |
| 1 | kawase | 226 | 2 | 8.00 | 0.002 | 0.048 | 0.000 | 0.000 | 2 passes |
| 1 | dual_filter | 183 | 2 | 9.25 | 0.002 | 0.048 | 0.000 | 0.293 | levels=1 o=0.25 — best tried fails phase |
| 2 | sep_linear | 226 | 2 | 12.00 | 0.011 | 0.025 | 0.000 | 0.000 | r=5 s=2.06 |
| 2 | sep_bilinear | 226 | 2 | 10.00 | 0.010 | 0.032 | 0.000 | 0.000 | m=5 s=2.03 |
| 2 | direct2d | 480 | 1 | 36.00 | 0.011 | 0.025 | 0.000 | 0.000 | r=5 s=2.06 |
| 2 | dual_filter | 183 | 2 | 9.25 | 0.050 | 0.085 | 0.000 | 0.117 | levels=1 o=1.31 — best tried fails leak,tv,phase |
| 2 | kawase | 339 | 3 | 12.00 | 0.064 | 0.117 | 0.000 | 0.000 | 3 passes — best tried fails leak,tv |
| 3 | sep_bilinear | 226 | 2 | 16.00 | 0.009 | 0.026 | 0.000 | 0.000 | m=8 s=3.06 |
| 3 | sep_linear | 248 | 2 | 18.00 | 0.010 | 0.020 | 0.000 | 0.000 | r=8 s=3.07 |
| 3 | pyramid | 209 | 4 | 3.75 | 0.008 | 0.003 | 0.000 | 0.095 | k=1 m=5 s=1.32 up=direct — best tried fails phase |
| 3 | dual_filter | 236 | 4 | 11.56 | 0.004 | 0.024 | 0.001 | 0.159 | levels=2 o=0.658 — best tried fails phase,sigma_err |
| 3 | kawase | 339 | 3 | 12.00 | 0.171 | 0.203 | 0.000 | 0.000 | 3 passes — best tried fails leak,tv |
| 3 | direct2d | 652 | 1 | 49.00 | 0.037 | 0.111 | 0.000 | 0.000 | r=6 s=3.59 — best tried fails leak,tv |
| 4 | dual_filter | 236 | 4 | 11.56 | 0.010 | 0.043 | 0.010 | 0.028 | levels=2 o=1.12 |
| 4 | sep_bilinear | 274 | 2 | 20.00 | 0.013 | 0.044 | 0.000 | 0.000 | m=10 s=4.22 |
| 4 | sep_linear | 300 | 2 | 22.00 | 0.013 | 0.036 | 0.000 | 0.000 | r=10 s=4.18 |
| 4 | pyramid | 209 | 4 | 4.25 | 0.008 | 0.006 | 0.000 | 0.071 | k=1 m=6 s=1.88 up=direct — best tried fails phase |
| 4 | kawase | 452 | 4 | 16.00 | 0.119 | 0.138 | 0.000 | 0.000 | 4 passes — best tried fails leak,tv |
| 4 | direct2d | ≥850 | | | | | | | rejected (>3x cost) |
| 6 | sep_bilinear | 406 | 2 | 30.00 | 0.013 | 0.047 | 0.000 | 0.000 | m=15 s=6.37 |
| 6 | sep_linear | 432 | 2 | 32.00 | 0.012 | 0.041 | 0.000 | 0.000 | r=15 s=6.32 |
| 6 | pyramid | 214 | 4 | 5.75 | 0.008 | 0.009 | 0.000 | 0.047 | k=1 m=9 s=2.95 up=direct — best tried fails phase |
| 6 | dual_filter | 257 | 6 | 12.14 | 0.005 | 0.022 | 0.000 | 0.223 | levels=3 o=0.585 — best tried fails phase,sigma_err |
| 6 | kawase | 565 | 5 | 20.00 | 0.083 | 0.108 | 0.000 | 0.000 | 5 passes — best tried fails leak,tv |
| 6 | direct2d | ≥1602 | | | | | | | rejected (>3x cost) |
| 8 | dual_filter | 257 | 6 | 12.14 | 0.006 | 0.037 | 0.005 | 0.015 | levels=3 o=1.08 |
| 8 | sep_bilinear | 538 | 2 | 40.00 | 0.013 | 0.048 | 0.000 | 0.000 | m=20 s=8.52 |
| 8 | sep_linear | 564 | 2 | 42.00 | 0.012 | 0.043 | 0.000 | 0.000 | r=20 s=8.45 |
| 8 | pyramid | 234 | 4 | 7.25 | 0.008 | 0.010 | 0.000 | 0.035 | k=1 m=12 s=3.99 up=direct — best tried fails phase |
| 8 | kawase | 678 | 6 | 24.00 | 0.064 | 0.085 | 0.000 | 0.000 | 6 passes — best tried fails leak,tv |
| 8 | direct2d | ≥2975 | | | | | | | rejected (>3x cost) |
| 12 | pyramid | 274 | 4 | 10.25 | 0.007 | 0.011 | 0.000 | 0.023 | k=1 m=18 s=6.04 up=chain |
| 12 | sep_bilinear | 802 | 2 | 60.00 | 0.011 | 0.050 | 0.000 | 0.000 | m=30 s=12.8 |
| 12 | dual_filter | 270 | 8 | 12.29 | 0.004 | 0.023 | 0.000 | 0.267 | levels=4 o=0.549 — best tried fails phase,sigma_err |
| 12 | sep_linear | 776 | 2 | 58.00 | 0.016 | 0.070 | 0.000 | 0.000 | r=28 s=13.2 — best tried fails tv |
| 12 | kawase | ≥904 | | | | | | | rejected (>3x cost) |
| 12 | direct2d | ≥6394 | | | | | | | rejected (>3x cost) |
| 16 | dual_filter | 270 | 8 | 12.29 | 0.005 | 0.036 | 0.002 | 0.011 | levels=4 o=1.07 |
| 16 | pyramid | 313 | 4 | 13.25 | 0.009 | 0.012 | 0.000 | 0.017 | k=1 m=24 s=8.09 up=chain |
| 16 | sep_linear | 776 | 2 | 58.00 | 0.103 | 0.269 | 0.000 | 0.000 | r=28 s=44.2 — best tried fails leak,tv |
| 16 | sep_bilinear | 802 | 2 | 60.00 | 0.072 | 0.213 | 0.000 | 0.000 | m=30 s=27.7 — best tried fails leak,tv |
| 16 | kawase | ≥1130 | | | | | | | rejected (>3x cost) |
| 16 | direct2d | ≥11107 | | | | | | | rejected (>3x cost) |
| 24 | pyramid | 196 | 5 | 3.56 | 0.009 | 0.011 | 0.000 | 0.028 | k=2 m=18 s=6.04 up=direct |
| 24 | dual_filter | 281 | 10 | 12.32 | 0.003 | 0.025 | 0.000 | 0.296 | levels=5 o=0.531 — best tried fails phase,sigma_err |
| 24 | sep_bilinear | ≥1119 | | | | | | | rejected (>3x cost) |
| 24 | sep_linear | ≥1145 | | | | | | | rejected (>3x cost) |
| 24 | kawase | ≥1356 | | | | | | | rejected (>3x cost) |
| 32 | pyramid | 206 | 5 | 4.31 | 0.007 | 0.012 | 0.000 | 0.021 | k=2 m=24 s=8.08 up=direct |
| 32 | dual_filter | 281 | 10 | 12.32 | 0.005 | 0.035 | 0.001 | 0.009 | levels=5 o=1.06 |
| 32 | sep_linear | ≥1489 | | | | | | | rejected (>3x cost) |
| 32 | sep_bilinear | ≥1489 | | | | | | | rejected (>3x cost) |
| 32 | kawase | ≥1695 | | | | | | | rejected (>3x cost) |
| 48 | dual_filter | 281 | 10 | 12.32 | 0.020 | 0.049 | 0.001 | 0.004 | levels=5 o=1.78 |
| 48 | pyramid | 240 | 12 | 1.67 | 0.009 | 0.013 | 0.000 | 0.149 | k=5 m=5 s=1.26 up=chain warp=iq — best tried fails phase |
| 48 | sep_linear | ≥2228 | | | | | | | rejected (>3x cost) |
| 48 | sep_bilinear | ≥2228 | | | | | | | rejected (>3x cost) |
| 48 | kawase | ≥2260 | | | | | | | rejected (>3x cost) |
| 64 | pyramid | 183 | 6 | 2.08 | 0.007 | 0.012 | 0.000 | 0.024 | k=3 m=24 s=8.08 up=direct |
| 64 | dual_filter | 291 | 12 | 12.33 | 0.005 | 0.035 | 0.001 | 0.009 | levels=6 o=1.06 |
| 64 | kawase | ≥2712 | | | | | | | rejected (>3x cost) |
| 64 | sep_bilinear | ≥2941 | | | | | | | rejected (>3x cost) |
| 64 | sep_linear | ≥2967 | | | | | | | rejected (>3x cost) |
| 100 | dual_filter | 291 | 12 | 12.33 | 0.020 | 0.049 | 0.000 | 0.003 | levels=6 o=1.86 |
| 100 | pyramid | 250 | 14 | 1.67 | 0.008 | 0.013 | 0.000 | 0.145 | k=6 m=5 s=1.33 up=chain warp=iq — best tried fails phase |
| 100 | kawase | ≥3616 | | | | | | | rejected (>3x cost) |
| 100 | sep_linear | ≥4604 | | | | | | | rejected (>3x cost) |
| 100 | sep_bilinear | ≥4604 | | | | | | | rejected (>3x cost) |
| 150 | kawase | 4633 | 41 | 164.00 | 0.006 | 0.007 | 0.000 | 0.000 | 41 passes |
| 150 | sep_bilinear | 10386 | 2 | 786.00 | 0.013 | 0.037 | 0.000 | 0.000 | m=393 s=157 |
| 150 | sep_linear | 10412 | 2 | 788.00 | 0.013 | 0.037 | 0.000 | 0.000 | r=393 s=157 |
| 150 | pyramid | 250 | 14 | 1.67 | 0.008 | 0.010 | 0.000 | 0.094 | k=6 m=7 s=2.21 up=chain warp=iq — best tried fails phase |
| 150 | dual_filter | 301 | 14 | 12.33 | 0.016 | 0.051 | 0.016 | 0.032 | levels=7 o=1.44 — best tried fails tv,phase,sigma_err |
| 200 | dual_filter | 301 | 14 | 12.33 | 0.019 | 0.049 | 0.000 | 0.002 | levels=7 o=1.86 |
| 200 | pyramid | 260 | 16 | 1.67 | 0.008 | 0.013 | 0.000 | 0.146 | k=7 m=5 s=1.33 up=chain warp=iq — best tried fails phase |
| 200 | kawase | ≥5650 | | | | | | | rejected (>3x cost) |
| 200 | sep_linear | ≥9171 | | | | | | | rejected (>3x cost) |
| 200 | sep_bilinear | ≥9171 | | | | | | | rejected (>3x cost) |
