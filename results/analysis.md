# Summary: cheapest method per sigma (GTX 1660 model, 1080p, RGB10A2)

Quality profile: medium (leak<=0.015, tv<=0.055, curv<=0.7, block<=0.35, aniso<=0.03, phase<=0.1, sigma_err<=0.02).
Cost columns re-price every candidate with a different per-pass overhead (model default 5 us).

| sigma | winner @5us | us @2 | us @5 | us @10 | us @20 | winner @20us if different | 10-bit err max/rms (LSB) |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | cs_tile r=3 (T=8, mem-bound) | 110 | 113 | 118 | 128 |  |  |
| 2 | cs_tile r=5 (T=16, mem-bound) | 110 | 113 | 118 | 128 |  |  |
| 3 | cs_tile r=7 (T=32, lds-bound) | 123 | 126 | 131 | 141 |  |  |
| 4 | hybrid: down 4 e5 | direct 2s | up 2x2 e2 | 157 | 169 | 189 | 202 | cs_tile r=10 (T=32, lds-bound) | 1.23 / 0.34 |
| 6 | hybrid: down 4 e3 | direct 2s | up 2x2 e1 | 163 | 175 | 195 | 235 |  | 1.39 / 0.40 |
| 8 | hybrid: down 4 e3 | sep 2s | up 4 e2 | 136 | 148 | 165 | 195 | hybrid: down 4 e3 | direct 2s | up 4 e2 | 1.06 / 0.32 |
| 12 | hybrid: down 4 e1 | sep 2.5s | up 4 e1 | 136 | 148 | 168 | 208 |  | 1.14 / 0.36 |
| 16 | hybrid: down 4x2 e3 | direct 2s | up 8 e1 | 130 | 142 | 162 | 202 |  | 1.08 / 0.35 |
| 24 | hybrid: down 4x2 e1 | sep 2.5s | up 8 e1 | 130 | 145 | 170 | 220 |  | 1.15 / 0.35 |
| 32 | hybrid: down 4x4 e5 | direct 2s | up 16 e1 | 124 | 136 | 156 | 196 |  | 1.06 / 0.35 |
| 48 | hybrid: down 4x4 e1 | direct 2.5s | up 16 e1 | 126 | 139 | 159 | 199 |  | 1.03 / 0.34 |
| 64 | hybrid: down 4x4x2 e3 | direct 2s | up 32 e1 | 126 | 141 | 161 | 201 | hybrid: down 4x4 e1 | direct 2.5s | up 16 e1 | 1.05 / 0.35 |
| 100 | hybrid: down 4x4x2 e1 | direct 2s | up 32 e2 | 126 | 141 | 166 | 216 |  | 0.86 / 0.31 |
| 150 | hybrid: down 4x4x4 e3 | direct 2s | up 64 e1 | 125 | 140 | 165 | 215 |  | 1.01 / 0.36 |
| 200 | hybrid: down 4x4x4 e1 | direct 2s | up 64 e2 | 125 | 140 | 165 | 215 |  | 0.83 / 0.31 |
