# Summary: cheapest method per sigma (GTX 1660 model, 1920x1080, RGB10A2)

us = marginal cost over a plain composite pass (blur fused into the consumer pass).

Quality profile: medium (leak<=0.012, tv<=0.032, curv<=0.4, block<=0.35, aniso<=0.03, phase<=0.1, iso<=0.032, sigma_err<=0.02).
Cost columns re-price every candidate with a different per-pass overhead (model default 5 us).

| sigma | winner @5us | us @2 | us @5 | us @10 | us @20 | winner @20us if different | 10-bit err max/rms (LSB) |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | direct2d | 116 | 116 | 116 | 116 |  |  |
| 2 | hybrid: down 2 e3 | direct 2s | up 2 p4 | 115 | 121 | 131 | 151 |  | 0.71 / 0.20 |
| 3 | hybrid: down 2 e1 | direct 2s | up 2 e2 | 138 | 144 | 154 | 174 |  | 0.54 / 0.13 |
| 4 | hybrid: down 4 e9 | direct 2s | up 2x2 e2 | 101 | 110 | 125 | 154 |  | 0.79 / 0.18 |
| 6 | hybrid: down 4 e5 | direct 2s | up 4 p5 | 78 | 84 | 94 | 114 |  | 0.60 / 0.18 |
| 8 | hybrid: down 8 e9 | sep 3s | up 2x4 p5 | 74 | 86 | 104 | 130 | hybrid: down 4 e1 | direct 2.5s | up 4 p4 | 1.12 / 0.27 |
| 12 | hybrid: down 8 e3 | direct 2s | up 8 p4 | 63 | 69 | 79 | 99 |  | 0.58 / 0.18 |
| 16 | hybrid: down 8 e1 | direct 2.5s | up 8 p4 | 65 | 73 | 83 | 103 |  | 0.54 / 0.18 |
| 24 | hybrid: down 16 e3 | direct 2s | up 16 p4 | 59 | 65 | 75 | 95 |  | 0.57 / 0.18 |
| 32 | hybrid: down 16 e3 | direct 2.5s | up 16 p4 | 60 | 66 | 76 | 96 |  | 0.49 / 0.18 |
| 48 | hybrid: down 16 e1 | direct 2.5s | up 16 e1 | 61 | 68 | 78 | 98 |  | 0.54 / 0.19 |
| 64 | hybrid: down 16x2 e9 | direct 2s | up 32 p4 | 61 | 70 | 80 | 100 | hybrid: down 16 e1 | direct 2.5s | up 16 e1 | 0.50 / 0.18 |
| 100 | hybrid: down 16x4 e9 | direct 2s | up 64 p4 | 60 | 69 | 84 | 114 |  | 0.46 / 0.18 |
| 150 | hybrid: down 16x4 e1 | direct 2.5s | up 64 p4 | 60 | 69 | 84 | 114 |  | 0.46 / 0.18 |
| 200 | hybrid: down 16x4 e1 | direct 2.5s | up 64 e1 | 60 | 69 | 84 | 114 |  | 0.51 / 0.19 |
