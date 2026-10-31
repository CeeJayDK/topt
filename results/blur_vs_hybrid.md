# TOPT_Blur against the hybrid search, per GPU

TOPT_Blur's class for each GPU profile (its per-GPU table rule) against the cheapest hybrid design
meeting the medium profile on that GPU (results/hybrid_gpu_best.json). us = marginal cost over the
GPU's plain composite pass; gain = (TOPT_Blur - hybrid) in % of the composite pass.

## 1080p

| sigma | median gain | worst GPU for TOPT_Blur | TOPT_Blur us | hybrid us | hybrid design |
|---:|---:|---|---:|---:|---|
| 2 | +0.0 % | RTX 2070 (2): +53.7 % | 91 | 65 | down 2 e3 / sep 2s / up 2 e1 |
| 3 | +5.8 % | RTX 2070 (2 sep): +67.1 % | 103 | 71 | down 2 e5 / sep 2s / up 2 e1 |
| 4 | +3.5 % | RTX 2070 (4s): +8.4 % | 82 | 78 | down 2 e1 / sep 2.5s / up 2 e1 |
| 6 | +23.7 % | RTX 2070 (4s sep): +71.1 % | 83 | 50 | down 4 e5 / sep 2s / up 2x2 e1 |
| 8 | +18.0 % | RTX 2070 (4 sep): +75.8 % | 75 | 39 | down 4 e3 / sep 2.5s / up 4 e1 |
| 12 | +35.2 % | RTX 2070 (4 sep): +87.0 % | 77 | 36 | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 16 | +2.8 % | RTX 2070 (8 sep): +54.6 % | 60 | 34 | down 8 e3 / sep 2.5s / up 8 e1 |
| 24 | +9.1 % | RTX 2070 (8 sep): +57.4 % | 61 | 33 | down 16 e3 / direct 2s / up 2x8 e1 |
| 32 | +6.8 % | GTX 1660 (16 sep): +107.7 % | 180 | 64 | down 8x2 e9 / direct 2s / up 16 e1 |
| 48 | +11.9 % | GTX 1660 (16 sep): +110.8 % | 180 | 62 | down 8x2 e1 / sep 2.5s / up 16 e1 |
| 64 | +11.8 % | GTX 1660 (32 sep): +113.5 % | 184 | 63 | down 8x2 e1 / sep 3s / up 16 e1 |
| 100 | +12.5 % | GTX 1660 (32 sep): +112.9 % | 185 | 64 | down 8x4 e1 / sep 2.5s / up 32 e1 |
| 150 | +12.0 % | GTX 1660 (64 sep): +110.8 % | 184 | 66 | down 8x4 e1 / sep 3s / up 32 e1 |
| 200 | +12.4 % | GTX 1660 (64 sep): +111.0 % | 185 | 66 | down 8x4x2 e1 / sep 2.5s / up 64 e1 |

## 4k

| sigma | median gain | worst GPU for TOPT_Blur | TOPT_Blur us | hybrid us | hybrid design |
|---:|---:|---|---:|---:|---|
| 2 | +0.0 % | RTX 2070 (2): +56.1 % | 356 | 252 | down 2 e3 / sep 2s / up 2 e1 |
| 3 | +5.2 % | RTX 2070 (2 sep): +68.2 % | 404 | 277 | down 2 e5 / sep 2s / up 2 e1 |
| 4 | +4.0 % | RTX 2070 (4s): +13.6 % | 328 | 302 | down 2 e1 / sep 2.5s / up 2 e1 |
| 6 | +19.4 % | RTX 2070 (4s sep): +72.5 % | 340 | 205 | down 4 e5 / sep 2s / up 2x2 e1 |
| 8 | +18.9 % | RTX 2070 (4 sep): +77.0 % | 310 | 167 | down 4 e3 / sep 2.5s / up 4 e1 |
| 12 | +37.1 % | RTX 2070 (4 sep): +96.2 % | 318 | 139 | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 16 | +3.0 % | RTX 2070 (8 sep): +55.5 % | 231 | 128 | down 8 e3 / sep 2.5s / up 8 e1 |
| 24 | +7.7 % | RTX 2070 (8 sep): +58.3 % | 233 | 125 | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | +2.6 % | RTX 2070 (16 sep): +53.6 % | 225 | 125 | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 48 | +4.0 % | RTX 2070 (32): +54.2 % | 224 | 124 | down 16x2 e3 / direct 2s / up 2x16 e1 |
| 64 | +2.3 % | RTX 2070 (32): +54.2 % | 225 | 124 | down 16x2 e3 / direct 2.5s / up 2x16 e1 |
| 100 | +3.1 % | RTX 2070 (32): +55.4 % | 226 | 123 | down 16x4 e3 / direct 2.5s / up 2x32 e1 |
| 150 | +2.2 % | RTX 2070 (64): +54.4 % | 223 | 122 | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 200 | +2.3 % | RTX 2070 (64): +54.4 % | 224 | 122 | down 16x4 e1 / direct 2.5s / up 64 e1 |

## Every GPU

| sigma | res | GPU | TOPT_Blur class | TOPT_Blur us | hybrid us | gain | hybrid design |
|---:|---|---|---|---:|---:|---:|---|
| 2 | 1080p | RX 6600 | 2 | 90 | 86 | +4.7 % | down 2 e9 / direct 2s / up 2 p4 |
| 2 | 4k | RX 6600 | 2 | 356 | 340 | +4.8 % | down 2 e9 / direct 2s / up 2 p4 |
| 2 | 1080p | RX 7900 XTX | 2 | 16 | 16 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RX 7900 XTX | 2 | 55 | 53 | +3.0 % | down 2 e3 / sep 2s / up 2 e1 |
| 2 | 1080p | RX 9070 XT | 2 | 19 | 19 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RX 9070 XT | 2 | 68 | 68 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | Radeon 680M | 2 | 383 | 381 | +0.7 % | down 2 e3 / direct 2s / up 2 e3 |
| 2 | 4k | Radeon 680M | 2 | 1498 | 1488 | +0.7 % | down 2 e3 / direct 2s / up 2 e3 |
| 2 | 1080p | RX 5500 XT | 2 | 105 | 105 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RX 5500 XT | 2 | 411 | 411 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | RX 590 | 2 | 88 | 88 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RX 590 | 2 | 343 | 343 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | Arc B580 | 2 | 50 | 50 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | Arc B580 | 2 | 190 | 190 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | Iris Xe | 2 | 1242 | 1242 | +0.0 % | down 2 e3 / direct 2s / up 2 e3 |
| 2 | 4k | Iris Xe | 2 | 4949 | 4949 | +0.0 % | down 2 e3 / direct 2s / up 2 e3 |
| 2 | 1080p | UHD 630 | 2 | 810 | 792 | +3.0 % | down 2 e3 / sep 2s / up 2 e1 |
| 2 | 4k | UHD 630 | 2 | 3214 | 3126 | +3.5 % | down 2 e3 / sep 2s / up 2 e1 |
| 2 | 1080p | GTX 1080 | 2 | 61 | 61 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | GTX 1080 | 2 | 237 | 237 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | GTX 1660 | 2 | 126 | 126 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | GTX 1660 | 2 | 498 | 498 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | GTX 860M | 2 | 280 | 280 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | GTX 860M | 2 | 1115 | 1115 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | RTX 2070 | 2 | 91 | 65 | +53.7 % | down 2 e3 / sep 2s / up 2 e1 |
| 2 | 4k | RTX 2070 | 2 | 356 | 252 | +56.1 % | down 2 e3 / sep 2s / up 2 e1 |
| 2 | 1080p | RTX 3060 | 2 | 60 | 60 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RTX 3060 | 2 | 234 | 234 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | RTX 4070 | 2 | 42 | 42 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RTX 4070 | 2 | 163 | 163 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | RTX 5070 | 2 | 35 | 35 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RTX 5070 | 2 | 137 | 145 | -7.4 % | down 2 e3 / sep 2s / up 2 e1 |
| 3 | 1080p | RX 6600 | 2 sep | 108 | 102 | +6.2 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 4k | RX 6600 | 2 sep | 422 | 404 | +5.4 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 1080p | RX 7900 XTX | 2 sep | 17 | 16 | +10.8 % | down 2 e1 / sep 2.5s / up 2 e1 |
| 3 | 4k | RX 7900 XTX | 2 sep | 58 | 53 | +11.8 % | down 2 e1 / sep 2.5s / up 2 e1 |
| 3 | 1080p | RX 9070 XT | 2 sep | 21 | 21 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | RX 9070 XT | 2 sep | 73 | 73 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | Radeon 680M | 2 | 454 | 414 | +10.6 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 4k | Radeon 680M | 2 | 1781 | 1622 | +10.7 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 1080p | RX 5500 XT | 2 sep | 110 | 106 | +5.5 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | RX 5500 XT | 2 sep | 430 | 412 | +5.5 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | RX 590 | 2 sep | 106 | 106 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | RX 590 | 2 sep | 413 | 413 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | Arc B580 | 2 sep | 59 | 59 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | Arc B580 | 2 sep | 221 | 221 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | Iris Xe | 2 | 1333 | 1270 | +5.1 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 4k | Iris Xe | 2 | 5313 | 5061 | +5.1 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 1080p | UHD 630 | 2 sep | 860 | 792 | +10.9 % | down 2 e5 / sep 2s / up 2 e1 |
| 3 | 4k | UHD 630 | 2 sep | 3399 | 3126 | +10.9 % | down 2 e5 / sep 2s / up 2 e1 |
| 3 | 1080p | GTX 1080 | 2 sep | 76 | 73 | +6.4 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 4k | GTX 1080 | 2 sep | 294 | 283 | +4.9 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 1080p | GTX 1660 | 2 sep | 145 | 137 | +7.1 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | GTX 1660 | 2 sep | 570 | 540 | +7.1 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | GTX 860M | 2 sep | 299 | 294 | +2.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | GTX 860M | 2 sep | 1188 | 1169 | +2.1 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | RTX 2070 | 2 sep | 103 | 71 | +67.1 % | down 2 e5 / sep 2s / up 2 e1 |
| 3 | 4k | RTX 2070 | 2 sep | 404 | 277 | +68.2 % | down 2 e5 / sep 2s / up 2 e1 |
| 3 | 1080p | RTX 3060 | 2 sep | 65 | 65 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | RTX 3060 | 2 sep | 247 | 247 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | RTX 4070 | 2 sep | 49 | 47 | +4.3 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | RTX 4070 | 2 sep | 188 | 182 | +4.4 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | RTX 5070 | 2 sep | 40 | 38 | +7.4 % | down 2 e5 / sep 2s / up 2 e1 |
| 3 | 4k | RTX 5070 | 2 sep | 154 | 145 | +7.6 % | down 2 e5 / sep 2s / up 2 e1 |
| 4 | 1080p | RX 6600 | 4s | 79 | 78 | +1.0 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RX 6600 | 4s | 317 | 312 | +1.4 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RX 7900 XTX | 4s | 14 | 14 | +6.1 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RX 7900 XTX | 4s | 46 | 43 | +6.6 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RX 9070 XT | 4s | 18 | 17 | +4.4 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RX 9070 XT | 4s | 59 | 56 | +4.7 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | Radeon 680M | 4s | 342 | 338 | +1.1 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | Radeon 680M | 4s | 1372 | 1370 | +0.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RX 5500 XT | 4s | 87 | 82 | +6.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RX 5500 XT | 4s | 337 | 317 | +6.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RX 590 | 4s | 76 | 75 | +1.0 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RX 590 | 4s | 294 | 290 | +1.0 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | Arc B580 | 4s | 44 | 43 | +2.4 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | Arc B580 | 4s | 169 | 166 | +1.9 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | Iris Xe | 4s | 1143 | 1135 | +0.7 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | Iris Xe | 4s | 4791 | 4791 | +0.0 % | down 4 e5 / direct 2s / up 2x2 e2 |
| 4 | 1080p | UHD 630 | 4s sep | 643 | 621 | +3.4 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | UHD 630 | 4s sep | 2627 | 2467 | +6.4 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | GTX 1080 | 4s | 55 | 55 | +0.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | GTX 1080 | 4s | 208 | 207 | +0.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | GTX 1660 | 4s | 109 | 105 | +3.6 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | GTX 1660 | 4s | 440 | 424 | +3.6 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | GTX 860M | 4s | 230 | 216 | +5.7 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | GTX 860M | 4s | 919 | 873 | +4.8 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RTX 2070 | 4s | 82 | 78 | +8.4 % | down 2 e1 / sep 2.5s / up 2 e1 |
| 4 | 4k | RTX 2070 | 4s | 328 | 302 | +13.6 % | down 2 e1 / sep 2.5s / up 2 e1 |
| 4 | 1080p | RTX 3060 | 4s | 51 | 48 | +4.5 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RTX 3060 | 4s | 191 | 182 | +4.6 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RTX 4070 | 4s | 37 | 36 | +3.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RTX 4070 | 4s | 145 | 141 | +3.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RTX 5070 | 4s | 30 | 29 | +4.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RTX 5070 | 4s | 119 | 114 | +4.3 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 6 | 1080p | RX 6600 | 4s sep | 82 | 56 | +30.7 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 4k | RX 6600 | 4s sep | 334 | 228 | +31.5 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 1080p | RX 7900 XTX | 4s sep | 16 | 14 | +13.3 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | RX 7900 XTX | 4s sep | 48 | 44 | +8.0 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 1080p | RX 9070 XT | 4s sep | 19 | 15 | +26.7 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 4k | RX 9070 XT | 4s sep | 61 | 50 | +19.5 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | Radeon 680M | 4s | 360 | 236 | +33.0 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | Radeon 680M | 4s | 1443 | 968 | +32.1 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 1080p | RX 5500 XT | 4s sep | 90 | 85 | +5.9 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | RX 5500 XT | 4s sep | 343 | 327 | +4.8 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | RX 590 | 4s sep | 82 | 59 | +27.3 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 4k | RX 590 | 4s sep | 312 | 229 | +25.3 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | Arc B580 | 4s sep | 46 | 31 | +33.1 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | Arc B580 | 4s sep | 178 | 124 | +31.0 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | Iris Xe | 4s | 1171 | 719 | +36.6 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | Iris Xe | 4s | 4882 | 3123 | +35.6 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 1080p | UHD 630 | 4s sep | 676 | 574 | +16.3 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 4k | UHD 630 | 4s sep | 2675 | 2352 | +12.9 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 1080p | GTX 1080 | 4s sep | 60 | 42 | +29.8 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 4k | GTX 1080 | 4s sep | 223 | 160 | +27.0 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 1080p | GTX 1660 | 4s sep | 111 | 93 | +16.3 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | GTX 1660 | 4s sep | 459 | 392 | +15.7 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | GTX 860M | 4s sep | 233 | 200 | +14.1 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | GTX 860M | 4s sep | 937 | 824 | +12.1 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | RTX 2070 | 4s sep | 83 | 50 | +71.1 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 4k | RTX 2070 | 4s sep | 340 | 205 | +72.5 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 1080p | RTX 3060 | 4s sep | 53 | 44 | +17.7 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | RTX 3060 | 4s sep | 195 | 164 | +16.1 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | RTX 4070 | 4s sep | 38 | 30 | +20.7 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | RTX 4070 | 4s sep | 152 | 124 | +19.3 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | RTX 5070 | 4s sep | 31 | 27 | +13.3 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 4k | RTX 5070 | 4s sep | 124 | 110 | +11.8 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 8 | 1080p | RX 6600 | 4 sep | 56 | 53 | +3.9 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 4k | RX 6600 | 4 sep | 236 | 209 | +7.9 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 1080p | RX 7900 XTX | 4 sep | 15 | 11 | +37.6 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | RX 7900 XTX | 4 sep | 49 | 32 | +41.1 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | RX 9070 XT | 4 sep | 16 | 13 | +17.5 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | RX 9070 XT | 4 sep | 52 | 42 | +18.7 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | Radeon 680M | 4 sep | 240 | 230 | +2.7 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 4k | Radeon 680M | 4 sep | 1032 | 908 | +8.4 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 1080p | RX 5500 XT | 4 sep | 90 | 61 | +35.2 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | RX 5500 XT | 4 sep | 350 | 233 | +35.6 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | RX 590 | 4 sep | 60 | 55 | +6.0 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 4k | RX 590 | 4 sep | 229 | 205 | +7.3 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 1080p | Arc B580 | 4 sep | 32 | 31 | +2.3 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | Arc B580 | 4 sep | 126 | 124 | +1.7 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | Iris Xe | 4 sep | 729 | 690 | +3.1 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 4k | Iris Xe | 4 sep | 3407 | 2995 | +8.3 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 1080p | UHD 630 | 4 sep | 694 | 448 | +39.3 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | UHD 630 | 4 sep | 2760 | 1774 | +39.5 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | GTX 1080 | 4 sep | 44 | 41 | +5.5 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 4k | GTX 1080 | 4 sep | 164 | 147 | +7.2 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 1080p | GTX 1660 | 4 sep | 98 | 71 | +25.4 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | GTX 1660 | 4 sep | 411 | 302 | +25.6 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | GTX 860M | 4 sep | 216 | 155 | +26.0 % | down 4x2 e3 / direct 2s / up 2x4 e2 |
| 8 | 4k | GTX 860M | 4 sep | 872 | 635 | +25.4 % | down 4x2 e3 / direct 2s / up 2x4 e2 |
| 8 | 1080p | RTX 2070 | 4 sep | 75 | 39 | +75.8 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | RTX 2070 | 4 sep | 310 | 167 | +77.0 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | RTX 3060 | 4 sep | 46 | 38 | +16.8 % | down 4x2 e3 / direct 2s / up 2x4 e2 |
| 8 | 4k | RTX 3060 | 4 sep | 172 | 135 | +19.1 % | down 4x2 e3 / direct 2s / up 2x4 e2 |
| 8 | 1080p | RTX 4070 | 4 sep | 32 | 25 | +18.5 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | RTX 4070 | 4 sep | 130 | 103 | +18.7 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | RTX 5070 | 4 sep | 29 | 21 | +27.0 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | RTX 5070 | 4 sep | 114 | 83 | +27.4 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 12 | 1080p | RX 6600 | 4 sep | 58 | 47 | +12.9 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | RX 6600 | 4 sep | 243 | 182 | +18.2 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 1080p | RX 7900 XTX | 4 sep | 16 | 10 | +52.2 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | RX 7900 XTX | 4 sep | 51 | 30 | +51.9 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | RX 9070 XT | 4 sep | 17 | 10 | +41.8 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | RX 9070 XT | 4 sep | 55 | 34 | +37.8 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 1080p | Radeon 680M | 4 sep | 245 | 206 | +10.3 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | Radeon 680M | 4 sep | 1038 | 790 | +16.7 % | down 8 e5 / sep 2.5s / up 8 p5 |
| 12 | 1080p | RX 5500 XT | 4 sep | 95 | 57 | +46.1 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 4k | RX 5500 XT | 4 sep | 368 | 211 | +47.8 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | RX 590 | 4 sep | 62 | 47 | +17.3 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | RX 590 | 4 sep | 235 | 182 | +16.3 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 1080p | Arc B580 | 4 sep | 33 | 26 | +15.9 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | Arc B580 | 4 sep | 130 | 109 | +12.5 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | Iris Xe | 4 sep | 736 | 649 | +7.0 % | down 8 e5 / sep 2s / up 8 p9 |
| 12 | 4k | Iris Xe | 4 sep | 3407 | 2568 | +17.0 % | down 8 e5 / sep 2s / up 8 p9 |
| 12 | 1080p | UHD 630 | 4 sep | 728 | 380 | +55.4 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 4k | UHD 630 | 4 sep | 2894 | 1525 | +54.9 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | GTX 1080 | 4 sep | 44 | 34 | +16.5 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | GTX 1080 | 4 sep | 164 | 129 | +15.1 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 1080p | GTX 1660 | 4 sep | 101 | 64 | +34.1 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 4k | GTX 1660 | 4 sep | 423 | 257 | +39.1 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | GTX 860M | 4 sep | 227 | 137 | +38.2 % | down 8 e5 / sep 3s / up 8 p4 |
| 12 | 4k | GTX 860M | 4 sep | 914 | 542 | +39.9 % | down 8 e5 / sep 3s / up 8 p4 |
| 12 | 1080p | RTX 2070 | 4 sep | 77 | 36 | +87.0 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 4k | RTX 2070 | 4 sep | 318 | 139 | +96.2 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | RTX 3060 | 4 sep | 48 | 30 | +36.6 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | RTX 3060 | 4 sep | 182 | 110 | +36.4 % | down 8 e5 / sep 3s / up 8 p4 |
| 12 | 1080p | RTX 4070 | 4 sep | 32 | 23 | +25.7 % | down 8 e3 / direct 2s / up 2x4 e1 |
| 12 | 4k | RTX 4070 | 4 sep | 133 | 88 | +31.2 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | RTX 5070 | 4 sep | 30 | 19 | +36.4 % | down 8 e3 / direct 2s / up 2x4 e1 |
| 12 | 4k | RTX 5070 | 4 sep | 118 | 71 | +41.1 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 16 | 1080p | RX 6600 | 8 sep | 48 | 48 | +0.1 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 4k | RX 6600 | 8 sep | 182 | 178 | +1.0 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 1080p | RX 7900 XTX | 8 sep | 11 | 9 | +15.2 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | RX 7900 XTX | 8 sep | 33 | 26 | +16.6 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | RX 9070 XT | 8 sep | 12 | 11 | +1.1 % | down 8 e1 / sep 2.5s / up 8 p4 |
| 16 | 4k | RX 9070 XT | 8 sep | 35 | 34 | +1.1 % | down 8 e1 / sep 2.5s / up 8 p4 |
| 16 | 1080p | Radeon 680M | 8 sep | 211 | 210 | +0.3 % | down 8 e1 / sep 2.5s / up 8 p4 |
| 16 | 4k | Radeon 680M | 8 sep | 794 | 784 | +0.7 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 1080p | RX 5500 XT | 8 sep | 58 | 49 | +11.5 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | RX 5500 XT | 8 sep | 222 | 184 | +11.7 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | RX 590 | 8 sep | 49 | 48 | +0.4 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 4k | RX 590 | 8 sep | 183 | 178 | +1.5 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 1080p | Arc B580 | 8 sep | 28 | 28 | +0.6 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | Arc B580 | 8 sep | 97 | 96 | +0.6 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | Iris Xe | 8 sep | 653 | 651 | +0.1 % | down 8 e1 / sep 2.5s / up 8 p4 |
| 16 | 4k | Iris Xe | 8 sep | 2582 | 2543 | +0.8 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 1080p | UHD 630 | 8 sep | 456 | 355 | +16.1 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | UHD 630 | 8 sep | 1785 | 1382 | +16.2 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | GTX 1080 | 8 sep | 36 | 36 | -0.2 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 4k | GTX 1080 | 8 sep | 131 | 128 | +1.4 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 1080p | GTX 1660 | 8 sep | 75 | 60 | +14.1 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | GTX 1660 | 8 sep | 289 | 229 | +14.2 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | GTX 860M | 8 sep | 140 | 130 | +4.5 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | GTX 860M | 8 sep | 552 | 510 | +4.5 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | RTX 2070 | 8 sep | 60 | 34 | +54.6 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | RTX 2070 | 8 sep | 231 | 128 | +55.5 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | RTX 3060 | 8 sep | 31 | 30 | +1.1 % | down 8 e1 / sep 2.5s / up 8 p4 |
| 16 | 4k | RTX 3060 | 8 sep | 113 | 111 | +1.0 % | down 8x2 e3 / direct 2s / up 2x8 e2 |
| 16 | 1080p | RTX 4070 | 8 sep | 24 | 21 | +8.6 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | RTX 4070 | 8 sep | 91 | 79 | +8.7 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | RTX 5070 | 8 sep | 21 | 17 | +13.2 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | RTX 5070 | 8 sep | 79 | 64 | +13.4 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 24 | 1080p | RX 6600 | 8 sep | 48 | 45 | +4.1 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | RX 6600 | 8 sep | 183 | 172 | +3.2 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | RX 7900 XTX | 8 sep | 11 | 9 | +17.7 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RX 7900 XTX | 8 sep | 33 | 25 | +19.4 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 1080p | RX 9070 XT | 8 sep | 12 | 10 | +13.5 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | RX 9070 XT | 8 sep | 35 | 31 | +7.6 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | Radeon 680M | 8 sep | 213 | 209 | +1.0 % | down 8x2 e3 / direct 2s / up 16 p4 |
| 24 | 4k | Radeon 680M | 8 sep | 798 | 760 | +2.6 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | RX 5500 XT | 8 sep | 59 | 48 | +14.1 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RX 5500 XT | 8 sep | 226 | 179 | +14.4 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | RX 590 | 8 sep | 49 | 44 | +5.5 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | RX 590 | 8 sep | 185 | 170 | +4.4 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | Arc B580 | 8 sep | 28 | 27 | +2.1 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | Arc B580 | 8 sep | 98 | 95 | +2.2 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 1080p | Iris Xe | 8 sep | 654 | 643 | +0.9 % | down 8x2 e3 / direct 2s / up 16 p4 |
| 24 | 4k | Iris Xe | 8 sep | 2589 | 2503 | +1.7 % | down 16 e5 / sep 2.5s / up 16 p4 |
| 24 | 1080p | UHD 630 | 8 sep | 465 | 356 | +17.4 % | down 8x2 e3 / sep 2s / up 2x8 e1 |
| 24 | 4k | UHD 630 | 8 sep | 1819 | 1314 | +20.2 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | GTX 1080 | 8 sep | 36 | 32 | +5.8 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | GTX 1080 | 8 sep | 131 | 121 | +4.2 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | GTX 1660 | 8 sep | 76 | 61 | +13.7 % | down 8 e1 / sep 2.5s / up 8 e1 |
| 24 | 4k | GTX 1660 | 8 sep | 293 | 223 | +16.3 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | GTX 860M | 8 sep | 143 | 129 | +5.7 % | down 8x2 e3 / sep 2s / up 2x8 e1 |
| 24 | 4k | GTX 860M | 8 sep | 563 | 490 | +7.8 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | RTX 2070 | 8 sep | 61 | 33 | +57.4 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RTX 2070 | 8 sep | 233 | 125 | +58.3 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | RTX 3060 | 8 sep | 32 | 28 | +7.9 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | RTX 3060 | 8 sep | 115 | 103 | +6.0 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | RTX 4070 | 8 sep | 25 | 21 | +10.4 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RTX 4070 | 8 sep | 92 | 77 | +10.5 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 1080p | RTX 5070 | 8 sep | 22 | 17 | +15.6 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RTX 5070 | 8 sep | 80 | 62 | +15.8 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 32 | 1080p | RX 6600 | 16 | 45 | 45 | +0.4 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | RX 6600 | 16 | 176 | 173 | +0.8 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | RX 7900 XTX | 16 | 10 | 9 | +2.4 % | down 8x2 e9 / direct 2s / up 16 e1 |
| 32 | 4k | RX 7900 XTX | 16 | 31 | 26 | +12.0 % | down 8x2 e9 / direct 2s / up 16 e1 |
| 32 | 1080p | RX 9070 XT | 16 | 10 | 10 | +0.9 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | RX 9070 XT | 16 | 32 | 32 | +0.6 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | Radeon 680M | 16 | 350 | 211 | +37.0 % | down 8x2 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | Radeon 680M | 16 | 769 | 764 | +0.3 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | RX 5500 XT | 16 sep | 55 | 49 | +7.5 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 4k | RX 5500 XT | 16 sep | 208 | 179 | +8.7 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RX 590 | 16 | 46 | 45 | +0.6 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | RX 590 | 16 | 176 | 171 | +1.3 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | Arc B580 | 16 | 26 | 27 | -4.0 % | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 32 | 4k | Arc B580 | 16 | 93 | 96 | -1.4 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | Iris Xe | 16 | 992 | 645 | +28.0 % | down 8x2 e3 / sep 2.5s / up 16 p4 |
| 32 | 4k | Iris Xe | 16 | 2518 | 2504 | +0.3 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | UHD 630 | 16 sep | 683 | 360 | +51.5 % | down 8x2 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 4k | UHD 630 | 16 sep | 1682 | 1318 | +14.6 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | GTX 1080 | 16 | 33 | 33 | +0.6 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | GTX 1080 | 16 | 125 | 123 | +0.8 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | GTX 1660 | 16 sep | 180 | 64 | +107.7 % | down 8x2 e9 / direct 2s / up 16 e1 |
| 32 | 4k | GTX 1660 | 16 sep | 279 | 224 | +13.0 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | GTX 860M | 16 sep | 185 | 130 | +23.6 % | down 8x2 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 4k | GTX 860M | 16 sep | 519 | 491 | +3.0 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RTX 2070 | 16 sep | 58 | 34 | +51.4 % | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 32 | 4k | RTX 2070 | 16 sep | 225 | 125 | +53.6 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RTX 3060 | 16 | 29 | 28 | +1.0 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | RTX 3060 | 16 | 108 | 103 | +2.3 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | RTX 4070 | 16 | 23 | 21 | +6.1 % | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 32 | 4k | RTX 4070 | 16 | 89 | 77 | +8.2 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RTX 5070 | 16 | 20 | 17 | +10.5 % | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 32 | 4k | RTX 5070 | 16 | 77 | 62 | +13.2 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 48 | 1080p | RX 6600 | 32 | 45 | 45 | +0.1 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 4k | RX 6600 | 32 | 173 | 172 | +0.1 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | RX 7900 XTX | 16 | 10 | 8 | +14.7 % | down 16 e1 / direct 2.5s / up 16 e1 |
| 48 | 4k | RX 7900 XTX | 16 | 32 | 24 | +18.3 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 1080p | RX 9070 XT | 16 | 10 | 10 | +0.3 % | down 16 e1 / direct 2.5s / up 16 e1 |
| 48 | 4k | RX 9070 XT | 16 | 34 | 32 | +3.4 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | Radeon 680M | 32 | 356 | 212 | +38.2 % | down 8x4 e3 / direct 2s / up 32 p4 |
| 48 | 4k | Radeon 680M | 32 | 765 | 763 | +0.2 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | RX 5500 XT | 32 | 55 | 46 | +10.8 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | RX 5500 XT | 32 | 208 | 173 | +10.6 % | down 16x2 e3 / direct 2s / up 2x16 e1 |
| 48 | 1080p | RX 590 | 32 | 45 | 45 | +0.2 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 4k | RX 590 | 32 | 170 | 170 | +0.2 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | Arc B580 | 32 | 27 | 26 | +0.9 % | down 16 e1 / direct 2.5s / up 16 e1 |
| 48 | 4k | Arc B580 | 32 | 92 | 93 | -0.3 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 1080p | Iris Xe | 32 | 993 | 644 | +28.2 % | down 8x4 e3 / direct 2s / up 32 p4 |
| 48 | 4k | Iris Xe | 32 | 2501 | 2497 | +0.1 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | UHD 630 | 16 sep | 686 | 355 | +52.9 % | down 8x2 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | UHD 630 | 16 sep | 1691 | 1290 | +16.1 % | down 16x2 e3 / sep 2s / up 2x16 e1 |
| 48 | 1080p | GTX 1080 | 32 | 33 | 33 | +0.1 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 4k | GTX 1080 | 32 | 122 | 122 | +0.1 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | GTX 1660 | 16 sep | 180 | 62 | +110.8 % | down 8x2 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | GTX 1660 | 16 sep | 280 | 220 | +14.1 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 1080p | GTX 860M | 16 sep | 186 | 128 | +24.9 % | down 8x2 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | GTX 860M | 16 sep | 521 | 479 | +4.5 % | down 16x2 e3 / sep 2s / up 2x16 e1 |
| 48 | 1080p | RTX 2070 | 32 | 58 | 33 | +53.2 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | RTX 2070 | 32 | 224 | 124 | +54.2 % | down 16x2 e3 / direct 2s / up 2x16 e1 |
| 48 | 1080p | RTX 3060 | 32 | 29 | 29 | +0.4 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 4k | RTX 3060 | 32 | 104 | 103 | +0.4 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | RTX 4070 | 32 | 24 | 21 | +8.3 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | RTX 4070 | 32 | 88 | 75 | +8.5 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 1080p | RTX 5070 | 32 | 20 | 17 | +13.1 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | RTX 5070 | 32 | 76 | 61 | +12.9 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 64 | 1080p | RX 6600 | 32 | 46 | 45 | +0.2 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 4k | RX 6600 | 32 | 173 | 173 | +0.2 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 1080p | RX 7900 XTX | 32 | 11 | 9 | +17.9 % | down 16 e1 / direct 2.5s / up 16 e1 |
| 64 | 4k | RX 7900 XTX | 32 | 31 | 25 | +15.3 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 64 | 1080p | RX 9070 XT | 32 | 11 | 11 | +0.4 % | down 16x2 e3 / direct 2.5s / up 32 p4 |
| 64 | 4k | RX 9070 XT | 32 | 32 | 32 | +0.5 % | down 16x2 e3 / direct 2.5s / up 32 p4 |
| 64 | 1080p | Radeon 680M | 32 | 358 | 215 | +38.3 % | down 8x4 e3 / direct 2.5s / up 32 p4 |
| 64 | 4k | Radeon 680M | 32 | 768 | 765 | +0.2 % | down 16x2 e3 / direct 2.5s / up 32 p4 |
| 64 | 1080p | RX 5500 XT | 32 | 55 | 46 | +10.6 % | down 16 e1 / sep 3s / up 16 e1 |
| 64 | 4k | RX 5500 XT | 32 | 209 | 174 | +10.8 % | down 16x2 e3 / sep 2.5s / up 2x16 e1 |
| 64 | 1080p | RX 590 | 32 | 46 | 45 | +0.3 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 4k | RX 590 | 32 | 171 | 171 | +0.2 % | down 16x4 e5 / direct 2s / up 2x32 p4 |
| 64 | 1080p | Arc B580 | 32 | 27 | 27 | -0.6 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 64 | 4k | Arc B580 | 32 | 93 | 94 | -0.6 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 64 | 1080p | Iris Xe | 32 | 998 | 646 | +28.4 % | down 8x4 e5 / direct 2s / up 32 e3 |
| 64 | 4k | Iris Xe | 32 | 2505 | 2499 | +0.1 % | down 16x2 e3 / sep 2.5s / up 32 p4 |
| 64 | 1080p | UHD 630 | 32 sep | 711 | 357 | +56.4 % | down 8x2x2 e3 / sep 2.5s / up 32 e1 |
| 64 | 4k | UHD 630 | 32 sep | 1694 | 1293 | +16.0 % | down 16x2 e3 / sep 2.5s / up 2x16 e1 |
| 64 | 1080p | GTX 1080 | 32 | 34 | 33 | +0.3 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 4k | GTX 1080 | 32 | 123 | 122 | +0.3 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 1080p | GTX 1660 | 32 sep | 184 | 63 | +113.5 % | down 8x2 e1 / sep 3s / up 16 e1 |
| 64 | 4k | GTX 1660 | 32 sep | 283 | 222 | +14.4 % | down 16x2 e3 / sep 2.5s / up 2x16 e1 |
| 64 | 1080p | GTX 860M | 32 sep | 192 | 129 | +27.0 % | down 8x2x2 e3 / sep 2.5s / up 32 e1 |
| 64 | 4k | GTX 860M | 32 sep | 520 | 480 | +4.2 % | down 16x2 e3 / sep 2.5s / up 2x16 e1 |
| 64 | 1080p | RTX 2070 | 32 | 59 | 33 | +53.2 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 64 | 4k | RTX 2070 | 32 | 225 | 124 | +54.2 % | down 16x2 e3 / direct 2.5s / up 2x16 e1 |
| 64 | 1080p | RTX 3060 | 32 | 29 | 29 | +0.5 % | down 16x2 e3 / direct 2.5s / up 32 p4 |
| 64 | 4k | RTX 3060 | 32 | 104 | 104 | +0.4 % | down 16x4 e5 / direct 2s / up 2x32 p4 |
| 64 | 1080p | RTX 4070 | 32 | 24 | 21 | +8.3 % | down 16 e1 / sep 3s / up 16 e1 |
| 64 | 4k | RTX 4070 | 32 | 88 | 76 | +8.4 % | down 16 e1 / sep 3s / up 16 e1 |
| 64 | 1080p | RTX 5070 | 32 | 21 | 17 | +13.0 % | down 16 e1 / sep 3s / up 16 e1 |
| 64 | 4k | RTX 5070 | 32 | 76 | 61 | +12.9 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 100 | 1080p | RX 6600 | 32 | 46 | 45 | +0.7 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | RX 6600 | 32 | 174 | 172 | +0.7 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | RX 7900 XTX | 32 | 11 | 9 | +15.1 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | RX 7900 XTX | 32 | 31 | 25 | +16.2 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 1080p | RX 9070 XT | 32 | 11 | 11 | +1.6 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | RX 9070 XT | 32 | 33 | 32 | +1.7 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | Radeon 680M | 32 | 362 | 217 | +38.7 % | down 8x2 e1 / sep 3s / up 16 e1 |
| 100 | 4k | Radeon 680M | 32 | 772 | 766 | +0.4 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | RX 5500 XT | 32 | 56 | 46 | +11.3 % | down 16x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | RX 5500 XT | 32 | 211 | 170 | +12.5 % | down 16x4 e9 / direct 2s / up 2x32 e1 |
| 100 | 1080p | RX 590 | 32 | 46 | 45 | +1.1 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | RX 590 | 32 | 173 | 169 | +1.1 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | Arc B580 | 32 | 27 | 27 | +0.1 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | Arc B580 | 32 | 93 | 93 | +0.1 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 1080p | Iris Xe | 32 | 1003 | 647 | +28.7 % | down 8x4 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | Iris Xe | 32 | 2511 | 2497 | +0.3 % | down 16x4 e3 / direct 2s / up 64 p8 |
| 100 | 1080p | UHD 630 | 32 sep | 714 | 363 | +56.1 % | down 8x2x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | UHD 630 | 32 sep | 1697 | 1288 | +16.4 % | down 16x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 1080p | GTX 1080 | 32 | 34 | 33 | +0.9 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | GTX 1080 | 32 | 123 | 121 | +1.0 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | GTX 1660 | 32 sep | 185 | 64 | +112.9 % | down 8x4 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | GTX 1660 | 32 sep | 283 | 220 | +14.8 % | down 16x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 1080p | GTX 860M | 32 sep | 193 | 131 | +26.8 % | down 8x2x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | GTX 860M | 32 sep | 521 | 478 | +4.6 % | down 16x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 1080p | RTX 2070 | 32 | 59 | 33 | +53.8 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | RTX 2070 | 32 | 226 | 123 | +55.4 % | down 16x4 e3 / direct 2.5s / up 2x32 e1 |
| 100 | 1080p | RTX 3060 | 32 | 29 | 28 | +1.7 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | RTX 3060 | 32 | 106 | 102 | +1.7 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | RTX 4070 | 32 | 24 | 21 | +8.8 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | RTX 4070 | 32 | 89 | 75 | +9.2 % | down 16x4 e9 / direct 2s / up 2x32 e1 |
| 100 | 1080p | RTX 5070 | 32 | 21 | 17 | +13.7 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | RTX 5070 | 32 | 77 | 61 | +14.0 % | down 16x4 e3 / direct 2.5s / up 2x32 e1 |
| 150 | 1080p | RX 6600 | 64 | 45 | 45 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | RX 6600 | 64 | 172 | 172 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | RX 7900 XTX | 64 | 11 | 9 | +14.6 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RX 7900 XTX | 64 | 30 | 24 | +15.9 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RX 9070 XT | 64 | 11 | 11 | +0.3 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | RX 9070 XT | 64 | 32 | 32 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | Radeon 680M | 64 | 361 | 220 | +37.7 % | down 8x4 e1 / sep 3s / up 32 e1 |
| 150 | 4k | Radeon 680M | 64 | 770 | 769 | +0.0 % | down 16x2 e3 / sep 2.5s / up 32 e2 |
| 150 | 1080p | RX 5500 XT | 64 | 54 | 45 | +10.9 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RX 5500 XT | 64 | 206 | 169 | +11.0 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RX 590 | 64 | 45 | 45 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | RX 590 | 64 | 169 | 169 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | Arc B580 | 64 | 26 | 26 | +0.0 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | Arc B580 | 64 | 92 | 92 | +0.0 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | Iris Xe | 64 | 997 | 649 | +28.1 % | down 8x4 e1 / sep 2.5s / up 32 e3 |
| 150 | 4k | Iris Xe | 64 | 2503 | 2500 | +0.1 % | down 16x4 e1 / sep 2.5s / up 64 e1 |
| 150 | 1080p | UHD 630 | 64 sep | 703 | 370 | +53.1 % | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 150 | 4k | UHD 630 | 64 sep | 1686 | 1293 | +15.8 % | down 16x2x2 e1 / sep 2.5s / up 64 e1 |
| 150 | 1080p | GTX 1080 | 64 | 33 | 33 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | GTX 1080 | 64 | 121 | 121 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | GTX 1660 | 64 sep | 184 | 66 | +110.8 % | down 8x4 e1 / sep 3s / up 32 e1 |
| 150 | 4k | GTX 1660 | 64 sep | 283 | 222 | +14.3 % | down 16x2 e1 / sep 3s / up 32 e1 |
| 150 | 1080p | GTX 860M | 64 sep | 193 | 133 | +25.3 % | down 8x2x2 e1 / sep 3s / up 32 e1 |
| 150 | 4k | GTX 860M | 64 sep | 520 | 479 | +4.3 % | down 16x2x2 e1 / sep 2.5s / up 64 e1 |
| 150 | 1080p | RTX 2070 | 64 | 58 | 33 | +53.5 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RTX 2070 | 64 | 223 | 122 | +54.4 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RTX 3060 | 64 | 28 | 28 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | RTX 3060 | 64 | 102 | 102 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | RTX 4070 | 64 | 23 | 20 | +8.7 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RTX 4070 | 64 | 87 | 75 | +8.8 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RTX 5070 | 64 | 20 | 16 | +13.1 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RTX 5070 | 64 | 75 | 60 | +13.3 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 200 | 1080p | RX 6600 | 64 | 45 | 45 | +0.2 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 4k | RX 6600 | 64 | 172 | 172 | +0.2 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | RX 7900 XTX | 64 | 11 | 9 | +14.9 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RX 7900 XTX | 64 | 31 | 24 | +15.9 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 1080p | RX 9070 XT | 64 | 11 | 11 | +0.3 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RX 9070 XT | 64 | 32 | 32 | +0.4 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | Radeon 680M | 64 | 365 | 221 | +38.4 % | down 8x4 e1 / sep 3s / up 32 e1 |
| 200 | 4k | Radeon 680M | 64 | 774 | 771 | +0.2 % | down 16x2 e1 / sep 3s / up 32 e1 |
| 200 | 1080p | RX 5500 XT | 64 | 54 | 45 | +11.3 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RX 5500 XT | 64 | 206 | 170 | +11.0 % | down 16x8 e3 / direct 2.5s / up 2x64 e1 |
| 200 | 1080p | RX 590 | 64 | 45 | 45 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RX 590 | 64 | 170 | 169 | +0.2 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | Arc B580 | 64 | 26 | 26 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | Arc B580 | 64 | 92 | 92 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 1080p | Iris Xe | 64 | 1002 | 650 | +28.4 % | down 8x4x4 e3 / direct 2s / up 128 p8 |
| 200 | 4k | Iris Xe | 64 | 2509 | 2501 | +0.2 % | down 16x4 e1 / sep 2.5s / up 64 e1 |
| 200 | 1080p | UHD 630 | 64 sep | 707 | 373 | +53.1 % | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 4k | UHD 630 | 64 sep | 1689 | 1296 | +15.8 % | down 16x2x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 1080p | GTX 1080 | 64 | 33 | 33 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | GTX 1080 | 64 | 122 | 121 | +0.2 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | GTX 1660 | 64 sep | 185 | 66 | +111.0 % | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 4k | GTX 1660 | 64 sep | 283 | 223 | +14.3 % | down 16x4 e1 / sep 2.5s / up 64 e1 |
| 200 | 1080p | GTX 860M | 64 sep | 194 | 135 | +25.1 % | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 4k | GTX 860M | 64 sep | 521 | 480 | +4.3 % | down 16x2x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 1080p | RTX 2070 | 64 | 58 | 33 | +53.5 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RTX 2070 | 64 | 224 | 122 | +54.4 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 1080p | RTX 3060 | 64 | 29 | 28 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RTX 3060 | 64 | 103 | 102 | +0.4 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | RTX 4070 | 64 | 23 | 20 | +8.7 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RTX 4070 | 64 | 87 | 75 | +8.8 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 1080p | RTX 5070 | 64 | 20 | 16 | +13.5 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RTX 5070 | 64 | 75 | 60 | +13.3 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
