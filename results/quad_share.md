# Quad sharing (ddx_fine / ddy_fine) vs the single-pass pinwheel (GTX 1660 model, 1080p)

us = marginal cost over a plain composite pass (texture reads only). The exchange costs
12 scalar derivatives per pixel whatever the read count, plus 12 MAD per read; the
composite is memory-bound, so this ALU is expected to hide. 'pinwheel' = TOPT_Blur size 1.

| sigma | quad: reads (samples) | quality | us | phase | block | pinwheel reads | pinwheel us |
|---:|---|---|---:|---:|---:|---:|---:|
| 0.7 | 3 (12) | medium | 0 | 0.009 | 0.05 | 9 | 30 |
| 0.8 | 3 (12) | medium | 0 | 0.015 | 0.10 | 9 | 30 |
| 0.9 | 4 (16) | strict | 0 | 0.009 | 0.07 | 9 | 30 |
| 1.0 | 5 (20) | medium | 0 | 0.007 | 0.05 | 13 | 84 |
| 1.1 | 4 (16) | medium | 0 | 0.018 | 0.12 | 13 | 84 |
| 1.2 | 5 (20) | medium | 0 | 0.026 | 0.24 | 17 | 137 |
| 1.3 | none up to 6 reads | | | | | 17 | 137 |
| 1.5 | none up to 6 reads | | | | | - | - |
