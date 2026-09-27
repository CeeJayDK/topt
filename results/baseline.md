# Baseline sweep (GTX 1660 model, 1920x1080, RGB10A2)

Limits: leak <= 0.02, tv <= 0.05, aniso <= 0.03, phase <= 0.03, sigma_err <= 0.02

| sigma | family | us | passes | fetch/px | leak | tv | aniso | phase | params / status |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | direct2d | 216 | 1 | 16.00 | 0.014 | 0.002 | 0.000 | 0.000 | r=3 s=1 |
| 1 | sep_linear | 226 | 2 | 8.00 | 0.014 | 0.002 | 0.000 | 0.000 | r=3 s=1 |
| 1 | sep_bilinear | 226 | 2 | 4.00 | 0.002 | 0.048 | 0.000 | 0.000 | m=2 s=0.954 |
| 1 | kawase | 226 | 2 | 8.00 | 0.002 | 0.048 | 0.000 | 0.000 | 2 passes |
| 1 | dual_filter | 183 | 2 | 9.25 | 0.002 | 0.048 | 0.000 | 0.293 | levels=1 o=0.25 — fails phase |
| 2 | sep_linear | 226 | 2 | 12.00 | 0.011 | 0.025 | 0.000 | 0.000 | r=5 s=2.06 |
| 2 | sep_bilinear | 226 | 2 | 10.00 | 0.010 | 0.032 | 0.000 | 0.000 | m=5 s=2.03 |
| 2 | direct2d | 480 | 1 | 36.00 | 0.011 | 0.025 | 0.000 | 0.000 | r=5 s=2.06 |
| 2 | dual_filter | 183 | 2 | 9.25 | 0.050 | 0.085 | 0.000 | 0.117 | levels=1 o=1.31 — fails leak,tv,phase |
| 2 | kawase | 339 | 3 | 12.00 | 0.064 | 0.117 | 0.000 | 0.000 | 3 passes — fails leak,tv |
| 4 | dual_filter | 236 | 4 | 11.56 | 0.009 | 0.041 | 0.009 | 0.025 | levels=2 o=1.1 |
| 4 | sep_bilinear | 274 | 2 | 20.00 | 0.013 | 0.044 | 0.000 | 0.000 | m=10 s=4.22 |
| 4 | sep_linear | 300 | 2 | 22.00 | 0.013 | 0.036 | 0.000 | 0.000 | r=10 s=4.18 |
| 4 | pyramid | 209 | 4 | 4.25 | 0.009 | 0.006 | 0.000 | 0.071 | k=1 m=6 s=1.88 up=direct — fails phase |
| 4 | kawase | 452 | 4 | 16.00 | 0.119 | 0.138 | 0.000 | 0.000 | 4 passes — fails leak,tv |
| 4 | direct2d | ≥850 | | | | | | | rejected (>3x cost) |
| 8 | dual_filter | 257 | 6 | 12.14 | 0.006 | 0.036 | 0.004 | 0.014 | levels=3 o=1.06 |
| 8 | sep_bilinear | 538 | 2 | 40.00 | 0.013 | 0.048 | 0.000 | 0.000 | m=20 s=8.52 |
| 8 | sep_linear | 564 | 2 | 42.00 | 0.012 | 0.043 | 0.000 | 0.000 | r=20 s=8.45 |
| 8 | pyramid | 234 | 4 | 7.25 | 0.007 | 0.010 | 0.000 | 0.035 | k=1 m=12 s=3.99 up=direct — fails phase |
| 8 | kawase | 678 | 6 | 24.00 | 0.064 | 0.085 | 0.000 | 0.000 | 6 passes — fails leak,tv |
| 8 | direct2d | ≥2975 | | | | | | | rejected (>3x cost) |
| 16 | dual_filter | 270 | 8 | 12.29 | 0.005 | 0.035 | 0.002 | 0.010 | levels=4 o=1.05 |
| 16 | pyramid | 313 | 4 | 13.25 | 0.008 | 0.012 | 0.000 | 0.017 | k=1 m=24 s=8.09 up=chain |
| 16 | sep_linear | 776 | 2 | 58.00 | 0.103 | 0.269 | 0.000 | 0.000 | r=28 s=44.2 — fails leak,tv |
| 16 | sep_bilinear | 802 | 2 | 60.00 | 0.072 | 0.213 | 0.000 | 0.000 | m=30 s=27.7 — fails leak,tv |
| 16 | kawase | ≥1130 | | | | | | | rejected (>3x cost) |
| 16 | direct2d | ≥11107 | | | | | | | rejected (>3x cost) |
