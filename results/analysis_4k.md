# Summary: cheapest method per sigma (GTX 1660 model, 3840x2160, RGB10A2)

us = marginal cost over a plain composite pass (blur fused into the consumer pass).

Quality profile: medium (leak<=0.012, tv<=0.032, curv<=0.4, block<=0.35, aniso<=0.03, phase<=0.1, iso<=0.032, sigma_err<=0.02).
Cost columns re-price every candidate with a different per-pass overhead (model default 5 us).

| sigma | winner @5us | us @2 | us @5 | us @10 | us @20 | winner @20us if different | 10-bit err max/rms (LSB) |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | direct2d | 466 | 466 | 466 | 466 |  |  |
| 2 | hybrid: down 2 e3 | direct 2s | up 2 p4 | 447 | 453 | 463 | 483 |  | 0.71 / 0.20 |
| 3 | hybrid: down 2 e1 | direct 2s | up 2 e2 | 539 | 545 | 555 | 575 |  | 0.54 / 0.13 |
| 4 | hybrid: down 4 e9 | direct 2s | up 2x2 e2 | 384 | 393 | 408 | 438 |  | 0.79 / 0.18 |
| 6 | hybrid: down 4 e5 | direct 2s | up 4 p5 | 300 | 306 | 316 | 336 |  | 0.60 / 0.18 |
| 8 | hybrid: down 8 e9 | sep 3s | up 2x4 p5 | 271 | 283 | 303 | 343 |  | 1.12 / 0.27 |
| 12 | hybrid: down 8 e3 | direct 2s | up 8 p4 | 240 | 246 | 256 | 276 |  | 0.58 / 0.18 |
| 16 | hybrid: down 16 e9 | sep 2s | up 2x8 p5 | 236 | 248 | 266 | 292 | hybrid: down 8 e1 | direct 2.5s | up 8 p4 | 1.06 / 0.28 |
| 24 | hybrid: down 16 e3 | direct 2s | up 16 p4 | 225 | 231 | 241 | 261 |  | 0.57 / 0.18 |
| 32 | hybrid: down 16 e3 | direct 2.5s | up 16 p4 | 227 | 235 | 245 | 265 |  | 0.49 / 0.18 |
| 48 | hybrid: down 16x2 e3 | direct 2s | up 32 p4 | 225 | 234 | 249 | 274 | hybrid: down 16 e1 | direct 2.5s | up 16 e1 | 0.57 / 0.19 |
| 64 | hybrid: down 16x2 e9 | direct 2s | up 32 p4 | 226 | 235 | 250 | 280 |  | 0.50 / 0.18 |
| 100 | hybrid: down 16x4 e9 | direct 2s | up 64 p4 | 224 | 233 | 248 | 278 |  | 0.46 / 0.18 |
| 150 | hybrid: down 16x4 e1 | direct 2.5s | up 64 p4 | 224 | 233 | 248 | 278 |  | 0.46 / 0.18 |
| 200 | hybrid: down 16x8 e3 | direct 2.5s | up 128 p4 | 224 | 233 | 248 | 278 |  | 0.37 / 0.15 |
