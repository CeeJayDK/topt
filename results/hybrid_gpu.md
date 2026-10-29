# Hybrid search per GPU profile

Cheapest design per GPU that meets the profile; us = marginal cost over that GPU's plain
composite pass. GPUs with the same winner are listed together.

## medium, 1080p

| sigma | design | GPUs (us) |
|---:|---|---|
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

## medium, 4k

| sigma | design | GPUs (us) |
|---:|---|---|
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

## strict, 1080p

| sigma | design | GPUs (us) |
|---:|---|---|
| 8 | down 4 e9 / sep 3s / up 2x2 e1 | GTX 860M 225, GTX 1080 59, GTX 1660 102, RTX 2070 53, RTX 3060 51, RTX 4070 35, RTX 5070 26, RX 590 81, RX 6600 78, RX 7900 XTX 15, Radeon 680M 338, UHD 630 594, Arc B580 51 |
|  | down 4 e9 / sep 2.5s / up 2x2 e2 | RX 5500 XT 89, RX 9070 XT 18, Iris Xe 1148 |
| 12 | down 4 e9 / sep 3s / up 4 e1 | GTX 1080 43, GTX 1660 77, RTX 2070 43, RTX 4070 27, RTX 5070 21, RX 5500 XT 69, RX 7900 XTX 11, RX 9070 XT 14, Radeon 680M 245, UHD 630 501, Arc B580 41 |
|  | down 4x2 e9 / direct 2s / up 2x4 e2 | RTX 3060 40, RX 590 60, RX 6600 57 |
|  | down 4x2 e9 / sep 2s / up 2x4 e2 | GTX 860M 169, Iris Xe 731 |
| 16 | down 4x2 e5 / sep 3s / up 2x4 e1 | GTX 860M 155, GTX 1080 44, GTX 1660 71, RTX 2070 40, RTX 3060 38, RTX 4070 26, RTX 5070 19, RX 590 60, RX 5500 XT 63, RX 6600 57, Radeon 680M 247, UHD 630 393, Iris Xe 723, Arc B580 41 |
|  | down 4x2 e5 / direct 2.5s / up 2x4 e1 | RX 7900 XTX 12 |
|  | down 4x2 e5 / sep 2.5s / up 2x4 e2 | RX 9070 XT 15 |

## strict, 4k

| sigma | design | GPUs (us) |
|---:|---|---|
| 8 | down 4 e9 / sep 3s / up 2x2 e1 | GTX 860M 904, GTX 1080 222, GTX 1660 425, RTX 2070 218, RTX 3060 193, RTX 4070 143, RTX 5070 102, RX 590 311, RX 6600 318, RX 7900 XTX 46, Radeon 680M 1415, UHD 630 2347, Arc B580 178 |
|  | down 4 e9 / sep 2.5s / up 2x2 e2 | RX 5500 XT 342, RX 9070 XT 60 |
|  | down 4 e9 / direct 2.5s / up 2x2 e1 | Iris Xe 4959 |
| 12 | down 4 e9 / sep 3s / up 4 e1 | GTX 1660 328, RTX 2070 183, RTX 4070 110, RTX 5070 82, RX 5500 XT 268, RX 7900 XTX 36, UHD 630 1985, Arc B580 144 |
|  | down 4x2 e9 / sep 2s / up 2x4 e2 | GTX 860M 673, RTX 3060 145, Radeon 680M 1001, Iris Xe 3307 |
|  | down 4x2 e9 / direct 2s / up 2x4 e2 | GTX 1080 161, RX 590 228, RX 6600 230, RX 9070 XT 45 |
| 16 | down 4x2 e5 / sep 3s / up 2x4 e1 | GTX 860M 634, GTX 1080 161, GTX 1660 290, RTX 2070 154, RTX 3060 138, RTX 4070 99, RTX 5070 71, RX 590 225, RX 5500 XT 235, RX 6600 225, RX 7900 XTX 33, Radeon 680M 990, UHD 630 1576, Arc B580 129 |
|  | down 4x2 e5 / sep 2.5s / up 2x4 e2 | RX 9070 XT 43 |
|  | down 4x2 e9 / sep 2s / up 2x4 e3 | Iris Xe 3310 |

