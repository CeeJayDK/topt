# Movie Night: soft glow cost (estimate)

Cost model estimate, 2.39:1 video on 16:9 (top and bottom bars), MOVIENIGHT_BLUR_SIZE 32,
Soft glow 1, each GPU's class from TOPT_Blur's tables. us for the whole technique (blur passes on
the strips + the bars pass); in brackets the extra over no soft glow. Ring: 8 more bilinear reads
per bar pixel (the upsample's reads skipped from 27 % into the bar on); frost: one noise read and the scattered read (TOPT_BlurResolve as before); 0.4f:
the earlier second blur level (three passes at 4 x coarser resolution, strips widened by its reach).
Both new options also widen the strips by their radius (2.5 sigma).

## 1080p (bars 138 px, sigma 32 px)

| GPU | class | no soft glow | 1 ring | 2 frost | 0.4f second level |
|---|---|---:|---:|---:|---:|
| RX 6600 | 16 | 44 | 59 (+15) | 52 (+8) | 63 (+18) |
| RX 7900 XTX | 12e sep | 11 | 16 (+4) | 12 (+1) | 17 (+6) |
| RX 9070 XT | 16 | 13 | 17 (+5) | 14 (+2) | 20 (+7) |
| Radeon 680M | 16 | 209 | 245 (+36) | 233 (+25) | 287 (+78) |
| RX 5500 XT | 12e sep | 47 | 81 (+34) | 55 (+7) | 68 (+20) |
| RX 590 | 16 | 45 | 61 (+15) | 52 (+7) | 63 (+18) |
| Arc B580 | 16 | 27 | 36 (+9) | 32 (+4) | 40 (+13) |
| Iris Xe | 16 | 607 | 700 (+93) | 700 (+93) | 820 (+213) |
| UHD 630 | 12e sep | 344 | 599 (+254) | 394 (+49) | 490 (+145) |
| GTX 1080 | 16 | 33 | 42 (+9) | 38 (+5) | 47 (+14) |
| GTX 1660 | 12e sep | 60 | 89 (+29) | 69 (+9) | 87 (+26) |
| GTX 860M | 16 sep | 133 | 206 (+73) | 162 (+28) | 191 (+57) |
| RTX 2070 | 12e sep | 31 | 51 (+19) | 37 (+6) | 45 (+13) |
| RTX 3060 | 16 | 31 | 47 (+16) | 38 (+6) | 46 (+15) |
| RTX 4070 | 12e sep | 21 | 30 (+9) | 24 (+3) | 30 (+9) |
| RTX 5070 | 12e sep | 17 | 26 (+9) | 20 (+2) | 25 (+7) |

## 4K (bars 277 px, sigma 64 px)

| GPU | class | no soft glow | 1 ring | 2 frost | 0.4f second level |
|---|---|---:|---:|---:|---:|
| RX 6600 | 32 | 164 | 223 (+59) | 195 (+31) | 227 (+63) |
| RX 7900 XTX | 24e | 24 | 42 (+17) | 28 (+3) | 35 (+11) |
| RX 9070 XT | 32 | 34 | 52 (+18) | 41 (+7) | 50 (+16) |
| Radeon 680M | 32 | 734 | 893 (+159) | 845 (+111) | 993 (+259) |
| RX 5500 XT | 24e sep | 161 | 293 (+133) | 186 (+25) | 222 (+61) |
| RX 590 | 32 | 162 | 224 (+61) | 188 (+25) | 220 (+58) |
| Arc B580 | 32 | 90 | 124 (+34) | 107 (+17) | 127 (+37) |
| Iris Xe | 32 | 2367 | 2739 (+372) | 2739 (+372) | 3174 (+807) |
| UHD 630 | 24e sep | 1210 | 2225 (+1015) | 1397 (+188) | 1663 (+453) |
| GTX 1080 | 32 | 117 | 150 (+34) | 135 (+18) | 159 (+42) |
| GTX 1660 | 24e sep | 208 | 322 (+114) | 242 (+35) | 288 (+81) |
| GTX 860M | 24e sep | 448 | 758 (+311) | 518 (+70) | 613 (+166) |
| RTX 2070 | 24e | 107 | 183 (+76) | 129 (+22) | 149 (+42) |
| RTX 3060 | 32 | 107 | 171 (+64) | 132 (+25) | 153 (+46) |
| RTX 4070 | 24e | 71 | 106 (+35) | 82 (+11) | 98 (+27) |
| RTX 5070 | 24e | 57 | 92 (+34) | 66 (+9) | 79 (+22) |

