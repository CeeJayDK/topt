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
| 24 | +3.0 % | RX 9070 XT (16): +10.6 % | 11 | 10 | down 16 e3 / direct 2s / up 16 p4 |
| 32 | +7.0 % | RTX 2070 (16 sep): +54.6 % | 60 | 34 | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 48 | +1.3 % | RX 7900 XTX (16e): +13.2 % | 10 | 8 | down 16 e1 / direct 2.5s / up 16 e1 |
| 64 | +3.3 % | RTX 2070 (32): +53.7 % | 59 | 33 | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 100 | +0.9 % | RX 7900 XTX (32e): +1.4 % | 9 | 9 | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 150 | +6.4 % | RTX 2070 (64): +54.4 % | 59 | 33 | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 200 | +1.3 % | GTX 1660 (64e sep): +8.0 % | 75 | 66 | down 8x4x2 e1 / sep 2.5s / up 64 e1 |

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
| 24 | +2.9 % | UHD 630 (8e sep): +5.4 % | 1449 | 1314 | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | +4.4 % | RTX 2070 (16 sep): +55.2 % | 228 | 125 | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 48 | +1.3 % | RX 7900 XTX (16e): +7.2 % | 27 | 24 | down 16 e1 / sep 2.5s / up 16 e1 |
| 64 | +3.1 % | RTX 2070 (32): +54.8 % | 226 | 124 | down 16x2 e3 / direct 2.5s / up 2x16 e1 |
| 100 | +1.2 % | RX 5500 XT (32e): +2.4 % | 178 | 170 | down 16x4 e9 / direct 2s / up 2x32 e1 |
| 150 | +4.2 % | RTX 2070 (64): +55.2 % | 225 | 122 | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 200 | +1.1 % | GTX 1660 (64e sep): +3.0 % | 236 | 223 | down 16x4 e1 / sep 2.5s / up 64 e1 |

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
| 24 | 1080p | RX 6600 | 16 | 47 | 45 | +2.6 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | RX 6600 | 16 | 178 | 172 | +1.7 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | RX 7900 XTX | 8e sep | 10 | 9 | +3.9 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RX 7900 XTX | 8e sep | 27 | 25 | +4.2 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 1080p | RX 9070 XT | 16 | 11 | 10 | +10.6 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | RX 9070 XT | 16 | 34 | 31 | +4.5 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | Radeon 680M | 16 | 210 | 209 | +0.3 % | down 8x2 e3 / direct 2s / up 16 p4 |
| 24 | 4k | Radeon 680M | 16 | 780 | 760 | +1.4 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | RX 5500 XT | 8e sep | 51 | 48 | +3.9 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RX 5500 XT | 8e sep | 193 | 179 | +4.2 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | RX 590 | 16 | 47 | 44 | +3.5 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | RX 590 | 16 | 178 | 170 | +2.4 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | Arc B580 | 16 | 27 | 27 | +0.3 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | Arc B580 | 16 | 95 | 95 | +0.3 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 1080p | Iris Xe | 16 | 645 | 643 | +0.1 % | down 8x2 e3 / direct 2s / up 16 p4 |
| 24 | 4k | Iris Xe | 16 | 2543 | 2503 | +0.8 % | down 16 e5 / sep 2.5s / up 16 p4 |
| 24 | 1080p | UHD 630 | 8e sep | 372 | 356 | +2.6 % | down 8x2 e3 / sep 2s / up 2x8 e1 |
| 24 | 4k | UHD 630 | 8e sep | 1449 | 1314 | +5.4 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | GTX 1080 | 16 | 35 | 32 | +4.1 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | GTX 1080 | 16 | 127 | 121 | +2.5 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | GTX 1660 | 8e sep | 61 | 61 | +0.4 % | down 8 e1 / sep 2.5s / up 8 e1 |
| 24 | 4k | GTX 1660 | 8e sep | 236 | 223 | +2.9 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | GTX 860M | 16 sep | 136 | 129 | +2.8 % | down 8x2 e3 / sep 2s / up 2x8 e1 |
| 24 | 4k | GTX 860M | 16 sep | 527 | 490 | +4.1 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | RTX 2070 | 8e sep | 35 | 33 | +3.9 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RTX 2070 | 8e sep | 132 | 125 | +4.0 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | RTX 3060 | 16 | 30 | 28 | +4.7 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | RTX 3060 | 16 | 109 | 103 | +2.9 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | RTX 4070 | 8e sep | 22 | 21 | +2.5 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RTX 4070 | 8e sep | 80 | 77 | +2.5 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 1080p | RTX 5070 | 8e sep | 18 | 17 | +3.2 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RTX 5070 | 8e sep | 66 | 62 | +3.3 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 32 | 1080p | RX 6600 | 16 | 47 | 45 | +2.7 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | RX 6600 | 16 | 181 | 173 | +2.3 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | RX 7900 XTX | 16 | 11 | 9 | +15.2 % | down 8x2 e9 / direct 2s / up 16 e1 |
| 32 | 4k | RX 7900 XTX | 16 | 33 | 26 | +16.6 % | down 8x2 e9 / direct 2s / up 16 e1 |
| 32 | 1080p | RX 9070 XT | 16 | 12 | 10 | +10.8 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | RX 9070 XT | 16 | 35 | 32 | +4.4 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | Radeon 680M | 16 | 213 | 211 | +0.4 % | down 8x2 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | Radeon 680M | 16 | 787 | 764 | +1.5 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | RX 5500 XT | 16 sep | 57 | 49 | +10.6 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 4k | RX 5500 XT | 16 sep | 214 | 179 | +10.7 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RX 590 | 16 | 48 | 45 | +3.7 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | RX 590 | 16 | 182 | 171 | +3.2 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | Arc B580 | 16 | 28 | 27 | +0.5 % | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 32 | 4k | Arc B580 | 16 | 97 | 96 | +0.5 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | Iris Xe | 16 | 649 | 645 | +0.3 % | down 8x2 e3 / sep 2.5s / up 16 p4 |
| 32 | 4k | Iris Xe | 16 | 2553 | 2504 | +1.0 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | UHD 630 | 16 sep | 449 | 360 | +14.2 % | down 8x2 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 4k | UHD 630 | 16 sep | 1711 | 1318 | +15.8 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | GTX 1080 | 16 | 35 | 33 | +4.3 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | GTX 1080 | 16 | 130 | 123 | +3.0 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | GTX 1660 | 16 sep | 76 | 64 | +11.1 % | down 8x2 e9 / direct 2s / up 16 e1 |
| 32 | 4k | GTX 1660 | 16 sep | 284 | 224 | +14.2 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | GTX 860M | 16 sep | 137 | 130 | +2.8 % | down 8x2 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 4k | GTX 860M | 16 sep | 530 | 491 | +4.2 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RTX 2070 | 16 sep | 60 | 34 | +54.6 % | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 32 | 4k | RTX 2070 | 16 sep | 228 | 125 | +55.2 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RTX 3060 | 16 | 31 | 28 | +5.0 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | RTX 3060 | 16 | 112 | 103 | +4.5 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | RTX 4070 | 16 | 24 | 21 | +9.0 % | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 32 | 4k | RTX 4070 | 16 | 91 | 77 | +9.7 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RTX 5070 | 16 | 21 | 17 | +13.6 % | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 32 | 4k | RTX 5070 | 16 | 79 | 62 | +14.7 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 48 | 1080p | RX 6600 | 32 | 46 | 45 | +1.0 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 4k | RX 6600 | 32 | 175 | 172 | +1.0 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | RX 7900 XTX | 16e | 10 | 8 | +13.2 % | down 16 e1 / direct 2.5s / up 16 e1 |
| 48 | 4k | RX 7900 XTX | 16e | 27 | 24 | +7.2 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 1080p | RX 9070 XT | 32 | 11 | 10 | +4.8 % | down 16 e1 / direct 2.5s / up 16 e1 |
| 48 | 4k | RX 9070 XT | 32 | 33 | 32 | +1.3 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | Radeon 680M | 32 | 213 | 212 | +0.3 % | down 8x4 e3 / direct 2s / up 32 p4 |
| 48 | 4k | Radeon 680M | 32 | 776 | 763 | +0.9 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | RX 5500 XT | 16e sep | 49 | 46 | +3.6 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | RX 5500 XT | 16e sep | 180 | 173 | +2.2 % | down 16x2 e3 / direct 2s / up 2x16 e1 |
| 48 | 1080p | RX 590 | 32 | 46 | 45 | +1.3 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 4k | RX 590 | 32 | 174 | 170 | +1.3 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | Arc B580 | 32 | 27 | 26 | +1.6 % | down 16 e1 / direct 2.5s / up 16 e1 |
| 48 | 4k | Arc B580 | 32 | 94 | 93 | +0.4 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 1080p | Iris Xe | 32 | 646 | 644 | +0.1 % | down 8x4 e3 / direct 2s / up 32 p4 |
| 48 | 4k | Iris Xe | 32 | 2530 | 2497 | +0.7 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | UHD 630 | 16e sep | 356 | 355 | +0.3 % | down 8x2 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | UHD 630 | 16e sep | 1335 | 1290 | +1.8 % | down 16x2 e3 / sep 2s / up 2x16 e1 |
| 48 | 1080p | GTX 1080 | 32 | 34 | 33 | +1.2 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 4k | GTX 1080 | 32 | 125 | 122 | +1.3 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | GTX 1660 | 16e sep | 62 | 62 | +0.3 % | down 8x2 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | GTX 1660 | 16e sep | 225 | 220 | +1.3 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 1080p | GTX 860M | 16e sep | 129 | 128 | +0.2 % | down 8x2 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | GTX 860M | 16e sep | 496 | 479 | +1.8 % | down 16x2 e3 / sep 2s / up 2x16 e1 |
| 48 | 1080p | RTX 2070 | 16e sep | 35 | 33 | +3.3 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | RTX 2070 | 16e sep | 127 | 124 | +1.8 % | down 16x2 e3 / direct 2s / up 2x16 e1 |
| 48 | 1080p | RTX 3060 | 32 | 29 | 29 | +1.3 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 4k | RTX 3060 | 32 | 105 | 103 | +1.3 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | RTX 4070 | 16e sep | 22 | 21 | +3.0 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | RTX 4070 | 16e sep | 78 | 75 | +1.6 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 1080p | RTX 5070 | 16e sep | 18 | 17 | +3.6 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | RTX 5070 | 16e sep | 63 | 61 | +1.6 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 64 | 1080p | RX 6600 | 32 | 46 | 45 | +1.0 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 4k | RX 6600 | 32 | 176 | 173 | +1.0 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 1080p | RX 7900 XTX | 32 | 11 | 9 | +18.7 % | down 16 e1 / direct 2.5s / up 16 e1 |
| 64 | 4k | RX 7900 XTX | 32 | 31 | 25 | +16.2 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 64 | 1080p | RX 9070 XT | 32 | 11 | 11 | +1.3 % | down 16x2 e3 / direct 2.5s / up 32 p4 |
| 64 | 4k | RX 9070 XT | 32 | 33 | 32 | +1.4 % | down 16x2 e3 / direct 2.5s / up 32 p4 |
| 64 | 1080p | Radeon 680M | 32 | 216 | 215 | +0.4 % | down 8x4 e3 / direct 2.5s / up 32 p4 |
| 64 | 4k | Radeon 680M | 32 | 779 | 765 | +0.9 % | down 16x2 e3 / direct 2.5s / up 32 p4 |
| 64 | 1080p | RX 5500 XT | 32 | 56 | 46 | +11.5 % | down 16 e1 / sep 3s / up 16 e1 |
| 64 | 4k | RX 5500 XT | 32 | 212 | 174 | +11.7 % | down 16x2 e3 / sep 2.5s / up 2x16 e1 |
| 64 | 1080p | RX 590 | 32 | 47 | 45 | +1.4 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 4k | RX 590 | 32 | 175 | 171 | +1.3 % | down 16x4 e5 / direct 2s / up 2x32 p4 |
| 64 | 1080p | Arc B580 | 32 | 27 | 27 | +0.1 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 64 | 4k | Arc B580 | 32 | 94 | 94 | +0.1 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 64 | 1080p | Iris Xe | 32 | 650 | 646 | +0.3 % | down 8x4 e5 / direct 2s / up 32 e3 |
| 64 | 4k | Iris Xe | 32 | 2534 | 2499 | +0.7 % | down 16x2 e3 / sep 2.5s / up 32 p4 |
| 64 | 1080p | UHD 630 | 32 sep | 460 | 357 | +16.4 % | down 8x2x2 e3 / sep 2.5s / up 32 e1 |
| 64 | 4k | UHD 630 | 32 sep | 1700 | 1293 | +16.3 % | down 16x2 e3 / sep 2.5s / up 2x16 e1 |
| 64 | 1080p | GTX 1080 | 32 | 34 | 33 | +1.4 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 4k | GTX 1080 | 32 | 125 | 122 | +1.4 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 1080p | GTX 1660 | 32 sep | 79 | 63 | +14.9 % | down 8x2 e1 / sep 3s / up 16 e1 |
| 64 | 4k | GTX 1660 | 32 sep | 285 | 222 | +15.0 % | down 16x2 e3 / sep 2.5s / up 2x16 e1 |
| 64 | 1080p | GTX 860M | 32 sep | 141 | 129 | +5.2 % | down 8x2x2 e3 / sep 2.5s / up 32 e1 |
| 64 | 4k | GTX 860M | 32 sep | 525 | 480 | +4.8 % | down 16x2 e3 / sep 2.5s / up 2x16 e1 |
| 64 | 1080p | RTX 2070 | 32 | 59 | 33 | +53.7 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 64 | 4k | RTX 2070 | 32 | 226 | 124 | +54.8 % | down 16x2 e3 / direct 2.5s / up 2x16 e1 |
| 64 | 1080p | RTX 3060 | 32 | 29 | 29 | +1.4 % | down 16x2 e3 / direct 2.5s / up 32 p4 |
| 64 | 4k | RTX 3060 | 32 | 106 | 104 | +1.3 % | down 16x4 e5 / direct 2s / up 2x32 p4 |
| 64 | 1080p | RTX 4070 | 32 | 24 | 21 | +8.9 % | down 16 e1 / sep 3s / up 16 e1 |
| 64 | 4k | RTX 4070 | 32 | 89 | 76 | +9.0 % | down 16 e1 / sep 3s / up 16 e1 |
| 64 | 1080p | RTX 5070 | 32 | 21 | 17 | +13.5 % | down 16 e1 / sep 3s / up 16 e1 |
| 64 | 4k | RTX 5070 | 32 | 77 | 61 | +13.5 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 100 | 1080p | RX 6600 | 64 | 46 | 45 | +0.9 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | RX 6600 | 64 | 175 | 172 | +0.9 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | RX 7900 XTX | 32e | 9 | 9 | +1.4 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | RX 7900 XTX | 32e | 25 | 25 | +1.1 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 1080p | RX 9070 XT | 64 | 11 | 11 | +1.1 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | RX 9070 XT | 64 | 32 | 32 | +1.2 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | Radeon 680M | 32 | 220 | 217 | +0.8 % | down 8x2 e1 / sep 3s / up 16 e1 |
| 100 | 4k | Radeon 680M | 32 | 783 | 766 | +1.2 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | RX 5500 XT | 32e | 47 | 46 | +1.3 % | down 16x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | RX 5500 XT | 32e | 178 | 170 | +2.4 % | down 16x4 e9 / direct 2s / up 2x32 e1 |
| 100 | 1080p | RX 590 | 64 | 46 | 45 | +1.2 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | RX 590 | 64 | 173 | 169 | +1.2 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | Arc B580 | 64 | 27 | 27 | +0.1 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | Arc B580 | 64 | 93 | 93 | +0.1 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 1080p | Iris Xe | 32 | 655 | 647 | +0.6 % | down 8x4 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | Iris Xe | 32 | 2539 | 2497 | +0.8 % | down 16x4 e3 / direct 2s / up 64 p8 |
| 100 | 1080p | UHD 630 | 32e sep | 366 | 363 | +0.6 % | down 8x2x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | UHD 630 | 32e sep | 1316 | 1288 | +1.1 % | down 16x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 1080p | GTX 1080 | 64 | 34 | 33 | +1.2 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | GTX 1080 | 64 | 124 | 121 | +1.2 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | GTX 1660 | 32e sep | 64 | 64 | +0.3 % | down 8x4 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | GTX 1660 | 32e sep | 226 | 220 | +1.2 % | down 16x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 1080p | GTX 860M | 32e sep | 133 | 131 | +0.9 % | down 8x2x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | GTX 860M | 32e sep | 488 | 478 | +1.1 % | down 16x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 1080p | RTX 2070 | 32e | 34 | 33 | +0.8 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | RTX 2070 | 32e | 126 | 123 | +1.6 % | down 16x4 e3 / direct 2.5s / up 2x32 e1 |
| 100 | 1080p | RTX 3060 | 64 | 29 | 28 | +1.2 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | RTX 3060 | 64 | 105 | 102 | +1.2 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | RTX 4070 | 32e | 21 | 21 | +0.8 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | RTX 4070 | 32e | 77 | 75 | +1.1 % | down 16x4 e9 / direct 2s / up 2x32 e1 |
| 100 | 1080p | RTX 5070 | 32e | 17 | 17 | +1.1 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | RTX 5070 | 32e | 62 | 61 | +1.2 % | down 16x4 e3 / direct 2.5s / up 2x32 e1 |
| 150 | 1080p | RX 6600 | 64 | 46 | 45 | +0.9 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | RX 6600 | 64 | 175 | 172 | +0.9 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | RX 7900 XTX | 64 | 11 | 9 | +15.6 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RX 7900 XTX | 64 | 31 | 24 | +17.1 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RX 9070 XT | 64 | 11 | 11 | +1.4 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | RX 9070 XT | 64 | 32 | 32 | +1.1 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | Radeon 680M | 64 | 232 | 220 | +3.4 % | down 8x4 e1 / sep 3s / up 32 e1 |
| 150 | 4k | Radeon 680M | 64 | 794 | 769 | +1.7 % | down 16x2 e3 / sep 2.5s / up 32 e2 |
| 150 | 1080p | RX 5500 XT | 64 | 55 | 45 | +12.1 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RX 5500 XT | 64 | 209 | 169 | +12.2 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RX 590 | 64 | 46 | 45 | +1.5 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | RX 590 | 64 | 173 | 169 | +1.2 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | Arc B580 | 64 | 27 | 26 | +0.8 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | Arc B580 | 64 | 93 | 92 | +0.8 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | Iris Xe | 64 | 660 | 649 | +1.0 % | down 8x4 e1 / sep 2.5s / up 32 e3 |
| 150 | 4k | Iris Xe | 64 | 2543 | 2500 | +0.9 % | down 16x4 e1 / sep 2.5s / up 64 e1 |
| 150 | 1080p | UHD 630 | 64 sep | 505 | 370 | +21.6 % | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 150 | 4k | UHD 630 | 64 sep | 1744 | 1293 | +18.1 % | down 16x2x2 e1 / sep 2.5s / up 64 e1 |
| 150 | 1080p | GTX 1080 | 64 | 34 | 33 | +1.5 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | GTX 1080 | 64 | 124 | 121 | +1.2 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | GTX 1660 | 64 sep | 89 | 66 | +21.9 % | down 8x4 e1 / sep 3s / up 32 e1 |
| 150 | 4k | GTX 1660 | 64 sep | 295 | 222 | +17.2 % | down 16x2 e1 / sep 3s / up 32 e1 |
| 150 | 1080p | GTX 860M | 64 sep | 160 | 133 | +11.3 % | down 8x2x2 e1 / sep 3s / up 32 e1 |
| 150 | 4k | GTX 860M | 64 sep | 543 | 479 | +6.8 % | down 16x2x2 e1 / sep 2.5s / up 64 e1 |
| 150 | 1080p | RTX 2070 | 64 | 59 | 33 | +54.4 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RTX 2070 | 64 | 225 | 122 | +55.2 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RTX 3060 | 64 | 29 | 28 | +1.5 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | RTX 3060 | 64 | 105 | 102 | +1.2 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | RTX 4070 | 64 | 24 | 20 | +9.5 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RTX 4070 | 64 | 88 | 75 | +9.6 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RTX 5070 | 64 | 21 | 16 | +13.9 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RTX 5070 | 64 | 76 | 60 | +14.1 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 200 | 1080p | RX 6600 | 128 | 46 | 45 | +0.9 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 4k | RX 6600 | 128 | 175 | 172 | +0.9 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | RX 7900 XTX | 64e | 9 | 9 | +1.3 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RX 7900 XTX | 64e | 24 | 24 | +1.1 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 1080p | RX 9070 XT | 128 | 11 | 11 | +1.1 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RX 9070 XT | 128 | 32 | 32 | +1.1 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | Radeon 680M | 64 | 236 | 221 | +4.1 % | down 8x4 e1 / sep 3s / up 32 e1 |
| 200 | 4k | Radeon 680M | 64 | 798 | 771 | +1.8 % | down 16x2 e1 / sep 3s / up 32 e1 |
| 200 | 1080p | RX 5500 XT | 64e | 46 | 45 | +1.5 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RX 5500 XT | 64e | 174 | 170 | +1.1 % | down 16x8 e3 / direct 2.5s / up 2x64 e1 |
| 200 | 1080p | RX 590 | 128 | 46 | 45 | +1.3 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RX 590 | 128 | 173 | 169 | +1.2 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | Arc B580 | 128 | 27 | 26 | +0.7 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | Arc B580 | 128 | 93 | 92 | +0.7 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 1080p | Iris Xe | 64 | 666 | 650 | +1.2 % | down 8x4x4 e3 / direct 2s / up 128 p8 |
| 200 | 4k | Iris Xe | 64 | 2548 | 2501 | +1.0 % | down 16x4 e1 / sep 2.5s / up 64 e1 |
| 200 | 1080p | UHD 630 | 64e sep | 412 | 373 | +6.1 % | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 4k | UHD 630 | 64e sep | 1358 | 1296 | +2.5 % | down 16x2x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 1080p | GTX 1080 | 128 | 34 | 33 | +1.3 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | GTX 1080 | 128 | 124 | 121 | +1.2 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | GTX 1660 | 64e sep | 75 | 66 | +8.0 % | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 4k | GTX 1660 | 64e sep | 236 | 223 | +3.0 % | down 16x4 e1 / sep 2.5s / up 64 e1 |
| 200 | 1080p | GTX 860M | 64e sep | 151 | 135 | +7.0 % | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 4k | GTX 860M | 64e sep | 506 | 480 | +2.7 % | down 16x2x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 1080p | RTX 2070 | 64e | 33 | 33 | +0.8 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RTX 2070 | 64e | 124 | 122 | +0.9 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 1080p | RTX 3060 | 128 | 29 | 28 | +1.2 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RTX 3060 | 128 | 104 | 102 | +1.2 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | RTX 4070 | 64e | 21 | 20 | +0.8 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RTX 4070 | 64e | 76 | 75 | +0.8 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 1080p | RTX 5070 | 64e | 17 | 16 | +1.1 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RTX 5070 | 64e | 61 | 60 | +0.8 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
