# Quad sharing (ddx_fine / ddy_fine) vs the single-pass pinwheel (GTX 1660 model, 1080p)

us = marginal cost over a plain composite pass: the reads plus 4 float3 quad exchanges
(TexBench's measured exchange cost; the 12 MAD per read are not counted, the composite
is memory-bound). 'pinwheel' = TOPT_Blur size 1.

| sigma | quad: reads (samples) | quality | us | phase | block | pinwheel reads | pinwheel us |
|---:|---|---|---:|---:|---:|---:|---:|
| 0.7 | 3 (12) | medium | 9 | 0.009 | 0.05 | 9 | 74 |
| 0.8 | 3 (12) | medium | 9 | 0.015 | 0.10 | 9 | 74 |
| 0.9 | 4 (16) | strict | 22 | 0.009 | 0.07 | 9 | 74 |
| 1.0 | 5 (20) | medium | 34 | 0.007 | 0.05 | 13 | 123 |
| 1.1 | 4 (16) | medium | 22 | 0.018 | 0.12 | 13 | 123 |
| 1.2 | 5 (20) | medium | 34 | 0.026 | 0.24 | 17 | 172 |
| 1.3 | none up to 6 reads | | | | | 17 | 172 |
| 1.5 | none up to 6 reads | | | | | - | - |
