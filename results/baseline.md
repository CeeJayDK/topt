# Baseline sweep (GTX 1660 model, 1920x1080, RGB10A2)

Limits: leak <= 0.02, tv <= 0.05, aniso <= 0.03, phase <= 0.03, curv <= 1.5, sigma_err <= 0.02

| sigma | family | us | passes | fetch/px | leak | tv | aniso | phase | curv | params / status |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2 | sep_linear | 226 | 2 | 12.00 | 0.011 | 0.025 | 0.000 | 0.000 | 0.18 | r=5 s=2.06 |
| 2 | sep_bilinear | 226 | 2 | 10.00 | 0.010 | 0.032 | 0.000 | 0.000 | 0.23 | m=5 s=2.03 |
| 2 | direct2d | 480 | 1 | 36.00 | 0.011 | 0.025 | 0.000 | 0.000 | 0.17 | r=5 s=2.06 |
| 2 | dual_filter | 183 | 2 | 9.25 | 0.050 | 0.085 | 0.000 | 0.117 | 1.48 | levels=1 o=1.31 — best tried fails leak,tv,phase |
| 2 | kawase | 339 | 3 | 12.00 | 0.064 | 0.117 | 0.000 | 0.000 | 1.23 | 3 passes — best tried fails leak,tv |
