# Hybrid search per GPU profile

Cheapest design per GPU that meets the profile; us = marginal cost over that GPU's plain
composite pass. GPUs with the same winner are listed together.

## medium, 1080p

| sigma | design | GPUs (us) |
|---:|---|---|
| 2 | down 2 e3 / direct 2s / up 2 p4 | GTX 860M 280, GTX 1080 61, GTX 1660 125, RTX 3060 60, RTX 4070 42, RTX 5070 33, RX 590 87, RX 5500 XT 104, RX 7900 XTX 15, RX 9070 XT 18, Arc B580 57 |
|  | down 2 e3 / sep 2s / up 2 e1 | RTX 2070 65, UHD 630 720 |
|  | down 2 e3 / direct 2s / up 2 e3 | Radeon 680M 381, Iris Xe 1242 |
|  | down 2 e9 / direct 2s / up 2 p4 | RX 6600 86 |
| 3 | down 2 e1 / sep 2s / up 2 e2 | GTX 860M 294, GTX 1660 137, RTX 3060 64, RTX 4070 47, RX 590 105, RX 5500 XT 105, RX 9070 XT 20, Arc B580 62 |
|  | down 2 e1 / direct 2s / up 2 e2 | GTX 1080 72, RX 6600 102, Radeon 680M 414, Iris Xe 1270 |
|  | down 2 e5 / sep 2s / up 2 e1 | RTX 2070 71, RTX 5070 34, UHD 630 720 |
|  | down 2 e1 / sep 2.5s / up 2 e1 | RX 7900 XTX 16 |
| 4 | down 4 e9 / direct 2s / up 2x2 e2 | GTX 860M 216, GTX 1080 54, GTX 1660 103, RTX 3060 48, RTX 4070 36, RTX 5070 28, RX 590 75, RX 5500 XT 81, RX 6600 78, RX 7900 XTX 13, RX 9070 XT 16, Radeon 680M 338, UHD 630 671, Iris Xe 1135, Arc B580 48 |
|  | down 2 e1 / sep 2.5s / up 2 e1 | RTX 2070 78 |
| 6 | down 4 e9 / sep 2.5s / up 4 p5 | GTX 860M 200, GTX 1660 91, RTX 3060 43, RTX 4070 30, RX 5500 XT 84, RX 7900 XTX 14, Radeon 680M 236, Iris Xe 719, Arc B580 47 |
|  | down 4 e5 / direct 2s / up 4 p5 | GTX 1080 41, RX 590 59, RX 6600 56, RX 9070 XT 15 |
|  | down 4 e5 / sep 2s / up 2x2 e1 | RTX 2070 50, RTX 5070 25, UHD 630 528 |
| 8 | down 4 e3 / sep 2.5s / up 4 e1 | GTX 1660 71, RTX 2070 39, RTX 4070 25, RTX 5070 19, RX 5500 XT 60, RX 7900 XTX 10, RX 9070 XT 13, UHD 630 417, Arc B580 37 |
|  | down 8 e9 / sep 3s / up 2x4 p5 | GTX 1080 40, RX 590 54, RX 6600 53, Radeon 680M 230, Iris Xe 690 |
|  | down 4x2 e3 / direct 2s / up 2x4 e2 | GTX 860M 155, RTX 3060 37 |
| 12 | down 8 e3 / direct 2s / up 8 p4 | GTX 1080 34, RTX 3060 30, RX 590 47, RX 6600 47, RX 7900 XTX 9, RX 9070 XT 10, Radeon 680M 206, Arc B580 33 |
|  | down 8 e3 / sep 2.5s / up 2x4 e1 | GTX 1660 65, RTX 2070 36, RX 5500 XT 56, UHD 630 347 |
|  | down 8 e3 / direct 2s / up 2x4 e1 | RTX 4070 23, RTX 5070 17 |
|  | down 8 e5 / sep 3s / up 8 p4 | GTX 860M 137 |
|  | down 8 e5 / sep 2s / up 8 p9 | Iris Xe 649 |
| 16 | down 8 e3 / sep 2.5s / up 8 e1 | GTX 860M 130, GTX 1660 60, RTX 2070 34, RTX 4070 21, RTX 5070 16, RX 5500 XT 48, RX 7900 XTX 9, UHD 630 325, Arc B580 31 |
|  | down 8 e1 / sep 2.5s / up 8 p4 | RTX 3060 30, RX 9070 XT 11, Radeon 680M 210, Iris Xe 651 |
|  | down 16 e9 / sep 2s / up 2x8 p5 | GTX 1080 35, RX 590 47, RX 6600 48 |
| 24 | down 16 e3 / direct 2s / up 2x8 e1 | RTX 2070 33, RTX 4070 21, RTX 5070 15, RX 5500 XT 47, RX 7900 XTX 8, Arc B580 30 |
|  | down 16 e3 / direct 2s / up 16 p4 | GTX 1080 32, RTX 3060 27, RX 590 44, RX 6600 45, RX 9070 XT 9 |
|  | down 8x2 e3 / sep 2s / up 2x8 e1 | GTX 860M 129, UHD 630 323 |
|  | down 8x2 e3 / direct 2s / up 16 p4 | Radeon 680M 209, Iris Xe 643 |
|  | down 8 e1 / sep 2.5s / up 8 e1 | GTX 1660 61 |
| 32 | down 16 e3 / direct 2.5s / up 16 p4 | GTX 1080 32, RTX 3060 28, RX 590 45, RX 6600 45, RX 9070 XT 9 |
|  | down 16 e3 / direct 2.5s / up 2x8 e1 | RTX 2070 34, RTX 4070 21, RTX 5070 16, Arc B580 31 |
|  | down 8x2 e3 / sep 2.5s / up 2x8 e1 | GTX 860M 130, UHD 630 327 |
|  | down 8x2 e9 / direct 2s / up 16 e1 | GTX 1660 62, RX 7900 XTX 9 |
|  | down 16 e3 / sep 2.5s / up 2x8 e1 | RX 5500 XT 48 |
|  | down 8x2 e3 / direct 2.5s / up 16 p4 | Radeon 680M 211 |
|  | down 8x2 e3 / sep 2.5s / up 16 p4 | Iris Xe 645 |
| 48 | down 16x2 e3 / direct 2s / up 32 p4 | GTX 1080 33, RTX 3060 28, RX 590 45, RX 6600 45 |
|  | down 16 e1 / sep 2.5s / up 16 e1 | RTX 2070 33, RTX 4070 21, RTX 5070 15, RX 5500 XT 45 |
|  | down 8x2 e1 / sep 2.5s / up 16 e1 | GTX 860M 128, GTX 1660 61, UHD 630 323 |
|  | down 16 e1 / direct 2.5s / up 16 e1 | RX 7900 XTX 8, RX 9070 XT 10, Arc B580 29 |
|  | down 8x4 e3 / direct 2s / up 32 p4 | Radeon 680M 212, Iris Xe 644 |
| 64 | down 16x2 e9 / direct 2s / up 32 p4 | GTX 1080 33, RX 590 45, RX 6600 45 |
|  | down 16 e1 / sep 3s / up 16 e1 | RTX 4070 21, RTX 5070 15, RX 5500 XT 46 |
|  | down 8x2x2 e3 / sep 2.5s / up 32 e1 | GTX 860M 129, UHD 630 324 |
|  | down 8x4 e5 / direct 2.5s / up 32 e1 | RTX 2070 33, Arc B580 30 |
|  | down 16x2 e3 / direct 2.5s / up 32 p4 | RTX 3060 28, RX 9070 XT 10 |
|  | down 8x2 e1 / sep 3s / up 16 e1 | GTX 1660 61 |
|  | down 16 e1 / direct 2.5s / up 16 e1 | RX 7900 XTX 8 |
|  | down 8x4 e3 / direct 2.5s / up 32 p4 | Radeon 680M 215 |
|  | down 8x4 e5 / direct 2s / up 32 e3 | Iris Xe 646 |
| 100 | down 16x4 e9 / direct 2s / up 64 p4 | GTX 1080 32, RTX 3060 28, RX 590 44, RX 6600 45, RX 9070 XT 10 |
|  | down 16x2 e1 / direct 2.5s / up 32 e1 | RTX 2070 33, RTX 4070 21, RTX 5070 15, RX 7900 XTX 8, Arc B580 30 |
|  | down 8x2x2 e1 / sep 2.5s / up 32 e1 | GTX 860M 131, UHD 630 330 |
|  | down 8x4 e1 / sep 2.5s / up 32 e1 | GTX 1660 62, Iris Xe 647 |
|  | down 16x2 e1 / sep 2.5s / up 32 e1 | RX 5500 XT 45 |
|  | down 8x2 e1 / sep 3s / up 16 e1 | Radeon 680M 217 |
| 150 | down 16x4 e3 / direct 2.5s / up 64 e1 | RTX 2070 33, RTX 4070 20, RTX 5070 15, RX 5500 XT 44, RX 7900 XTX 8, Arc B580 29 |
|  | down 16x4 e1 / direct 2.5s / up 64 p4 | GTX 1080 32, RTX 3060 28, RX 590 44, RX 6600 45, RX 9070 XT 10 |
|  | down 8x4 e1 / sep 3s / up 32 e1 | GTX 1660 63, Radeon 680M 220 |
|  | down 8x2x2 e1 / sep 3s / up 32 e1 | GTX 860M 133 |
|  | down 8x4x2 e1 / sep 2.5s / up 64 e1 | UHD 630 336 |
|  | down 8x4 e1 / sep 2.5s / up 32 e3 | Iris Xe 649 |

## medium, 4k

| sigma | design | GPUs (us) |
|---:|---|---|
| 2 | down 2 e3 / direct 2s / up 2 p4 | GTX 860M 1115, GTX 1080 236, GTX 1660 492, RTX 3060 233, RTX 4070 163, RX 590 343, RX 5500 XT 410, RX 9070 XT 68, Arc B580 214 |
|  | down 2 e3 / sep 2s / up 2 e1 | RTX 2070 252, RTX 5070 128, RX 7900 XTX 53, UHD 630 2846 |
|  | down 2 e3 / direct 2s / up 2 e3 | Radeon 680M 1488, Iris Xe 4949 |
|  | down 2 e9 / direct 2s / up 2 p4 | RX 6600 340 |
| 3 | down 2 e1 / sep 2s / up 2 e2 | GTX 860M 1169, GTX 1660 538, RTX 3060 247, RTX 4070 182, RX 590 412, RX 5500 XT 411, RX 9070 XT 72, Arc B580 224 |
|  | down 2 e1 / direct 2s / up 2 e2 | GTX 1080 283, RX 6600 404, Radeon 680M 1622, Iris Xe 5061 |
|  | down 2 e5 / sep 2s / up 2 e1 | RTX 2070 277, RTX 5070 128, UHD 630 2846 |
|  | down 2 e1 / sep 2.5s / up 2 e1 | RX 7900 XTX 53 |
| 4 | down 4 e9 / direct 2s / up 2x2 e2 | GTX 860M 873, GTX 1080 206, GTX 1660 418, RTX 3060 181, RTX 4070 141, RTX 5070 107, RX 590 290, RX 5500 XT 316, RX 6600 312, RX 7900 XTX 42, RX 9070 XT 55, Radeon 680M 1370, UHD 630 2658, Arc B580 171 |
|  | down 2 e1 / sep 2.5s / up 2 e1 | RTX 2070 302 |
|  | down 4 e5 / direct 2s / up 2x2 e2 | Iris Xe 4791 |
| 6 | down 4 e9 / sep 2.5s / up 4 p5 | GTX 860M 824, GTX 1660 384, RTX 3060 163, RTX 4070 124, RX 590 228, RX 5500 XT 326, RX 9070 XT 49, Arc B580 169 |
|  | down 4 e5 / direct 2s / up 4 p5 | GTX 1080 159, RX 6600 228, Radeon 680M 968, Iris Xe 3123 |
|  | down 4 e5 / sep 2s / up 2x2 e1 | RTX 2070 205, RTX 5070 98, RX 7900 XTX 44, UHD 630 2141 |
| 8 | down 4 e3 / sep 2.5s / up 4 e1 | GTX 1660 304, RTX 2070 167, RTX 4070 103, RTX 5070 74, RX 5500 XT 232, RX 7900 XTX 31, RX 9070 XT 41, UHD 630 1652, Arc B580 129 |
|  | down 8 e9 / sep 3s / up 2x4 p5 | GTX 1080 146, RX 590 204, RX 6600 209, Radeon 680M 908, Iris Xe 2995 |
|  | down 4x2 e3 / direct 2s / up 2x4 e2 | GTX 860M 635, RTX 3060 134 |
| 12 | down 8 e3 / sep 2.5s / up 2x4 e1 | GTX 1660 260, RTX 2070 139, RTX 4070 88, RTX 5070 63, RX 5500 XT 210, RX 7900 XTX 29, UHD 630 1396, Arc B580 114 |
|  | down 8 e3 / direct 2s / up 8 p4 | GTX 1080 129, RX 590 181, RX 6600 182, RX 9070 XT 33 |
|  | down 8 e5 / sep 3s / up 8 p4 | GTX 860M 542, RTX 3060 110 |
|  | down 8 e5 / sep 2.5s / up 8 p5 | Radeon 680M 790 |
|  | down 8 e5 / sep 2s / up 8 p9 | Iris Xe 2568 |
| 16 | down 8 e3 / sep 2.5s / up 8 e1 | GTX 860M 510, GTX 1660 231, RTX 2070 128, RTX 4070 79, RTX 5070 57, RX 5500 XT 183, RX 7900 XTX 25, UHD 630 1268, Arc B580 102 |
|  | down 16 e9 / sep 2s / up 2x8 p5 | GTX 1080 127, RX 590 177, RX 6600 178, Radeon 680M 784, Iris Xe 2543 |
|  | down 8x2 e3 / direct 2s / up 2x8 e2 | RTX 3060 110 |
|  | down 8 e1 / sep 2.5s / up 8 p4 | RX 9070 XT 33 |
| 24 | down 16 e3 / direct 2s / up 16 p4 | GTX 1080 121, RTX 3060 103, RX 590 170, RX 6600 172, RX 9070 XT 31, Radeon 680M 760 |
|  | down 16 e3 / sep 2.5s / up 2x8 e1 | GTX 860M 490, GTX 1660 225, RTX 2070 125, RX 5500 XT 178, UHD 630 1198 |
|  | down 16 e3 / direct 2s / up 2x8 e1 | RTX 4070 77, RTX 5070 55, RX 7900 XTX 24, Arc B580 99 |
|  | down 16 e5 / sep 2.5s / up 16 p4 | Iris Xe 2503 |
| 32 | down 16 e3 / sep 2.5s / up 2x8 e1 | GTX 860M 491, GTX 1660 226, RTX 2070 125, RTX 4070 77, RTX 5070 55, RX 5500 XT 178, UHD 630 1202, Arc B580 101 |
|  | down 16 e3 / sep 2.5s / up 16 p4 | GTX 1080 122, RTX 3060 103, RX 590 171, RX 6600 173, RX 9070 XT 31, Radeon 680M 764, Iris Xe 2504 |
|  | down 8x2 e9 / direct 2s / up 16 e1 | RX 7900 XTX 25 |
| 48 | down 16x2 e3 / direct 2s / up 32 p4 | GTX 1080 121, RTX 3060 102, RX 590 169, RX 6600 172, RX 9070 XT 31, Radeon 680M 763, Iris Xe 2497 |
|  | down 16 e1 / sep 2.5s / up 16 e1 | GTX 1660 222, RTX 4070 75, RTX 5070 54, RX 7900 XTX 24, Arc B580 97 |
|  | down 16x2 e3 / sep 2s / up 2x16 e1 | GTX 860M 479, UHD 630 1173 |
|  | down 16x2 e3 / direct 2s / up 2x16 e1 | RTX 2070 124, RX 5500 XT 172 |
| 64 | down 16x2 e3 / sep 2.5s / up 2x16 e1 | GTX 860M 480, GTX 1660 223, RX 5500 XT 173, UHD 630 1177 |
|  | down 8x4 e5 / direct 2.5s / up 32 e1 | RTX 5070 54, RX 7900 XTX 24, Arc B580 98 |
|  | down 16x2 e9 / direct 2s / up 32 p4 | GTX 1080 121, RX 6600 173 |
|  | down 16x4 e5 / direct 2s / up 2x32 p4 | RTX 3060 103, RX 590 170 |
|  | down 16x2 e3 / direct 2.5s / up 32 p4 | RX 9070 XT 31, Radeon 680M 765 |
|  | down 16x2 e3 / direct 2.5s / up 2x16 e1 | RTX 2070 124 |
|  | down 16 e1 / sep 3s / up 16 e1 | RTX 4070 76 |
|  | down 16x2 e3 / sep 2.5s / up 32 p4 | Iris Xe 2499 |
| 100 | down 16x4 e9 / direct 2s / up 64 p4 | GTX 1080 120, RTX 3060 101, RX 590 168, RX 6600 172, RX 9070 XT 31, Radeon 680M 766 |
|  | down 16x2 e1 / sep 2.5s / up 32 e1 | GTX 860M 478, GTX 1660 221, UHD 630 1173 |
|  | down 16x4 e3 / direct 2.5s / up 2x32 e1 | RTX 2070 123, RTX 5070 54 |
|  | down 16x4 e9 / direct 2s / up 2x32 e1 | RTX 4070 75, RX 5500 XT 170 |
|  | down 16x2 e1 / direct 2.5s / up 32 e1 | RX 7900 XTX 24, Arc B580 97 |
|  | down 16x4 e3 / direct 2s / up 64 p8 | Iris Xe 2497 |
| 150 | down 16x4 e3 / direct 2.5s / up 64 e1 | RTX 2070 122, RTX 4070 75, RTX 5070 53, RX 5500 XT 169, RX 7900 XTX 23, Arc B580 95 |
|  | down 16x4 e1 / direct 2.5s / up 64 p4 | GTX 1080 121, RTX 3060 102, RX 590 169, RX 6600 172, RX 9070 XT 31 |
|  | down 16x2x2 e1 / sep 2.5s / up 64 e1 | GTX 860M 479, UHD 630 1177 |
|  | down 16x2 e1 / sep 3s / up 32 e1 | GTX 1660 222 |
|  | down 16x2 e3 / sep 2.5s / up 32 e2 | Radeon 680M 769 |
|  | down 16x4 e1 / sep 2.5s / up 64 e1 | Iris Xe 2500 |

## strict, 1080p

| sigma | design | GPUs (us) |
|---:|---|---|
| 2 | none found | |
| 3 | none found | |
| 4 | none found | |
| 6 | down 2 e3 / sep 3s / up 2 p5 | GTX 860M 408, GTX 1080 77, GTX 1660 179, RTX 2070 128, RTX 3060 84, RTX 4070 59, RTX 5070 50, RX 590 112, RX 5500 XT 163, RX 7900 XTX 24, RX 9070 XT 26, UHD 630 1310, Iris Xe 1554, Arc B580 86 |
|  | down 2 e9 / sep 2.5s / up 2 p5 | RX 6600 114, Radeon 680M 479 |
| 8 | down 4 e9 / sep 3s / up 2x2 e1 | GTX 860M 225, GTX 1080 59, GTX 1660 102, RTX 2070 53, RTX 3060 51, RTX 4070 35, RTX 5070 26, RX 590 81, RX 6600 78, RX 7900 XTX 15, Radeon 680M 338, UHD 630 594, Arc B580 51 |
|  | down 4 e9 / sep 2.5s / up 2x2 e2 | RX 5500 XT 89, RX 9070 XT 18, Iris Xe 1148 |
| 12 | down 4 e9 / sep 3s / up 4 e1 | GTX 1080 43, GTX 1660 77, RTX 2070 43, RTX 4070 27, RTX 5070 21, RX 5500 XT 69, RX 7900 XTX 11, RX 9070 XT 14, Radeon 680M 245, UHD 630 501, Arc B580 41 |
|  | down 4x2 e9 / direct 2s / up 2x4 e2 | RTX 3060 40, RX 590 60, RX 6600 57 |
|  | down 4x2 e9 / sep 2s / up 2x4 e2 | GTX 860M 169, Iris Xe 731 |
| 16 | down 4x2 e5 / sep 3s / up 2x4 e1 | GTX 860M 155, GTX 1080 44, GTX 1660 71, RTX 2070 40, RTX 3060 38, RTX 4070 26, RTX 5070 19, RX 590 60, RX 5500 XT 63, RX 6600 57, Radeon 680M 247, UHD 630 393, Iris Xe 723, Arc B580 41 |
|  | down 4x2 e5 / direct 2.5s / up 2x4 e1 | RX 7900 XTX 12 |
|  | down 4x2 e5 / sep 2.5s / up 2x4 e2 | RX 9070 XT 15 |
| 24 | down 4x2 e5 / sep 3s / up 8 e1 | GTX 860M 147, GTX 1660 67, RTX 2070 38, RTX 4070 24, RTX 5070 18, RX 5500 XT 56, RX 7900 XTX 11, UHD 630 379, Arc B580 37 |
|  | down 4x4 e9 / direct 2s / up 2x8 e2 | GTX 1080 38, RTX 3060 33, RX 590 52, RX 6600 52, RX 9070 XT 12, Iris Xe 689 |
|  | down 4x2 e5 / sep 2.5s / up 8 e2 | Radeon 680M 230 |
| 32 | down 8 e9 / sep 3s / up 8 e1 | GTX 1080 36, GTX 1660 63, RTX 2070 36, RTX 3060 32, RTX 4070 22, RTX 5070 17, RX 590 49, RX 6600 49, RX 7900 XTX 9, RX 9070 XT 11, Radeon 680M 214, Iris Xe 657, Arc B580 33 |
|  | down 8x2 e9 / sep 2.5s / up 2x8 e1 | GTX 860M 134, RX 5500 XT 51, UHD 630 346 |
| 48 | down 8x2 e9 / sep 2.5s / up 16 e1 | GTX 860M 132, GTX 1660 62, RTX 2070 35, RTX 4070 22, RTX 5070 16, RX 5500 XT 49, Radeon 680M 216, UHD 630 342, Iris Xe 649 |
|  | down 8x4 e9 / direct 2s / up 2x16 e2 | GTX 1080 35, RTX 3060 30, RX 590 47, RX 6600 47 |
|  | down 8x2 e9 / direct 2.5s / up 16 e1 | RX 7900 XTX 9, RX 9070 XT 11, Arc B580 33 |
| 64 | down 8x4 e9 / direct 2.5s / up 2x16 e1 | GTX 1080 35, RTX 2070 35, RTX 3060 30, RTX 4070 22, RTX 5070 16, RX 590 47, RX 5500 XT 47, RX 6600 47, RX 7900 XTX 9, RX 9070 XT 11, Arc B580 33 |
|  | down 8x2 e5 / sep 3s / up 16 e1 | GTX 860M 130, GTX 1660 61, Radeon 680M 216, UHD 630 335, Iris Xe 648 |
| 100 | down 16x2 e9 / direct 2.5s / up 32 e1 | GTX 1080 33, RTX 2070 34, RTX 3060 29, RTX 4070 21, RTX 5070 15, RX 590 45, RX 6600 46, RX 7900 XTX 8, RX 9070 XT 10, Arc B580 30 |
|  | down 8x2x2 e3 / sep 3s / up 32 e1 | GTX 860M 132, UHD 630 334 |
|  | down 8x4 e5 / sep 3s / up 32 e1 | GTX 1660 62 |
|  | down 16x2 e9 / sep 3s / up 32 e1 | RX 5500 XT 46 |
|  | down 8x2 e3 / sep 3s / up 16 e1 | Radeon 680M 217 |
|  | down 8x4 e5 / sep 3s / up 32 e3 | Iris Xe 648 |
| 150 | down 16x4 e9 / direct 2.5s / up 64 p4 | GTX 1080 32, RTX 3060 28, RX 590 45, RX 6600 45, RX 9070 XT 10 |
|  | down 16x4 e9 / direct 2.5s / up 2x32 e1 | RTX 2070 34, RTX 4070 21, RTX 5070 16, RX 5500 XT 46 |
|  | down 8x4 e5 / sep 3s / up 32 e1 | GTX 1660 63, Radeon 680M 220, Iris Xe 649 |
|  | down 8x2x2 e3 / sep 3s / up 32 e1 | GTX 860M 133, UHD 630 341 |
|  | down 16x2 e5 / direct 3s / up 32 e1 | RX 7900 XTX 9, Arc B580 31 |

## strict, 4k

| sigma | design | GPUs (us) |
|---:|---|---|
| 2 | none found | |
| 3 | none found | |
| 4 | none found | |
| 6 | down 2 e3 / sep 3s / up 2 p5 | GTX 860M 1622, GTX 1080 297, GTX 1660 708, RTX 2070 505, RTX 3060 327, RTX 4070 228, RTX 5070 192, RX 590 439, RX 5500 XT 643, RX 7900 XTX 85, RX 9070 XT 96, UHD 630 5205, Iris Xe 6187, Arc B580 321 |
|  | down 2 e9 / sep 2.5s / up 2 p5 | RX 6600 448, Radeon 680M 1863 |
| 8 | down 4 e9 / sep 3s / up 2x2 e1 | GTX 860M 904, GTX 1080 222, GTX 1660 425, RTX 2070 218, RTX 3060 193, RTX 4070 143, RTX 5070 102, RX 590 311, RX 6600 318, RX 7900 XTX 46, Radeon 680M 1415, UHD 630 2347, Arc B580 178 |
|  | down 4 e9 / sep 2.5s / up 2x2 e2 | RX 5500 XT 342, RX 9070 XT 60 |
|  | down 4 e9 / direct 2.5s / up 2x2 e1 | Iris Xe 4959 |
| 12 | down 4 e9 / sep 3s / up 4 e1 | GTX 1660 328, RTX 2070 183, RTX 4070 110, RTX 5070 82, RX 5500 XT 268, RX 7900 XTX 36, UHD 630 1985, Arc B580 144 |
|  | down 4x2 e9 / sep 2s / up 2x4 e2 | GTX 860M 673, RTX 3060 145, Radeon 680M 1001, Iris Xe 3307 |
|  | down 4x2 e9 / direct 2s / up 2x4 e2 | GTX 1080 161, RX 590 228, RX 6600 230, RX 9070 XT 45 |
| 16 | down 4x2 e5 / sep 3s / up 2x4 e1 | GTX 860M 634, GTX 1080 161, GTX 1660 290, RTX 2070 154, RTX 3060 138, RTX 4070 99, RTX 5070 71, RX 590 225, RX 5500 XT 235, RX 6600 225, RX 7900 XTX 33, Radeon 680M 990, UHD 630 1576, Arc B580 129 |
|  | down 4x2 e5 / sep 2.5s / up 2x4 e2 | RX 9070 XT 43 |
|  | down 4x2 e9 / sep 2s / up 2x4 e3 | Iris Xe 3310 |
| 24 | down 4x2 e5 / sep 3s / up 8 e1 | GTX 1660 265, RTX 2070 144, RTX 4070 90, RTX 5070 66, RX 5500 XT 213, RX 7900 XTX 30, UHD 630 1483, Arc B580 119 |
|  | down 4x4 e9 / direct 2s / up 2x8 e2 | GTX 1080 141, RTX 3060 120, RX 590 197, RX 6600 199, RX 9070 XT 37, Radeon 680M 877 |
|  | down 4x4 e9 / sep 2s / up 2x8 e2 | GTX 860M 584, Iris Xe 2854 |
| 32 | down 8x2 e9 / sep 2.5s / up 2x8 e1 | GTX 860M 514, GTX 1080 132, GTX 1660 234, RTX 2070 130, RTX 3060 113, RTX 4070 80, RTX 5070 58, RX 590 184, RX 5500 XT 188, RX 6600 184, Radeon 680M 803, UHD 630 1273, Iris Xe 2582, Arc B580 107 |
|  | down 8 e9 / sep 3s / up 8 e1 | RX 7900 XTX 27, RX 9070 XT 36 |
| 48 | down 8x2 e9 / sep 2.5s / up 16 e1 | GTX 860M 507, GTX 1660 230, RTX 2070 129, RTX 4070 79, RTX 5070 57, RX 5500 XT 182, RX 7900 XTX 26, UHD 630 1260, Arc B580 103 |
|  | down 8x4 e9 / direct 2s / up 2x16 e2 | GTX 1080 126, RTX 3060 106, RX 590 175, RX 6600 177, RX 9070 XT 33, Radeon 680M 784, Iris Xe 2543 |
| 64 | down 8x4 e9 / direct 2.5s / up 2x16 e1 | GTX 1080 126, RTX 2070 126, RTX 3060 107, RTX 4070 77, RTX 5070 56, RX 590 176, RX 6600 178, RX 7900 XTX 25, RX 9070 XT 33, Arc B580 101 |
|  | down 8x4 e9 / sep 3s / up 2x16 e1 | GTX 1660 228, RX 5500 XT 176, Iris Xe 2544 |
|  | down 8x2x2 e5 / sep 2.5s / up 2x16 e1 | GTX 860M 493, UHD 630 1218 |
|  | down 8x2 e5 / sep 3s / up 16 e1 | Radeon 680M 786 |
| 100 | down 16x2 e9 / sep 3s / up 32 e1 | GTX 860M 483, GTX 1080 122, GTX 1660 223, RTX 2070 124, RTX 3060 104, RTX 4070 76, RTX 5070 54, RX 590 170, RX 5500 XT 171, RX 6600 173, Radeon 680M 770, UHD 630 1195 |
|  | down 16x2 e9 / direct 2.5s / up 32 e1 | RX 7900 XTX 24, RX 9070 XT 32, Arc B580 98 |
|  | down 16x2 e9 / sep 2.5s / up 32 e3 | Iris Xe 2503 |
| 150 | down 16x4 e9 / direct 2.5s / up 2x32 e1 | RTX 2070 123, RTX 4070 75, RTX 5070 54, RX 5500 XT 170, RX 7900 XTX 24, Arc B580 98 |
|  | down 16x2 e5 / sep 3s / up 32 e1 | GTX 860M 481, GTX 1660 222, Radeon 680M 770, UHD 630 1189, Iris Xe 2502 |
|  | down 16x4 e9 / direct 2.5s / up 64 p4 | GTX 1080 121, RTX 3060 102, RX 590 169, RX 6600 172, RX 9070 XT 31 |

