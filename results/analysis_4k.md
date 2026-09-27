# Summary: cheapest method per sigma (GTX 1660 model, 3840x2160, RGB10A2)

us = marginal cost over a plain composite pass (blur fused into the consumer pass).

Quality profile: medium (leak<=0.015, tv<=0.055, curv<=0.7, block<=0.35, aniso<=0.03, phase<=0.1, sigma_err<=0.02).
Cost columns re-price every candidate with a different per-pass overhead (model default 5 us).

| sigma | winner @5us | us @2 | us @5 | us @10 | us @20 | winner @20us if different | 10-bit err max/rms (LSB) |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | direct2d | 466 | 466 | 466 | 466 |  |  |
| 2 | hybrid: down 2 e3 | direct 2s | up 2 e3 | 478 | 484 | 494 | 514 |  | 0.57 / 0.13 |
| 3 | hybrid: down 2 e1 | direct 2s | up 2 e1 | 539 | 545 | 555 | 575 |  | 0.65 / 0.19 |
| 4 | hybrid: down 4 e5 | direct 2s | up 2x2 e2 | 387 | 396 | 411 | 441 |  | 0.78 / 0.18 |
| 6 | hybrid: down 4 e3 | direct 2s | up 2x2 e1 | 410 | 419 | 434 | 464 |  | 0.90 / 0.25 |
| 8 | hybrid: down 4 e3 | sep 2s | up 4 e2 | 303 | 312 | 327 | 357 |  | 0.59 / 0.14 |
| 12 | hybrid: down 4 e1 | sep 2.5s | up 4 e1 | 303 | 312 | 327 | 357 |  | 0.65 / 0.20 |
| 16 | hybrid: down 4x2 e3 | sep 2s | up 8 e2 | 271 | 283 | 300 | 330 | hybrid: down 4x2 e3 | direct 2s | up 8 e1 | 0.57 / 0.14 |
| 24 | hybrid: down 4x2 e1 | sep 2.5s | up 8 e1 | 271 | 283 | 303 | 343 |  | 0.71 / 0.20 |
| 32 | hybrid: down 4x4 e5 | direct 2s | up 16 e1 | 256 | 265 | 280 | 310 |  | 0.59 / 0.20 |
| 48 | hybrid: down 4x4 e1 | sep 2.5s | up 16 e1 | 256 | 268 | 288 | 328 |  | 0.61 / 0.19 |
| 64 | hybrid: down 4x4x2 e3 | direct 2s | up 32 e1 | 254 | 266 | 286 | 326 |  | 0.59 / 0.20 |
| 100 | hybrid: down 4x4x2 e1 | direct 2s | up 32 e2 | 256 | 268 | 288 | 328 |  | 0.39 / 0.12 |
| 150 | hybrid: down 4x4x4 e3 | direct 2s | up 64 e1 | 253 | 265 | 285 | 325 |  | 0.53 / 0.21 |
| 200 | hybrid: down 4x4x4 e1 | direct 2s | up 64 e2 | 254 | 266 | 286 | 326 |  | 0.35 / 0.12 |
