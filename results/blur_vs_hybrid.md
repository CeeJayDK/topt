# TOPT_Blur against the hybrid search, per GPU

TOPT_Blur's class for each GPU profile (its per-GPU table rule) against the cheapest hybrid design
meeting the medium profile on that GPU (results/hybrid_gpu_best.json). us = marginal cost over the
GPU's plain composite pass; gain = (TOPT_Blur - hybrid) in % of the composite pass.

## 1080p

| sigma | median gain | worst GPU for TOPT_Blur | TOPT_Blur us | hybrid us | hybrid design |
|---:|---:|---|---:|---:|---|
| 2 | +0.0 % | RTX 2070 (2): +53.7 % | 91 | 65 | down 2 e3 / sep 2s / up 2 e1 |
| 3 | +5.7 % | RTX 2070 (2 sep): +67.1 % | 103 | 71 | down 2 e5 / sep 2s / up 2 e1 |
| 4 | +4.1 % | RTX 2070 (4s): +8.4 % | 82 | 78 | down 2 e1 / sep 2.5s / up 2 e1 |
| 6 | +22.3 % | RTX 2070 (4s sep): +71.1 % | 83 | 50 | down 4 e5 / sep 2s / up 2x2 e1 |
| 8 | +20.7 % | RTX 2070 (4 sep): +75.8 % | 75 | 39 | down 4 e3 / sep 2.5s / up 4 e1 |
| 12 | +37.3 % | RTX 2070 (4 sep): +87.0 % | 77 | 36 | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 16 | +6.5 % | RTX 2070 (8 sep): +54.6 % | 60 | 34 | down 8 e3 / sep 2.5s / up 8 e1 |
| 24 | +10.9 % | RTX 2070 (8 sep): +57.4 % | 61 | 33 | down 16 e3 / direct 2s / up 2x8 e1 |
| 32 | +6.9 % | UHD 630 (16 sep): +61.6 % | 678 | 327 | down 8x2 e3 / sep 2.5s / up 2x8 e1 |
| 48 | +12.9 % | UHD 630 (16 sep): +62.9 % | 682 | 323 | down 8x2 e1 / sep 2.5s / up 16 e1 |
| 64 | +13.4 % | UHD 630 (32 sep): +66.7 % | 705 | 324 | down 8x2x2 e3 / sep 2.5s / up 32 e1 |
| 100 | +13.6 % | UHD 630 (32 sep): +66.4 % | 709 | 330 | down 8x2x2 e1 / sep 2.5s / up 32 e1 |
| 150 | +12.9 % | UHD 630 (64 sep): +63.1 % | 696 | 336 | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 200 | +13.3 % | UHD 630 (64 sep): +63.1 % | 700 | 339 | down 8x4x2 e1 / sep 2.5s / up 64 e1 |

## 4k

| sigma | median gain | worst GPU for TOPT_Blur | TOPT_Blur us | hybrid us | hybrid design |
|---:|---:|---|---:|---:|---|
| 2 | +0.0 % | RTX 2070 (2): +56.1 % | 356 | 252 | down 2 e3 / sep 2s / up 2 e1 |
| 3 | +5.2 % | RTX 2070 (2 sep): +68.2 % | 404 | 277 | down 2 e5 / sep 2s / up 2 e1 |
| 4 | +4.7 % | RTX 2070 (4s): +13.6 % | 328 | 302 | down 2 e1 / sep 2.5s / up 2 e1 |
| 6 | +19.2 % | RTX 2070 (4s sep): +72.5 % | 340 | 205 | down 4 e5 / sep 2s / up 2x2 e1 |
| 8 | +21.2 % | RTX 2070 (4 sep): +77.0 % | 310 | 167 | down 4 e3 / sep 2.5s / up 4 e1 |
| 12 | +37.0 % | RTX 2070 (4 sep): +96.2 % | 318 | 139 | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 16 | +6.6 % | RTX 2070 (8 sep): +55.5 % | 231 | 128 | down 8 e3 / sep 2.5s / up 8 e1 |
| 24 | +9.2 % | RTX 2070 (8 sep): +58.3 % | 233 | 125 | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | +5.4 % | RTX 2070 (16 sep): +53.6 % | 225 | 125 | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 48 | +6.5 % | RTX 2070 (32): +54.2 % | 224 | 124 | down 16x2 e3 / direct 2s / up 2x16 e1 |
| 64 | +6.3 % | RTX 2070 (32): +54.2 % | 225 | 124 | down 16x2 e3 / direct 2.5s / up 2x16 e1 |
| 100 | +6.9 % | RTX 2070 (32): +55.4 % | 226 | 123 | down 16x4 e3 / direct 2.5s / up 2x32 e1 |
| 150 | +6.6 % | RTX 2070 (64): +54.4 % | 223 | 122 | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 200 | +6.6 % | RTX 2070 (64): +54.4 % | 224 | 122 | down 16x4 e1 / direct 2.5s / up 64 e1 |

## Every GPU

| sigma | res | GPU | TOPT_Blur class | TOPT_Blur us | hybrid us | gain | hybrid design |
|---:|---|---|---|---:|---:|---:|---|
| 2 | 1080p | GTX 860M | 2 | 280 | 280 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | GTX 860M | 2 | 1115 | 1115 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | GTX 1080 | 2 | 61 | 61 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | GTX 1080 | 2 | 236 | 236 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | GTX 1660 | 2 | 125 | 125 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | GTX 1660 | 2 | 492 | 492 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | RTX 2070 | 2 | 91 | 65 | +53.7 % | down 2 e3 / sep 2s / up 2 e1 |
| 2 | 4k | RTX 2070 | 2 | 356 | 252 | +56.1 % | down 2 e3 / sep 2s / up 2 e1 |
| 2 | 1080p | RTX 3060 | 2 | 60 | 60 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RTX 3060 | 2 | 233 | 233 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | RTX 4070 | 2 | 42 | 42 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RTX 4070 | 2 | 163 | 163 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | RTX 5070 | 2 | 33 | 33 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RTX 5070 | 2 | 129 | 128 | +0.9 % | down 2 e3 / sep 2s / up 2 e1 |
| 2 | 1080p | RX 590 | 2 | 87 | 87 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RX 590 | 2 | 343 | 343 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | RX 5500 XT | 2 | 104 | 104 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RX 5500 XT | 2 | 410 | 410 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | RX 6600 | 2 | 90 | 86 | +4.7 % | down 2 e9 / direct 2s / up 2 p4 |
| 2 | 4k | RX 6600 | 2 | 356 | 340 | +4.8 % | down 2 e9 / direct 2s / up 2 p4 |
| 2 | 1080p | RX 7900 XTX | 2 | 15 | 15 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RX 7900 XTX | 2 | 54 | 53 | +3.6 % | down 2 e3 / sep 2s / up 2 e1 |
| 2 | 1080p | RX 9070 XT | 2 | 18 | 18 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | RX 9070 XT | 2 | 68 | 68 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 1080p | Radeon 680M | 2 | 383 | 381 | +0.7 % | down 2 e3 / direct 2s / up 2 e3 |
| 2 | 4k | Radeon 680M | 2 | 1498 | 1488 | +0.7 % | down 2 e3 / direct 2s / up 2 e3 |
| 2 | 1080p | UHD 630 | 2 sep | 811 | 720 | +16.0 % | down 2 e3 / sep 2s / up 2 e1 |
| 2 | 4k | UHD 630 | 2 sep | 3211 | 2846 | +16.1 % | down 2 e3 / sep 2s / up 2 e1 |
| 2 | 1080p | Iris Xe | 2 | 1242 | 1242 | +0.0 % | down 2 e3 / direct 2s / up 2 e3 |
| 2 | 4k | Iris Xe | 2 | 4949 | 4949 | +0.0 % | down 2 e3 / direct 2s / up 2 e3 |
| 2 | 1080p | Arc B580 | 2 | 57 | 57 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 2 | 4k | Arc B580 | 2 | 214 | 214 | +0.0 % | down 2 e3 / direct 2s / up 2 p4 |
| 3 | 1080p | GTX 860M | 2 sep | 299 | 294 | +2.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | GTX 860M | 2 sep | 1188 | 1169 | +2.1 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | GTX 1080 | 2 sep | 76 | 72 | +6.0 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 4k | GTX 1080 | 2 sep | 294 | 283 | +4.8 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 1080p | GTX 1660 | 2 sep | 143 | 137 | +5.9 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | GTX 1660 | 2 sep | 564 | 538 | +6.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | RTX 2070 | 2 sep | 103 | 71 | +67.1 % | down 2 e5 / sep 2s / up 2 e1 |
| 3 | 4k | RTX 2070 | 2 sep | 404 | 277 | +68.2 % | down 2 e5 / sep 2s / up 2 e1 |
| 3 | 1080p | RTX 3060 | 2 sep | 64 | 64 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | RTX 3060 | 2 sep | 247 | 247 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | RTX 4070 | 2 sep | 49 | 47 | +4.3 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | RTX 4070 | 2 sep | 188 | 182 | +4.4 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | RTX 5070 | 2 sep | 38 | 34 | +15.1 % | down 2 e5 / sep 2s / up 2 e1 |
| 3 | 4k | RTX 5070 | 2 sep | 144 | 128 | +15.4 % | down 2 e5 / sep 2s / up 2 e1 |
| 3 | 1080p | RX 590 | 2 sep | 105 | 105 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | RX 590 | 2 sep | 412 | 412 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | RX 5500 XT | 2 sep | 110 | 105 | +5.5 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | RX 5500 XT | 2 sep | 429 | 411 | +5.5 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | RX 6600 | 2 sep | 108 | 102 | +6.2 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 4k | RX 6600 | 2 sep | 422 | 404 | +5.4 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 1080p | RX 7900 XTX | 2 sep | 17 | 16 | +11.0 % | down 2 e1 / sep 2.5s / up 2 e1 |
| 3 | 4k | RX 7900 XTX | 2 sep | 58 | 53 | +11.9 % | down 2 e1 / sep 2.5s / up 2 e1 |
| 3 | 1080p | RX 9070 XT | 2 sep | 20 | 20 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | RX 9070 XT | 2 sep | 72 | 72 | +0.0 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 1080p | Radeon 680M | 2 | 454 | 414 | +10.6 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 4k | Radeon 680M | 2 | 1781 | 1622 | +10.7 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 1080p | UHD 630 | 2 sep | 892 | 720 | +30.2 % | down 2 e5 / sep 2s / up 2 e1 |
| 3 | 4k | UHD 630 | 2 sep | 3536 | 2846 | +30.4 % | down 2 e5 / sep 2s / up 2 e1 |
| 3 | 1080p | Iris Xe | 2 | 1333 | 1270 | +5.1 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 4k | Iris Xe | 2 | 5313 | 5061 | +5.1 % | down 2 e1 / direct 2s / up 2 e2 |
| 3 | 1080p | Arc B580 | 2 sep | 64 | 62 | +4.4 % | down 2 e1 / sep 2s / up 2 e2 |
| 3 | 4k | Arc B580 | 2 sep | 232 | 224 | +4.6 % | down 2 e1 / sep 2s / up 2 e2 |
| 4 | 1080p | GTX 860M | 4s | 230 | 216 | +5.7 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | GTX 860M | 4s | 919 | 873 | +4.8 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | GTX 1080 | 4s | 54 | 54 | +0.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | GTX 1080 | 4s | 207 | 206 | +0.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | GTX 1660 | 4s | 107 | 103 | +3.5 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | GTX 1660 | 4s | 434 | 418 | +3.6 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RTX 2070 | 4s | 82 | 78 | +8.4 % | down 2 e1 / sep 2.5s / up 2 e1 |
| 4 | 4k | RTX 2070 | 4s | 328 | 302 | +13.6 % | down 2 e1 / sep 2.5s / up 2 e1 |
| 4 | 1080p | RTX 3060 | 4s | 50 | 48 | +4.6 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RTX 3060 | 4s | 190 | 181 | +4.6 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RTX 4070 | 4s | 37 | 36 | +3.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RTX 4070 | 4s | 145 | 141 | +3.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RTX 5070 | 4s | 29 | 28 | +4.8 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RTX 5070 | 4s | 112 | 107 | +4.9 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RX 590 | 4s | 76 | 75 | +1.0 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RX 590 | 4s | 293 | 290 | +1.0 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RX 5500 XT | 4s | 86 | 81 | +6.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RX 5500 XT | 4s | 336 | 316 | +6.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RX 6600 | 4s | 79 | 78 | +1.0 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RX 6600 | 4s | 317 | 312 | +1.4 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RX 7900 XTX | 4s | 14 | 13 | +6.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RX 7900 XTX | 4s | 45 | 42 | +6.7 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | RX 9070 XT | 4s | 17 | 16 | +4.4 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | RX 9070 XT | 4s | 58 | 55 | +4.7 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | Radeon 680M | 4s | 342 | 338 | +1.1 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | Radeon 680M | 4s | 1372 | 1370 | +0.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | UHD 630 | 4s sep | 692 | 671 | +3.7 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | UHD 630 | 4s sep | 2798 | 2658 | +6.2 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 1080p | Iris Xe | 4s | 1143 | 1135 | +0.7 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | Iris Xe | 4s | 4791 | 4791 | +0.0 % | down 4 e5 / direct 2s / up 2x2 e2 |
| 4 | 1080p | Arc B580 | 4s | 50 | 48 | +5.4 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 4 | 4k | Arc B580 | 4s | 180 | 171 | +5.1 % | down 4 e9 / direct 2s / up 2x2 e2 |
| 6 | 1080p | GTX 860M | 4s sep | 233 | 200 | +14.1 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | GTX 860M | 4s sep | 937 | 824 | +12.1 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | GTX 1080 | 4s sep | 59 | 41 | +29.1 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 4k | GTX 1080 | 4s sep | 222 | 159 | +26.9 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 1080p | GTX 1660 | 4s sep | 109 | 91 | +16.5 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | GTX 1660 | 4s sep | 452 | 384 | +15.9 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | RTX 2070 | 4s sep | 83 | 50 | +71.1 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 4k | RTX 2070 | 4s sep | 340 | 205 | +72.5 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 1080p | RTX 3060 | 4s sep | 52 | 43 | +17.3 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | RTX 3060 | 4s sep | 194 | 163 | +16.0 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | RTX 4070 | 4s sep | 38 | 30 | +20.7 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | RTX 4070 | 4s sep | 152 | 124 | +19.3 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | RTX 5070 | 4s sep | 30 | 25 | +19.7 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 4k | RTX 5070 | 4s sep | 116 | 98 | +18.5 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 1080p | RX 590 | 4s sep | 81 | 59 | +26.8 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 4k | RX 590 | 4s sep | 311 | 228 | +25.2 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | RX 5500 XT | 4s sep | 89 | 84 | +5.7 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | RX 5500 XT | 4s sep | 342 | 326 | +4.8 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | RX 6600 | 4s sep | 82 | 56 | +30.7 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 4k | RX 6600 | 4s sep | 334 | 228 | +31.5 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 1080p | RX 7900 XTX | 4s sep | 15 | 14 | +11.4 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | RX 7900 XTX | 4s sep | 47 | 44 | +8.0 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 1080p | RX 9070 XT | 4s sep | 18 | 15 | +23.9 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 4k | RX 9070 XT | 4s sep | 60 | 49 | +19.2 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 1080p | Radeon 680M | 4s | 360 | 236 | +33.0 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | Radeon 680M | 4s | 1443 | 968 | +32.1 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 1080p | UHD 630 | 4s sep | 727 | 528 | +34.8 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 4k | UHD 630 | 4s sep | 2879 | 2141 | +32.5 % | down 4 e5 / sep 2s / up 2x2 e1 |
| 6 | 1080p | Iris Xe | 4s | 1171 | 719 | +36.6 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | Iris Xe | 4s | 4882 | 3123 | +35.6 % | down 4 e5 / direct 2s / up 4 p5 |
| 6 | 1080p | Arc B580 | 4s sep | 53 | 47 | +14.8 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 6 | 4k | Arc B580 | 4s sep | 187 | 169 | +10.1 % | down 4 e9 / sep 2.5s / up 4 p5 |
| 8 | 1080p | GTX 860M | 4 sep | 216 | 155 | +26.0 % | down 4x2 e3 / direct 2s / up 2x4 e2 |
| 8 | 4k | GTX 860M | 4 sep | 872 | 635 | +25.4 % | down 4x2 e3 / direct 2s / up 2x4 e2 |
| 8 | 1080p | GTX 1080 | 4 sep | 43 | 40 | +5.9 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 4k | GTX 1080 | 4 sep | 163 | 146 | +7.3 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 1080p | GTX 1660 | 4 sep | 96 | 71 | +22.9 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | GTX 1660 | 4 sep | 403 | 304 | +23.1 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | RTX 2070 | 4 sep | 75 | 39 | +75.8 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | RTX 2070 | 4 sep | 310 | 167 | +77.0 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | RTX 3060 | 4 sep | 45 | 37 | +17.4 % | down 4x2 e3 / direct 2s / up 2x4 e2 |
| 8 | 4k | RTX 3060 | 4 sep | 172 | 134 | +19.3 % | down 4x2 e3 / direct 2s / up 2x4 e2 |
| 8 | 1080p | RTX 4070 | 4 sep | 32 | 25 | +18.5 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | RTX 4070 | 4 sep | 130 | 103 | +18.7 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | RTX 5070 | 4 sep | 28 | 19 | +34.2 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | RTX 5070 | 4 sep | 110 | 74 | +34.9 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | RX 590 | 4 sep | 59 | 54 | +6.3 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 4k | RX 590 | 4 sep | 228 | 204 | +7.3 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 1080p | RX 5500 XT | 4 sep | 90 | 60 | +35.3 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | RX 5500 XT | 4 sep | 349 | 232 | +35.6 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | RX 6600 | 4 sep | 56 | 53 | +3.9 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 4k | RX 6600 | 4 sep | 236 | 209 | +7.9 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 1080p | RX 7900 XTX | 4 sep | 14 | 10 | +38.4 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | RX 7900 XTX | 4 sep | 48 | 31 | +41.3 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | RX 9070 XT | 4 sep | 15 | 13 | +17.8 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | RX 9070 XT | 4 sep | 52 | 41 | +18.8 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | Radeon 680M | 4 sep | 240 | 230 | +2.7 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 4k | Radeon 680M | 4 sep | 1032 | 908 | +8.4 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 1080p | UHD 630 | 4 sep | 735 | 417 | +55.8 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | UHD 630 | 4 sep | 2925 | 1652 | +56.0 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 1080p | Iris Xe | 4 sep | 729 | 690 | +3.1 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 4k | Iris Xe | 4 sep | 3407 | 2995 | +8.3 % | down 8 e9 / sep 3s / up 2x4 p5 |
| 8 | 1080p | Arc B580 | 4 sep | 49 | 37 | +27.6 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 8 | 4k | Arc B580 | 4 sep | 179 | 129 | +28.7 % | down 4 e3 / sep 2.5s / up 4 e1 |
| 12 | 1080p | GTX 860M | 4 sep | 227 | 137 | +38.2 % | down 8 e5 / sep 3s / up 8 p4 |
| 12 | 4k | GTX 860M | 4 sep | 914 | 542 | +39.9 % | down 8 e5 / sep 3s / up 8 p4 |
| 12 | 1080p | GTX 1080 | 4 sep | 43 | 34 | +16.2 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | GTX 1080 | 4 sep | 164 | 129 | +15.1 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 1080p | GTX 1660 | 4 sep | 99 | 65 | +31.4 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 4k | GTX 1660 | 4 sep | 415 | 260 | +36.2 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | RTX 2070 | 4 sep | 77 | 36 | +87.0 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 4k | RTX 2070 | 4 sep | 318 | 139 | +96.2 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | RTX 3060 | 4 sep | 48 | 30 | +36.3 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | RTX 3060 | 4 sep | 181 | 110 | +36.5 % | down 8 e5 / sep 3s / up 8 p4 |
| 12 | 1080p | RTX 4070 | 4 sep | 32 | 23 | +25.7 % | down 8 e3 / direct 2s / up 2x4 e1 |
| 12 | 4k | RTX 4070 | 4 sep | 133 | 88 | +31.2 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | RTX 5070 | 4 sep | 29 | 17 | +44.5 % | down 8 e3 / direct 2s / up 2x4 e1 |
| 12 | 4k | RTX 5070 | 4 sep | 113 | 63 | +49.4 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | RX 590 | 4 sep | 61 | 47 | +17.0 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | RX 590 | 4 sep | 235 | 181 | +16.2 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 1080p | RX 5500 XT | 4 sep | 94 | 56 | +46.6 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 4k | RX 5500 XT | 4 sep | 367 | 210 | +48.0 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | RX 6600 | 4 sep | 58 | 47 | +12.9 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | RX 6600 | 4 sep | 243 | 182 | +18.2 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 1080p | RX 7900 XTX | 4 sep | 15 | 9 | +51.1 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | RX 7900 XTX | 4 sep | 50 | 29 | +52.8 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | RX 9070 XT | 4 sep | 16 | 10 | +40.8 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | RX 9070 XT | 4 sep | 54 | 33 | +37.5 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 1080p | Radeon 680M | 4 sep | 245 | 206 | +10.3 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | Radeon 680M | 4 sep | 1038 | 790 | +16.7 % | down 8 e5 / sep 2.5s / up 8 p5 |
| 12 | 1080p | UHD 630 | 4 sep | 770 | 347 | +74.1 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 4k | UHD 630 | 4 sep | 3064 | 1396 | +73.4 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 12 | 1080p | Iris Xe | 4 sep | 736 | 649 | +7.0 % | down 8 e5 / sep 2s / up 8 p9 |
| 12 | 4k | Iris Xe | 4 sep | 3407 | 2568 | +17.0 % | down 8 e5 / sep 2s / up 8 p9 |
| 12 | 1080p | Arc B580 | 4 sep | 51 | 33 | +40.2 % | down 8 e3 / direct 2s / up 8 p4 |
| 12 | 4k | Arc B580 | 4 sep | 187 | 114 | +41.5 % | down 8 e3 / sep 2.5s / up 2x4 e1 |
| 16 | 1080p | GTX 860M | 8 sep | 140 | 130 | +4.5 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | GTX 860M | 8 sep | 552 | 510 | +4.5 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | GTX 1080 | 8 sep | 35 | 35 | +0.2 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 4k | GTX 1080 | 8 sep | 130 | 127 | +1.5 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 1080p | GTX 1660 | 8 sep | 73 | 60 | +11.7 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | GTX 1660 | 8 sep | 282 | 231 | +11.8 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | RTX 2070 | 8 sep | 60 | 34 | +54.6 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | RTX 2070 | 8 sep | 231 | 128 | +55.5 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | RTX 3060 | 8 sep | 30 | 30 | +1.1 % | down 8 e1 / sep 2.5s / up 8 p4 |
| 16 | 4k | RTX 3060 | 8 sep | 112 | 110 | +1.1 % | down 8x2 e3 / direct 2s / up 2x8 e2 |
| 16 | 1080p | RTX 4070 | 8 sep | 24 | 21 | +8.6 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | RTX 4070 | 8 sep | 91 | 79 | +8.7 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | RTX 5070 | 8 sep | 21 | 16 | +18.4 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | RTX 5070 | 8 sep | 76 | 57 | +18.7 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | RX 590 | 8 sep | 48 | 47 | +0.6 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 4k | RX 590 | 8 sep | 182 | 177 | +1.6 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 1080p | RX 5500 XT | 8 sep | 58 | 48 | +11.6 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | RX 5500 XT | 8 sep | 221 | 183 | +11.7 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | RX 6600 | 8 sep | 48 | 48 | +0.1 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 4k | RX 6600 | 8 sep | 182 | 178 | +1.0 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 1080p | RX 7900 XTX | 8 sep | 10 | 9 | +15.5 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | RX 7900 XTX | 8 sep | 32 | 25 | +16.7 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | RX 9070 XT | 8 sep | 11 | 11 | +1.1 % | down 8 e1 / sep 2.5s / up 8 p4 |
| 16 | 4k | RX 9070 XT | 8 sep | 34 | 33 | +1.1 % | down 8 e1 / sep 2.5s / up 8 p4 |
| 16 | 1080p | Radeon 680M | 8 sep | 211 | 210 | +0.3 % | down 8 e1 / sep 2.5s / up 8 p4 |
| 16 | 4k | Radeon 680M | 8 sep | 794 | 784 | +0.7 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 1080p | UHD 630 | 8 sep | 492 | 325 | +29.2 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | UHD 630 | 8 sep | 1933 | 1268 | +29.3 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 1080p | Iris Xe | 8 sep | 653 | 651 | +0.1 % | down 8 e1 / sep 2.5s / up 8 p4 |
| 16 | 4k | Iris Xe | 8 sep | 2582 | 2543 | +0.8 % | down 16 e9 / sep 2s / up 2x8 p5 |
| 16 | 1080p | Arc B580 | 8 sep | 35 | 31 | +9.2 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 16 | 4k | Arc B580 | 8 sep | 119 | 102 | +9.6 % | down 8 e3 / sep 2.5s / up 8 e1 |
| 24 | 1080p | GTX 860M | 8 sep | 143 | 129 | +5.7 % | down 8x2 e3 / sep 2s / up 2x8 e1 |
| 24 | 4k | GTX 860M | 8 sep | 563 | 490 | +7.8 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | GTX 1080 | 8 sep | 35 | 32 | +5.4 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | GTX 1080 | 8 sep | 130 | 121 | +4.1 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | GTX 1660 | 8 sep | 74 | 61 | +11.4 % | down 8 e1 / sep 2.5s / up 8 e1 |
| 24 | 4k | GTX 1660 | 8 sep | 285 | 225 | +14.0 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | RTX 2070 | 8 sep | 61 | 33 | +57.4 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RTX 2070 | 8 sep | 233 | 125 | +58.3 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | RTX 3060 | 8 sep | 31 | 27 | +7.4 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | RTX 3060 | 8 sep | 114 | 103 | +5.9 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | RTX 4070 | 8 sep | 25 | 21 | +10.4 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RTX 4070 | 8 sep | 92 | 77 | +10.5 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 1080p | RTX 5070 | 8 sep | 21 | 15 | +21.0 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RTX 5070 | 8 sep | 77 | 55 | +21.4 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 1080p | RX 590 | 8 sep | 48 | 44 | +5.2 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | RX 590 | 8 sep | 184 | 170 | +4.3 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | RX 5500 XT | 8 sep | 59 | 47 | +14.1 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RX 5500 XT | 8 sep | 226 | 178 | +14.5 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | RX 6600 | 8 sep | 48 | 45 | +4.1 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | RX 6600 | 8 sep | 183 | 172 | +3.2 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | RX 7900 XTX | 8 sep | 10 | 8 | +18.1 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | RX 7900 XTX | 8 sep | 32 | 24 | +19.5 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 1080p | RX 9070 XT | 8 sep | 11 | 9 | +12.1 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 4k | RX 9070 XT | 8 sep | 35 | 31 | +7.2 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | Radeon 680M | 8 sep | 213 | 209 | +1.0 % | down 8x2 e3 / direct 2s / up 16 p4 |
| 24 | 4k | Radeon 680M | 8 sep | 798 | 760 | +2.6 % | down 16 e3 / direct 2s / up 16 p4 |
| 24 | 1080p | UHD 630 | 8 sep | 501 | 323 | +31.1 % | down 8x2 e3 / sep 2s / up 2x8 e1 |
| 24 | 4k | UHD 630 | 8 sep | 1968 | 1198 | +33.9 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 24 | 1080p | Iris Xe | 8 sep | 654 | 643 | +0.9 % | down 8x2 e3 / direct 2s / up 16 p4 |
| 24 | 4k | Iris Xe | 8 sep | 2589 | 2503 | +1.7 % | down 16 e5 / sep 2.5s / up 16 p4 |
| 24 | 1080p | Arc B580 | 8 sep | 36 | 30 | +11.9 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 24 | 4k | Arc B580 | 8 sep | 121 | 99 | +12.4 % | down 16 e3 / direct 2s / up 2x8 e1 |
| 32 | 1080p | GTX 860M | 16 sep | 185 | 130 | +23.6 % | down 8x2 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 4k | GTX 860M | 16 sep | 519 | 491 | +3.0 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | GTX 1080 | 16 | 33 | 32 | +0.6 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | GTX 1080 | 16 | 124 | 122 | +1.0 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | GTX 1660 | 16 sep | 108 | 62 | +42.6 % | down 8x2 e9 / direct 2s / up 16 e1 |
| 32 | 4k | GTX 1660 | 16 sep | 272 | 226 | +10.7 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RTX 2070 | 16 sep | 58 | 34 | +51.4 % | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 32 | 4k | RTX 2070 | 16 sep | 225 | 125 | +53.6 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RTX 3060 | 16 sep | 28 | 28 | +0.5 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | RTX 3060 | 16 sep | 103 | 103 | +0.3 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | RTX 4070 | 16 | 23 | 21 | +6.1 % | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 32 | 4k | RTX 4070 | 16 | 89 | 77 | +8.2 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RTX 5070 | 16 | 20 | 16 | +15.1 % | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 32 | 4k | RTX 5070 | 16 | 74 | 55 | +18.4 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RX 590 | 16 | 45 | 45 | +0.6 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | RX 590 | 16 | 175 | 171 | +1.4 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | RX 5500 XT | 16 sep | 54 | 48 | +7.8 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 4k | RX 5500 XT | 16 sep | 207 | 178 | +8.8 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | RX 6600 | 16 | 45 | 45 | +0.4 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | RX 6600 | 16 | 176 | 173 | +0.8 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | RX 7900 XTX | 16 | 9 | 9 | +4.6 % | down 8x2 e9 / direct 2s / up 16 e1 |
| 32 | 4k | RX 7900 XTX | 16 | 30 | 25 | +12.6 % | down 8x2 e9 / direct 2s / up 16 e1 |
| 32 | 1080p | RX 9070 XT | 16 | 10 | 9 | +0.9 % | down 16 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | RX 9070 XT | 16 | 32 | 31 | +1.1 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | Radeon 680M | 16 | 350 | 211 | +37.0 % | down 8x2 e3 / direct 2.5s / up 16 p4 |
| 32 | 4k | Radeon 680M | 16 | 769 | 764 | +0.3 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | UHD 630 | 16 sep | 678 | 327 | +61.6 % | down 8x2 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 4k | UHD 630 | 16 sep | 1829 | 1202 | +27.6 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 32 | 1080p | Iris Xe | 16 | 992 | 645 | +28.0 % | down 8x2 e3 / sep 2.5s / up 16 p4 |
| 32 | 4k | Iris Xe | 16 | 2518 | 2504 | +0.3 % | down 16 e3 / sep 2.5s / up 16 p4 |
| 32 | 1080p | Arc B580 | 16 | 32 | 31 | +2.9 % | down 16 e3 / direct 2.5s / up 2x8 e1 |
| 32 | 4k | Arc B580 | 16 | 114 | 101 | +7.7 % | down 16 e3 / sep 2.5s / up 2x8 e1 |
| 48 | 1080p | GTX 860M | 16 sep | 186 | 128 | +24.9 % | down 8x2 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | GTX 860M | 16 sep | 521 | 479 | +4.5 % | down 16x2 e3 / sep 2s / up 2x16 e1 |
| 48 | 1080p | GTX 1080 | 32 | 33 | 33 | +0.1 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 4k | GTX 1080 | 32 | 121 | 121 | +0.1 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | GTX 1660 | 16 sep | 108 | 61 | +43.9 % | down 8x2 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | GTX 1660 | 16 sep | 272 | 222 | +11.8 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 1080p | RTX 2070 | 32 | 58 | 33 | +53.2 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | RTX 2070 | 32 | 224 | 124 | +54.2 % | down 16x2 e3 / direct 2s / up 2x16 e1 |
| 48 | 1080p | RTX 3060 | 32 | 28 | 28 | +0.4 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 4k | RTX 3060 | 32 | 103 | 102 | +0.4 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | RTX 4070 | 32 | 24 | 21 | +8.3 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | RTX 4070 | 32 | 88 | 75 | +8.5 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 1080p | RTX 5070 | 32 | 20 | 15 | +18.1 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | RTX 5070 | 32 | 72 | 54 | +18.1 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 1080p | RX 590 | 32 | 45 | 45 | +0.2 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 4k | RX 590 | 32 | 170 | 169 | +0.2 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | RX 5500 XT | 32 | 54 | 45 | +10.8 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | RX 5500 XT | 32 | 207 | 172 | +10.7 % | down 16x2 e3 / direct 2s / up 2x16 e1 |
| 48 | 1080p | RX 6600 | 32 | 45 | 45 | +0.1 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 4k | RX 6600 | 32 | 173 | 172 | +0.1 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | RX 7900 XTX | 16 | 9 | 8 | +15.0 % | down 16 e1 / direct 2.5s / up 16 e1 |
| 48 | 4k | RX 7900 XTX | 16 | 31 | 24 | +19.0 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 48 | 1080p | RX 9070 XT | 32 | 10 | 10 | +2.4 % | down 16 e1 / direct 2.5s / up 16 e1 |
| 48 | 4k | RX 9070 XT | 32 | 31 | 31 | +0.4 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | Radeon 680M | 32 | 356 | 212 | +38.2 % | down 8x4 e3 / direct 2s / up 32 p4 |
| 48 | 4k | Radeon 680M | 32 | 765 | 763 | +0.2 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | UHD 630 | 16 sep | 682 | 323 | +62.9 % | down 8x2 e1 / sep 2.5s / up 16 e1 |
| 48 | 4k | UHD 630 | 16 sep | 1838 | 1173 | +29.2 % | down 16x2 e3 / sep 2s / up 2x16 e1 |
| 48 | 1080p | Iris Xe | 32 | 993 | 644 | +28.2 % | down 8x4 e3 / direct 2s / up 32 p4 |
| 48 | 4k | Iris Xe | 32 | 2501 | 2497 | +0.1 % | down 16x2 e3 / direct 2s / up 32 p4 |
| 48 | 1080p | Arc B580 | 32 | 34 | 29 | +9.6 % | down 16 e1 / direct 2.5s / up 16 e1 |
| 48 | 4k | Arc B580 | 32 | 112 | 97 | +8.8 % | down 16 e1 / sep 2.5s / up 16 e1 |
| 64 | 1080p | GTX 860M | 32 sep | 192 | 129 | +27.0 % | down 8x2x2 e3 / sep 2.5s / up 32 e1 |
| 64 | 4k | GTX 860M | 32 sep | 520 | 480 | +4.2 % | down 16x2 e3 / sep 2.5s / up 2x16 e1 |
| 64 | 1080p | GTX 1080 | 32 | 33 | 33 | +0.3 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 4k | GTX 1080 | 32 | 122 | 121 | +0.3 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 1080p | GTX 1660 | 32 sep | 111 | 61 | +45.8 % | down 8x2 e1 / sep 3s / up 16 e1 |
| 64 | 4k | GTX 1660 | 32 sep | 273 | 223 | +11.8 % | down 16x2 e3 / sep 2.5s / up 2x16 e1 |
| 64 | 1080p | RTX 2070 | 32 | 59 | 33 | +53.2 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 64 | 4k | RTX 2070 | 32 | 225 | 124 | +54.2 % | down 16x2 e3 / direct 2.5s / up 2x16 e1 |
| 64 | 1080p | RTX 3060 | 32 | 28 | 28 | +0.5 % | down 16x2 e3 / direct 2.5s / up 32 p4 |
| 64 | 4k | RTX 3060 | 32 | 104 | 103 | +0.5 % | down 16x4 e5 / direct 2s / up 2x32 p4 |
| 64 | 1080p | RTX 4070 | 32 | 24 | 21 | +8.3 % | down 16 e1 / sep 3s / up 16 e1 |
| 64 | 4k | RTX 4070 | 32 | 88 | 76 | +8.4 % | down 16 e1 / sep 3s / up 16 e1 |
| 64 | 1080p | RTX 5070 | 32 | 20 | 15 | +18.0 % | down 16 e1 / sep 3s / up 16 e1 |
| 64 | 4k | RTX 5070 | 32 | 73 | 54 | +18.2 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 64 | 1080p | RX 590 | 32 | 45 | 45 | +0.3 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 4k | RX 590 | 32 | 171 | 170 | +0.3 % | down 16x4 e5 / direct 2s / up 2x32 p4 |
| 64 | 1080p | RX 5500 XT | 32 | 54 | 46 | +10.6 % | down 16 e1 / sep 3s / up 16 e1 |
| 64 | 4k | RX 5500 XT | 32 | 209 | 173 | +11.0 % | down 16x2 e3 / sep 2.5s / up 2x16 e1 |
| 64 | 1080p | RX 6600 | 32 | 46 | 45 | +0.2 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 4k | RX 6600 | 32 | 173 | 173 | +0.2 % | down 16x2 e9 / direct 2s / up 32 p4 |
| 64 | 1080p | RX 7900 XTX | 32 | 10 | 8 | +16.1 % | down 16 e1 / direct 2.5s / up 16 e1 |
| 64 | 4k | RX 7900 XTX | 32 | 30 | 24 | +15.4 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 64 | 1080p | RX 9070 XT | 32 | 10 | 10 | +0.4 % | down 16x2 e3 / direct 2.5s / up 32 p4 |
| 64 | 4k | RX 9070 XT | 32 | 32 | 31 | +0.5 % | down 16x2 e3 / direct 2.5s / up 32 p4 |
| 64 | 1080p | Radeon 680M | 32 | 358 | 215 | +38.3 % | down 8x4 e3 / direct 2.5s / up 32 p4 |
| 64 | 4k | Radeon 680M | 32 | 768 | 765 | +0.2 % | down 16x2 e3 / direct 2.5s / up 32 p4 |
| 64 | 1080p | UHD 630 | 32 sep | 705 | 324 | +66.7 % | down 8x2x2 e3 / sep 2.5s / up 32 e1 |
| 64 | 4k | UHD 630 | 32 sep | 1839 | 1177 | +29.1 % | down 16x2 e3 / sep 2.5s / up 2x16 e1 |
| 64 | 1080p | Iris Xe | 32 | 998 | 646 | +28.4 % | down 8x4 e5 / direct 2s / up 32 e3 |
| 64 | 4k | Iris Xe | 32 | 2505 | 2499 | +0.1 % | down 16x2 e3 / sep 2.5s / up 32 p4 |
| 64 | 1080p | Arc B580 | 32 | 34 | 30 | +8.4 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 64 | 4k | Arc B580 | 32 | 113 | 98 | +8.8 % | down 8x4 e5 / direct 2.5s / up 32 e1 |
| 100 | 1080p | GTX 860M | 32 sep | 193 | 131 | +26.8 % | down 8x2x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | GTX 860M | 32 sep | 521 | 478 | +4.6 % | down 16x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 1080p | GTX 1080 | 32 | 33 | 32 | +0.9 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | GTX 1080 | 32 | 123 | 120 | +1.0 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | GTX 1660 | 32 sep | 111 | 62 | +45.5 % | down 8x4 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | GTX 1660 | 32 sep | 274 | 221 | +12.2 % | down 16x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 1080p | RTX 2070 | 32 | 59 | 33 | +53.8 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | RTX 2070 | 32 | 226 | 123 | +55.4 % | down 16x4 e3 / direct 2.5s / up 2x32 e1 |
| 100 | 1080p | RTX 3060 | 32 | 29 | 28 | +1.7 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | RTX 3060 | 32 | 105 | 101 | +1.7 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | RTX 4070 | 32 | 24 | 21 | +8.8 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | RTX 4070 | 32 | 89 | 75 | +9.2 % | down 16x4 e9 / direct 2s / up 2x32 e1 |
| 100 | 1080p | RTX 5070 | 32 | 20 | 15 | +18.8 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | RTX 5070 | 32 | 73 | 54 | +19.2 % | down 16x4 e3 / direct 2.5s / up 2x32 e1 |
| 100 | 1080p | RX 590 | 32 | 45 | 44 | +1.1 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | RX 590 | 32 | 172 | 168 | +1.1 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | RX 5500 XT | 32 | 55 | 45 | +11.7 % | down 16x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | RX 5500 XT | 32 | 211 | 170 | +12.6 % | down 16x4 e9 / direct 2s / up 2x32 e1 |
| 100 | 1080p | RX 6600 | 32 | 46 | 45 | +0.7 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | RX 6600 | 32 | 174 | 172 | +0.7 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | RX 7900 XTX | 32 | 10 | 8 | +15.5 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | RX 7900 XTX | 32 | 31 | 24 | +16.3 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 1080p | RX 9070 XT | 32 | 10 | 10 | +1.6 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 4k | RX 9070 XT | 32 | 32 | 31 | +1.7 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | Radeon 680M | 32 | 362 | 217 | +38.7 % | down 8x2 e1 / sep 3s / up 16 e1 |
| 100 | 4k | Radeon 680M | 32 | 772 | 766 | +0.4 % | down 16x4 e9 / direct 2s / up 64 p4 |
| 100 | 1080p | UHD 630 | 32 sep | 709 | 330 | +66.4 % | down 8x2x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | UHD 630 | 32 sep | 1842 | 1173 | +29.4 % | down 16x2 e1 / sep 2.5s / up 32 e1 |
| 100 | 1080p | Iris Xe | 32 | 1003 | 647 | +28.7 % | down 8x4 e1 / sep 2.5s / up 32 e1 |
| 100 | 4k | Iris Xe | 32 | 2511 | 2497 | +0.3 % | down 16x4 e3 / direct 2s / up 64 p8 |
| 100 | 1080p | Arc B580 | 32 | 34 | 30 | +9.1 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 100 | 4k | Arc B580 | 32 | 114 | 97 | +9.5 % | down 16x2 e1 / direct 2.5s / up 32 e1 |
| 150 | 1080p | GTX 860M | 64 sep | 193 | 133 | +25.3 % | down 8x2x2 e1 / sep 3s / up 32 e1 |
| 150 | 4k | GTX 860M | 64 sep | 520 | 479 | +4.3 % | down 16x2x2 e1 / sep 2.5s / up 64 e1 |
| 150 | 1080p | GTX 1080 | 64 | 32 | 32 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | GTX 1080 | 64 | 121 | 121 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | GTX 1660 | 64 sep | 111 | 63 | +44.4 % | down 8x4 e1 / sep 3s / up 32 e1 |
| 150 | 4k | GTX 1660 | 64 sep | 273 | 222 | +11.9 % | down 16x2 e1 / sep 3s / up 32 e1 |
| 150 | 1080p | RTX 2070 | 64 | 58 | 33 | +53.5 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RTX 2070 | 64 | 223 | 122 | +54.4 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RTX 3060 | 64 | 28 | 28 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | RTX 3060 | 64 | 102 | 102 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | RTX 4070 | 64 | 23 | 20 | +8.7 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RTX 4070 | 64 | 87 | 75 | +8.8 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RTX 5070 | 64 | 20 | 15 | +18.2 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RTX 5070 | 64 | 72 | 53 | +18.5 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RX 590 | 64 | 45 | 44 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | RX 590 | 64 | 169 | 169 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | RX 5500 XT | 64 | 54 | 44 | +10.9 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RX 5500 XT | 64 | 205 | 169 | +11.0 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RX 6600 | 64 | 45 | 45 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | RX 6600 | 64 | 172 | 172 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | RX 7900 XTX | 64 | 10 | 8 | +14.9 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | RX 7900 XTX | 64 | 30 | 23 | +16.0 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 1080p | RX 9070 XT | 64 | 10 | 10 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 4k | RX 9070 XT | 64 | 31 | 31 | +0.0 % | down 16x4 e1 / direct 2.5s / up 64 p4 |
| 150 | 1080p | Radeon 680M | 64 | 361 | 220 | +37.7 % | down 8x4 e1 / sep 3s / up 32 e1 |
| 150 | 4k | Radeon 680M | 64 | 770 | 769 | +0.0 % | down 16x2 e3 / sep 2.5s / up 32 e2 |
| 150 | 1080p | UHD 630 | 64 sep | 696 | 336 | +63.1 % | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 150 | 4k | UHD 630 | 64 sep | 1829 | 1177 | +28.7 % | down 16x2x2 e1 / sep 2.5s / up 64 e1 |
| 150 | 1080p | Iris Xe | 64 | 997 | 649 | +28.1 % | down 8x4 e1 / sep 2.5s / up 32 e3 |
| 150 | 4k | Iris Xe | 64 | 2503 | 2500 | +0.1 % | down 16x4 e1 / sep 2.5s / up 64 e1 |
| 150 | 1080p | Arc B580 | 64 | 34 | 29 | +8.9 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 150 | 4k | Arc B580 | 64 | 111 | 95 | +9.3 % | down 16x4 e3 / direct 2.5s / up 64 e1 |
| 200 | 1080p | GTX 860M | 64 sep | 194 | 135 | +25.1 % | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 4k | GTX 860M | 64 sep | 521 | 480 | +4.3 % | down 16x2x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 1080p | GTX 1080 | 64 | 33 | 32 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | GTX 1080 | 64 | 121 | 120 | +0.2 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | GTX 1660 | 64 sep | 111 | 64 | +44.1 % | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 4k | GTX 1660 | 64 sep | 274 | 223 | +11.9 % | down 16x4 e1 / sep 2.5s / up 64 e1 |
| 200 | 1080p | RTX 2070 | 64 | 58 | 33 | +53.5 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RTX 2070 | 64 | 224 | 122 | +54.4 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 1080p | RTX 3060 | 64 | 28 | 28 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RTX 3060 | 64 | 102 | 101 | +0.4 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | RTX 4070 | 64 | 23 | 20 | +8.7 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RTX 4070 | 64 | 87 | 75 | +8.8 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 1080p | RTX 5070 | 64 | 20 | 15 | +18.5 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RTX 5070 | 64 | 72 | 53 | +18.5 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 1080p | RX 590 | 64 | 45 | 44 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RX 590 | 64 | 169 | 168 | +0.2 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | RX 5500 XT | 64 | 54 | 44 | +11.3 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RX 5500 XT | 64 | 205 | 169 | +11.1 % | down 16x8 e3 / direct 2.5s / up 2x64 e1 |
| 200 | 1080p | RX 6600 | 64 | 45 | 45 | +0.2 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 4k | RX 6600 | 64 | 172 | 172 | +0.2 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | RX 7900 XTX | 64 | 10 | 8 | +15.2 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RX 7900 XTX | 64 | 30 | 23 | +16.0 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 1080p | RX 9070 XT | 64 | 10 | 10 | +0.4 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | RX 9070 XT | 64 | 31 | 31 | +0.4 % | down 16x8 e3 / direct 2.5s / up 128 p4 |
| 200 | 1080p | Radeon 680M | 64 | 365 | 221 | +38.4 % | down 8x4 e1 / sep 3s / up 32 e1 |
| 200 | 4k | Radeon 680M | 64 | 774 | 771 | +0.2 % | down 16x2 e1 / sep 3s / up 32 e1 |
| 200 | 1080p | UHD 630 | 64 sep | 700 | 339 | +63.1 % | down 8x4x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 4k | UHD 630 | 64 sep | 1833 | 1180 | +28.7 % | down 16x2x2 e1 / sep 2.5s / up 64 e1 |
| 200 | 1080p | Iris Xe | 64 | 1002 | 650 | +28.4 % | down 8x4x4 e3 / direct 2s / up 128 p8 |
| 200 | 4k | Iris Xe | 64 | 2509 | 2501 | +0.2 % | down 16x4 e1 / sep 2.5s / up 64 e1 |
| 200 | 1080p | Arc B580 | 64 | 34 | 30 | +8.9 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
| 200 | 4k | Arc B580 | 64 | 112 | 95 | +9.3 % | down 16x4 e1 / direct 2.5s / up 64 e1 |
