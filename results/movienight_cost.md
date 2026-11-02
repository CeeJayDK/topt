# Movie Night: soft glow cost (estimate)

Cost model estimate, 2.39:1 video on 16:9 (top and bottom bars), MOVIENIGHT_BLUR_SIZE 32,
Soft glow 1, each GPU's class from TOPT_Blur's tables. us for the whole technique (blur passes on
the strips + the bars pass); in brackets the extra over no soft glow. Ring: 8 more bilinear reads
per bar pixel (the upsample's reads skipped from 27 % into the bar on); frost: one noise read and the scattered read (TOPT_BlurResolve as before); 0.4f:
the earlier second blur level (three passes at 4 x coarser resolution, strips widened by its reach).
Both new options also widen the strips by their radius (ring 2.5, frost 3.5 sigma).

## 1080p (bars 138 px, sigma 32 px)

| GPU | class | no soft glow | 1 ring | 2 frost | 0.4f second level |
|---|---|---:|---:|---:|---:|
| RX 6600 | 16 | 44 | 59 (+15) | 55 (+10) | 63 (+18) |
| RX 7900 XTX | 12e sep | 11 | 16 (+4) | 13 (+1) | 17 (+6) |
| RX 9070 XT | 16 | 13 | 17 (+5) | 15 (+2) | 20 (+7) |
| Radeon 680M | 16 | 209 | 245 (+36) | 244 (+36) | 287 (+78) |
| RX 5500 XT | 12e sep | 47 | 81 (+34) | 58 (+10) | 68 (+20) |
| RX 590 | 16 | 45 | 61 (+15) | 54 (+9) | 63 (+18) |
| Arc B580 | 16 | 27 | 36 (+9) | 33 (+6) | 40 (+13) |
| Iris Xe | 16 | 607 | 700 (+93) | 738 (+131) | 820 (+213) |
| UHD 630 | 12e sep | 344 | 599 (+254) | 413 (+69) | 490 (+145) |
| GTX 1080 | 16 | 33 | 42 (+9) | 40 (+7) | 47 (+14) |
| GTX 1660 | 12e sep | 60 | 89 (+29) | 73 (+12) | 87 (+26) |
| GTX 860M | 16 sep | 133 | 206 (+73) | 169 (+35) | 191 (+57) |
| RTX 2070 | 12e sep | 31 | 51 (+19) | 38 (+7) | 45 (+13) |
| RTX 3060 | 16 | 31 | 47 (+16) | 39 (+8) | 46 (+15) |
| RTX 4070 | 12e sep | 21 | 30 (+9) | 25 (+4) | 30 (+9) |
| RTX 5070 | 12e sep | 17 | 26 (+9) | 21 (+3) | 25 (+7) |

## 4K (bars 277 px, sigma 64 px)

| GPU | class | no soft glow | 1 ring | 2 frost | 0.4f second level |
|---|---|---:|---:|---:|---:|
| RX 6600 | 32 | 164 | 223 (+59) | 205 (+41) | 227 (+63) |
| RX 7900 XTX | 24e | 24 | 42 (+17) | 29 (+5) | 35 (+11) |
| RX 9070 XT | 32 | 34 | 52 (+18) | 43 (+9) | 50 (+16) |
| Radeon 680M | 32 | 734 | 893 (+159) | 890 (+156) | 993 (+259) |
| RX 5500 XT | 24e sep | 161 | 293 (+133) | 196 (+36) | 222 (+61) |
| RX 590 | 32 | 162 | 224 (+61) | 198 (+35) | 220 (+58) |
| Arc B580 | 32 | 90 | 124 (+34) | 113 (+23) | 127 (+37) |
| Iris Xe | 32 | 2367 | 2739 (+372) | 2888 (+521) | 3174 (+807) |
| UHD 630 | 24e sep | 1210 | 2225 (+1015) | 1472 (+263) | 1663 (+453) |
| GTX 1080 | 32 | 117 | 150 (+34) | 142 (+25) | 159 (+42) |
| GTX 1660 | 24e sep | 208 | 322 (+114) | 255 (+47) | 288 (+81) |
| GTX 860M | 24e sep | 448 | 758 (+311) | 546 (+98) | 613 (+166) |
| RTX 2070 | 24e | 107 | 183 (+76) | 134 (+28) | 149 (+42) |
| RTX 3060 | 32 | 107 | 171 (+64) | 138 (+31) | 153 (+46) |
| RTX 4070 | 24e | 71 | 106 (+35) | 87 (+16) | 98 (+27) |
| RTX 5070 | 24e | 57 | 92 (+34) | 70 (+13) | 79 (+22) |

