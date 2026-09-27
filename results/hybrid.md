# Hybrid down/blur/up search (GTX 1660 model, 1920x1080, RGB10A2)

Profiles: **strict** leak<=0.01, tv<=0.02, curv<=0.2, aniso<=0.03, phase<=0.01, sigma_err<=0.02; **medium** leak<=0.015, tv<=0.055, curv<=0.7, aniso<=0.03, phase<=0.03, sigma_err<=0.02; **loose** leak<=0.02, tv<=0.1, curv<=1.7, aniso<=0.05, phase<=0.06, sigma_err<=0.03

## Cheapest design per profile

| sigma | profile | us | passes | leak | tv | phase | curv | design | best baseline |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| 2 | strict | | | | | | | none found | none |
| 2 | medium | 180 | 3 | 0.012 | 0.008 | 0.023 | 0.38 | down 2 e3 | direct 2s | up 2 e1 | sep_linear 226 us |
| 2 | loose | 180 | 3 | 0.012 | 0.008 | 0.023 | 0.38 | down 2 e3 | direct 2s | up 2 e1 | sep_linear 226 us |
| 3 | strict | | | | | | | none found | none |
| 3 | medium | 203 | 3 | 0.007 | 0.027 | 0.005 | 0.28 | down 2 e3 | direct 2s | up 2 e1 | sep_linear 226 us |
| 3 | loose | 200 | 5 | 0.010 | 0.018 | 0.054 | 0.63 | down 2x2 e3 | direct 2s | up 2x2 e1 | sep_linear 226 us |
| 4 | strict | 209 | 4 | 0.007 | 0.013 | 0.002 | 0.19 | down 2 e3 | sep 2.5s | up 2 e2 | none |
| 4 | medium | 200 | 5 | 0.004 | 0.014 | 0.015 | 0.29 | down 2x2 e3 | direct 2s | up 2x2 e2 | dual_filter 236 us |
| 4 | loose | 137 | 3 | 0.011 | 0.012 | 0.053 | 0.96 | down 4 e5 | direct 2s | up 4 e1 | dual_filter 236 us |
| 6 | strict | 207 | 5 | 0.006 | 0.010 | 0.003 | 0.15 | down 2x2 e3 | direct 2s | up 2x2 e2 | none |
| 6 | medium | 175 | 4 | 0.007 | 0.025 | 0.025 | 0.29 | down 4 e5 | direct 2s | up 2x2 e1 | sep_bilinear 406 us |
| 6 | loose | 143 | 3 | 0.006 | 0.032 | 0.046 | 0.92 | down 4 e3 | direct 2s | up 4 e1 | pyramid 214 us |
| 8 | strict | 212 | 6 | 0.007 | 0.010 | 0.001 | 0.07 | down 2x2 e3 | sep 2.5s | up 2x2 e2 | none |
| 8 | medium | 148 | 4 | 0.007 | 0.014 | 0.018 | 0.30 | down 4 e5 | sep 2.5s | up 4 e2 | dual_filter 257 us |
| 8 | loose | 138 | 4 | 0.010 | 0.016 | 0.033 | 0.98 | down 4x2 e5 | direct 2s | up 8 e2 | pyramid 234 us |
| 12 | strict | 180 | 5 | 0.009 | 0.020 | 0.002 | 0.14 | down 2x2 e3 | sep 2.5s | up 4 e1 | none |
| 12 | medium | 140 | 4 | 0.007 | 0.025 | 0.024 | 0.65 | down 4x2 e3 | direct 2s | up 8 e1 | pyramid 274 us |
| 12 | loose | 140 | 4 | 0.007 | 0.025 | 0.024 | 0.65 | down 4x2 e3 | direct 2s | up 8 e1 | pyramid 274 us |
| 16 | strict | 155 | 4 | 0.008 | 0.010 | 0.008 | 0.07 | down 4 e5 | sep 3s | up 4 e1 | none |
| 16 | medium | 142 | 4 | 0.009 | 0.049 | 0.017 | 0.48 | down 4x2 e3 | direct 2s | up 8 e1 | dual_filter 270 us |
| 16 | loose | 136 | 4 | 0.011 | 0.012 | 0.046 | 0.97 | down 4x4 e5 | direct 2s | up 16 e1 | dual_filter 270 us |
| 24 | strict | 145 | 5 | 0.007 | 0.018 | 0.006 | 0.13 | down 4x2 e5 | sep 2.5s | up 8 e1 | none |
| 24 | medium | 136 | 4 | 0.006 | 0.029 | 0.020 | 0.65 | down 4x4 e5 | direct 2s | up 16 e1 | pyramid 196 us |
| 24 | loose | 136 | 4 | 0.006 | 0.030 | 0.035 | 0.66 | down 4x4 e3 | direct 2s | up 16 e1 | pyramid 196 us |
| 32 | strict | 146 | 5 | 0.006 | 0.010 | 0.008 | 0.06 | down 4x2 e3 | sep 3s | up 8 e1 | none |
| 32 | medium | 136 | 4 | 0.012 | 0.054 | 0.024 | 0.61 | down 4x4 e3 | direct 2s | up 16 e1 | pyramid 206 us |
| 32 | loose | 136 | 4 | 0.012 | 0.054 | 0.024 | 0.61 | down 4x4 e3 | direct 2s | up 16 e1 | pyramid 206 us |
| 48 | strict | 139 | 4 | 0.007 | 0.016 | 0.007 | 0.15 | down 4x4 e5 | direct 2.5s | up 16 e1 | kawase 2260 us |
| 48 | medium | 139 | 4 | 0.006 | 0.016 | 0.015 | 0.16 | down 4x4 e3 | direct 2.5s | up 16 e1 | kawase 2260 us |
| 48 | loose | 138 | 4 | 0.016 | 0.073 | 0.015 | 0.67 | down 4x4 e3 | direct 2s | up 16 e2 | kawase 2260 us |
| 64 | strict | 141 | 5 | 0.010 | 0.010 | 0.005 | 0.07 | down 4x4 e5 | sep 3s | up 16 e1 | none |
| 64 | medium | 141 | 5 | 0.009 | 0.048 | 0.013 | 0.43 | down 4x4x2 e3 | direct 2s | up 32 e1 | pyramid 183 us |
| 64 | loose | 140 | 5 | 0.010 | 0.013 | 0.055 | 1.00 | down 4x4x4 e3 | direct 2s | up 64 e1 | pyramid 183 us |
| 100 | strict | 141 | 5 | 0.005 | 0.018 | 0.008 | 0.13 | down 4x4x2 e3 | direct 2.5s | up 32 e2 | kawase 3616 us |
| 100 | medium | 140 | 5 | 0.008 | 0.041 | 0.024 | 0.62 | down 4x4x4 e3 | direct 2s | up 64 e1 | kawase 3616 us |
| 100 | loose | 140 | 5 | 0.008 | 0.041 | 0.024 | 0.62 | down 4x4x4 e3 | direct 2s | up 64 e1 | kawase 3616 us |
| 150 | strict | 140 | 5 | 0.007 | 0.016 | 0.007 | 0.20 | down 4x4x4 e5 | direct 2.5s | up 64 e1 | kawase 4633 us |
| 150 | medium | 140 | 5 | 0.012 | 0.049 | 0.013 | 0.48 | down 4x4x4 e3 | direct 2s | up 64 e1 | kawase 4633 us |
| 150 | loose | 140 | 5 | 0.012 | 0.049 | 0.013 | 0.48 | down 4x4x4 e3 | direct 2s | up 64 e1 | dual_filter 301 us |
| 200 | strict | 140 | 5 | 0.006 | 0.019 | 0.009 | 0.14 | down 4x4x4 e3 | direct 2.5s | up 64 e2 | kawase 5650 us |
| 200 | medium | 140 | 5 | 0.012 | 0.050 | 0.009 | 0.48 | down 4x4x4 e3 | direct 2s | up 64 e1 | kawase 5650 us |
| 200 | loose | 140 | 5 | 0.012 | 0.050 | 0.009 | 0.48 | down 4x4x4 e3 | direct 2s | up 64 e1 | kawase 5650 us |

## Cost vs shift-variance Pareto front (candidates also meeting the other 'medium' limits)

**sigma 2**: 180 us / phase 0.019 (down 2 e5 | direct 2s | up 2 e1), 209 us / phase 0.017 (down 2 e5 | sep 3s | up 2 e1)

**sigma 3**: 168 us / phase 0.091 (down 4 e5 | direct 2s | up 2x2 e1), 200 us / phase 0.054 (down 2x2 e3 | direct 2s | up 2x2 e1), 203 us / phase 0.005 (down 2 e5 | direct 2s | up 2 e1), 209 us / phase 0.005 (down 2 e5 | sep 2s | up 2 e1)

**sigma 4**: 169 us / phase 0.047 (down 4 e5 | direct 2s | up 2x2 e2), 200 us / phase 0.008 (down 2x2 e5 | direct 2s | up 2x2 e2), 209 us / phase 0.002 (down 2 e5 | sep 2s | up 2 e2)

**sigma 6**: 175 us / phase 0.025 (down 4 e5 | direct 2s | up 2x2 e2), 180 us / phase 0.025 (down 4 e5 | sep 2s | up 2x2 e1), 207 us / phase 0.001 (down 2x2 e5 | direct 2s | up 2x2 e2), 209 us / phase 0.001 (down 2 e5 | sep 2.5s | up 2 e2)

**sigma 8**: 148 us / phase 0.018 (down 4 e5 | sep 2.5s | up 4 e2), 150 us / phase 0.018 (down 4 e5 | direct 2s | up 4 e2), 180 us / phase 0.005 (down 2x2 e5 | sep 2s | up 4 e1), 212 us / phase 0.000 (down 2x2 e5 | sep 2s | up 2x2 e2)

**sigma 12**: 140 us / phase 0.015 (down 4x2 e5 | direct 2s | up 8 e1), 145 us / phase 0.015 (down 4x2 e5 | sep 2s | up 8 e1), 148 us / phase 0.011 (down 4 e5 | sep 2.5s | up 4 e2), 172 us / phase 0.010 (down 2x2x2 e3 | direct 2s | up 8 e1), 180 us / phase 0.002 (down 2x2 e5 | sep 2.5s | up 4 e1)

**sigma 16**: 142 us / phase 0.010 (down 4x2 e5 | direct 2s | up 8 e2), 145 us / phase 0.010 (down 4x2 e5 | sep 2s | up 8 e2), 151 us / phase 0.008 (down 4 e5 | sep 2.5s | up 4 e2)

**sigma 24**: 136 us / phase 0.137 (down 4x4 e1 | direct 2s | up 16 e1), 136 us / phase 0.020 (down 4x4 e5 | direct 2s | up 16 e1), 141 us / phase 0.020 (down 4x4 e5 | sep 2s | up 16 e1), 143 us / phase 0.012 (down 4x2x2 e5 | direct 2s | up 16 e1), 145 us / phase 0.006 (down 4x2 e5 | sep 2.5s | up 8 e1)

**sigma 32**: 136 us / phase 0.100 (down 4x4 e1 | direct 2s | up 16 e2), 136 us / phase 0.012 (down 4x4 e5 | direct 2s | up 16 e2), 141 us / phase 0.012 (down 4x4 e5 | sep 2s | up 16 e2), 143 us / phase 0.007 (down 4x2x2 e5 | direct 2s | up 16 e1), 146 us / phase 0.004 (down 4x2 e5 | sep 2.5s | up 8 e2)

**sigma 48**: 139 us / phase 0.067 (down 4x4 e1 | direct 2.5s | up 16 e1), 139 us / phase 0.007 (down 4x4 e5 | direct 2.5s | up 16 e2), 141 us / phase 0.007 (down 4x4 e5 | sep 2.5s | up 16 e2)

**sigma 64**: 141 us / phase 0.103 (down 4x4x2 e1 | direct 2s | up 32 e1), 141 us / phase 0.007 (down 4x4x2 e5 | direct 2s | up 32 e2), 141 us / phase 0.005 (down 4x4 e5 | sep 2.5s | up 16 e2)

**sigma 100**: 140 us / phase 0.137 (down 4x4x4 e1 | direct 2s | up 64 e1), 140 us / phase 0.015 (down 4x4x4 e5 | direct 2s | up 64 e1), 141 us / phase 0.004 (down 4x4x2 e5 | direct 2s | up 32 e1), 141 us / phase 0.004 (down 4x4x2 e5 | direct 2.5s | up 32 e2), 142 us / phase 0.003 (down 4x4 e5 | sep 2.5s | up 16 e2)

**sigma 150**: 140 us / phase 0.089 (down 4x4x4 e1 | direct 2s | up 64 e1), 140 us / phase 0.007 (down 4x4x4 e5 | direct 2s | up 64 e2), 142 us / phase 0.002 (down 4x4x2 e5 | direct 2.5s | up 32 e2), 143 us / phase 0.002 (down 4x4 e5 | sep 2.5s | up 16 e2), 143 us / phase 0.002 (down 4x4 e5 | sep 3s | up 16 e2)

**sigma 200**: 140 us / phase 0.066 (down 4x4x4 e1 | direct 2s | up 64 e2), 140 us / phase 0.004 (down 4x4x4 e5 | direct 2s | up 64 e2)

