# Hybrid down/blur/up search (GTX 1660 model, 1920x1080, RGB10A2)

us = marginal cost over a plain composite pass (the last pass is the composite).

Profiles: **strict** leak<=0.01, tv<=0.02, curv<=0.2, block<=0.1, aniso<=0.03, phase<=0.01, sigma_err<=0.02; **medium** leak<=0.015, tv<=0.055, curv<=0.7, block<=0.35, aniso<=0.03, phase<=0.1, sigma_err<=0.02; **loose** leak<=0.02, tv<=0.1, curv<=1.7, block<=0.45, aniso<=0.05, phase<=0.15, sigma_err<=0.03

## Cheapest design per profile

| sigma | profile | us | passes | leak | tv | phase | curv | design | best baseline |
|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| 2 | strict | | | | | | | none found | none |
| 2 | medium | 129 | 3 | 0.005 | 0.024 | 0.022 | 0.38 | down 2 e3 | direct 2s | up 2 e3 | sep_linear 167 us |
| 2 | loose | 121 | 3 | 0.012 | 0.008 | 0.023 | 0.38 | down 2 e3 | direct 2s | up 2 e1 | sep_linear 167 us |
| 3 | strict | | | | | | | none found | none |
| 3 | medium | 144 | 3 | 0.009 | 0.037 | 0.092 | 0.38 | down 2 e1 | direct 2s | up 2 e1 | pyramid 150 us |
| 3 | loose | 144 | 3 | 0.009 | 0.037 | 0.092 | 0.38 | down 2 e1 | direct 2s | up 2 e1 | pyramid 150 us |
| 4 | strict | | | | | | | none found | none |
| 4 | medium | 110 | 4 | 0.005 | 0.012 | 0.047 | 0.30 | down 4 e5 | direct 2s | up 2x2 e2 | dual_filter 139 us |
| 4 | loose | 110 | 4 | 0.005 | 0.011 | 0.075 | 0.30 | down 4 e3 | direct 2s | up 2x2 e2 | dual_filter 139 us |
| 6 | strict | | | | | | | none found | none |
| 6 | medium | 116 | 4 | 0.008 | 0.027 | 0.045 | 0.31 | down 4 e3 | direct 2s | up 2x2 e1 | pyramid 155 us |
| 6 | loose | 116 | 4 | 0.008 | 0.030 | 0.111 | 0.34 | down 4 e1 | direct 2s | up 2x2 e1 | pyramid 155 us |
| 8 | strict | 153 | 6 | 0.007 | 0.010 | 0.001 | 0.07 | down 2x2 e3 | sep 2.5s | up 2x2 e2 | none |
| 8 | medium | 89 | 4 | 0.005 | 0.050 | 0.033 | 0.48 | down 4 e3 | sep 2s | up 4 e2 | pyramid 153 us |
| 8 | loose | 89 | 4 | 0.006 | 0.053 | 0.081 | 0.52 | down 4 e1 | sep 2s | up 4 e2 | pyramid 153 us |
| 12 | strict | 121 | 5 | 0.009 | 0.020 | 0.002 | 0.14 | down 2x2 e3 | sep 2.5s | up 4 e1 | none |
| 12 | medium | 89 | 4 | 0.010 | 0.022 | 0.055 | 0.17 | down 4 e1 | sep 2.5s | up 4 e1 | pyramid 123 us |
| 12 | loose | 89 | 4 | 0.010 | 0.022 | 0.055 | 0.17 | down 4 e1 | sep 2.5s | up 4 e1 | pyramid 123 us |
| 16 | strict | 96 | 4 | 0.008 | 0.010 | 0.008 | 0.07 | down 4 e5 | sep 3s | up 4 e1 | none |
| 16 | medium | 83 | 4 | 0.009 | 0.049 | 0.017 | 0.48 | down 4x2 e3 | direct 2s | up 8 e1 | pyramid 128 us |
| 16 | loose | 83 | 4 | 0.006 | 0.040 | 0.094 | 0.43 | down 4x2 e1 | direct 2s | up 8 e2 | pyramid 128 us |
| 24 | strict | 86 | 5 | 0.007 | 0.018 | 0.006 | 0.13 | down 4x2 e5 | sep 2.5s | up 8 e1 | none |
| 24 | medium | 86 | 5 | 0.008 | 0.021 | 0.063 | 0.23 | down 4x2 e1 | sep 2.5s | up 8 e1 | pyramid 118 us |
| 24 | loose | 86 | 5 | 0.008 | 0.021 | 0.063 | 0.23 | down 4x2 e1 | sep 2.5s | up 8 e1 | pyramid 118 us |
| 32 | strict | 87 | 5 | 0.006 | 0.010 | 0.008 | 0.06 | down 4x2 e3 | sep 3s | up 8 e1 | none |
| 32 | medium | 77 | 4 | 0.010 | 0.053 | 0.013 | 0.50 | down 4x4 e5 | direct 2s | up 16 e1 | pyramid 119 us |
| 32 | loose | 77 | 4 | 0.007 | 0.039 | 0.100 | 0.39 | down 4x4 e1 | direct 2s | up 16 e2 | pyramid 119 us |
| 48 | strict | 80 | 4 | 0.004 | 0.013 | 0.007 | 0.10 | down 4x4 e5 | direct 2.5s | up 16 e2 | none |
| 48 | medium | 80 | 4 | 0.007 | 0.016 | 0.067 | 0.15 | down 4x4 e1 | direct 2.5s | up 16 e1 | pyramid 121 us |
| 48 | loose | 79 | 4 | 0.017 | 0.073 | 0.065 | 0.73 | down 4x4 e1 | direct 2s | up 16 e2 | pyramid 121 us |
| 64 | strict | 82 | 5 | 0.010 | 0.010 | 0.005 | 0.07 | down 4x4 e5 | sep 3s | up 16 e1 | none |
| 64 | medium | 82 | 5 | 0.009 | 0.048 | 0.013 | 0.43 | down 4x4x2 e3 | direct 2s | up 32 e1 | pyramid 121 us |
| 64 | loose | 82 | 5 | 0.006 | 0.039 | 0.103 | 0.37 | down 4x4x2 e1 | direct 2s | up 32 e2 | pyramid 121 us |
| 100 | strict | 82 | 5 | 0.005 | 0.018 | 0.008 | 0.13 | down 4x4x2 e3 | direct 2.5s | up 32 e2 | none |
| 100 | medium | 82 | 5 | 0.007 | 0.043 | 0.065 | 0.39 | down 4x4x2 e1 | direct 2s | up 32 e2 | pyramid 122 us |
| 100 | loose | 82 | 5 | 0.019 | 0.081 | 0.004 | 0.74 | down 4x4x2 e5 | direct 2s | up 32 e2 | pyramid 122 us |
| 150 | strict | 84 | 5 | 0.009 | 0.008 | 0.005 | 0.05 | down 4x4x2 e3 | direct 3s | up 32 e2 | none |
| 150 | medium | 81 | 5 | 0.012 | 0.049 | 0.013 | 0.48 | down 4x4x4 e3 | direct 2s | up 64 e1 | pyramid 125 us |
| 150 | loose | 81 | 5 | 0.008 | 0.038 | 0.089 | 0.37 | down 4x4x4 e1 | direct 2s | up 64 e2 | pyramid 125 us |
| 200 | strict | 81 | 5 | 0.006 | 0.019 | 0.009 | 0.14 | down 4x4x4 e3 | direct 2.5s | up 64 e2 | none |
| 200 | medium | 81 | 5 | 0.010 | 0.043 | 0.066 | 0.39 | down 4x4x4 e1 | direct 2s | up 64 e2 | pyramid 125 us |
| 200 | loose | 81 | 5 | 0.012 | 0.050 | 0.066 | 0.57 | down 4x4x4 e1 | direct 2s | up 64 e1 | pyramid 125 us |

## Cost vs shift-variance Pareto front (candidates also meeting the other 'medium' limits)

**sigma 2**: 129 us / phase 0.022 (down 2 e3 | direct 2s | up 2 e3), 150 us / phase 0.017 (down 2 e5 | sep 3s | up 2 e1)

**sigma 3**: 144 us / phase 0.005 (down 2 e5 | direct 2s | up 2 e1), 150 us / phase 0.005 (down 2 e5 | sep 2s | up 2 e1)

**sigma 4**: 110 us / phase 0.047 (down 4 e5 | direct 2s | up 2x2 e2), 142 us / phase 0.008 (down 2x2 e5 | direct 2s | up 2x2 e2), 150 us / phase 0.002 (down 2 e5 | sep 2s | up 2 e2), 174 us / phase 0.002 (down 2 e5 | direct 2s | up 2 e2)

**sigma 6**: 116 us / phase 0.025 (down 4 e5 | direct 2s | up 2x2 e2), 121 us / phase 0.025 (down 4 e5 | sep 2s | up 2x2 e1), 148 us / phase 0.001 (down 2x2 e5 | direct 2s | up 2x2 e2), 150 us / phase 0.001 (down 2 e5 | sep 2.5s | up 2 e2)

**sigma 8**: 89 us / phase 0.018 (down 4 e5 | sep 2.5s | up 4 e2), 121 us / phase 0.005 (down 2x2 e5 | sep 2s | up 4 e1), 153 us / phase 0.000 (down 2x2 e5 | sep 2s | up 2x2 e2)

**sigma 12**: 89 us / phase 0.011 (down 4 e5 | sep 2.5s | up 4 e2), 110 us / phase 0.011 (down 4 e5 | sep 2.5s | up 4 e3), 121 us / phase 0.002 (down 2x2 e5 | sep 2.5s | up 4 e1)

**sigma 16**: 83 us / phase 0.010 (down 4x2 e5 | direct 2s | up 8 e2), 86 us / phase 0.010 (down 4x2 e5 | sep 2s | up 8 e2), 92 us / phase 0.008 (down 4 e5 | sep 2.5s | up 4 e2)

**sigma 24**: 86 us / phase 0.006 (down 4x2 e5 | sep 2.5s | up 8 e1)

**sigma 32**: 77 us / phase 0.012 (down 4x4 e5 | direct 2s | up 16 e2), 84 us / phase 0.007 (down 4x2x2 e5 | direct 2s | up 16 e1), 87 us / phase 0.004 (down 4x2 e5 | sep 2.5s | up 8 e2)

**sigma 48**: 80 us / phase 0.067 (down 4x4 e1 | direct 2.5s | up 16 e1), 80 us / phase 0.007 (down 4x4 e5 | direct 2.5s | up 16 e2)

**sigma 64**: 82 us / phase 0.007 (down 4x4x2 e5 | direct 2s | up 32 e2), 82 us / phase 0.005 (down 4x4 e5 | sep 2.5s | up 16 e2)

**sigma 100**: 82 us / phase 0.065 (down 4x4x2 e1 | direct 2s | up 32 e2), 82 us / phase 0.004 (down 4x4x2 e5 | direct 2s | up 32 e1), 82 us / phase 0.004 (down 4x4x2 e5 | direct 2.5s | up 32 e2), 83 us / phase 0.003 (down 4x4 e5 | sep 2.5s | up 16 e2)

**sigma 150**: 81 us / phase 0.007 (down 4x4x4 e5 | direct 2s | up 64 e2), 83 us / phase 0.002 (down 4x4x2 e5 | direct 2.5s | up 32 e2), 84 us / phase 0.002 (down 4x4 e5 | sep 2.5s | up 16 e2), 84 us / phase 0.002 (down 4x4 e5 | sep 3s | up 16 e2)

**sigma 200**: 81 us / phase 0.066 (down 4x4x4 e1 | direct 2s | up 64 e2), 81 us / phase 0.004 (down 4x4x4 e5 | direct 2s | up 64 e2)

