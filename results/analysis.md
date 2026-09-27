# Summary: cheapest method per sigma (GTX 1660 model, 1920x1080, RGB10A2)

us = marginal cost over a plain composite pass (blur fused into the consumer pass).

Quality profile: medium (leak<=0.015, tv<=0.055, curv<=0.7, block<=0.35, aniso<=0.03, phase<=0.1, sigma_err<=0.02).
Cost columns re-price every candidate with a different per-pass overhead (model default 5 us).

| sigma | winner @5us | us @2 | us @5 | us @10 | us @20 | winner @20us if different | 10-bit err max/rms (LSB) |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | direct2d | 116 | 116 | 116 | 116 |  |  |
| 2 | hybrid: down 2 e3 | direct 2s | up 2 e3 | 123 | 129 | 139 | 159 |  | 0.57 / 0.13 |
| 3 | hybrid: down 2 e1 | direct 2s | up 2 e1 | 138 | 144 | 154 | 174 |  | 0.65 / 0.19 |
| 4 | hybrid: down 4 e5 | direct 2s | up 2x2 e2 | 101 | 110 | 125 | 155 |  | 0.78 / 0.18 |
| 6 | hybrid: down 4 e3 | direct 2s | up 2x2 e1 | 107 | 116 | 131 | 161 |  | 0.90 / 0.25 |
| 8 | hybrid: down 4 e3 | sep 2s | up 4 e2 | 80 | 89 | 101 | 121 | hybrid: down 4 e3 | direct 2s | up 4 e2 | 0.59 / 0.14 |
| 12 | hybrid: down 4 e1 | sep 2.5s | up 4 e1 | 80 | 89 | 104 | 134 |  | 0.65 / 0.20 |
| 16 | hybrid: down 4x2 e3 | direct 2s | up 8 e1 | 74 | 83 | 98 | 128 |  | 0.59 / 0.20 |
| 24 | hybrid: down 4x2 e1 | sep 2.5s | up 8 e1 | 74 | 86 | 106 | 146 |  | 0.71 / 0.20 |
| 32 | hybrid: down 4x4 e5 | direct 2s | up 16 e1 | 68 | 77 | 92 | 122 |  | 0.59 / 0.20 |
| 48 | hybrid: down 4x4 e1 | direct 2.5s | up 16 e1 | 71 | 80 | 95 | 125 |  | 0.54 / 0.19 |
| 64 | hybrid: down 4x4x2 e3 | direct 2s | up 32 e1 | 70 | 82 | 97 | 127 | hybrid: down 4x4 e1 | direct 2.5s | up 16 e1 | 0.59 / 0.20 |
| 100 | hybrid: down 4x4x2 e1 | direct 2s | up 32 e2 | 70 | 82 | 102 | 142 |  | 0.39 / 0.12 |
| 150 | hybrid: down 4x4x4 e3 | direct 2s | up 64 e1 | 69 | 81 | 101 | 141 |  | 0.53 / 0.21 |
| 200 | hybrid: down 4x4x4 e1 | direct 2s | up 64 e2 | 69 | 81 | 101 | 141 |  | 0.35 / 0.12 |
