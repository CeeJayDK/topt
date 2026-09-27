# Baseline sweep (GTX 1660 model, 1920x1080, RGB10A2)

us = marginal cost over a plain composite pass (the last pass is the composite).

Limits: leak <= 0.015, tv <= 0.055, curv <= 0.7, block <= 0.35, aniso <= 0.03, phase <= 0.1, sigma_err <= 0.02

| sigma | family | us | passes | fetch/px | leak | tv | aniso | phase | curv | params / status |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2 | sep_linear | 167 | 2 | 13.00 | 0.011 | 0.025 | 0.000 | 0.000 | 0.18 | r=5 s=2.06 |
| 2 | sep_bilinear | 167 | 2 | 11.00 | 0.010 | 0.032 | 0.000 | 0.000 | 0.23 | m=5 s=2.03 |
| 2 | direct2d | 380 | 1 | 37.00 | 0.011 | 0.025 | 0.000 | 0.000 | 0.17 | r=5 s=2.06 |
| 2 | dual_filter | 86 | 2 | 10.25 | 0.050 | 0.085 | 0.000 | 0.117 | 1.46 | levels=1 o=1.31 — best tried fails leak,tv,curv,block,phase |
| 2 | kawase | 280 | 3 | 13.00 | 0.064 | 0.117 | 0.000 | 0.000 | 1.23 | 3 passes — best tried fails leak,tv,curv |
