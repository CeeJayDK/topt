# Stochastic / interleaved sparse blurs (GTX 1660 model, 1080p)

us = marginal cost over a plain composite pass. 'noise-blind' ignores the
shift-variance metrics (phase, block) that measure the static pattern noise.

| sigma | profile | us | design | phase | block | leak | tv | iso | best non-stochastic |
|---:|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | strict | | none | | | | | | - |
| 1 | medium | | none | | | | | | - |
| 1 | loose | | none | | | | | | - |
| 1 | strict noise-blind | | none | | | | | | - |
| 1 | medium noise-blind | | none | | | | | | - |
| 1 | loose noise-blind | | none | | | | | | - |
| 1.5 | strict | | none | | | | | | - |
| 1.5 | medium | | none | | | | | | - |
| 1.5 | loose | | none | | | | | | - |
| 1.5 | strict noise-blind | | none | | | | | | - |
| 1.5 | medium noise-blind | | none | | | | | | - |
| 1.5 | loose noise-blind | | none | | | | | | - |
| 2 | strict | | none | | | | | | - |
| 2 | medium | 131 | down 2 e3 | sot 12 wei k3 tile 2b | up 2 p4 | 0.022 | 0.32 | 0.004 | 0.022 | 0.009 | 121 us |
| 2 | loose | 118 | down 2 e3 | vogel 4 imp k3 tile 2b | up 2 e2 | 0.046 | 0.43 | 0.007 | 0.017 | 0.014 | 121 us |
| 2 | strict noise-blind | | none | | | | | | - |
| 2 | medium noise-blind | 118 | down 2 e3 | vogel 8 wei k3 tile 2b | up 2 e2 | 0.032 | 0.38 | 0.006 | 0.017 | 0.010 | 121 us |
| 2 | loose noise-blind | 118 | down 2 e3 | vogel 4 imp k3 tile 2b | up 2 e2 | 0.046 | 0.43 | 0.007 | 0.017 | 0.014 | 121 us |
| 3 | strict | | none | | | | | | - |
| 3 | medium | | none | | | | | | 144 us |
| 3 | loose | 144 | down 2 e3 | vogel 16 imp k3 tile 2b | up 2 e2 | 0.037 | 0.45 | 0.010 | 0.020 | 0.027 | 144 us |
| 3 | strict noise-blind | | none | | | | | | - |
| 3 | medium noise-blind | | none | | | | | | 144 us |
| 3 | loose noise-blind | 131 | down 2 e3 | vogel 12 imp k3 tile 2b | up 2 e2 | 0.051 | 0.55 | 0.009 | 0.021 | 0.029 | 144 us |
| 4 | strict | | none | | | | | | - |
| 4 | medium | | none | | | | | | 110 us |
| 4 | loose | | none | | | | | | 89 us |
| 4 | strict noise-blind | | none | | | | | | - |
| 4 | medium noise-blind | | none | | | | | | 110 us |
| 4 | loose noise-blind | 81 | down 4 e3 | vogel 12 wei k3 tile 2b | up 4 p4 | 0.095 | 0.71 | 0.007 | 0.021 | 0.004 | 89 us |
| 6 | strict | | none | | | | | | 155 us |
| 6 | medium | | none | | | | | | 84 us |
| 6 | loose | | none | | | | | | 84 us |
| 6 | strict noise-blind | | none | | | | | | 155 us |
| 6 | medium noise-blind | | none | | | | | | 84 us |
| 6 | loose noise-blind | | none | | | | | | 84 us |
| 8 | strict | | none | | | | | | 121 us |
| 8 | medium | | none | | | | | | 86 us |
| 8 | loose | | none | | | | | | 79 us |
| 8 | strict noise-blind | | none | | | | | | 121 us |
| 8 | medium noise-blind | | none | | | | | | 86 us |
| 8 | loose noise-blind | 91 | down 8 e3 | sot 12 wei k3 tile 2b | up 8 p9 | 0.120 | 0.76 | 0.010 | 0.020 | 0.005 | 79 us |
| 12 | strict | | none | | | | | | 91 us |
| 12 | medium | | none | | | | | | 69 us |
| 12 | loose | | none | | | | | | 69 us |
| 12 | strict noise-blind | | none | | | | | | 91 us |
| 12 | medium noise-blind | | none | | | | | | 69 us |
| 12 | loose noise-blind | | none | | | | | | 69 us |
| 16 | strict | | none | | | | | | 96 us |
| 16 | medium | | none | | | | | | 73 us |
| 16 | loose | | none | | | | | | 71 us |
| 16 | strict noise-blind | | none | | | | | | 96 us |
| 16 | medium noise-blind | | none | | | | | | 73 us |
| 16 | loose noise-blind | | none | | | | | | 71 us |
