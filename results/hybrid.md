# Hybrid down/blur/up search (GTX 1660 model, 1920x1080, RGB10A2)

us = marginal cost over a plain composite pass (the last pass is the composite).

Profiles: **strict** leak<=0.01, tv<=0.02, curv<=0.2, block<=0.1, aniso<=0.03, phase<=0.01, sigma_err<=0.02; **medium** leak<=0.015, tv<=0.055, curv<=0.7, block<=0.35, aniso<=0.03, phase<=0.1, sigma_err<=0.02; **loose** leak<=0.02, tv<=0.1, curv<=1.7, block<=0.45, aniso<=0.05, phase<=0.15, sigma_err<=0.03

## Cheapest design per profile

| sigma | profile | us | passes | leak | tv | phase | curv | design | best baseline |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| 2 | strict | | | | | | | none found | none |
| 2 | medium | 121 | 3 | 0.012 | 0.008 | 0.023 | 0.35 | down 2 e3 | direct 2s | up 2 p4 | sep_linear 167 us |
| 2 | loose | 121 | 3 | 0.012 | 0.008 | 0.023 | 0.38 | down 2 e3 | direct 2s | up 2 e1 | sep_linear 167 us |
| 3 | strict | | | | | | | none found | none |
| 3 | medium | 144 | 3 | 0.009 | 0.037 | 0.092 | 0.38 | down 2 e1 | direct 2s | up 2 e1 | pyramid 150 us |
| 3 | loose | 144 | 3 | 0.009 | 0.037 | 0.092 | 0.38 | down 2 e1 | direct 2s | up 2 e1 | pyramid 150 us |
| 4 | strict | | | | | | | none found | none |
| 4 | medium | 110 | 4 | 0.004 | 0.013 | 0.023 | 0.29 | down 4 e9 | direct 2s | up 2x2 e2 | dual_filter 139 us |
| 4 | loose | 89 | 4 | 0.005 | 0.027 | 0.026 | 0.49 | down 4 e9 | sep 2s | up 4 p5 | dual_filter 139 us |
| 6 | strict | 150 | 4 | 0.008 | 0.020 | 0.001 | 0.17 | down 2 e3 | sep 2.5s | up 2 p5 | none |
| 6 | medium | 84 | 3 | 0.006 | 0.026 | 0.025 | 0.40 | down 4 e5 | direct 2s | up 4 p5 | pyramid 155 us |
| 6 | loose | 84 | 3 | 0.006 | 0.029 | 0.045 | 0.47 | down 4 e3 | direct 2s | up 4 p4 | pyramid 155 us |
| 8 | strict | 121 | 5 | 0.007 | 0.011 | 0.005 | 0.11 | down 4 e9 | sep 2.5s | up 2x2 e2 | none |
| 8 | medium | 86 | 5 | 0.002 | 0.027 | 0.055 | 0.36 | down 8 e9 | sep 3s | up 2x4 p5 | pyramid 153 us |
| 8 | loose | 79 | 4 | 0.007 | 0.009 | 0.040 | 0.45 | down 4x2 e3 | direct 2s | up 8 p5 | pyramid 153 us |
| 12 | strict | 89 | 4 | 0.009 | 0.017 | 0.004 | 0.12 | down 4 e9 | sep 2.5s | up 4 e2 | none |
| 12 | medium | 69 | 3 | 0.005 | 0.028 | 0.059 | 0.34 | down 8 e3 | direct 2s | up 8 p4 | pyramid 123 us |
| 12 | loose | 69 | 3 | 0.005 | 0.029 | 0.128 | 0.32 | down 8 e1 | direct 2s | up 8 p5 | pyramid 123 us |
| 16 | strict | 95 | 5 | 0.007 | 0.015 | 0.002 | 0.10 | down 4x2 e9 | direct 2s | up 2x4 e2 | none |
| 16 | medium | 71 | 3 | 0.012 | 0.052 | 0.042 | 0.49 | down 8 e3 | direct 2s | up 8 p4 | pyramid 128 us |
| 16 | loose | 71 | 3 | 0.012 | 0.054 | 0.093 | 0.57 | down 8 e1 | direct 2s | up 8 p4 | pyramid 128 us |
| 24 | strict | 84 | 5 | 0.007 | 0.011 | 0.007 | 0.18 | down 4x4 e9 | direct 2s | up 2x8 e2 | none |
| 24 | medium | 65 | 3 | 0.005 | 0.028 | 0.067 | 0.34 | down 16 e3 | direct 2s | up 16 p4 | pyramid 118 us |
| 24 | loose | 65 | 3 | 0.005 | 0.028 | 0.067 | 0.34 | down 16 e3 | direct 2s | up 16 p4 | pyramid 118 us |
| 32 | strict | 76 | 4 | 0.006 | 0.010 | 0.009 | 0.07 | down 8 e9 | sep 3s | up 8 e1 | none |
| 32 | medium | 66 | 3 | 0.012 | 0.052 | 0.048 | 0.48 | down 16 e3 | direct 2s | up 16 p4 | pyramid 119 us |
| 32 | loose | 65 | 3 | 0.007 | 0.039 | 0.100 | 0.42 | down 16 e1 | direct 2s | up 16 e2 | pyramid 119 us |
| 48 | strict | 75 | 4 | 0.010 | 0.011 | 0.007 | 0.09 | down 8x2 e9 | direct 2.5s | up 16 e1 | none |
| 48 | medium | 68 | 3 | 0.009 | 0.016 | 0.067 | 0.15 | down 16 e1 | direct 2.5s | up 16 e1 | pyramid 121 us |
| 48 | loose | 67 | 3 | 0.017 | 0.073 | 0.065 | 0.73 | down 16 e1 | direct 2s | up 16 e2 | pyramid 121 us |
| 64 | strict | 77 | 5 | 0.008 | 0.012 | 0.007 | 0.12 | down 8x4 e9 | direct 2.5s | up 2x16 e1 | none |
| 64 | medium | 70 | 4 | 0.008 | 0.046 | 0.028 | 0.39 | down 16x2 e3 | direct 2s | up 32 p4 | pyramid 121 us |
| 64 | loose | 69 | 4 | 0.009 | 0.051 | 0.103 | 0.53 | down 16x2 e1 | direct 2s | up 32 p5 | pyramid 121 us |
| 100 | strict | 71 | 4 | 0.007 | 0.016 | 0.009 | 0.12 | down 16x2 e9 | direct 2.5s | up 32 e1 | none |
| 100 | medium | 69 | 4 | 0.007 | 0.037 | 0.037 | 0.38 | down 16x4 e3 | direct 2s | up 64 p4 | pyramid 122 us |
| 100 | loose | 69 | 4 | 0.007 | 0.037 | 0.037 | 0.38 | down 16x4 e3 | direct 2s | up 64 p4 | pyramid 122 us |
| 150 | strict | 70 | 4 | 0.009 | 0.014 | 0.007 | 0.11 | down 16x4 e9 | direct 2.5s | up 64 p4 | none |
| 150 | medium | 69 | 4 | 0.008 | 0.038 | 0.089 | 0.37 | down 16x4 e1 | direct 2s | up 64 e2 | pyramid 125 us |
| 150 | loose | 69 | 4 | 0.008 | 0.038 | 0.089 | 0.37 | down 16x4 e1 | direct 2s | up 64 e2 | pyramid 125 us |
| 200 | strict | 70 | 4 | 0.006 | 0.018 | 0.010 | 0.13 | down 16x4 e5 | direct 2.5s | up 64 e2 | none |
| 200 | medium | 69 | 4 | 0.010 | 0.043 | 0.066 | 0.39 | down 16x4 e1 | direct 2s | up 64 e2 | pyramid 125 us |
| 200 | loose | 69 | 4 | 0.012 | 0.050 | 0.066 | 0.57 | down 16x4 e1 | direct 2s | up 64 e1 | pyramid 125 us |

## Cost vs shift-variance Pareto front (candidates also meeting the other 'medium' limits)

**sigma 2**: 121 us / phase 0.017 (down 2 e5 | direct 2s | up 2 p5), 133 us / phase 0.017 (down 2 e9 | direct 2s | up 2 p5)

**sigma 3**: 144 us / phase 0.004 (down 2 e5 | direct 2s | up 2 p5), 150 us / phase 0.004 (down 2 e5 | sep 2s | up 2 p5)

**sigma 4**: 110 us / phase 0.023 (down 4 e9 | direct 2s | up 2x2 e2), 142 us / phase 0.008 (down 2x2 e5 | direct 2s | up 2x2 e2), 150 us / phase 0.002 (down 2 e5 | sep 2.5s | up 2 p5), 165 us / phase 0.001 (down 2 e9 | sep 2s | up 2 p5), 189 us / phase 0.001 (down 2 e9 | direct 2s | up 2 p5)

**sigma 6**: 84 us / phase 0.010 (down 4 e9 | direct 2s | up 4 p5), 89 us / phase 0.010 (down 4 e9 | sep 2s | up 4 p5), 116 us / phase 0.004 (down 2x2 e5 | direct 2s | up 4 p5), 121 us / phase 0.004 (down 2x2 e5 | sep 2s | up 4 p5), 148 us / phase 0.001 (down 2x2 e5 | direct 2s | up 2x2 e2), 150 us / phase 0.000 (down 2 e5 | sep 2.5s | up 2 p5)

**sigma 8**: 86 us / phase 0.055 (down 8 e9 | sep 3s | up 2x4 p5), 89 us / phase 0.006 (down 4 e9 | sep 2.5s | up 4 p5), 121 us / phase 0.002 (down 2x2 e5 | sep 2s | up 4 p5)

**sigma 12**: 69 us / phase 0.030 (down 8 e9 | direct 2s | up 8 p5), 74 us / phase 0.029 (down 8 e9 | sep 2s | up 8 p5), 81 us / phase 0.012 (down 4x2 e5 | direct 2s | up 8 p5), 82 us / phase 0.005 (down 4x2 e9 | direct 2s | up 8 p5), 87 us / phase 0.005 (down 4x2 e9 | sep 2s | up 8 p5), 89 us / phase 0.003 (down 4 e9 | sep 2.5s | up 4 p5)

**sigma 16**: 71 us / phase 0.021 (down 8 e9 | direct 2s | up 8 p5), 73 us / phase 0.021 (down 8 e9 | direct 2.5s | up 8 p5), 74 us / phase 0.020 (down 8 e9 | sep 2.5s | up 8 p5), 83 us / phase 0.008 (down 4x2 e5 | direct 2s | up 8 p5), 84 us / phase 0.003 (down 4x2 e9 | direct 2s | up 8 p5), 87 us / phase 0.003 (down 4x2 e9 | sep 2s | up 8 p5)

**sigma 24**: 65 us / phase 0.037 (down 16 e9 | direct 2s | up 16 p5), 70 us / phase 0.036 (down 16 e9 | sep 2s | up 16 p5), 72 us / phase 0.022 (down 8x2 e5 | direct 2s | up 16 p5), 72 us / phase 0.014 (down 8x2 e9 | direct 2s | up 16 p5), 74 us / phase 0.013 (down 8 e9 | sep 2.5s | up 8 p5), 77 us / phase 0.008 (down 4x4 e9 | direct 2s | up 16 p5)

**sigma 32**: 66 us / phase 0.026 (down 16 e9 | direct 2s | up 16 p5), 72 us / phase 0.016 (down 8x2 e5 | direct 2s | up 16 p5), 73 us / phase 0.010 (down 8x2 e9 | direct 2s | up 16 p5), 75 us / phase 0.009 (down 8 e9 | sep 2.5s | up 8 p5)

**sigma 48**: 68 us / phase 0.067 (down 16 e1 | direct 2.5s | up 16 p5), 69 us / phase 0.016 (down 16 e9 | direct 2.5s | up 16 p5), 70 us / phase 0.016 (down 16 e9 | sep 2.5s | up 16 p5), 71 us / phase 0.011 (down 8x4 e9 | direct 2s | up 32 p5), 74 us / phase 0.007 (down 8x2 e9 | direct 2s | up 16 e2), 75 us / phase 0.006 (down 8x2 e9 | direct 2.5s | up 16 p5)

**sigma 64**: 70 us / phase 0.020 (down 16x2 e5 | direct 2s | up 32 p5), 70 us / phase 0.014 (down 16x2 e9 | direct 2s | up 32 p5), 70 us / phase 0.012 (down 16 e9 | sep 2.5s | up 16 p5), 71 us / phase 0.007 (down 8x4 e9 | direct 2s | up 32 p5), 71 us / phase 0.007 (down 8x4 e9 | direct 2.5s | up 32 p5), 76 us / phase 0.007 (down 8x4 e9 | sep 2.5s | up 32 p5)

**sigma 100**: 69 us / phase 0.012 (down 16x4 e9 | direct 2s | up 64 p5), 71 us / phase 0.009 (down 16x2 e9 | direct 2.5s | up 32 p5), 71 us / phase 0.008 (down 16 e9 | sep 2.5s | up 16 e2), 72 us / phase 0.004 (down 8x4 e9 | direct 2s | up 32 p5), 72 us / phase 0.004 (down 8x4 e9 | direct 2.5s | up 32 p5)

**sigma 150**: 69 us / phase 0.089 (down 16x4 e1 | direct 2s | up 64 e2), 70 us / phase 0.007 (down 16x4 e9 | direct 2s | up 64 p5), 70 us / phase 0.007 (down 16x4 e9 | direct 2.5s | up 64 p5)

**sigma 200**: 69 us / phase 0.066 (down 16x4 e1 | direct 2s | up 64 e2), 69 us / phase 0.018 (down 16x8 e9 | direct 2s | up 128 p5), 70 us / phase 0.005 (down 16x4 e9 | direct 2s | up 64 p5), 70 us / phase 0.005 (down 16x4 e9 | direct 2.5s | up 64 p5), 70 us / phase 0.005 (down 16x4 e9 | direct 3s | up 64 p5)

