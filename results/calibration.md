# Cost model vs TexBench

Model (topt/cost.py, profile from topt/gpu_profiles.json) against the TexBench report the profile
was made from, 3840 x 2160, ms. err = model / measured - 1.

| GPU | core | report | tests | median abs err | worst |
|---|---|---|---|---|---|
| RX 6600 | yes | amd-radeon-rx-6600.csv | 46 | 2 % | +176 % (1/16 (960 x 540)) |
| RX 7900 XTX | yes | amd-radeon-rx-7900-xtx.csv | 23 | 4 % | +109 % (half bilinear RGBA8) |
| RX 9070 XT | yes | amd-radeon-rx-9070-xt-4.csv | 23 | 3 % | +84 % (half bilinear RGBA8) |
| Radeon 680M | yes | amd-radeon-0x1681.csv | 46 | 4 % | +210 % (R8 write noise) |
| RX 5500 XT | yes | amd-radeon-rx-5500-xt.csv | 23 | 0 % | -7 % (half bilinear RGB10A2) |
| RX 590 | yes | amd-radeon-rx-590.csv | 23 | 4 % | +12 % (RGBA16F add blend) |
| Arc B580 | yes | intel-arc-b580-3.csv | 53 | 2 % | +113 % (1/256 (240 x 135)) |
| Iris Xe | yes | intel-iris-xe-3.csv | 46 | 4 % | +196 % (R8 write noise) |
| UHD 630 | yes | intel-uhd-630-26.csv | 53 | 0 % | -77 % (64 reads into 480 x 270) |
| GTX 1080 | yes | nvidia-gtx-1080.csv | 23 | 2 % | +9 % (RGBA8 write noise) |
| GTX 1660 | yes | nvidia-gtx-1660-22.csv | 53 | 1 % | +75 % (1/1024 (120 x 67)) |
| GTX 860M | yes | nvidia-gtx-860m-4.csv | 46 | 0 % | -7 % (6 reads) |
| RTX 2070 | yes | nvidia-rtx-2070-3.csv | 46 | 6 % | +461 % (1/1024 (120 x 67)) |
| RTX 3060 | yes | nvidia-rtx-3060.csv | 23 | 1 % | +2 % (half bilinear RGBA8) |
| RTX 4070 | yes | nvidia-rtx-4070.csv | 46 | 1 % | +213 % (1/16 (960 x 540)) |
| RTX 5070 | yes | nvidia-rtx-5070-2.csv | 46 | 4 % | +577 % (1/16 (960 x 540)) |
| AMD 0x15E7 |  | amd-radeon-0x15e7.csv | 46 | 3 % | +131 % (1/64 (480 x 270)) |
| HD 6450 |  | amd-radeon-hd-6450.csv | 46 | 0 % | +60 % (copy Sample RGBA8) |
| RX 6650 XT |  | amd-radeon-rx-6650-xt.csv | 46 | 2 % | +147 % (1/16 (960 x 540)) |
| RX 6900 XT |  | amd-radeon-rx-6900-xt.csv | 23 | 2 % | +64 % (half bilinear RGBA8) |
| RX 7900 GRE |  | amd-radeon-rx-7900-gre.csv | 23 | 48 % | +211 % (half bilinear RGBA8) |
| AMD 0x13C0 |  | amd-radeon-granite-ridge.csv | 23 | 0 % | +20 % (copy Sample RGBA32F) |
| AMD 0x1636 |  | amd-radeon-0x1636-3.csv | 53 | 2 % | -44 % (64 reads into 480 x 270) |
| AMD 0x1638 |  | amd-radeon-0x1638.csv | 46 | 9 % | +216 % (R8 write noise) |
| AMD 0x164E |  | amd-radeon-0x164e-2.csv | 46 | 1 % | -50 % (1/256 (240 x 135)) |
| RX Vega 11 |  | amd-radeon-rx-vega-11-picasso.csv | 23 | 6 % | +50 % (RG11B10F add blend) |
| HD 3000 |  | intel-hd-graphics-3000.csv | 53 | 0 % | -77 % (64 reads into 240 x 135) |
| HD 4600 |  | intel-hd-graphics-4600-4.csv | 46 | 6 % | -41 % (1/64 (480 x 270)) |
| HD 520 |  | intel-hd-graphics-520.csv | 23 | 3 % | +9 % (RG16F write noise) |
| HD4600 |  | intel-hd4600-2.csv | 23 | 0 % | +6 % (half bilinear RGBA8) |
| Iris 540 |  | intel-iris-540-5.csv | 46 | 6 % | +104 % (1/16 (960 x 540)) |
| UHD 630 0x3E98 |  | intel-uhd-630-4.csv | 23 | 0 % | -14 % (half bilinear RGB10A2) |
| GT 1030 |  | nvidia-gt-1030.csv | 53 | 3 % | +207 % (1/256, 2 passes) |
| GT 530 |  | nvidia-gt-530-7.csv | 53 | 1 % | -77 % (64 reads into 240 x 135) |
| RTX 2050 |  | nvidia-rtx-2050.csv | 46 | 1 % | -36 % (1/64, 2 passes) |
| RTX 2060 |  | nvidia-rtx-2060-5.csv | 46 | 1 % | +158 % (1/1024 (120 x 67)) |
| RTX 2060 0x1F15 |  | nvidia-rtx-2060-4.csv | 46 | 4 % | +91 % (1/1024 (120 x 67)) |
| RTX 2080 |  | nvidia-rtx-2080.csv | 46 | 1 % | +537 % (1/1024 (120 x 67)) |
| RTX 3050 Laptop GPU |  | nvidia-rtx-3050-laptop-gpu-2.csv | 46 | 1 % | +25 % (1/256, 8 passes) |
| RTX 3070 Ti Laptop GPU |  | nvidia-rtx-3070-ti-laptop-gpu.csv | 46 | 2 % | +262 % (1/1024 (120 x 67)) |
| RTX 3090 |  | nvidia-rtx-3090.csv | 23 | 0 % | +1125 % (copy Sample RGBA8) |
| RTX 4090 |  | nvidia-rtx-4090-2.csv | 23 | 5 % | +433 % (half bilinear RGB10A2) |
| RTX 4090 Laptop GPU |  | nvidia-rtx-4090-laptop-gpu-2.csv | 46 | 3 % | +533 % (half bilinear RGBA8) |
| RTX 5080 |  | nvidia-rtx-5080.csv | 23 | 3 % | +625 % (half bilinear RGBA8) |
| NVS 310 |  | nvidia-nvs-310.csv | 43 | 1 % | +38 % (copy Sample RGB10A2) |
| Quadro M5000M |  | nvidia-quadro-m5000m-4.csv | 46 | 1 % | +20 % (4 reads) |
| T600 |  | nvidia-t600.csv | 23 | 1 % | +17 % (half bilinear RGB10A2) |

## RX 6600 (AMD RDNA 2)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0965 | 0.1644 | +70 % |
| write | RG8 write noise | 0.1048 | 0.1644 | +57 % |
| write | R16F write noise | 0.1029 | 0.1644 | +60 % |
| write | RGBA8 write noise | 0.1646 | 0.1684 | +2 % |
| write | RGB10A2 write noise | 0.1646 | 0.1684 | +2 % |
| write | RG11B10F write noise | 0.1646 | 0.1684 | +2 % |
| write | RG16F write noise | 0.1647 | 0.1684 | +2 % |
| write | R32F write noise | 0.1647 | 0.1684 | +2 % |
| write | RGBA16F write noise | 0.3292 | 0.3359 | +2 % |
| write | RGBA32F write noise | 0.6594 | 0.6708 | +2 % |
| copy | copy Sample RGBA8 | 0.3349 | 0.3359 | +0 % |
| half | half bilinear RGBA8 | 0.1991 | 0.2103 | +6 % |
| copy | copy Sample RGB10A2 | 0.3347 | 0.3359 | +0 % |
| half | half bilinear RGB10A2 | 0.1991 | 0.2103 | +6 % |
| copy | copy Sample RGBA16F | 0.6704 | 0.6708 | +0 % |
| half | half bilinear RGBA16F | 0.4023 | 0.4196 | +4 % |
| copy | copy Sample RGBA32F | 1.3487 | 1.3406 | -1 % |
| half | half bilinear RGBA32F | 0.8058 | 0.8382 | +4 % |
| reads | 1 read | 0.3403 | 0.3359 | -1 % |
| reads | 2 reads | 0.3370 | 0.3359 | -0 % |
| reads | 3 reads | 0.3375 | 0.3359 | -0 % |
| reads | 4 reads | 0.2569 | 0.3359 | +31 % |
| reads | 6 reads | 0.3489 | 0.3359 | -4 % |
| reads | 8 reads | 0.3941 | 0.3836 | -3 % |
| reads | 10 reads | 0.4382 | 0.4383 | +0 % |
| reads | 12 reads | 0.4859 | 0.4931 | +1 % |
| reads | 16 reads | 0.5865 | 0.6027 | +3 % |
| reads | 24 reads | 0.8299 | 0.8218 | -1 % |
| size | 1/4 (1920 x 1080) | 0.1990 | 0.2103 | +6 % |
| size | 1/16 (960 x 540) | 0.0649 | 0.1789 | +176 % |
| size | 1/64 (480 x 270) | 0.0384 | 0.0601 | +57 % |
| size | 1/256 (240 x 135) | 0.0213 | 0.0158 | -26 % |
| size | 1/1024 (120 x 67) | 0.0021 | 0.0047 | +122 % |
| chain | 1/64, 2 passes | 0.0062 | 0.0080 | +28 % |
| chain | 1/64, 8 passes | 0.0282 | 0.0318 | +13 % |
| chain | 1/64, 32 passes | 0.1256 | 0.1274 | +1 % |
| chain | 1/256, 2 passes | 0.0030 | 0.0035 | +16 % |
| chain | 1/256, 8 passes | 0.0125 | 0.0139 | +12 % |
| chain | 1/256, 32 passes | 0.0553 | 0.0558 | +1 % |
| quad | 4 reads + 12 exchanges | 0.3890 | 0.3900 | +0 % |
| quad | 16 reads | 0.5865 | 0.6027 | +3 % |
| blend | RGBA8 add blend | 0.3855 | 0.3865 | +0 % |
| blend | RGB10A2 add blend | 0.3834 | 0.3844 | +0 % |
| blend | RG11B10F add blend | 0.3860 | 0.3870 | +0 % |
| blend | RGBA16F add blend | 0.7618 | 0.7628 | +0 % |
| blend | RGBA32F add blend | 1.4252 | 1.4262 | +0 % |

## RX 7900 XTX (AMD RDNA 3)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0429 | 0.0442 | +3 % |
| write | RG8 write noise | 0.0328 | 0.0341 | +4 % |
| write | R16F write noise | 0.0313 | 0.0326 | +4 % |
| write | RGBA8 write noise | 0.0337 | 0.0350 | +4 % |
| write | RGB10A2 write noise | 0.0334 | 0.0347 | +4 % |
| write | RG11B10F write noise | 0.0327 | 0.0340 | +4 % |
| write | RG16F write noise | 0.0323 | 0.0336 | +4 % |
| write | R32F write noise | 0.0315 | 0.0328 | +4 % |
| write | RGBA16F write noise | 0.0797 | 0.0810 | +2 % |
| write | RGBA32F write noise | 0.1563 | 0.1576 | +1 % |
| copy | copy Sample RGBA8 | 0.0397 | 0.0410 | +3 % |
| half | half bilinear RGBA8 | 0.0125 | 0.0261 | +109 % |
| copy | copy Sample RGB10A2 | 0.0377 | 0.0410 | +9 % |
| half | half bilinear RGB10A2 | 0.0125 | 0.0261 | +109 % |
| copy | copy Sample RGBA16F | 0.1551 | 0.0810 | -48 % |
| half | half bilinear RGBA16F | 0.0256 | 0.0509 | +99 % |
| copy | copy Sample RGBA32F | 0.3125 | 0.1601 | -49 % |
| half | half bilinear RGBA32F | 0.2100 | 0.1005 | -52 % |
| blend | RGBA8 add blend | 0.0364 | 0.0410 | +13 % |
| blend | RGB10A2 add blend | 0.0364 | 0.0410 | +13 % |
| blend | RG11B10F add blend | 0.0369 | 0.0410 | +11 % |
| blend | RGBA16F add blend | 0.1523 | 0.1536 | +1 % |
| blend | RGBA32F add blend | 0.3065 | 0.3078 | +0 % |

## RX 9070 XT (AMD RDNA 4)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0430 | 0.0443 | +3 % |
| write | RG8 write noise | 0.0416 | 0.0429 | +3 % |
| write | R16F write noise | 0.0417 | 0.0430 | +3 % |
| write | RGBA8 write noise | 0.0502 | 0.0515 | +3 % |
| write | RGB10A2 write noise | 0.0502 | 0.0515 | +3 % |
| write | RG11B10F write noise | 0.0501 | 0.0514 | +3 % |
| write | RG16F write noise | 0.0502 | 0.0515 | +3 % |
| write | R32F write noise | 0.0502 | 0.0515 | +3 % |
| write | RGBA16F write noise | 0.1026 | 0.1039 | +1 % |
| write | RGBA32F write noise | 0.2082 | 0.2095 | +1 % |
| copy | copy Sample RGBA8 | 0.0551 | 0.0564 | +2 % |
| half | half bilinear RGBA8 | 0.0194 | 0.0357 | +84 % |
| copy | copy Sample RGB10A2 | 0.0522 | 0.0564 | +8 % |
| half | half bilinear RGB10A2 | 0.0194 | 0.0357 | +84 % |
| copy | copy Sample RGBA16F | 0.1093 | 0.1115 | +2 % |
| half | half bilinear RGBA16F | 0.0385 | 0.0702 | +82 % |
| copy | copy Sample RGBA32F | 0.3464 | 0.2217 | -36 % |
| half | half bilinear RGBA32F | 0.1797 | 0.1390 | -23 % |
| blend | RGBA8 add blend | 0.0904 | 0.0917 | +1 % |
| blend | RGB10A2 add blend | 0.0904 | 0.0917 | +1 % |
| blend | RG11B10F add blend | 0.0890 | 0.0903 | +1 % |
| blend | RGBA16F add blend | 0.1989 | 0.2002 | +1 % |
| blend | RGBA32F add blend | 0.4185 | 0.4198 | +0 % |

## Radeon 680M (AMD RDNA 2 iGPU)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.2865 | 0.8886 | +210 % |
| write | RG8 write noise | 0.3937 | 0.8886 | +126 % |
| write | R16F write noise | 0.3947 | 0.8886 | +125 % |
| write | RGBA8 write noise | 0.7740 | 0.8886 | +15 % |
| write | RGB10A2 write noise | 0.7195 | 0.8886 | +24 % |
| write | RG11B10F write noise | 0.7526 | 0.8886 | +18 % |
| write | RG16F write noise | 0.7317 | 0.8886 | +21 % |
| write | R32F write noise | 0.7318 | 0.8886 | +21 % |
| write | RGBA16F write noise | 1.5533 | 1.5591 | +0 % |
| write | RGBA32F write noise | 3.0143 | 3.0201 | +0 % |
| copy | copy Sample RGBA8 | 1.4766 | 1.4824 | +0 % |
| half | half bilinear RGBA8 | 0.9457 | 0.9286 | -2 % |
| copy | copy Sample RGB10A2 | 1.4975 | 1.4824 | -1 % |
| half | half bilinear RGB10A2 | 0.9053 | 0.9286 | +3 % |
| copy | copy Sample RGBA16F | 2.9290 | 2.9590 | +1 % |
| half | half bilinear RGBA16F | 1.8239 | 1.8515 | +2 % |
| copy | copy Sample RGBA32F | 6.8023 | 5.9122 | -13 % |
| half | half bilinear RGBA32F | 3.6007 | 3.6973 | +3 % |
| reads | 1 read | 1.4599 | 1.4824 | +2 % |
| reads | 2 reads | 1.5489 | 1.4824 | -4 % |
| reads | 3 reads | 1.5507 | 1.4824 | -4 % |
| reads | 4 reads | 1.1464 | 1.4824 | +29 % |
| reads | 6 reads | 1.5976 | 1.4824 | -7 % |
| reads | 8 reads | 1.5189 | 1.4824 | -2 % |
| reads | 10 reads | 1.5684 | 1.5942 | +2 % |
| reads | 12 reads | 1.7208 | 1.7354 | +1 % |
| reads | 16 reads | 1.9171 | 2.0176 | +5 % |
| reads | 24 reads | 2.6284 | 2.5821 | -2 % |
| size | 1/4 (1920 x 1080) | 0.9078 | 0.9286 | +2 % |
| size | 1/16 (960 x 540) | 0.7558 | 0.7902 | +5 % |
| size | 1/64 (480 x 270) | 0.7384 | 0.7556 | +2 % |
| size | 1/256 (240 x 135) | 0.3545 | 0.1932 | -45 % |
| size | 1/1024 (120 x 67) | 0.0891 | 0.0891 | -0 % |
| chain | 1/64, 2 passes | 0.0131 | 0.0229 | +75 % |
| chain | 1/64, 8 passes | 0.0538 | 0.0914 | +70 % |
| chain | 1/64, 32 passes | 0.3560 | 0.3658 | +3 % |
| chain | 1/256, 2 passes | 0.0090 | 0.0143 | +59 % |
| chain | 1/256, 8 passes | 0.0314 | 0.0574 | +83 % |
| chain | 1/256, 32 passes | 0.2242 | 0.2295 | +2 % |
| quad | 4 reads + 12 exchanges | 1.1625 | 1.4824 | +28 % |
| quad | 16 reads | 1.9171 | 2.0176 | +5 % |
| blend | RGBA8 add blend | 1.4454 | 1.4824 | +3 % |
| blend | RGB10A2 add blend | 1.4265 | 1.4824 | +4 % |
| blend | RG11B10F add blend | 1.4962 | 1.5020 | +0 % |
| blend | RGBA16F add blend | 2.8265 | 2.9590 | +5 % |
| blend | RGBA32F add blend | 5.8031 | 5.9122 | +2 % |

## RX 5500 XT (AMD RDNA 1)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.3121 | 0.3134 | +0 % |
| write | RG8 write noise | 0.2987 | 0.3000 | +0 % |
| write | R16F write noise | 0.2961 | 0.2974 | +0 % |
| write | RGBA8 write noise | 0.2970 | 0.2983 | +0 % |
| write | RGB10A2 write noise | 0.3122 | 0.3135 | +0 % |
| write | RG11B10F write noise | 0.3200 | 0.3213 | +0 % |
| write | RG16F write noise | 0.2967 | 0.2980 | +0 % |
| write | R32F write noise | 0.2971 | 0.2984 | +0 % |
| write | RGBA16F write noise | 0.3357 | 0.3370 | +0 % |
| write | RGBA32F write noise | 0.6525 | 0.6545 | +0 % |
| copy | copy Sample RGBA8 | 0.3266 | 0.3279 | +0 % |
| half | half bilinear RGBA8 | 0.2181 | 0.2054 | -6 % |
| copy | copy Sample RGB10A2 | 0.3265 | 0.3279 | +0 % |
| half | half bilinear RGB10A2 | 0.2205 | 0.2054 | -7 % |
| copy | copy Sample RGBA16F | 0.6623 | 0.6545 | -1 % |
| half | half bilinear RGBA16F | 0.4274 | 0.4095 | -4 % |
| copy | copy Sample RGBA32F | 1.3470 | 1.3077 | -3 % |
| half | half bilinear RGBA32F | 0.8108 | 0.8178 | +1 % |
| blend | RGBA8 add blend | 0.3433 | 0.3446 | +0 % |
| blend | RGB10A2 add blend | 0.3456 | 0.3469 | +0 % |
| blend | RG11B10F add blend | 0.3462 | 0.3475 | +0 % |
| blend | RGBA16F add blend | 0.6559 | 0.6572 | +0 % |
| blend | RGBA32F add blend | 1.3039 | 1.3077 | +0 % |

## RX 590 (AMD GCN 4)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.1798 | 0.1811 | +1 % |
| write | RG8 write noise | 0.1786 | 0.1799 | +1 % |
| write | R16F write noise | 0.1810 | 0.1823 | +1 % |
| write | RGBA8 write noise | 0.1799 | 0.1812 | +1 % |
| write | RGB10A2 write noise | 0.1891 | 0.1904 | +1 % |
| write | RG11B10F write noise | 0.2012 | 0.2025 | +1 % |
| write | RG16F write noise | 0.2004 | 0.2017 | +1 % |
| write | R32F write noise | 0.1862 | 0.1875 | +1 % |
| write | RGBA16F write noise | 0.3027 | 0.3287 | +9 % |
| write | RGBA32F write noise | 0.6042 | 0.6561 | +9 % |
| copy | copy Sample RGBA8 | 0.3274 | 0.3287 | +0 % |
| half | half bilinear RGBA8 | 0.1892 | 0.2059 | +9 % |
| copy | copy Sample RGB10A2 | 0.3162 | 0.3287 | +4 % |
| half | half bilinear RGB10A2 | 0.1896 | 0.2059 | +9 % |
| copy | copy Sample RGBA16F | 0.6198 | 0.6561 | +6 % |
| half | half bilinear RGBA16F | 0.3693 | 0.4105 | +11 % |
| copy | copy Sample RGBA32F | 1.2358 | 1.3109 | +6 % |
| half | half bilinear RGBA32F | 0.7662 | 0.8198 | +7 % |
| blend | RGBA8 add blend | 0.3182 | 0.3287 | +3 % |
| blend | RGB10A2 add blend | 0.3177 | 0.3287 | +3 % |
| blend | RG11B10F add blend | 0.3113 | 0.3287 | +6 % |
| blend | RGBA16F add blend | 0.5850 | 0.6561 | +12 % |
| blend | RGBA32F add blend | 1.2601 | 1.3109 | +4 % |

## Arc B580 (Intel Xe2)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0438 | 0.0839 | +91 % |
| write | RG8 write noise | 0.0451 | 0.0839 | +86 % |
| write | R16F write noise | 0.0453 | 0.0839 | +85 % |
| write | RGBA8 write noise | 0.0824 | 0.0880 | +7 % |
| write | RGB10A2 write noise | 0.0816 | 0.0880 | +8 % |
| write | RG11B10F write noise | 0.1735 | 0.1750 | +1 % |
| write | RG16F write noise | 0.0756 | 0.0880 | +16 % |
| write | R32F write noise | 0.0741 | 0.0880 | +19 % |
| write | RGBA16F write noise | 0.1634 | 0.1745 | +7 % |
| write | RGBA32F write noise | 0.3236 | 0.3475 | +7 % |
| copy | copy Sample RGBA8 | 0.1730 | 0.1745 | +1 % |
| half | half bilinear RGBA8 | 0.1066 | 0.1097 | +3 % |
| copy | copy Sample RGB10A2 | 0.1742 | 0.1745 | +0 % |
| half | half bilinear RGB10A2 | 0.1070 | 0.1097 | +2 % |
| copy | copy Sample RGBA16F | 0.3325 | 0.3475 | +5 % |
| half | half bilinear RGBA16F | 0.2072 | 0.2178 | +5 % |
| copy | copy Sample RGBA32F | 0.6792 | 0.6935 | +2 % |
| half | half bilinear RGBA32F | 0.4127 | 0.4340 | +5 % |
| reads | 1 read | 0.1717 | 0.1745 | +2 % |
| reads | 2 reads | 0.1733 | 0.1745 | +1 % |
| reads | 3 reads | 0.1718 | 0.1745 | +2 % |
| reads | 4 reads | 0.1744 | 0.1745 | +0 % |
| reads | 6 reads | 0.1898 | 0.1801 | -5 % |
| reads | 8 reads | 0.2174 | 0.2122 | -2 % |
| reads | 10 reads | 0.2409 | 0.2443 | +1 % |
| reads | 12 reads | 0.2696 | 0.2764 | +3 % |
| reads | 16 reads | 0.3369 | 0.3406 | +1 % |
| reads | 24 reads | 0.4701 | 0.4690 | -0 % |
| size | 1/4 (1920 x 1080) | 0.1062 | 0.1097 | +3 % |
| size | 1/16 (960 x 540) | 0.0843 | 0.0934 | +11 % |
| size | 1/64 (480 x 270) | 0.0772 | 0.0489 | -37 % |
| size | 1/256 (240 x 135) | 0.0063 | 0.0134 | +113 % |
| size | 1/1024 (120 x 67) | 0.0028 | 0.0045 | +60 % |
| chain | 1/64, 2 passes | 0.0059 | 0.0055 | -7 % |
| chain | 1/64, 8 passes | 0.0221 | 0.0219 | -1 % |
| chain | 1/64, 32 passes | 0.0880 | 0.0876 | -0 % |
| chain | 1/256, 2 passes | 0.0037 | 0.0037 | -1 % |
| chain | 1/256, 8 passes | 0.0150 | 0.0147 | -2 % |
| chain | 1/256, 32 passes | 0.0588 | 0.0588 | -0 % |
| quad | 4 reads + 12 exchanges | 0.6064 | 0.6079 | +0 % |
| quad | 16 reads | 0.3369 | 0.3406 | +1 % |
| underfill | 64 reads into 120 x 67 | 0.0232 | 0.0232 | +0 % |
| underfill | 64 reads into 240 x 135 | 0.0276 | 0.0235 | -15 % |
| underfill | 64 reads into 480 x 270 | 0.0628 | 0.0245 | -61 % |
| blend | RGBA8 add blend | 0.1749 | 0.1764 | +1 % |
| blend | RGB10A2 add blend | 0.1846 | 0.1861 | +1 % |
| blend | RG11B10F add blend | 0.1730 | 0.1745 | +1 % |
| blend | RGBA16F add blend | 0.3383 | 0.3475 | +3 % |
| blend | RGBA32F add blend | 0.6857 | 0.6935 | +1 % |
| blend | R8 add blend | 0.1006 | 0.1021 | +2 % |
| blend | R16F add blend | 0.1073 | 0.1088 | +1 % |
| blend | R32F add blend | 0.1668 | 0.1745 | +5 % |
| blend | RG16F add blend | 0.1699 | 0.1745 | +3 % |

## Iris Xe (Intel Gen12)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 1.2151 | 3.5958 | +196 % |
| write | RG8 write noise | 2.3290 | 3.5958 | +54 % |
| write | R16F write noise | 2.4665 | 3.5958 | +46 % |
| write | RGBA8 write noise | 4.7295 | 4.7326 | +0 % |
| write | RGB10A2 write noise | 4.9156 | 4.9187 | +0 % |
| write | RG11B10F write noise | 4.8847 | 4.8878 | +0 % |
| write | RG16F write noise | 4.8886 | 4.8917 | +0 % |
| write | R32F write noise | 5.2473 | 5.2504 | +0 % |
| write | RGBA16F write noise | 10.6334 | 10.6365 | +0 % |
| write | RGBA32F write noise | 21.5145 | 21.5176 | +0 % |
| copy | copy Sample RGBA8 | 4.9424 | 4.9455 | +0 % |
| half | half bilinear RGBA8 | 2.3000 | 3.0921 | +34 % |
| copy | copy Sample RGB10A2 | 4.7729 | 4.9455 | +4 % |
| half | half bilinear RGB10A2 | 2.3422 | 3.0921 | +32 % |
| copy | copy Sample RGBA16F | 10.3323 | 10.6365 | +3 % |
| half | half bilinear RGBA16F | 5.1840 | 6.1811 | +19 % |
| copy | copy Sample RGBA32F | 21.9306 | 21.5176 | -2 % |
| half | half bilinear RGBA32F | 10.9824 | 12.3591 | +13 % |
| reads | 1 read | 4.6953 | 4.9455 | +5 % |
| reads | 2 reads | 4.6407 | 4.9455 | +7 % |
| reads | 3 reads | 4.4976 | 4.9455 | +10 % |
| reads | 4 reads | 3.1296 | 4.9455 | +58 % |
| reads | 6 reads | 4.2849 | 4.9455 | +15 % |
| reads | 8 reads | 4.6435 | 4.9455 | +7 % |
| reads | 10 reads | 4.8232 | 4.9455 | +3 % |
| reads | 12 reads | 4.6777 | 4.9455 | +6 % |
| reads | 16 reads | 5.2910 | 5.3928 | +2 % |
| reads | 24 reads | 6.3897 | 6.2913 | -2 % |
| size | 1/4 (1920 x 1080) | 2.4477 | 3.0921 | +26 % |
| size | 1/16 (960 x 540) | 2.5028 | 2.6288 | +5 % |
| size | 1/64 (480 x 270) | 2.9162 | 2.5130 | -14 % |
| size | 1/256 (240 x 135) | 0.7736 | 0.6306 | -18 % |
| size | 1/1024 (120 x 67) | 0.2479 | 0.2479 | -0 % |
| chain | 1/64, 2 passes | 0.0149 | 0.0153 | +3 % |
| chain | 1/64, 8 passes | 0.0600 | 0.0612 | +2 % |
| chain | 1/64, 32 passes | 0.2445 | 0.2449 | +0 % |
| chain | 1/256, 2 passes | 0.0080 | 0.0085 | +7 % |
| chain | 1/256, 8 passes | 0.0335 | 0.0342 | +2 % |
| chain | 1/256, 32 passes | 0.1362 | 0.1367 | +0 % |
| quad | 4 reads + 12 exchanges | 3.0917 | 4.9455 | +60 % |
| quad | 16 reads | 5.2910 | 5.3928 | +2 % |
| blend | RGBA8 add blend | 4.7086 | 4.9455 | +5 % |
| blend | RGB10A2 add blend | 4.6098 | 4.9455 | +7 % |
| blend | RG11B10F add blend | 4.7046 | 4.9455 | +5 % |
| blend | RGBA16F add blend | 11.5040 | 11.5071 | +0 % |
| blend | RGBA32F add blend | 24.0743 | 24.0774 | +0 % |

## UHD 630 (Intel Gen9.5)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 1.0767 | 1.0812 | +0 % |
| write | RG8 write noise | 1.0800 | 1.0845 | +0 % |
| write | R16F write noise | 1.0806 | 1.0851 | +0 % |
| write | RGBA8 write noise | 1.4429 | 1.4474 | +0 % |
| write | RGB10A2 write noise | 1.4949 | 1.4994 | +0 % |
| write | RG11B10F write noise | 1.6361 | 1.6406 | +0 % |
| write | RG16F write noise | 1.6970 | 1.7015 | +0 % |
| write | R32F write noise | 1.5161 | 1.5206 | +0 % |
| write | RGBA16F write noise | 2.9179 | 2.9224 | +0 % |
| write | RGBA32F write noise | 5.8122 | 5.8167 | +0 % |
| copy | copy Sample RGBA8 | 2.4901 | 2.4946 | +0 % |
| half | half bilinear RGBA8 | 1.3017 | 1.5608 | +20 % |
| copy | copy Sample RGB10A2 | 2.9161 | 2.4946 | -14 % |
| half | half bilinear RGB10A2 | 1.4430 | 1.5608 | +8 % |
| copy | copy Sample RGBA16F | 5.5848 | 4.9847 | -11 % |
| half | half bilinear RGBA16F | 3.1239 | 3.1171 | -0 % |
| copy | copy Sample RGBA32F | 10.4369 | 9.9649 | -5 % |
| half | half bilinear RGBA32F | 4.9268 | 6.2297 | +26 % |
| reads | 1 read | 2.2692 | 2.4946 | +10 % |
| reads | 2 reads | 2.3975 | 2.4946 | +4 % |
| reads | 3 reads | 2.2700 | 2.4946 | +10 % |
| reads | 4 reads | 2.4773 | 2.4946 | +1 % |
| reads | 6 reads | 3.6420 | 3.4231 | -6 % |
| reads | 8 reads | 4.4628 | 4.5012 | +1 % |
| reads | 10 reads | 5.6006 | 5.5793 | -0 % |
| reads | 12 reads | 6.6591 | 6.6573 | -0 % |
| reads | 16 reads | 8.8224 | 8.8135 | -0 % |
| reads | 24 reads | 13.1099 | 13.1258 | +0 % |
| size | 1/4 (1920 x 1080) | 1.3005 | 1.5608 | +20 % |
| size | 1/16 (960 x 540) | 0.8720 | 1.3273 | +52 % |
| size | 1/64 (480 x 270) | 0.7909 | 0.8021 | +1 % |
| size | 1/256 (240 x 135) | 0.2061 | 0.2039 | -1 % |
| size | 1/1024 (120 x 67) | 0.0898 | 0.0930 | +4 % |
| chain | 1/64, 2 passes | 0.0389 | 0.0409 | +5 % |
| chain | 1/64, 8 passes | 0.1572 | 0.1636 | +4 % |
| chain | 1/64, 32 passes | 0.6523 | 0.6543 | +0 % |
| chain | 1/256, 2 passes | 0.0170 | 0.0169 | -0 % |
| chain | 1/256, 8 passes | 0.0675 | 0.0677 | +0 % |
| chain | 1/256, 32 passes | 0.2708 | 0.2707 | -0 % |
| quad | 4 reads + 12 exchanges | 6.4311 | 6.4356 | +0 % |
| quad | 16 reads | 8.8224 | 8.8135 | -0 % |
| underfill | 64 reads into 120 x 67 | 0.5633 | 0.5633 | -0 % |
| underfill | 64 reads into 240 x 135 | 0.9370 | 0.3206 | -66 % |
| underfill | 64 reads into 480 x 270 | 2.4209 | 0.5464 | -77 % |
| blend | RGBA8 add blend | 2.8568 | 2.8613 | +0 % |
| blend | RGB10A2 add blend | 2.9963 | 3.0008 | +0 % |
| blend | RG11B10F add blend | 2.7538 | 2.7583 | +0 % |
| blend | RGBA16F add blend | 6.3469 | 6.3514 | +0 % |
| blend | RGBA32F add blend | 10.9173 | 10.9218 | +0 % |
| blend | R8 add blend | 0.9725 | 0.9770 | +0 % |
| blend | R16F add blend | 1.1666 | 1.2495 | +7 % |
| blend | R32F add blend | 2.5130 | 2.5175 | +0 % |
| blend | RG16F add blend | 2.8206 | 2.8251 | +0 % |

## GTX 1080 (NVIDIA Pascal)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0733 | 0.0746 | +2 % |
| write | RG8 write noise | 0.0746 | 0.0759 | +2 % |
| write | R16F write noise | 0.0770 | 0.0783 | +2 % |
| write | RGBA8 write noise | 0.1078 | 0.1175 | +9 % |
| write | RGB10A2 write noise | 0.1088 | 0.1175 | +8 % |
| write | RG11B10F write noise | 0.1084 | 0.1175 | +8 % |
| write | RG16F write noise | 0.1079 | 0.1175 | +9 % |
| write | R32F write noise | 0.1078 | 0.1175 | +9 % |
| write | RGBA16F write noise | 0.2151 | 0.2337 | +9 % |
| write | RGBA32F write noise | 0.4345 | 0.4661 | +7 % |
| copy | copy Sample RGBA8 | 0.2324 | 0.2337 | +1 % |
| half | half bilinear RGBA8 | 0.1440 | 0.1465 | +2 % |
| copy | copy Sample RGB10A2 | 0.2328 | 0.2337 | +0 % |
| half | half bilinear RGB10A2 | 0.1439 | 0.1465 | +2 % |
| copy | copy Sample RGBA16F | 0.4632 | 0.4661 | +1 % |
| half | half bilinear RGBA16F | 0.2880 | 0.2918 | +1 % |
| copy | copy Sample RGBA32F | 0.9358 | 0.9309 | -1 % |
| half | half bilinear RGBA32F | 0.5752 | 0.5823 | +1 % |
| blend | RGBA8 add blend | 0.2312 | 0.2337 | +1 % |
| blend | RGB10A2 add blend | 0.2320 | 0.2337 | +1 % |
| blend | RG11B10F add blend | 0.2318 | 0.2337 | +1 % |
| blend | RGBA16F add blend | 0.4642 | 0.4661 | +0 % |
| blend | RGBA32F add blend | 1.0877 | 1.0890 | +0 % |

## GTX 1660 (NVIDIA Turing)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.2808 | 0.2819 | +0 % |
| write | RG8 write noise | 0.2811 | 0.2822 | +0 % |
| write | R16F write noise | 0.2810 | 0.2821 | +0 % |
| write | RGBA8 write noise | 0.2935 | 0.2946 | +0 % |
| write | RGB10A2 write noise | 0.2930 | 0.2941 | +0 % |
| write | RG11B10F write noise | 0.2932 | 0.2943 | +0 % |
| write | RG16F write noise | 0.2942 | 0.2953 | +0 % |
| write | R32F write noise | 0.2936 | 0.2947 | +0 % |
| write | RGBA16F write noise | 0.4268 | 0.4279 | +0 % |
| write | RGBA32F write noise | 0.8589 | 0.8600 | +0 % |
| copy | copy Sample RGBA8 | 0.4235 | 0.4246 | +0 % |
| half | half bilinear RGBA8 | 0.2498 | 0.2658 | +6 % |
| copy | copy Sample RGB10A2 | 0.4220 | 0.4246 | +1 % |
| half | half bilinear RGB10A2 | 0.2501 | 0.2658 | +6 % |
| copy | copy Sample RGBA16F | 0.8592 | 0.8481 | -1 % |
| half | half bilinear RGBA16F | 0.5005 | 0.5305 | +6 % |
| copy | copy Sample RGBA32F | 1.6758 | 1.6951 | +1 % |
| half | half bilinear RGBA32F | 1.0023 | 1.0598 | +6 % |
| reads | 1 read | 0.4276 | 0.4246 | -1 % |
| reads | 2 reads | 0.4240 | 0.4246 | +0 % |
| reads | 3 reads | 0.4240 | 0.4246 | +0 % |
| reads | 4 reads | 0.4346 | 0.4356 | +0 % |
| reads | 6 reads | 0.4941 | 0.5343 | +8 % |
| reads | 8 reads | 0.6179 | 0.6330 | +2 % |
| reads | 10 reads | 0.7355 | 0.7317 | -1 % |
| reads | 12 reads | 0.8329 | 0.8304 | -0 % |
| reads | 16 reads | 1.0408 | 1.0278 | -1 % |
| reads | 24 reads | 1.4130 | 1.4226 | +1 % |
| size | 1/4 (1920 x 1080) | 0.2506 | 0.2658 | +6 % |
| size | 1/16 (960 x 540) | 0.2129 | 0.2261 | +6 % |
| size | 1/64 (480 x 270) | 0.1010 | 0.0997 | -1 % |
| size | 1/256 (240 x 135) | 0.0253 | 0.0257 | +2 % |
| size | 1/1024 (120 x 67) | 0.0111 | 0.0194 | +75 % |
| chain | 1/64, 2 passes | 0.0066 | 0.0066 | -1 % |
| chain | 1/64, 8 passes | 0.0263 | 0.0263 | -0 % |
| chain | 1/64, 32 passes | 0.1051 | 0.1051 | -0 % |
| chain | 1/256, 2 passes | 0.0030 | 0.0033 | +9 % |
| chain | 1/256, 8 passes | 0.0108 | 0.0131 | +21 % |
| chain | 1/256, 32 passes | 0.0522 | 0.0525 | +1 % |
| quad | 4 reads + 12 exchanges | 0.5385 | 0.5396 | +0 % |
| quad | 16 reads | 1.0408 | 1.0278 | -1 % |
| underfill | 64 reads into 120 x 67 | 0.1603 | 0.1603 | +0 % |
| underfill | 64 reads into 240 x 135 | 0.1943 | 0.0549 | -72 % |
| underfill | 64 reads into 480 x 270 | 0.1103 | 0.0573 | -48 % |
| blend | RGBA8 add blend | 0.4155 | 0.4246 | +2 % |
| blend | RGB10A2 add blend | 0.4196 | 0.4246 | +1 % |
| blend | RG11B10F add blend | 0.4111 | 0.4246 | +3 % |
| blend | RGBA16F add blend | 0.8446 | 0.8481 | +0 % |
| blend | RGBA32F add blend | 1.7106 | 1.7117 | +0 % |
| blend | R8 add blend | 0.2492 | 0.2503 | +0 % |
| blend | R16F add blend | 0.2490 | 0.2501 | +0 % |
| blend | R32F add blend | 0.4191 | 0.4246 | +1 % |
| blend | RG16F add blend | 0.4216 | 0.4246 | +1 % |

## GTX 860M (NVIDIA Maxwell)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.5061 | 0.5070 | +0 % |
| write | RG8 write noise | 0.5061 | 0.5070 | +0 % |
| write | R16F write noise | 0.5061 | 0.5070 | +0 % |
| write | RGBA8 write noise | 0.5062 | 0.5071 | +0 % |
| write | RGB10A2 write noise | 0.5069 | 0.5078 | +0 % |
| write | RG11B10F write noise | 0.5062 | 0.5071 | +0 % |
| write | RG16F write noise | 0.5062 | 0.5071 | +0 % |
| write | R32F write noise | 0.5062 | 0.5071 | +0 % |
| write | RGBA16F write noise | 1.0120 | 1.0129 | +0 % |
| write | RGBA32F write noise | 2.0240 | 2.0249 | +0 % |
| copy | copy Sample RGBA8 | 0.9330 | 0.9339 | +0 % |
| half | half bilinear RGBA8 | 0.5679 | 0.5840 | +3 % |
| copy | copy Sample RGB10A2 | 0.9327 | 0.9339 | +0 % |
| half | half bilinear RGB10A2 | 0.5677 | 0.5840 | +3 % |
| copy | copy Sample RGBA16F | 1.8645 | 1.8669 | +0 % |
| half | half bilinear RGBA16F | 1.1373 | 1.1671 | +3 % |
| copy | copy Sample RGBA32F | 3.7175 | 3.7329 | +0 % |
| half | half bilinear RGBA32F | 2.2766 | 2.3334 | +2 % |
| reads | 1 read | 0.9333 | 0.9339 | +0 % |
| reads | 2 reads | 0.9359 | 0.9339 | -0 % |
| reads | 3 reads | 0.9560 | 0.9339 | -2 % |
| reads | 4 reads | 0.9489 | 0.9339 | -2 % |
| reads | 6 reads | 1.2338 | 1.1431 | -7 % |
| reads | 8 reads | 1.5165 | 1.4848 | -2 % |
| reads | 10 reads | 1.8344 | 1.8265 | -0 % |
| reads | 12 reads | 2.1661 | 2.1682 | +0 % |
| reads | 16 reads | 2.7721 | 2.8517 | +3 % |
| reads | 24 reads | 4.2562 | 4.2185 | -1 % |
| size | 1/4 (1920 x 1080) | 0.5676 | 0.5840 | +3 % |
| size | 1/16 (960 x 540) | 0.4762 | 0.4966 | +4 % |
| size | 1/64 (480 x 270) | 0.2299 | 0.2333 | +1 % |
| size | 1/256 (240 x 135) | 0.0596 | 0.0590 | -1 % |
| size | 1/1024 (120 x 67) | 0.0218 | 0.0218 | +0 % |
| chain | 1/64, 2 passes | 0.0175 | 0.0179 | +3 % |
| chain | 1/64, 8 passes | 0.0747 | 0.0718 | -4 % |
| chain | 1/64, 32 passes | 0.2867 | 0.2871 | +0 % |
| chain | 1/256, 2 passes | 0.0057 | 0.0058 | +2 % |
| chain | 1/256, 8 passes | 0.0221 | 0.0233 | +6 % |
| chain | 1/256, 32 passes | 0.0932 | 0.0933 | +0 % |
| quad | 4 reads + 12 exchanges | 3.1511 | 3.1520 | +0 % |
| quad | 16 reads | 2.7721 | 2.8517 | +3 % |
| blend | RGBA8 add blend | 0.9293 | 0.9339 | +0 % |
| blend | RGB10A2 add blend | 1.0355 | 1.0364 | +0 % |
| blend | RG11B10F add blend | 1.0359 | 1.0368 | +0 % |
| blend | RGBA16F add blend | 1.8773 | 1.8782 | +0 % |
| blend | RGBA32F add blend | 7.1846 | 7.1855 | +0 % |

## RTX 2070 (NVIDIA Turing RTX)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.1114 | 0.1523 | +37 % |
| write | RG8 write noise | 0.1286 | 0.1523 | +18 % |
| write | R16F write noise | 0.1296 | 0.1523 | +18 % |
| write | RGBA8 write noise | 0.1353 | 0.1523 | +13 % |
| write | RGB10A2 write noise | 0.1323 | 0.1523 | +15 % |
| write | RG11B10F write noise | 0.1330 | 0.1523 | +15 % |
| write | RG16F write noise | 0.1349 | 0.1523 | +13 % |
| write | R32F write noise | 0.1273 | 0.1523 | +20 % |
| write | RGBA16F write noise | 0.2318 | 0.2328 | +0 % |
| write | RGBA32F write noise | 0.4554 | 0.4564 | +0 % |
| copy | copy Sample RGBA8 | 0.1691 | 0.1860 | +10 % |
| half | half bilinear RGBA8 | 0.1000 | 0.1067 | +7 % |
| copy | copy Sample RGB10A2 | 0.1688 | 0.1860 | +10 % |
| half | half bilinear RGB10A2 | 0.1000 | 0.1067 | +7 % |
| copy | copy Sample RGBA16F | 0.3297 | 0.3392 | +3 % |
| half | half bilinear RGBA16F | 0.1994 | 0.2124 | +7 % |
| copy | copy Sample RGBA32F | 0.6630 | 0.6774 | +2 % |
| half | half bilinear RGBA32F | 0.3997 | 0.4238 | +6 % |
| reads | 1 read | 0.1690 | 0.1860 | +10 % |
| reads | 2 reads | 0.1704 | 0.2197 | +29 % |
| reads | 3 reads | 0.1980 | 0.2535 | +28 % |
| reads | 4 reads | 0.2394 | 0.2872 | +20 % |
| reads | 6 reads | 0.3268 | 0.3546 | +9 % |
| reads | 8 reads | 0.4046 | 0.4220 | +4 % |
| reads | 10 reads | 0.5012 | 0.4895 | -2 % |
| reads | 12 reads | 0.5525 | 0.5569 | +1 % |
| reads | 16 reads | 0.7064 | 0.6918 | -2 % |
| reads | 24 reads | 0.9519 | 0.9615 | +1 % |
| size | 1/4 (1920 x 1080) | 0.1001 | 0.1067 | +7 % |
| size | 1/16 (960 x 540) | 0.0877 | 0.0908 | +4 % |
| size | 1/64 (480 x 270) | 0.0803 | 0.0753 | -6 % |
| size | 1/256 (240 x 135) | 0.0183 | 0.0196 | +7 % |
| size | 1/1024 (120 x 67) | 0.0010 | 0.0056 | +461 % |
| chain | 1/64, 2 passes | 0.0051 | 0.0053 | +3 % |
| chain | 1/64, 8 passes | 0.0212 | 0.0211 | -1 % |
| chain | 1/64, 32 passes | 0.0841 | 0.0843 | +0 % |
| chain | 1/256, 2 passes | 0.0026 | 0.0028 | +9 % |
| chain | 1/256, 8 passes | 0.0094 | 0.0113 | +20 % |
| chain | 1/256, 32 passes | 0.0450 | 0.0452 | +1 % |
| quad | 4 reads + 12 exchanges | 0.3896 | 0.3906 | +0 % |
| quad | 16 reads | 0.7064 | 0.6918 | -2 % |
| blend | RGBA8 add blend | 0.1628 | 0.1701 | +4 % |
| blend | RGB10A2 add blend | 0.2259 | 0.2269 | +0 % |
| blend | RG11B10F add blend | 0.2667 | 0.2677 | +0 % |
| blend | RGBA16F add blend | 0.3274 | 0.3392 | +4 % |
| blend | RGBA32F add blend | 1.2183 | 1.2193 | +0 % |

## RTX 3060 (NVIDIA Ampere)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.1459 | 0.1472 | +1 % |
| write | RG8 write noise | 0.1314 | 0.1327 | +1 % |
| write | R16F write noise | 0.1301 | 0.1314 | +1 % |
| write | RGBA8 write noise | 0.1302 | 0.1315 | +1 % |
| write | RGB10A2 write noise | 0.1300 | 0.1313 | +1 % |
| write | RG11B10F write noise | 0.1300 | 0.1313 | +1 % |
| write | RG16F write noise | 0.1298 | 0.1311 | +1 % |
| write | R32F write noise | 0.1297 | 0.1310 | +1 % |
| write | RGBA16F write noise | 0.2020 | 0.2033 | +1 % |
| write | RGBA32F write noise | 0.4035 | 0.4048 | +0 % |
| copy | copy Sample RGBA8 | 0.1947 | 0.1960 | +1 % |
| half | half bilinear RGBA8 | 0.1209 | 0.1230 | +2 % |
| copy | copy Sample RGB10A2 | 0.1940 | 0.1960 | +1 % |
| half | half bilinear RGB10A2 | 0.1210 | 0.1230 | +2 % |
| copy | copy Sample RGBA16F | 0.3889 | 0.3907 | +0 % |
| half | half bilinear RGBA16F | 0.2420 | 0.2447 | +1 % |
| copy | copy Sample RGBA32F | 0.7815 | 0.7801 | -0 % |
| half | half bilinear RGBA32F | 0.4813 | 0.4880 | +1 % |
| blend | RGBA8 add blend | 0.2102 | 0.2115 | +1 % |
| blend | RGB10A2 add blend | 0.2636 | 0.2649 | +0 % |
| blend | RG11B10F add blend | 0.2631 | 0.2644 | +0 % |
| blend | RGBA16F add blend | 0.3979 | 0.3992 | +0 % |
| blend | RGBA32F add blend | 1.5138 | 1.5151 | +0 % |

## RTX 4070 (NVIDIA Ada)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0730 | 0.0818 | +12 % |
| write | RG8 write noise | 0.0818 | 0.0825 | +1 % |
| write | R16F write noise | 0.0815 | 0.0822 | +1 % |
| write | RGBA8 write noise | 0.0818 | 0.0825 | +1 % |
| write | RGB10A2 write noise | 0.0811 | 0.0818 | +1 % |
| write | RG11B10F write noise | 0.0843 | 0.0850 | +1 % |
| write | RG16F write noise | 0.0812 | 0.0819 | +1 % |
| write | R32F write noise | 0.0813 | 0.0820 | +1 % |
| write | RGBA16F write noise | 0.1366 | 0.1443 | +6 % |
| write | RGBA32F write noise | 0.2783 | 0.2879 | +3 % |
| copy | copy Sample RGBA8 | 0.1436 | 0.1443 | +1 % |
| half | half bilinear RGBA8 | 0.0667 | 0.0905 | +36 % |
| copy | copy Sample RGB10A2 | 0.1437 | 0.1443 | +0 % |
| half | half bilinear RGB10A2 | 0.0663 | 0.0905 | +36 % |
| copy | copy Sample RGBA16F | 0.2863 | 0.2879 | +1 % |
| half | half bilinear RGBA16F | 0.1749 | 0.1802 | +3 % |
| copy | copy Sample RGBA32F | 0.5782 | 0.5751 | -1 % |
| half | half bilinear RGBA32F | 0.3484 | 0.3597 | +3 % |
| reads | 1 read | 0.1438 | 0.1443 | +0 % |
| reads | 2 reads | 0.1407 | 0.1443 | +3 % |
| reads | 3 reads | 0.1482 | 0.1443 | -3 % |
| reads | 4 reads | 0.1249 | 0.1443 | +16 % |
| reads | 6 reads | 0.1769 | 0.1721 | -3 % |
| reads | 8 reads | 0.2093 | 0.2022 | -3 % |
| reads | 10 reads | 0.2316 | 0.2323 | +0 % |
| reads | 12 reads | 0.2585 | 0.2624 | +2 % |
| reads | 16 reads | 0.3111 | 0.3227 | +4 % |
| reads | 24 reads | 0.4486 | 0.4431 | -1 % |
| size | 1/4 (1920 x 1080) | 0.0680 | 0.0905 | +33 % |
| size | 1/16 (960 x 540) | 0.0246 | 0.0770 | +213 % |
| size | 1/64 (480 x 270) | 0.0237 | 0.0225 | -5 % |
| size | 1/256 (240 x 135) | 0.0059 | 0.0062 | +5 % |
| size | 1/1024 (120 x 67) | 0.0014 | 0.0021 | +49 % |
| chain | 1/64, 2 passes | 0.0033 | 0.0032 | -3 % |
| chain | 1/64, 8 passes | 0.0127 | 0.0129 | +1 % |
| chain | 1/64, 32 passes | 0.0515 | 0.0514 | -0 % |
| chain | 1/256, 2 passes | 0.0019 | 0.0019 | +0 % |
| chain | 1/256, 8 passes | 0.0070 | 0.0076 | +9 % |
| chain | 1/256, 32 passes | 0.0304 | 0.0304 | +0 % |
| quad | 4 reads + 12 exchanges | 0.1679 | 0.1686 | +0 % |
| quad | 16 reads | 0.3111 | 0.3227 | +4 % |
| blend | RGBA8 add blend | 0.1440 | 0.1447 | +1 % |
| blend | RGB10A2 add blend | 0.1818 | 0.1825 | +0 % |
| blend | RG11B10F add blend | 0.1813 | 0.1820 | +0 % |
| blend | RGBA16F add blend | 0.2954 | 0.2961 | +0 % |
| blend | RGBA32F add blend | 0.8282 | 0.8289 | +0 % |

## RTX 5070 (NVIDIA Blackwell)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0371 | 0.0514 | +39 % |
| write | RG8 write noise | 0.0398 | 0.0514 | +29 % |
| write | R16F write noise | 0.0402 | 0.0514 | +28 % |
| write | RGBA8 write noise | 0.0550 | 0.0581 | +6 % |
| write | RGB10A2 write noise | 0.0547 | 0.0581 | +6 % |
| write | RG11B10F write noise | 0.0547 | 0.0581 | +6 % |
| write | RG16F write noise | 0.0546 | 0.0581 | +6 % |
| write | R32F write noise | 0.0546 | 0.0581 | +6 % |
| write | RGBA16F write noise | 0.1101 | 0.1155 | +5 % |
| write | RGBA32F write noise | 0.2204 | 0.2303 | +4 % |
| copy | copy Sample RGBA8 | 0.1148 | 0.1155 | +1 % |
| half | half bilinear RGBA8 | 0.0144 | 0.0724 | +403 % |
| copy | copy Sample RGB10A2 | 0.1147 | 0.1155 | +1 % |
| half | half bilinear RGB10A2 | 0.0178 | 0.0724 | +307 % |
| copy | copy Sample RGBA16F | 0.2299 | 0.2303 | +0 % |
| half | half bilinear RGBA16F | 0.1310 | 0.1442 | +10 % |
| copy | copy Sample RGBA32F | 0.4624 | 0.4599 | -1 % |
| half | half bilinear RGBA32F | 0.2715 | 0.2877 | +6 % |
| reads | 1 read | 0.1148 | 0.1155 | +1 % |
| reads | 2 reads | 0.1159 | 0.1155 | -0 % |
| reads | 3 reads | 0.1160 | 0.1155 | -0 % |
| reads | 4 reads | 0.0972 | 0.1155 | +19 % |
| reads | 6 reads | 0.1457 | 0.1467 | +1 % |
| reads | 8 reads | 0.1781 | 0.1785 | +0 % |
| reads | 10 reads | 0.2067 | 0.2103 | +2 % |
| reads | 12 reads | 0.2433 | 0.2421 | -0 % |
| reads | 16 reads | 0.3070 | 0.3057 | -0 % |
| reads | 24 reads | 0.4311 | 0.4328 | +0 % |
| size | 1/4 (1920 x 1080) | 0.0120 | 0.0724 | +503 % |
| size | 1/16 (960 x 540) | 0.0091 | 0.0616 | +577 % |
| size | 1/64 (480 x 270) | 0.0093 | 0.0159 | +71 % |
| size | 1/256 (240 x 135) | 0.0026 | 0.0045 | +72 % |
| size | 1/1024 (120 x 67) | 0.0008 | 0.0016 | +100 % |
| chain | 1/64, 2 passes | 0.0026 | 0.0026 | -2 % |
| chain | 1/64, 8 passes | 0.0097 | 0.0102 | +6 % |
| chain | 1/64, 32 passes | 0.0410 | 0.0410 | -0 % |
| chain | 1/256, 2 passes | 0.0017 | 0.0016 | -4 % |
| chain | 1/256, 8 passes | 0.0060 | 0.0065 | +8 % |
| chain | 1/256, 32 passes | 0.0261 | 0.0260 | -0 % |
| quad | 4 reads + 12 exchanges | 0.1524 | 0.1531 | +0 % |
| quad | 16 reads | 0.3070 | 0.3057 | -0 % |
| blend | RGBA8 add blend | 0.1087 | 0.1155 | +6 % |
| blend | RGB10A2 add blend | 0.1310 | 0.1317 | +1 % |
| blend | RG11B10F add blend | 0.1273 | 0.1280 | +1 % |
| blend | RGBA16F add blend | 0.2421 | 0.2428 | +0 % |
| blend | RGBA32F add blend | 0.5966 | 0.5973 | +0 % |

## AMD 0x15E7 (AMD Ryzen iGPUs (RDNA 2 / 3))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 1.4687 | 1.4741 | +0 % |
| write | RG8 write noise | 1.4762 | 1.4816 | +0 % |
| write | R16F write noise | 1.4766 | 1.4820 | +0 % |
| write | RGBA8 write noise | 1.4897 | 1.5305 | +3 % |
| write | RGB10A2 write noise | 1.4992 | 1.5305 | +2 % |
| write | RG11B10F write noise | 1.4955 | 1.5305 | +2 % |
| write | RG16F write noise | 1.5120 | 1.5305 | +1 % |
| write | R32F write noise | 1.6426 | 1.6480 | +0 % |
| write | RGBA16F write noise | 2.1101 | 3.0557 | +45 % |
| write | RGBA32F write noise | 3.6107 | 6.1060 | +69 % |
| copy | copy Sample RGBA8 | 3.0503 | 3.0557 | +0 % |
| half | half bilinear RGBA8 | 1.8639 | 1.9118 | +3 % |
| copy | copy Sample RGB10A2 | 3.0108 | 3.0557 | +1 % |
| half | half bilinear RGB10A2 | 1.0063 | 1.9118 | +90 % |
| copy | copy Sample RGBA16F | 3.3479 | 6.1060 | +82 % |
| half | half bilinear RGBA16F | 2.0962 | 3.8182 | +82 % |
| copy | copy Sample RGBA32F | 6.8072 | 12.2066 | +79 % |
| half | half bilinear RGBA32F | 4.2047 | 7.6311 | +81 % |
| reads | 1 read | 3.0476 | 3.0557 | +0 % |
| reads | 2 reads | 3.0749 | 3.0557 | -1 % |
| reads | 3 reads | 3.1406 | 3.0557 | -3 % |
| reads | 4 reads | 2.2147 | 3.0557 | +38 % |
| reads | 6 reads | 3.5006 | 3.2986 | -6 % |
| reads | 8 reads | 4.1625 | 4.1204 | -1 % |
| reads | 10 reads | 4.9311 | 4.9421 | +0 % |
| reads | 12 reads | 5.7255 | 5.7639 | +1 % |
| reads | 16 reads | 7.3667 | 7.4075 | +1 % |
| reads | 24 reads | 10.7160 | 10.6947 | -0 % |
| size | 1/4 (1920 x 1080) | 1.8664 | 1.9118 | +2 % |
| size | 1/16 (960 x 540) | 0.8197 | 1.6258 | +98 % |
| size | 1/64 (480 x 270) | 0.4039 | 0.9328 | +131 % |
| size | 1/256 (240 x 135) | 0.3701 | 0.2372 | -36 % |
| size | 1/1024 (120 x 67) | 0.0523 | 0.0629 | +20 % |
| chain | 1/64, 2 passes | 0.0536 | 0.0589 | +10 % |
| chain | 1/64, 8 passes | 0.2232 | 0.2356 | +6 % |
| chain | 1/64, 32 passes | 0.9371 | 0.9424 | +1 % |
| chain | 1/256, 2 passes | 0.0189 | 0.0228 | +20 % |
| chain | 1/256, 8 passes | 0.0836 | 0.0911 | +9 % |
| chain | 1/256, 32 passes | 0.3604 | 0.3643 | +1 % |
| quad | 4 reads + 12 exchanges | 4.7003 | 4.7057 | +0 % |
| quad | 16 reads | 7.3667 | 7.4075 | +1 % |
| blend | RGBA8 add blend | 1.6280 | 3.0557 | +88 % |
| blend | RGB10A2 add blend | 1.6972 | 3.0557 | +80 % |
| blend | RG11B10F add blend | 1.6384 | 3.0557 | +87 % |
| blend | RGBA16F add blend | 3.6758 | 6.1060 | +66 % |
| blend | RGBA32F add blend | 7.1175 | 12.2066 | +72 % |

## HD 6450 (AMD GCN (Polaris, Vega))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 7.7351 | 7.7369 | +0 % |
| write | RG8 write noise | 8.2607 | 8.2625 | +0 % |
| write | R16F write noise | 8.2539 | 8.2557 | +0 % |
| write | RGBA8 write noise | 9.7379 | 9.7397 | +0 % |
| write | RGB10A2 write noise | 9.7377 | 9.7395 | +0 % |
| write | RG11B10F write noise | 9.7378 | 9.7396 | +0 % |
| write | RG16F write noise | 9.7334 | 9.7352 | +0 % |
| write | R32F write noise | 9.9266 | 9.9284 | +0 % |
| write | RGBA16F write noise | 12.7273 | 12.7291 | +0 % |
| write | RGBA32F write noise | 18.9339 | 18.9357 | +0 % |
| copy | copy Sample RGBA8 | 6.0822 | 9.7397 | +60 % |
| half | half bilinear RGBA8 | 3.7156 | 3.8032 | +2 % |
| copy | copy Sample RGB10A2 | 6.0822 | 9.7395 | +60 % |
| half | half bilinear RGB10A2 | 3.7128 | 3.8032 | +2 % |
| copy | copy Sample RGBA16F | 11.8613 | 12.7291 | +7 % |
| half | half bilinear RGBA16F | 7.3593 | 7.6046 | +3 % |
| copy | copy Sample RGBA32F | 23.3606 | 24.3306 | +4 % |
| half | half bilinear RGBA32F | 14.6058 | 15.2073 | +4 % |
| reads | 1 read | 6.0831 | 9.7397 | +60 % |
| reads | 2 reads | 6.4521 | 9.7397 | +51 % |
| reads | 3 reads | 6.7131 | 9.7397 | +45 % |
| reads | 4 reads | 7.0491 | 9.7397 | +38 % |
| reads | 6 reads | 10.0576 | 10.0040 | -1 % |
| reads | 8 reads | 13.3317 | 13.3167 | -0 % |
| reads | 10 reads | 16.6192 | 16.6293 | +0 % |
| reads | 12 reads | 19.9314 | 19.9419 | +0 % |
| reads | 16 reads | 26.5592 | 26.5672 | +0 % |
| reads | 24 reads | 39.8222 | 39.8177 | -0 % |
| size | 1/4 (1920 x 1080) | 3.7232 | 3.8032 | +2 % |
| size | 1/16 (960 x 540) | 3.1482 | 3.2330 | +3 % |
| size | 1/64 (480 x 270) | 1.5301 | 2.3454 | +53 % |
| size | 1/256 (240 x 135) | 0.7908 | 0.5877 | -26 % |
| size | 1/1024 (120 x 67) | 0.1996 | 0.1996 | +0 % |
| chain | 1/64, 2 passes | 0.1930 | 0.1976 | +2 % |
| chain | 1/64, 8 passes | 0.7855 | 0.7906 | +1 % |
| chain | 1/64, 32 passes | 3.1577 | 3.1623 | +0 % |
| chain | 1/256, 2 passes | 0.0500 | 0.0522 | +4 % |
| chain | 1/256, 8 passes | 0.2066 | 0.2086 | +1 % |
| chain | 1/256, 32 passes | 0.8323 | 0.8345 | +0 % |
| quad | 4 reads + 12 exchanges | 26.5524 | 26.5542 | +0 % |
| quad | 16 reads | 26.5592 | 26.5672 | +0 % |
| blend | RGBA8 add blend | 13.5138 | 13.5156 | +0 % |
| blend | RGB10A2 add blend | 13.4939 | 13.4957 | +0 % |
| blend | RG11B10F add blend | 13.4952 | 13.4970 | +0 % |
| blend | RGBA16F add blend | 19.3181 | 19.3199 | +0 % |
| blend | RGBA32F add blend | 31.1607 | 31.1625 | +0 % |

## RX 6650 XT (AMD RDNA 2)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.1481 | 0.1493 | +1 % |
| write | RG8 write noise | 0.0963 | 0.0975 | +1 % |
| write | R16F write noise | 0.0958 | 0.0970 | +1 % |
| write | RGBA8 write noise | 0.1346 | 0.1377 | +2 % |
| write | RGB10A2 write noise | 0.1348 | 0.1377 | +2 % |
| write | RG11B10F write noise | 0.1347 | 0.1377 | +2 % |
| write | RG16F write noise | 0.1348 | 0.1377 | +2 % |
| write | R32F write noise | 0.1348 | 0.1377 | +2 % |
| write | RGBA16F write noise | 0.2700 | 0.2741 | +2 % |
| write | RGBA32F write noise | 0.5395 | 0.5470 | +1 % |
| copy | copy Sample RGBA8 | 0.2729 | 0.2741 | +0 % |
| half | half bilinear RGBA8 | 0.1603 | 0.1718 | +7 % |
| copy | copy Sample RGB10A2 | 0.2730 | 0.2741 | +0 % |
| half | half bilinear RGB10A2 | 0.1603 | 0.1718 | +7 % |
| copy | copy Sample RGBA16F | 0.5502 | 0.5470 | -1 % |
| half | half bilinear RGBA16F | 0.3292 | 0.3424 | +4 % |
| copy | copy Sample RGBA32F | 1.1064 | 1.0928 | -1 % |
| half | half bilinear RGBA32F | 0.6695 | 0.6835 | +2 % |
| reads | 1 read | 0.2749 | 0.2741 | -0 % |
| reads | 2 reads | 0.2874 | 0.2741 | -5 % |
| reads | 3 reads | 0.2822 | 0.2741 | -3 % |
| reads | 4 reads | 0.2127 | 0.2741 | +29 % |
| reads | 6 reads | 0.2822 | 0.2741 | -3 % |
| reads | 8 reads | 0.2971 | 0.3537 | +19 % |
| reads | 10 reads | 0.3448 | 0.4419 | +28 % |
| reads | 12 reads | 0.4092 | 0.5300 | +30 % |
| reads | 16 reads | 0.6281 | 0.7062 | +12 % |
| reads | 24 reads | 0.9774 | 1.0587 | +8 % |
| size | 1/4 (1920 x 1080) | 0.1620 | 0.1718 | +6 % |
| size | 1/16 (960 x 540) | 0.0591 | 0.1462 | +147 % |
| size | 1/64 (480 x 270) | 0.0387 | 0.0590 | +52 % |
| size | 1/256 (240 x 135) | 0.0208 | 0.0157 | -25 % |
| size | 1/1024 (120 x 67) | 0.0044 | 0.0048 | +10 % |
| chain | 1/64, 2 passes | 0.0061 | 0.0082 | +35 % |
| chain | 1/64, 8 passes | 0.0308 | 0.0328 | +7 % |
| chain | 1/64, 32 passes | 0.1292 | 0.1313 | +2 % |
| chain | 1/256, 2 passes | 0.0028 | 0.0039 | +40 % |
| chain | 1/256, 8 passes | 0.0136 | 0.0157 | +15 % |
| chain | 1/256, 32 passes | 0.0615 | 0.0626 | +2 % |
| quad | 4 reads + 12 exchanges | 0.3554 | 0.3566 | +0 % |
| quad | 16 reads | 0.6281 | 0.7062 | +12 % |
| blend | RGBA8 add blend | 0.2837 | 0.2849 | +0 % |
| blend | RGB10A2 add blend | 0.2985 | 0.2997 | +0 % |
| blend | RG11B10F add blend | 0.2992 | 0.3004 | +0 % |
| blend | RGBA16F add blend | 0.5993 | 0.6005 | +0 % |
| blend | RGBA32F add blend | 1.1736 | 1.1748 | +0 % |

## RX 6900 XT (AMD RDNA 2)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0519 | 0.0532 | +2 % |
| write | RG8 write noise | 0.0520 | 0.0533 | +2 % |
| write | R16F write noise | 0.0524 | 0.0537 | +2 % |
| write | RGBA8 write noise | 0.0523 | 0.0536 | +2 % |
| write | RGB10A2 write noise | 0.0526 | 0.0539 | +2 % |
| write | RG11B10F write noise | 0.0525 | 0.0538 | +2 % |
| write | RG16F write noise | 0.0524 | 0.0537 | +2 % |
| write | R32F write noise | 0.0528 | 0.0541 | +2 % |
| write | RGBA16F write noise | 0.0603 | 0.0616 | +2 % |
| write | RGBA32F write noise | 0.2814 | 0.2827 | +0 % |
| copy | copy Sample RGBA8 | 0.0541 | 0.0554 | +2 % |
| half | half bilinear RGBA8 | 0.0214 | 0.0351 | +64 % |
| copy | copy Sample RGB10A2 | 0.0524 | 0.0554 | +6 % |
| half | half bilinear RGB10A2 | 0.0215 | 0.0351 | +63 % |
| copy | copy Sample RGBA16F | 0.1542 | 0.1095 | -29 % |
| half | half bilinear RGBA16F | 0.0430 | 0.0689 | +60 % |
| copy | copy Sample RGBA32F | 0.5851 | 0.2827 | -52 % |
| half | half bilinear RGBA32F | 0.3249 | 0.1365 | -58 % |
| blend | RGBA8 add blend | 0.0528 | 0.0554 | +5 % |
| blend | RGB10A2 add blend | 0.0526 | 0.0554 | +5 % |
| blend | RG11B10F add blend | 0.0528 | 0.0554 | +5 % |
| blend | RGBA16F add blend | 0.0813 | 0.1095 | +35 % |
| blend | RGBA32F add blend | 0.5980 | 0.5993 | +0 % |

## RX 7900 GRE (AMD RDNA 3)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0689 | 0.0702 | +2 % |
| write | RG8 write noise | 0.0418 | 0.0431 | +3 % |
| write | R16F write noise | 0.0418 | 0.0431 | +3 % |
| write | RGBA8 write noise | 0.0420 | 0.0625 | +49 % |
| write | RGB10A2 write noise | 0.0417 | 0.0625 | +50 % |
| write | RG11B10F write noise | 0.0416 | 0.0625 | +50 % |
| write | RG16F write noise | 0.0416 | 0.0625 | +50 % |
| write | R32F write noise | 0.0411 | 0.0625 | +52 % |
| write | RGBA16F write noise | 0.1239 | 0.1252 | +1 % |
| write | RGBA32F write noise | 0.2429 | 0.2463 | +1 % |
| copy | copy Sample RGBA8 | 0.1225 | 0.1238 | +1 % |
| half | half bilinear RGBA8 | 0.0250 | 0.0778 | +211 % |
| copy | copy Sample RGB10A2 | 0.0835 | 0.1238 | +48 % |
| half | half bilinear RGB10A2 | 0.0322 | 0.0778 | +142 % |
| copy | copy Sample RGBA16F | 0.5658 | 0.2463 | -56 % |
| half | half bilinear RGBA16F | 0.2271 | 0.1544 | -32 % |
| copy | copy Sample RGBA32F | 0.7463 | 0.4913 | -34 % |
| half | half bilinear RGBA32F | 0.4949 | 0.3075 | -38 % |
| blend | RGBA8 add blend | 0.0539 | 0.1238 | +130 % |
| blend | RGB10A2 add blend | 0.0669 | 0.1238 | +85 % |
| blend | RG11B10F add blend | 0.0543 | 0.1238 | +128 % |
| blend | RGBA16F add blend | 0.2514 | 0.2527 | +1 % |
| blend | RGBA32F add blend | 0.5253 | 0.5266 | +0 % |

## AMD 0x13C0 (AMD)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.8415 | 0.8428 | +0 % |
| write | RG8 write noise | 0.5677 | 0.5690 | +0 % |
| write | R16F write noise | 0.5608 | 0.5621 | +0 % |
| write | RGBA8 write noise | 0.8253 | 0.8266 | +0 % |
| write | RGB10A2 write noise | 0.8245 | 0.8258 | +0 % |
| write | RG11B10F write noise | 0.7179 | 0.7192 | +0 % |
| write | RG16F write noise | 0.7310 | 0.7323 | +0 % |
| write | R32F write noise | 0.7225 | 0.7238 | +0 % |
| write | RGBA16F write noise | 1.2286 | 1.2299 | +0 % |
| write | RGBA32F write noise | 2.1392 | 2.1405 | +0 % |
| copy | copy Sample RGBA8 | 1.0267 | 1.0280 | +0 % |
| half | half bilinear RGBA8 | 0.5757 | 0.6430 | +12 % |
| copy | copy Sample RGB10A2 | 1.0231 | 1.0280 | +0 % |
| half | half bilinear RGB10A2 | 0.5742 | 0.6430 | +12 % |
| copy | copy Sample RGBA16F | 1.7857 | 2.0547 | +15 % |
| half | half bilinear RGBA16F | 1.1590 | 1.2847 | +11 % |
| copy | copy Sample RGBA32F | 3.4224 | 4.1081 | +20 % |
| half | half bilinear RGBA32F | 2.3918 | 2.5680 | +7 % |
| blend | RGBA8 add blend | 1.2089 | 1.2102 | +0 % |
| blend | RGB10A2 add blend | 1.1632 | 1.1645 | +0 % |
| blend | RG11B10F add blend | 1.1655 | 1.1668 | +0 % |
| blend | RGBA16F add blend | 1.8829 | 2.0547 | +9 % |
| blend | RGBA32F add blend | 3.9900 | 4.1081 | +3 % |

## AMD 0x1636 (AMD Ryzen iGPUs (RDNA 2 / 3))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.7206 | 0.9012 | +25 % |
| write | RG8 write noise | 1.0904 | 1.0930 | +0 % |
| write | R16F write noise | 1.2164 | 1.2190 | +0 % |
| write | RGBA8 write noise | 1.5738 | 1.5764 | +0 % |
| write | RGB10A2 write noise | 1.0601 | 1.0627 | +0 % |
| write | RG11B10F write noise | 1.3257 | 1.3283 | +0 % |
| write | RG16F write noise | 1.0353 | 1.0379 | +0 % |
| write | R32F write noise | 1.1992 | 1.2018 | +0 % |
| write | RGBA16F write noise | 2.2388 | 2.2414 | +0 % |
| write | RGBA32F write noise | 5.0946 | 5.0972 | +0 % |
| copy | copy Sample RGBA8 | 1.9518 | 1.9544 | +0 % |
| half | half bilinear RGBA8 | 1.1565 | 1.2225 | +6 % |
| copy | copy Sample RGB10A2 | 1.9924 | 1.9544 | -2 % |
| half | half bilinear RGB10A2 | 1.1575 | 1.2225 | +6 % |
| copy | copy Sample RGBA16F | 4.4749 | 3.9062 | -13 % |
| half | half bilinear RGBA16F | 2.4687 | 2.4424 | -1 % |
| copy | copy Sample RGBA32F | 8.0591 | 7.8098 | -3 % |
| half | half bilinear RGBA32F | 5.2547 | 4.8821 | -7 % |
| reads | 1 read | 1.8474 | 1.9544 | +6 % |
| reads | 2 reads | 1.9030 | 1.9544 | +3 % |
| reads | 3 reads | 2.0347 | 1.9544 | -4 % |
| reads | 4 reads | 2.0964 | 1.9544 | -7 % |
| reads | 6 reads | 2.3459 | 2.1591 | -8 % |
| reads | 8 reads | 2.6550 | 2.5784 | -3 % |
| reads | 10 reads | 2.9876 | 2.9977 | +0 % |
| reads | 12 reads | 3.3640 | 3.4170 | +2 % |
| reads | 16 reads | 4.1831 | 4.2556 | +2 % |
| reads | 24 reads | 5.9786 | 5.9328 | -1 % |
| size | 1/4 (1920 x 1080) | 1.0921 | 1.2225 | +12 % |
| size | 1/16 (960 x 540) | 0.8587 | 1.0395 | +21 % |
| size | 1/64 (480 x 270) | 0.4289 | 0.6059 | +41 % |
| size | 1/256 (240 x 135) | 0.1975 | 0.1535 | -22 % |
| size | 1/1024 (120 x 67) | 0.0487 | 0.0460 | -6 % |
| chain | 1/64, 2 passes | 0.0265 | 0.0276 | +4 % |
| chain | 1/64, 8 passes | 0.1086 | 0.1105 | +2 % |
| chain | 1/64, 32 passes | 0.4408 | 0.4419 | +0 % |
| chain | 1/256, 2 passes | 0.0105 | 0.0109 | +4 % |
| chain | 1/256, 8 passes | 0.0423 | 0.0435 | +3 % |
| chain | 1/256, 32 passes | 0.1736 | 0.1740 | +0 % |
| quad | 4 reads + 12 exchanges | 3.1304 | 3.1330 | +0 % |
| quad | 16 reads | 4.1831 | 4.2556 | +2 % |
| underfill | 64 reads into 120 x 67 | 0.2862 | 0.2862 | -0 % |
| underfill | 64 reads into 240 x 135 | 0.3131 | 0.2504 | -20 % |
| underfill | 64 reads into 480 x 270 | 0.4714 | 0.2619 | -44 % |
| blend | RGBA8 add blend | 2.0771 | 2.0797 | +0 % |
| blend | RGB10A2 add blend | 2.0717 | 2.0743 | +0 % |
| blend | RG11B10F add blend | 2.0645 | 2.0671 | +0 % |
| blend | RGBA16F add blend | 4.4862 | 4.4888 | +0 % |
| blend | RGBA32F add blend | 9.4817 | 9.4843 | +0 % |
| blend | R8 add blend | 0.7600 | 0.9012 | +19 % |
| blend | R16F add blend | 1.0845 | 1.0871 | +0 % |
| blend | R32F add blend | 2.0635 | 2.0661 | +0 % |
| blend | RG16F add blend | 2.0619 | 2.0645 | +0 % |

## AMD 0x1638 (AMD Ryzen iGPUs (RDNA 2 / 3))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 1.1698 | 3.6968 | +216 % |
| write | RG8 write noise | 1.2080 | 3.6968 | +206 % |
| write | R16F write noise | 1.1958 | 3.6968 | +209 % |
| write | RGBA8 write noise | 2.6013 | 3.6968 | +42 % |
| write | RGB10A2 write noise | 2.0739 | 3.6968 | +78 % |
| write | RG11B10F write noise | 2.1224 | 3.6968 | +74 % |
| write | RG16F write noise | 1.9724 | 3.6968 | +87 % |
| write | R32F write noise | 2.8377 | 3.6968 | +30 % |
| write | RGBA16F write noise | 4.1971 | 4.6990 | +12 % |
| write | RGBA32F write noise | 10.0073 | 10.0093 | +0 % |
| copy | copy Sample RGBA8 | 4.6970 | 4.6990 | +0 % |
| half | half bilinear RGBA8 | 2.6177 | 2.9377 | +12 % |
| copy | copy Sample RGB10A2 | 4.9272 | 4.6990 | -5 % |
| half | half bilinear RGB10A2 | 2.7550 | 2.9377 | +7 % |
| copy | copy Sample RGBA16F | 9.4446 | 9.3960 | -1 % |
| half | half bilinear RGBA16F | 5.7278 | 5.8733 | +3 % |
| copy | copy Sample RGBA32F | 19.1766 | 18.7900 | -2 % |
| half | half bilinear RGBA32F | 12.4514 | 11.7445 | -6 % |
| reads | 1 read | 4.2400 | 4.6990 | +11 % |
| reads | 2 reads | 4.5040 | 4.6990 | +4 % |
| reads | 3 reads | 4.5996 | 4.6990 | +2 % |
| reads | 4 reads | 3.6480 | 4.6990 | +29 % |
| reads | 6 reads | 4.8077 | 4.6990 | -2 % |
| reads | 8 reads | 4.9940 | 4.8407 | -3 % |
| reads | 10 reads | 5.1955 | 5.1267 | -1 % |
| reads | 12 reads | 5.4046 | 5.4126 | +0 % |
| reads | 16 reads | 5.5568 | 5.9846 | +8 % |
| reads | 24 reads | 7.3320 | 7.1285 | -3 % |
| size | 1/4 (1920 x 1080) | 2.2838 | 2.9377 | +29 % |
| size | 1/16 (960 x 540) | 1.9592 | 2.4973 | +27 % |
| size | 1/64 (480 x 270) | 1.2682 | 2.0350 | +60 % |
| size | 1/256 (240 x 135) | 0.7030 | 0.5103 | -27 % |
| size | 1/1024 (120 x 67) | 0.3030 | 0.3030 | +0 % |
| chain | 1/64, 2 passes | 0.0388 | 0.0425 | +9 % |
| chain | 1/64, 8 passes | 0.1613 | 0.1698 | +5 % |
| chain | 1/64, 32 passes | 0.6757 | 0.6794 | +1 % |
| chain | 1/256, 2 passes | 0.0119 | 0.0137 | +15 % |
| chain | 1/256, 8 passes | 0.0515 | 0.0547 | +6 % |
| chain | 1/256, 32 passes | 0.2169 | 0.2187 | +1 % |
| quad | 4 reads + 12 exchanges | 4.4063 | 4.6990 | +7 % |
| quad | 16 reads | 5.5568 | 5.9846 | +8 % |
| blend | RGBA8 add blend | 4.1993 | 4.6990 | +12 % |
| blend | RGB10A2 add blend | 3.6080 | 4.6990 | +30 % |
| blend | RG11B10F add blend | 4.1650 | 4.6990 | +13 % |
| blend | RGBA16F add blend | 8.4840 | 9.3960 | +11 % |
| blend | RGBA32F add blend | 16.8610 | 18.7900 | +11 % |

## AMD 0x164E (AMD Ryzen iGPUs (RDNA 2 / 3))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.9503 | 0.9539 | +0 % |
| write | RG8 write noise | 0.6371 | 0.6407 | +1 % |
| write | R16F write noise | 0.5753 | 0.5789 | +1 % |
| write | RGBA8 write noise | 0.9243 | 0.9279 | +0 % |
| write | RGB10A2 write noise | 0.9237 | 0.9273 | +0 % |
| write | RG11B10F write noise | 0.8225 | 0.8261 | +0 % |
| write | RG16F write noise | 0.7672 | 0.7708 | +0 % |
| write | R32F write noise | 0.7692 | 0.7728 | +0 % |
| write | RGBA16F write noise | 1.2939 | 1.2975 | +0 % |
| write | RGBA32F write noise | 2.4569 | 2.4605 | +0 % |
| copy | copy Sample RGBA8 | 1.2081 | 1.2117 | +0 % |
| half | half bilinear RGBA8 | 0.6947 | 0.7586 | +9 % |
| copy | copy Sample RGB10A2 | 1.2220 | 1.2117 | -1 % |
| half | half bilinear RGB10A2 | 0.6948 | 0.7586 | +9 % |
| copy | copy Sample RGBA16F | 2.1658 | 2.4198 | +12 % |
| half | half bilinear RGBA16F | 1.4080 | 1.5137 | +8 % |
| copy | copy Sample RGBA32F | 4.2425 | 4.8360 | +14 % |
| half | half bilinear RGBA32F | 2.8877 | 3.0238 | +5 % |
| reads | 1 read | 1.7354 | 1.2117 | -30 % |
| reads | 2 reads | 1.3260 | 1.3010 | -2 % |
| reads | 3 reads | 1.7786 | 1.8028 | +1 % |
| reads | 4 reads | 2.2229 | 2.3046 | +4 % |
| reads | 6 reads | 3.3383 | 3.3082 | -1 % |
| reads | 8 reads | 4.2908 | 4.3119 | +0 % |
| reads | 10 reads | 5.2803 | 5.3155 | +1 % |
| reads | 12 reads | 6.3774 | 6.3191 | -1 % |
| reads | 16 reads | 8.3202 | 8.3263 | +0 % |
| reads | 24 reads | 12.3270 | 12.3408 | +0 % |
| size | 1/4 (1920 x 1080) | 0.6938 | 0.7586 | +9 % |
| size | 1/16 (960 x 540) | 0.6432 | 0.6454 | +0 % |
| size | 1/64 (480 x 270) | 0.6334 | 0.6171 | -3 % |
| size | 1/256 (240 x 135) | 0.3160 | 0.1570 | -50 % |
| size | 1/1024 (120 x 67) | 0.0771 | 0.0771 | +0 % |
| chain | 1/64, 2 passes | 0.0241 | 0.0228 | -5 % |
| chain | 1/64, 8 passes | 0.0858 | 0.0914 | +6 % |
| chain | 1/64, 32 passes | 0.3342 | 0.3655 | +9 % |
| chain | 1/256, 2 passes | 0.0093 | 0.0111 | +19 % |
| chain | 1/256, 8 passes | 0.0408 | 0.0443 | +9 % |
| chain | 1/256, 32 passes | 0.1674 | 0.1773 | +6 % |
| quad | 4 reads + 12 exchanges | 5.3237 | 5.3273 | +0 % |
| quad | 16 reads | 8.3202 | 8.3263 | +0 % |
| blend | RGBA8 add blend | 1.3604 | 1.3640 | +0 % |
| blend | RGB10A2 add blend | 1.3598 | 1.3634 | +0 % |
| blend | RG11B10F add blend | 1.3615 | 1.3651 | +0 % |
| blend | RGBA16F add blend | 2.2394 | 2.4198 | +8 % |
| blend | RGBA32F add blend | 4.7128 | 4.8360 | +3 % |

## RX Vega 11 (AMD Ryzen iGPUs (RDNA 2 / 3))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 1.9790 | 1.9803 | +0 % |
| write | RG8 write noise | 1.2013 | 1.2026 | +0 % |
| write | R16F write noise | 0.7958 | 0.7971 | +0 % |
| write | RGBA8 write noise | 1.2057 | 1.2273 | +2 % |
| write | RGB10A2 write noise | 1.1459 | 1.2273 | +7 % |
| write | RG11B10F write noise | 2.0651 | 2.0664 | +0 % |
| write | RG16F write noise | 1.2887 | 1.2900 | +0 % |
| write | R32F write noise | 0.8222 | 1.2273 | +49 % |
| write | RGBA16F write noise | 2.5442 | 2.5455 | +0 % |
| write | RGBA32F write noise | 3.3126 | 4.9053 | +48 % |
| copy | copy Sample RGBA8 | 2.4520 | 2.4533 | +0 % |
| half | half bilinear RGBA8 | 1.6867 | 1.5338 | -9 % |
| copy | copy Sample RGB10A2 | 2.4997 | 2.4533 | -2 % |
| half | half bilinear RGB10A2 | 1.5883 | 1.5338 | -3 % |
| copy | copy Sample RGBA16F | 3.7196 | 4.9053 | +32 % |
| half | half bilinear RGBA16F | 2.9054 | 3.0663 | +6 % |
| copy | copy Sample RGBA32F | 6.9129 | 9.8093 | +42 % |
| half | half bilinear RGBA32F | 5.8756 | 6.1313 | +4 % |
| blend | RGBA8 add blend | 1.7044 | 2.4533 | +44 % |
| blend | RGB10A2 add blend | 1.6700 | 2.4533 | +47 % |
| blend | RG11B10F add blend | 1.6327 | 2.4533 | +50 % |
| blend | RGBA16F add blend | 3.4081 | 4.9053 | +44 % |
| blend | RGBA32F add blend | 6.7786 | 9.8093 | +45 % |

## HD 3000 (Intel)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 3.2165 | 3.2202 | +0 % |
| write | RG8 write noise | 3.5461 | 3.5498 | +0 % |
| write | R16F write noise | 3.5434 | 3.5471 | +0 % |
| write | RGBA8 write noise | 4.2780 | 4.2817 | +0 % |
| write | RGB10A2 write noise | 4.2772 | 4.2809 | +0 % |
| write | RG11B10F write noise | 4.2778 | 4.2815 | +0 % |
| write | RG16F write noise | 4.2774 | 4.2811 | +0 % |
| write | R32F write noise | 5.5340 | 5.5377 | +0 % |
| write | RGBA16F write noise | 5.7736 | 5.7773 | +0 % |
| write | RGBA32F write noise | 8.9642 | 8.9679 | +0 % |
| copy | copy Sample RGBA8 | 2.7681 | 4.2817 | +55 % |
| half | half bilinear RGBA8 | 1.6417 | 1.7338 | +6 % |
| copy | copy Sample RGB10A2 | 2.7681 | 4.2809 | +55 % |
| half | half bilinear RGB10A2 | 1.6409 | 1.7338 | +6 % |
| copy | copy Sample RGBA16F | 5.4357 | 5.7773 | +6 % |
| half | half bilinear RGBA16F | 3.2034 | 3.4639 | +8 % |
| copy | copy Sample RGBA32F | 11.0616 | 11.0761 | +0 % |
| half | half bilinear RGBA32F | 6.4363 | 6.9240 | +8 % |
| reads | 1 read | 2.7686 | 4.2817 | +55 % |
| reads | 2 reads | 2.9278 | 4.2817 | +46 % |
| reads | 3 reads | 4.1644 | 4.2817 | +3 % |
| reads | 4 reads | 5.5331 | 5.5367 | +0 % |
| reads | 6 reads | 8.2979 | 8.3016 | +0 % |
| reads | 8 reads | 11.0628 | 11.0665 | +0 % |
| reads | 10 reads | 13.8276 | 13.8314 | +0 % |
| reads | 12 reads | 16.5926 | 16.5963 | +0 % |
| reads | 16 reads | 22.1222 | 22.1261 | +0 % |
| reads | 24 reads | 33.1820 | 33.1857 | +0 % |
| size | 1/4 (1920 x 1080) | 1.6427 | 1.7338 | +6 % |
| size | 1/16 (960 x 540) | 1.3649 | 1.4743 | +8 % |
| size | 1/64 (480 x 270) | 0.6790 | 1.0807 | +59 % |
| size | 1/256 (240 x 135) | 0.3742 | 0.2730 | -27 % |
| size | 1/1024 (120 x 67) | 0.1156 | 0.1524 | +32 % |
| chain | 1/64, 2 passes | 0.0968 | 0.0968 | -0 % |
| chain | 1/64, 8 passes | 0.3871 | 0.3872 | +0 % |
| chain | 1/64, 32 passes | 1.5487 | 1.5487 | -0 % |
| chain | 1/256, 2 passes | 0.0298 | 0.0298 | -0 % |
| chain | 1/256, 8 passes | 0.1192 | 0.1191 | -0 % |
| chain | 1/256, 32 passes | 0.4766 | 0.4766 | -0 % |
| quad | 4 reads + 12 exchanges | 22.1223 | 22.1260 | +0 % |
| quad | 16 reads | 22.1222 | 22.1261 | +0 % |
| underfill | 64 reads into 120 x 67 | 0.7767 | 0.7767 | +0 % |
| underfill | 64 reads into 240 x 135 | 1.5198 | 0.3551 | -77 % |
| underfill | 64 reads into 480 x 270 | 2.8131 | 1.3862 | -51 % |
| blend | RGBA8 add blend | 6.0268 | 6.0305 | +0 % |
| blend | RGB10A2 add blend | 6.0325 | 6.0362 | +0 % |
| blend | RG11B10F add blend | 6.0355 | 6.0392 | +0 % |
| blend | RGBA16F add blend | 8.6482 | 8.6519 | +0 % |
| blend | RGBA32F add blend | 14.2106 | 14.2143 | +0 % |
| blend | R8 add blend | 4.0617 | 4.0654 | +0 % |
| blend | R16F add blend | 4.7209 | 4.7246 | +0 % |
| blend | R32F add blend | 11.0602 | 11.0639 | +0 % |
| blend | RG16F add blend | 6.0253 | 6.0290 | +0 % |

## HD 4600 (Intel)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 3.6313 | 3.6354 | +0 % |
| write | RG8 write noise | 3.6500 | 3.6541 | +0 % |
| write | R16F write noise | 3.7551 | 3.7592 | +0 % |
| write | RGBA8 write noise | 3.6447 | 3.6488 | +0 % |
| write | RGB10A2 write noise | 3.6542 | 3.6583 | +0 % |
| write | RG11B10F write noise | 3.6744 | 3.6785 | +0 % |
| write | RG16F write noise | 3.6458 | 3.6499 | +0 % |
| write | R32F write noise | 3.6397 | 3.6438 | +0 % |
| write | RGBA16F write noise | 3.6534 | 3.6575 | +0 % |
| write | RGBA32F write noise | 5.6202 | 5.8427 | +4 % |
| copy | copy Sample RGBA8 | 2.9193 | 3.6488 | +25 % |
| half | half bilinear RGBA8 | 1.6495 | 1.8287 | +11 % |
| copy | copy Sample RGB10A2 | 2.9559 | 3.6583 | +24 % |
| half | half bilinear RGB10A2 | 1.6166 | 1.8287 | +13 % |
| copy | copy Sample RGBA16F | 5.9521 | 5.8427 | -2 % |
| half | half bilinear RGBA16F | 3.5981 | 3.6532 | +2 % |
| copy | copy Sample RGBA32F | 13.5840 | 11.6813 | -14 % |
| half | half bilinear RGBA32F | 7.2302 | 7.3024 | +1 % |
| reads | 1 read | 3.0516 | 3.6488 | +20 % |
| reads | 2 reads | 3.1198 | 3.6488 | +17 % |
| reads | 3 reads | 3.1628 | 3.6488 | +15 % |
| reads | 4 reads | 3.8857 | 4.1147 | +6 % |
| reads | 6 reads | 5.5529 | 6.1700 | +11 % |
| reads | 8 reads | 7.3152 | 8.2254 | +12 % |
| reads | 10 reads | 9.1090 | 10.2807 | +13 % |
| reads | 12 reads | 10.9235 | 12.3360 | +13 % |
| reads | 16 reads | 14.8054 | 16.4466 | +11 % |
| reads | 24 reads | 23.6988 | 24.6678 | +4 % |
| size | 1/4 (1920 x 1080) | 2.8384 | 1.8287 | -36 % |
| size | 1/16 (960 x 540) | 2.6240 | 1.5550 | -41 % |
| size | 1/64 (480 x 270) | 2.5274 | 1.4866 | -41 % |
| size | 1/256 (240 x 135) | 0.3235 | 0.3747 | +16 % |
| size | 1/1024 (120 x 67) | 0.0895 | 0.0961 | +7 % |
| chain | 1/64, 2 passes | 0.0684 | 0.0778 | +14 % |
| chain | 1/64, 8 passes | 0.2861 | 0.3112 | +9 % |
| chain | 1/64, 32 passes | 1.2354 | 1.2448 | +1 % |
| chain | 1/256, 2 passes | 0.0243 | 0.0256 | +5 % |
| chain | 1/256, 8 passes | 0.0929 | 0.1025 | +10 % |
| chain | 1/256, 32 passes | 0.4088 | 0.4101 | +0 % |
| quad | 4 reads + 12 exchanges | 7.2208 | 7.2249 | +0 % |
| quad | 16 reads | 14.8054 | 16.4466 | +11 % |
| blend | RGBA8 add blend | 3.6782 | 3.6823 | +0 % |
| blend | RGB10A2 add blend | 3.6893 | 3.6934 | +0 % |
| blend | RG11B10F add blend | 3.6568 | 3.6609 | +0 % |
| blend | RGBA16F add blend | 6.0207 | 6.0248 | +0 % |
| blend | RGBA32F add blend | 12.4077 | 12.4118 | +0 % |

## HD 520 (Intel Gen9 (Skylake))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 1.5039 | 1.5052 | +0 % |
| write | RG8 write noise | 1.5218 | 1.5231 | +0 % |
| write | R16F write noise | 1.5159 | 1.5172 | +0 % |
| write | RGBA8 write noise | 1.5176 | 1.6494 | +9 % |
| write | RGB10A2 write noise | 1.5166 | 1.6494 | +9 % |
| write | RG11B10F write noise | 1.5469 | 1.6494 | +7 % |
| write | RG16F write noise | 1.5157 | 1.6494 | +9 % |
| write | R32F write noise | 1.5873 | 1.6494 | +4 % |
| write | RGBA16F write noise | 3.5993 | 3.6006 | +0 % |
| write | RGBA32F write noise | 6.0888 | 6.5937 | +8 % |
| copy | copy Sample RGBA8 | 3.2962 | 3.2975 | +0 % |
| half | half bilinear RGBA8 | 1.9582 | 2.0614 | +5 % |
| copy | copy Sample RGB10A2 | 3.4040 | 3.2975 | -3 % |
| half | half bilinear RGB10A2 | 2.1346 | 2.0614 | -3 % |
| copy | copy Sample RGBA16F | 6.6101 | 6.5937 | -0 % |
| half | half bilinear RGBA16F | 3.9902 | 4.1215 | +3 % |
| copy | copy Sample RGBA32F | 13.6858 | 13.1861 | -4 % |
| half | half bilinear RGBA32F | 7.9507 | 8.2418 | +4 % |
| blend | RGBA8 add blend | 3.3276 | 3.3289 | +0 % |
| blend | RGB10A2 add blend | 3.2272 | 3.2975 | +2 % |
| blend | RG11B10F add blend | 3.2087 | 3.2975 | +3 % |
| blend | RGBA16F add blend | 6.4285 | 6.5937 | +3 % |
| blend | RGBA32F add blend | 12.8254 | 13.1861 | +3 % |

## HD4600 (Intel)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 2.6878 | 2.6891 | +0 % |
| write | RG8 write noise | 2.6837 | 2.6850 | +0 % |
| write | R16F write noise | 2.6867 | 2.6880 | +0 % |
| write | RGBA8 write noise | 2.6930 | 2.6943 | +0 % |
| write | RGB10A2 write noise | 2.6941 | 2.6954 | +0 % |
| write | RG11B10F write noise | 2.6934 | 2.6947 | +0 % |
| write | RG16F write noise | 2.6933 | 2.6946 | +0 % |
| write | R32F write noise | 2.6924 | 2.6937 | +0 % |
| write | RGBA16F write noise | 2.7342 | 2.8005 | +2 % |
| write | RGBA32F write noise | 5.6706 | 5.6719 | +0 % |
| copy | copy Sample RGBA8 | 2.7992 | 2.8005 | +0 % |
| half | half bilinear RGBA8 | 1.6447 | 1.7508 | +6 % |
| copy | copy Sample RGB10A2 | 2.8799 | 2.8005 | -3 % |
| half | half bilinear RGB10A2 | 1.8243 | 1.7508 | -4 % |
| copy | copy Sample RGBA16F | 5.8502 | 5.5997 | -4 % |
| half | half bilinear RGBA16F | 3.4018 | 3.5003 | +3 % |
| copy | copy Sample RGBA32F | 11.9412 | 11.1981 | -6 % |
| half | half bilinear RGBA32F | 6.9262 | 6.9993 | +1 % |
| blend | RGBA8 add blend | 3.0847 | 3.0860 | +0 % |
| blend | RGB10A2 add blend | 3.1290 | 3.1303 | +0 % |
| blend | RG11B10F add blend | 3.1281 | 3.1294 | +0 % |
| blend | RGBA16F add blend | 5.9754 | 5.9767 | +0 % |
| blend | RGBA32F add blend | 11.9962 | 11.9975 | +0 % |

## Iris 540 (Intel Gen9 (Skylake))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.9073 | 0.9157 | +1 % |
| write | RG8 write noise | 0.8891 | 0.8975 | +1 % |
| write | R16F write noise | 0.9098 | 0.9182 | +1 % |
| write | RGBA8 write noise | 0.9615 | 1.4197 | +48 % |
| write | RGB10A2 write noise | 0.8582 | 1.4197 | +65 % |
| write | RG11B10F write noise | 0.9740 | 1.4197 | +46 % |
| write | RG16F write noise | 0.9658 | 1.4197 | +47 % |
| write | R32F write noise | 0.9740 | 1.4197 | +46 % |
| write | RGBA16F write noise | 3.8636 | 3.8720 | +0 % |
| write | RGBA32F write noise | 7.5049 | 7.5133 | +0 % |
| copy | copy Sample RGBA8 | 2.8227 | 2.8311 | +0 % |
| half | half bilinear RGBA8 | 0.8717 | 1.7726 | +103 % |
| copy | copy Sample RGB10A2 | 2.3855 | 2.8311 | +19 % |
| half | half bilinear RGB10A2 | 0.9028 | 1.7726 | +96 % |
| copy | copy Sample RGBA16F | 10.7095 | 5.6538 | -47 % |
| half | half bilinear RGBA16F | 4.8624 | 3.5367 | -27 % |
| copy | copy Sample RGBA32F | 21.8107 | 11.2992 | -48 % |
| half | half bilinear RGBA32F | 13.5990 | 7.0651 | -48 % |
| reads | 1 read | 2.6109 | 2.8311 | +8 % |
| reads | 2 reads | 2.6934 | 2.8311 | +5 % |
| reads | 3 reads | 2.7086 | 2.8311 | +5 % |
| reads | 4 reads | 2.5331 | 2.8311 | +12 % |
| reads | 6 reads | 3.3281 | 2.8318 | -15 % |
| reads | 8 reads | 3.8673 | 3.7468 | -3 % |
| reads | 10 reads | 4.6072 | 4.6619 | +1 % |
| reads | 12 reads | 5.4364 | 5.5769 | +3 % |
| reads | 16 reads | 7.4203 | 7.4070 | -0 % |
| reads | 24 reads | 11.0869 | 11.0673 | -0 % |
| size | 1/4 (1920 x 1080) | 0.8736 | 1.7726 | +103 % |
| size | 1/16 (960 x 540) | 0.7404 | 1.5079 | +104 % |
| size | 1/64 (480 x 270) | 0.7450 | 0.7961 | +7 % |
| size | 1/256 (240 x 135) | 0.2183 | 0.2053 | -6 % |
| size | 1/1024 (120 x 67) | 0.0691 | 0.0691 | -0 % |
| chain | 1/64, 2 passes | 0.0393 | 0.0377 | -4 % |
| chain | 1/64, 8 passes | 0.1567 | 0.1507 | -4 % |
| chain | 1/64, 32 passes | 0.6044 | 0.6028 | -0 % |
| chain | 1/256, 2 passes | 0.0194 | 0.0220 | +13 % |
| chain | 1/256, 8 passes | 0.0849 | 0.0879 | +4 % |
| chain | 1/256, 32 passes | 0.3491 | 0.3517 | +1 % |
| quad | 4 reads + 12 exchanges | 5.4170 | 5.4254 | +0 % |
| quad | 16 reads | 7.4203 | 7.4070 | -0 % |
| blend | RGBA8 add blend | 1.7232 | 2.8311 | +64 % |
| blend | RGB10A2 add blend | 1.7120 | 2.8311 | +65 % |
| blend | RG11B10F add blend | 1.7601 | 2.8311 | +61 % |
| blend | RGBA16F add blend | 9.3231 | 9.3315 | +0 % |
| blend | RGBA32F add blend | 26.3123 | 26.3207 | +0 % |

## UHD 630 0x3E98 (Intel Gen9.5 (Coffee Lake))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 1.5330 | 1.5343 | +0 % |
| write | RG8 write noise | 1.5377 | 1.5390 | +0 % |
| write | R16F write noise | 1.5492 | 1.5505 | +0 % |
| write | RGBA8 write noise | 1.5681 | 1.5694 | +0 % |
| write | RGB10A2 write noise | 1.5566 | 1.5579 | +0 % |
| write | RG11B10F write noise | 1.5464 | 1.5477 | +0 % |
| write | RG16F write noise | 1.5636 | 1.5649 | +0 % |
| write | R32F write noise | 1.5709 | 1.5722 | +0 % |
| write | RGBA16F write noise | 2.1712 | 2.1725 | +0 % |
| write | RGBA32F write noise | 4.4552 | 4.4565 | +0 % |
| copy | copy Sample RGBA8 | 2.0123 | 2.0136 | +0 % |
| half | half bilinear RGBA8 | 1.2345 | 1.2590 | +2 % |
| copy | copy Sample RGB10A2 | 1.9455 | 2.0136 | +3 % |
| half | half bilinear RGB10A2 | 1.4650 | 1.2590 | -14 % |
| copy | copy Sample RGBA16F | 4.2296 | 4.0259 | -5 % |
| half | half bilinear RGBA16F | 2.6489 | 2.5167 | -5 % |
| copy | copy Sample RGBA32F | 8.2461 | 8.0505 | -2 % |
| half | half bilinear RGBA32F | 5.3729 | 5.0320 | -6 % |
| blend | RGBA8 add blend | 2.0022 | 2.0136 | +1 % |
| blend | RGB10A2 add blend | 2.0436 | 2.0449 | +0 % |
| blend | RG11B10F add blend | 1.9571 | 2.0136 | +3 % |
| blend | RGBA16F add blend | 4.0184 | 4.0259 | +0 % |
| blend | RGBA32F add blend | 8.3154 | 8.3167 | +0 % |

## GT 1030 (NVIDIA Pascal)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.4653 | 0.6146 | +32 % |
| write | RG8 write noise | 0.5487 | 0.6146 | +12 % |
| write | R16F write noise | 0.5223 | 0.6146 | +18 % |
| write | RGBA8 write noise | 1.8705 | 1.8707 | +0 % |
| write | RGB10A2 write noise | 1.8762 | 1.8764 | +0 % |
| write | RG11B10F write noise | 1.8821 | 1.8823 | +0 % |
| write | RG16F write noise | 1.8762 | 1.8764 | +0 % |
| write | R32F write noise | 1.8746 | 1.8748 | +0 % |
| write | RGBA16F write noise | 3.6628 | 3.6630 | +0 % |
| write | RGBA32F write noise | 6.0762 | 6.0764 | +0 % |
| copy | copy Sample RGBA8 | 1.6491 | 1.8707 | +13 % |
| half | half bilinear RGBA8 | 0.9923 | 1.0309 | +4 % |
| copy | copy Sample RGB10A2 | 1.6488 | 1.8764 | +14 % |
| half | half bilinear RGB10A2 | 0.9921 | 1.0309 | +4 % |
| copy | copy Sample RGBA16F | 3.2710 | 3.6630 | +12 % |
| half | half bilinear RGBA16F | 1.9855 | 2.0616 | +4 % |
| copy | copy Sample RGBA32F | 6.5495 | 6.5966 | +1 % |
| half | half bilinear RGBA32F | 3.9678 | 4.1230 | +4 % |
| reads | 1 read | 1.6490 | 1.8707 | +13 % |
| reads | 2 reads | 1.6763 | 1.8707 | +12 % |
| reads | 3 reads | 1.6832 | 1.8707 | +11 % |
| reads | 4 reads | 1.7132 | 1.8707 | +9 % |
| reads | 6 reads | 1.8831 | 1.8707 | -1 % |
| reads | 8 reads | 2.2246 | 2.1634 | -3 % |
| reads | 10 reads | 2.5395 | 2.5506 | +0 % |
| reads | 12 reads | 2.9107 | 2.9378 | +1 % |
| reads | 16 reads | 3.6484 | 3.7122 | +2 % |
| reads | 24 reads | 5.3006 | 5.2609 | -1 % |
| size | 1/4 (1920 x 1080) | 0.9920 | 1.0309 | +4 % |
| size | 1/16 (960 x 540) | 0.8360 | 0.8763 | +5 % |
| size | 1/64 (480 x 270) | 0.3993 | 0.4006 | +0 % |
| size | 1/256 (240 x 135) | 0.1009 | 0.1003 | -1 % |
| size | 1/1024 (120 x 67) | 0.0581 | 0.0531 | -9 % |
| chain | 1/64, 2 passes | 0.0520 | 0.0602 | +16 % |
| chain | 1/64, 8 passes | 0.2073 | 0.2409 | +16 % |
| chain | 1/64, 32 passes | 0.8282 | 0.9636 | +16 % |
| chain | 1/256, 2 passes | 0.0050 | 0.0154 | +207 % |
| chain | 1/256, 8 passes | 0.0269 | 0.0614 | +128 % |
| chain | 1/256, 32 passes | 0.1082 | 0.2457 | +127 % |
| quad | 4 reads + 12 exchanges | 2.2436 | 2.2438 | +0 % |
| quad | 16 reads | 3.6484 | 3.7122 | +2 % |
| underfill | 64 reads into 120 x 67 | 0.4410 | 0.4410 | -0 % |
| underfill | 64 reads into 240 x 135 | 0.5225 | 0.2096 | -60 % |
| underfill | 64 reads into 480 x 270 | 0.5097 | 0.2192 | -57 % |
| blend | RGBA8 add blend | 2.7615 | 2.7617 | +0 % |
| blend | RGB10A2 add blend | 2.8060 | 2.8062 | +0 % |
| blend | RG11B10F add blend | 2.7868 | 2.7870 | +0 % |
| blend | RGBA16F add blend | 5.2275 | 5.2277 | +0 % |
| blend | RGBA32F add blend | 9.4164 | 9.4166 | +0 % |
| blend | R8 add blend | 0.5105 | 0.6146 | +20 % |
| blend | R16F add blend | 0.9845 | 0.9847 | +0 % |
| blend | R32F add blend | 2.7661 | 2.7663 | +0 % |
| blend | RG16F add blend | 2.7928 | 2.7930 | +0 % |

## GT 530 (NVIDIA)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 3.1183 | 3.1242 | +0 % |
| write | RG8 write noise | 3.1752 | 3.1811 | +0 % |
| write | R16F write noise | 3.1847 | 3.1906 | +0 % |
| write | RGBA8 write noise | 3.3046 | 3.3105 | +0 % |
| write | RGB10A2 write noise | 3.3167 | 3.3226 | +0 % |
| write | RG11B10F write noise | 6.1112 | 6.1171 | +0 % |
| write | RG16F write noise | 3.3137 | 3.3196 | +0 % |
| write | R32F write noise | 3.3302 | 3.3361 | +0 % |
| write | RGBA16F write noise | 5.9373 | 5.9432 | +0 % |
| write | RGBA32F write noise | 12.0875 | 12.0934 | +0 % |
| copy | copy Sample RGBA8 | 3.0418 | 3.3105 | +9 % |
| half | half bilinear RGBA8 | 1.8060 | 1.9070 | +6 % |
| copy | copy Sample RGB10A2 | 3.0536 | 3.3226 | +9 % |
| half | half bilinear RGB10A2 | 1.8055 | 1.9070 | +6 % |
| copy | copy Sample RGBA16F | 5.9265 | 6.0895 | +3 % |
| half | half bilinear RGBA16F | 3.6110 | 3.8081 | +5 % |
| copy | copy Sample RGBA32F | 12.1106 | 12.1731 | +1 % |
| half | half bilinear RGBA32F | 7.1674 | 7.6104 | +6 % |
| reads | 1 read | 3.0545 | 3.3105 | +8 % |
| reads | 2 reads | 3.4487 | 3.3105 | -4 % |
| reads | 3 reads | 3.6280 | 3.3105 | -9 % |
| reads | 4 reads | 3.8408 | 4.0538 | +6 % |
| reads | 6 reads | 5.5986 | 5.7152 | +2 % |
| reads | 8 reads | 6.9792 | 7.3766 | +6 % |
| reads | 10 reads | 9.2499 | 9.0381 | -2 % |
| reads | 12 reads | 10.8783 | 10.6995 | -2 % |
| reads | 16 reads | 14.1417 | 14.0223 | -1 % |
| reads | 24 reads | 20.5262 | 20.6680 | +1 % |
| size | 1/4 (1920 x 1080) | 1.8134 | 1.9070 | +5 % |
| size | 1/16 (960 x 540) | 1.5583 | 1.6218 | +4 % |
| size | 1/64 (480 x 270) | 0.7396 | 0.7711 | +4 % |
| size | 1/256 (240 x 135) | 0.2055 | 0.1972 | -4 % |
| size | 1/1024 (120 x 67) | 0.0988 | 0.0989 | +0 % |
| chain | 1/64, 2 passes | 0.1056 | 0.1079 | +2 % |
| chain | 1/64, 8 passes | 0.4219 | 0.4317 | +2 % |
| chain | 1/64, 32 passes | 1.7245 | 1.7268 | +0 % |
| chain | 1/256, 2 passes | 0.0318 | 0.0358 | +12 % |
| chain | 1/256, 8 passes | 0.1441 | 0.1431 | -1 % |
| chain | 1/256, 32 passes | 0.5684 | 0.5724 | +1 % |
| quad | 4 reads + 12 exchanges | 11.3231 | 11.3290 | +0 % |
| quad | 16 reads | 14.1417 | 14.0223 | -1 % |
| underfill | 64 reads into 120 x 67 | 0.7538 | 0.7538 | -0 % |
| underfill | 64 reads into 240 x 135 | 1.6902 | 0.3920 | -77 % |
| underfill | 64 reads into 480 x 270 | 2.1716 | 0.8479 | -61 % |
| blend | RGBA8 add blend | 5.1235 | 5.1294 | +0 % |
| blend | RGB10A2 add blend | 6.9863 | 6.9922 | +0 % |
| blend | RG11B10F add blend | 6.9743 | 6.9802 | +0 % |
| blend | RGBA16F add blend | 7.0959 | 7.1018 | +0 % |
| blend | RGBA32F add blend | 47.4581 | 47.4640 | +0 % |
| blend | R8 add blend | 4.6410 | 4.6469 | +0 % |
| blend | R16F add blend | 5.9612 | 5.9671 | +0 % |
| blend | R32F add blend | 11.8816 | 11.8875 | +0 % |
| blend | RG16F add blend | 6.9745 | 6.9804 | +0 % |

## RTX 2050 (NVIDIA Ampere)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.1916 | 0.1924 | +0 % |
| write | RG8 write noise | 0.1927 | 0.1935 | +0 % |
| write | R16F write noise | 0.1926 | 0.1934 | +0 % |
| write | RGBA8 write noise | 0.3323 | 0.3331 | +0 % |
| write | RGB10A2 write noise | 0.3320 | 0.3328 | +0 % |
| write | RG11B10F write noise | 0.3322 | 0.3330 | +0 % |
| write | RG16F write noise | 0.3321 | 0.3329 | +0 % |
| write | R32F write noise | 0.3325 | 0.3333 | +0 % |
| write | RGBA16F write noise | 0.6799 | 0.6807 | +0 % |
| write | RGBA32F write noise | 1.4067 | 1.4075 | +0 % |
| copy | copy Sample RGBA8 | 0.6335 | 0.6343 | +0 % |
| half | half bilinear RGBA8 | 0.3844 | 0.3967 | +3 % |
| copy | copy Sample RGB10A2 | 0.6345 | 0.6343 | -0 % |
| half | half bilinear RGB10A2 | 0.3844 | 0.3967 | +3 % |
| copy | copy Sample RGBA16F | 1.2687 | 1.2678 | -0 % |
| half | half bilinear RGBA16F | 0.7700 | 0.7927 | +3 % |
| copy | copy Sample RGBA32F | 2.5334 | 2.5348 | +0 % |
| half | half bilinear RGBA32F | 1.5388 | 1.5845 | +3 % |
| reads | 1 read | 0.6351 | 0.6343 | -0 % |
| reads | 2 reads | 0.6375 | 0.6343 | -1 % |
| reads | 3 reads | 0.6309 | 0.6343 | +1 % |
| reads | 4 reads | 0.4863 | 0.6343 | +30 % |
| reads | 6 reads | 0.6764 | 0.6343 | -6 % |
| reads | 8 reads | 0.7438 | 0.7123 | -4 % |
| reads | 10 reads | 0.8512 | 0.8643 | +2 % |
| reads | 12 reads | 0.9960 | 1.0164 | +2 % |
| reads | 16 reads | 1.3060 | 1.3205 | +1 % |
| reads | 24 reads | 1.9412 | 1.9287 | -1 % |
| size | 1/4 (1920 x 1080) | 0.3846 | 0.3967 | +3 % |
| size | 1/16 (960 x 540) | 0.3285 | 0.3373 | +3 % |
| size | 1/64 (480 x 270) | 0.1590 | 0.1578 | -1 % |
| size | 1/256 (240 x 135) | 0.0399 | 0.0400 | +0 % |
| size | 1/1024 (120 x 67) | 0.0143 | 0.0143 | -0 % |
| chain | 1/64, 2 passes | 0.0153 | 0.0098 | -36 % |
| chain | 1/64, 8 passes | 0.0453 | 0.0394 | -13 % |
| chain | 1/64, 32 passes | 0.1629 | 0.1574 | -3 % |
| chain | 1/256, 2 passes | 0.0032 | 0.0037 | +14 % |
| chain | 1/256, 8 passes | 0.0151 | 0.0146 | -3 % |
| chain | 1/256, 32 passes | 0.0580 | 0.0585 | +1 % |
| quad | 4 reads + 12 exchanges | 0.7766 | 0.7774 | +0 % |
| quad | 16 reads | 1.3060 | 1.3205 | +1 % |
| blend | RGBA8 add blend | 0.6864 | 0.6872 | +0 % |
| blend | RGB10A2 add blend | 0.6285 | 0.6343 | +1 % |
| blend | RG11B10F add blend | 0.6298 | 0.6343 | +1 % |
| blend | RGBA16F add blend | 1.4131 | 1.4139 | +0 % |
| blend | RGBA32F add blend | 2.7837 | 2.7845 | +0 % |

## RTX 2060 (NVIDIA Turing (TU10x, TU117))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.1024 | 0.1483 | +45 % |
| write | RG8 write noise | 0.1094 | 0.1483 | +36 % |
| write | R16F write noise | 0.1099 | 0.1483 | +35 % |
| write | RGBA8 write noise | 0.1519 | 0.1648 | +9 % |
| write | RGB10A2 write noise | 0.1532 | 0.1648 | +8 % |
| write | RG11B10F write noise | 0.1521 | 0.1648 | +8 % |
| write | RG16F write noise | 0.1532 | 0.1648 | +8 % |
| write | R32F write noise | 0.1524 | 0.1648 | +8 % |
| write | RGBA16F write noise | 0.3039 | 0.3285 | +8 % |
| write | RGBA32F write noise | 0.6201 | 0.6558 | +6 % |
| copy | copy Sample RGBA8 | 0.3273 | 0.3285 | +0 % |
| half | half bilinear RGBA8 | 0.2052 | 0.2058 | +0 % |
| copy | copy Sample RGB10A2 | 0.3274 | 0.3285 | +0 % |
| half | half bilinear RGB10A2 | 0.1982 | 0.2058 | +4 % |
| copy | copy Sample RGBA16F | 0.6547 | 0.6558 | +0 % |
| half | half bilinear RGBA16F | 0.3963 | 0.4103 | +4 % |
| copy | copy Sample RGBA32F | 1.3155 | 1.3104 | -0 % |
| half | half bilinear RGBA32F | 0.7904 | 0.8194 | +4 % |
| reads | 1 read | 0.3275 | 0.3285 | +0 % |
| reads | 2 reads | 0.3278 | 0.3285 | +0 % |
| reads | 3 reads | 0.3325 | 0.3285 | -1 % |
| reads | 4 reads | 0.2567 | 0.3285 | +28 % |
| reads | 6 reads | 0.3617 | 0.3646 | +1 % |
| reads | 8 reads | 0.4325 | 0.4367 | +1 % |
| reads | 10 reads | 0.5151 | 0.5088 | -1 % |
| reads | 12 reads | 0.5767 | 0.5809 | +1 % |
| reads | 16 reads | 0.7213 | 0.7251 | +1 % |
| reads | 24 reads | 1.0134 | 1.0135 | +0 % |
| size | 1/4 (1920 x 1080) | 0.1980 | 0.2058 | +4 % |
| size | 1/16 (960 x 540) | 0.1709 | 0.1751 | +2 % |
| size | 1/64 (480 x 270) | 0.1587 | 0.1568 | -1 % |
| size | 1/256 (240 x 135) | 0.0396 | 0.0401 | +1 % |
| size | 1/1024 (120 x 67) | 0.0042 | 0.0108 | +158 % |
| chain | 1/64, 2 passes | 0.0048 | 0.0057 | +18 % |
| chain | 1/64, 8 passes | 0.0249 | 0.0227 | -9 % |
| chain | 1/64, 32 passes | 0.0899 | 0.0908 | +1 % |
| chain | 1/256, 2 passes | 0.0025 | 0.0032 | +28 % |
| chain | 1/256, 8 passes | 0.0093 | 0.0128 | +38 % |
| chain | 1/256, 32 passes | 0.0505 | 0.0512 | +1 % |
| quad | 4 reads + 12 exchanges | 0.4136 | 0.4148 | +0 % |
| quad | 16 reads | 0.7213 | 0.7251 | +1 % |
| blend | RGBA8 add blend | 0.3259 | 0.3285 | +1 % |
| blend | RGB10A2 add blend | 0.3313 | 0.3325 | +0 % |
| blend | RG11B10F add blend | 0.3252 | 0.3285 | +1 % |
| blend | RGBA16F add blend | 0.6501 | 0.6558 | +1 % |
| blend | RGBA32F add blend | 1.5364 | 1.5376 | +0 % |

## RTX 2060 0x1F15 (NVIDIA Turing (TU10x, TU117))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.1508 | 0.1899 | +26 % |
| write | RG8 write noise | 0.1357 | 0.1899 | +40 % |
| write | R16F write noise | 0.1398 | 0.1899 | +36 % |
| write | RGBA8 write noise | 0.1355 | 0.1899 | +40 % |
| write | RGB10A2 write noise | 0.1332 | 0.1899 | +43 % |
| write | RG11B10F write noise | 0.1383 | 0.1899 | +37 % |
| write | RG16F write noise | 0.1377 | 0.1899 | +38 % |
| write | R32F write noise | 0.1397 | 0.1899 | +36 % |
| write | RGBA16F write noise | 0.2594 | 0.2842 | +10 % |
| write | RGBA32F write noise | 0.5232 | 0.5672 | +8 % |
| copy | copy Sample RGBA8 | 0.2830 | 0.2842 | +0 % |
| half | half bilinear RGBA8 | 0.1703 | 0.1780 | +5 % |
| copy | copy Sample RGB10A2 | 0.2825 | 0.2842 | +1 % |
| half | half bilinear RGB10A2 | 0.1704 | 0.1780 | +4 % |
| copy | copy Sample RGBA16F | 0.5669 | 0.5672 | +0 % |
| half | half bilinear RGBA16F | 0.3397 | 0.3549 | +4 % |
| copy | copy Sample RGBA32F | 1.1386 | 1.1332 | -0 % |
| half | half bilinear RGBA32F | 0.6798 | 0.7087 | +4 % |
| reads | 1 read | 0.2826 | 0.2842 | +1 % |
| reads | 2 reads | 0.2835 | 0.2842 | +0 % |
| reads | 3 reads | 0.2873 | 0.3045 | +6 % |
| reads | 4 reads | 0.2924 | 0.3427 | +17 % |
| reads | 6 reads | 0.3878 | 0.4191 | +8 % |
| reads | 8 reads | 0.4905 | 0.4955 | +1 % |
| reads | 10 reads | 0.5816 | 0.5719 | -2 % |
| reads | 12 reads | 0.6280 | 0.6483 | +3 % |
| reads | 16 reads | 0.8172 | 0.8010 | -2 % |
| reads | 24 reads | 1.1002 | 1.1066 | +1 % |
| size | 1/4 (1920 x 1080) | 0.1699 | 0.1780 | +5 % |
| size | 1/16 (960 x 540) | 0.1476 | 0.1515 | +3 % |
| size | 1/64 (480 x 270) | 0.1354 | 0.1335 | -1 % |
| size | 1/256 (240 x 135) | 0.0338 | 0.0343 | +1 % |
| size | 1/1024 (120 x 67) | 0.0049 | 0.0094 | +91 % |
| chain | 1/64, 2 passes | 0.0049 | 0.0054 | +11 % |
| chain | 1/64, 8 passes | 0.0234 | 0.0218 | -7 % |
| chain | 1/64, 32 passes | 0.0866 | 0.0871 | +1 % |
| chain | 1/256, 2 passes | 0.0026 | 0.0031 | +19 % |
| chain | 1/256, 8 passes | 0.0095 | 0.0124 | +30 % |
| chain | 1/256, 32 passes | 0.0490 | 0.0495 | +1 % |
| quad | 4 reads + 12 exchanges | 0.4456 | 0.4468 | +0 % |
| quad | 16 reads | 0.8172 | 0.8010 | -2 % |
| blend | RGBA8 add blend | 0.2784 | 0.2842 | +2 % |
| blend | RGB10A2 add blend | 0.2818 | 0.2842 | +1 % |
| blend | RG11B10F add blend | 0.2819 | 0.2842 | +1 % |
| blend | RGBA16F add blend | 0.5629 | 0.5672 | +1 % |
| blend | RGBA32F add blend | 1.5635 | 1.5647 | +0 % |

## RTX 2080 (NVIDIA Turing (TU10x, TU117))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0783 | 0.0794 | +1 % |
| write | RG8 write noise | 0.0783 | 0.0794 | +1 % |
| write | R16F write noise | 0.0842 | 0.0853 | +1 % |
| write | RGBA8 write noise | 0.0856 | 0.0867 | +1 % |
| write | RGB10A2 write noise | 0.0918 | 0.0929 | +1 % |
| write | RG11B10F write noise | 0.0923 | 0.0934 | +1 % |
| write | RG16F write noise | 0.0903 | 0.0914 | +1 % |
| write | R32F write noise | 0.0915 | 0.0926 | +1 % |
| write | RGBA16F write noise | 0.1638 | 0.1678 | +2 % |
| write | RGBA32F write noise | 0.3279 | 0.3345 | +2 % |
| copy | copy Sample RGBA8 | 0.1667 | 0.1678 | +1 % |
| half | half bilinear RGBA8 | 0.1003 | 0.1052 | +5 % |
| copy | copy Sample RGB10A2 | 0.1670 | 0.1678 | +0 % |
| half | half bilinear RGB10A2 | 0.1003 | 0.1052 | +5 % |
| copy | copy Sample RGBA16F | 0.3332 | 0.3345 | +0 % |
| half | half bilinear RGBA16F | 0.1996 | 0.2094 | +5 % |
| copy | copy Sample RGBA32F | 0.6658 | 0.6679 | +0 % |
| half | half bilinear RGBA32F | 0.3996 | 0.4178 | +5 % |
| reads | 1 read | 0.1671 | 0.1678 | +0 % |
| reads | 2 reads | 0.1665 | 0.1678 | +1 % |
| reads | 3 reads | 0.1679 | 0.1678 | -0 % |
| reads | 4 reads | 0.1468 | 0.1744 | +19 % |
| reads | 6 reads | 0.2125 | 0.2238 | +5 % |
| reads | 8 reads | 0.2690 | 0.2732 | +2 % |
| reads | 10 reads | 0.3244 | 0.3226 | -1 % |
| reads | 12 reads | 0.3699 | 0.3720 | +1 % |
| reads | 16 reads | 0.4726 | 0.4708 | -0 % |
| reads | 24 reads | 0.6659 | 0.6685 | +0 % |
| size | 1/4 (1920 x 1080) | 0.1004 | 0.1052 | +5 % |
| size | 1/16 (960 x 540) | 0.0873 | 0.0896 | +3 % |
| size | 1/64 (480 x 270) | 0.0800 | 0.0765 | -4 % |
| size | 1/256 (240 x 135) | 0.0191 | 0.0199 | +4 % |
| size | 1/1024 (120 x 67) | 0.0009 | 0.0057 | +537 % |
| chain | 1/64, 2 passes | 0.0043 | 0.0046 | +8 % |
| chain | 1/64, 8 passes | 0.0186 | 0.0185 | -1 % |
| chain | 1/64, 32 passes | 0.0737 | 0.0740 | +0 % |
| chain | 1/256, 2 passes | 0.0025 | 0.0027 | +9 % |
| chain | 1/256, 8 passes | 0.0090 | 0.0109 | +21 % |
| chain | 1/256, 32 passes | 0.0435 | 0.0437 | +1 % |
| quad | 4 reads + 12 exchanges | 0.2669 | 0.2680 | +0 % |
| quad | 16 reads | 0.4726 | 0.4708 | -0 % |
| blend | RGBA8 add blend | 0.1651 | 0.1678 | +2 % |
| blend | RGB10A2 add blend | 0.1728 | 0.1739 | +1 % |
| blend | RG11B10F add blend | 0.1709 | 0.1720 | +1 % |
| blend | RGBA16F add blend | 0.3324 | 0.3345 | +1 % |
| blend | RGBA32F add blend | 1.2264 | 1.2275 | +0 % |

## RTX 3050 Laptop GPU (NVIDIA Ampere)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.1455 | 0.1591 | +9 % |
| write | RG8 write noise | 0.1501 | 0.1591 | +6 % |
| write | R16F write noise | 0.1551 | 0.1591 | +3 % |
| write | RGBA8 write noise | 0.1859 | 0.1869 | +1 % |
| write | RGB10A2 write noise | 0.1850 | 0.1860 | +1 % |
| write | RG11B10F write noise | 0.1834 | 0.1844 | +1 % |
| write | RG16F write noise | 0.1806 | 0.1834 | +2 % |
| write | R32F write noise | 0.1777 | 0.1834 | +3 % |
| write | RGBA16F write noise | 0.3571 | 0.3657 | +2 % |
| write | RGBA32F write noise | 0.7453 | 0.7463 | +0 % |
| copy | copy Sample RGBA8 | 0.3647 | 0.3657 | +0 % |
| half | half bilinear RGBA8 | 0.2264 | 0.2289 | +1 % |
| copy | copy Sample RGB10A2 | 0.3649 | 0.3657 | +0 % |
| half | half bilinear RGB10A2 | 0.2257 | 0.2289 | +1 % |
| copy | copy Sample RGBA16F | 0.7261 | 0.7304 | +1 % |
| half | half bilinear RGBA16F | 0.4481 | 0.4569 | +2 % |
| copy | copy Sample RGBA32F | 1.4572 | 1.4598 | +0 % |
| half | half bilinear RGBA32F | 0.9628 | 0.9128 | -5 % |
| reads | 1 read | 0.3670 | 0.3657 | -0 % |
| reads | 2 reads | 0.3810 | 0.3657 | -4 % |
| reads | 3 reads | 0.4034 | 0.3657 | -9 % |
| reads | 4 reads | 0.3644 | 0.4232 | +16 % |
| reads | 6 reads | 0.5428 | 0.5552 | +2 % |
| reads | 8 reads | 0.6893 | 0.6873 | -0 % |
| reads | 10 reads | 0.7850 | 0.8193 | +4 % |
| reads | 12 reads | 0.9800 | 0.9514 | -3 % |
| reads | 16 reads | 1.2224 | 1.2155 | -1 % |
| reads | 24 reads | 1.7355 | 1.7437 | +0 % |
| size | 1/4 (1920 x 1080) | 0.2248 | 0.2289 | +2 % |
| size | 1/16 (960 x 540) | 0.1916 | 0.1948 | +2 % |
| size | 1/64 (480 x 270) | 0.0929 | 0.0946 | +2 % |
| size | 1/256 (240 x 135) | 0.0249 | 0.0244 | -2 % |
| size | 1/1024 (120 x 67) | 0.0121 | 0.0121 | -0 % |
| chain | 1/64, 2 passes | 0.0087 | 0.0070 | -20 % |
| chain | 1/64, 8 passes | 0.0303 | 0.0278 | -8 % |
| chain | 1/64, 32 passes | 0.1131 | 0.1114 | -2 % |
| chain | 1/256, 2 passes | 0.0027 | 0.0032 | +20 % |
| chain | 1/256, 8 passes | 0.0104 | 0.0130 | +25 % |
| chain | 1/256, 32 passes | 0.0514 | 0.0519 | +1 % |
| quad | 4 reads + 12 exchanges | 0.6832 | 0.6842 | +0 % |
| quad | 16 reads | 1.2224 | 1.2155 | -1 % |
| blend | RGBA8 add blend | 0.3642 | 0.3657 | +0 % |
| blend | RGB10A2 add blend | 0.4030 | 0.4040 | +0 % |
| blend | RG11B10F add blend | 0.4033 | 0.4043 | +0 % |
| blend | RGBA16F add blend | 0.7872 | 0.7882 | +0 % |
| blend | RGBA32F add blend | 2.3878 | 2.3888 | +0 % |

## RTX 3070 Ti Laptop GPU (NVIDIA Ampere)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0767 | 0.0777 | +1 % |
| write | RG8 write noise | 0.0933 | 0.0943 | +1 % |
| write | R16F write noise | 0.1018 | 0.1028 | +1 % |
| write | RGBA8 write noise | 0.1017 | 0.1027 | +1 % |
| write | RGB10A2 write noise | 0.1062 | 0.1072 | +1 % |
| write | RG11B10F write noise | 0.1046 | 0.1056 | +1 % |
| write | RG16F write noise | 0.1012 | 0.1022 | +1 % |
| write | R32F write noise | 0.1073 | 0.1083 | +1 % |
| write | RGBA16F write noise | 0.1632 | 0.1662 | +2 % |
| write | RGBA32F write noise | 0.3228 | 0.3314 | +3 % |
| copy | copy Sample RGBA8 | 0.1652 | 0.1662 | +1 % |
| half | half bilinear RGBA8 | 0.1037 | 0.1043 | +1 % |
| copy | copy Sample RGB10A2 | 0.1658 | 0.1662 | +0 % |
| half | half bilinear RGB10A2 | 0.0998 | 0.1043 | +4 % |
| copy | copy Sample RGBA16F | 0.3342 | 0.3314 | -1 % |
| half | half bilinear RGBA16F | 0.1998 | 0.2075 | +4 % |
| copy | copy Sample RGBA32F | 0.6739 | 0.6618 | -2 % |
| half | half bilinear RGBA32F | 0.3997 | 0.4140 | +4 % |
| reads | 1 read | 0.1664 | 0.1662 | -0 % |
| reads | 2 reads | 0.1645 | 0.1662 | +1 % |
| reads | 3 reads | 0.1698 | 0.1662 | -2 % |
| reads | 4 reads | 0.1853 | 0.1847 | -0 % |
| reads | 6 reads | 0.2369 | 0.2593 | +9 % |
| reads | 8 reads | 0.3126 | 0.3339 | +7 % |
| reads | 10 reads | 0.3654 | 0.4085 | +12 % |
| reads | 12 reads | 0.4440 | 0.4831 | +9 % |
| reads | 16 reads | 0.8026 | 0.6323 | -21 % |
| reads | 24 reads | 0.8589 | 0.9308 | +8 % |
| size | 1/4 (1920 x 1080) | 0.0998 | 0.1043 | +4 % |
| size | 1/16 (960 x 540) | 0.0837 | 0.0888 | +6 % |
| size | 1/64 (480 x 270) | 0.0406 | 0.0372 | -8 % |
| size | 1/256 (240 x 135) | 0.0092 | 0.0101 | +9 % |
| size | 1/1024 (120 x 67) | 0.0009 | 0.0033 | +262 % |
| chain | 1/64, 2 passes | 0.0039 | 0.0043 | +10 % |
| chain | 1/64, 8 passes | 0.0172 | 0.0171 | -0 % |
| chain | 1/64, 32 passes | 0.0681 | 0.0685 | +1 % |
| chain | 1/256, 2 passes | 0.0023 | 0.0026 | +13 % |
| chain | 1/256, 8 passes | 0.0084 | 0.0104 | +23 % |
| chain | 1/256, 32 passes | 0.0412 | 0.0415 | +1 % |
| quad | 4 reads + 12 exchanges | 0.3171 | 0.3181 | +0 % |
| quad | 16 reads | 0.8026 | 0.6323 | -21 % |
| blend | RGBA8 add blend | 0.1681 | 0.1691 | +1 % |
| blend | RGB10A2 add blend | 0.1794 | 0.1804 | +1 % |
| blend | RG11B10F add blend | 0.1760 | 0.1770 | +1 % |
| blend | RGBA16F add blend | 0.3258 | 0.3314 | +2 % |
| blend | RGBA32F add blend | 0.8283 | 0.8293 | +0 % |

## RTX 3090 (NVIDIA Ampere)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.1865 | 0.1878 | +1 % |
| write | RG8 write noise | 0.3398 | 0.3411 | +0 % |
| write | R16F write noise | 0.9336 | 0.9349 | +0 % |
| write | RGBA8 write noise | 1.9524 | 1.9537 | +0 % |
| write | RGB10A2 write noise | 1.8301 | 1.8314 | +0 % |
| write | RG11B10F write noise | 1.8841 | 1.8854 | +0 % |
| write | RG16F write noise | 1.6740 | 1.6753 | +0 % |
| write | R32F write noise | 1.8011 | 1.8024 | +0 % |
| write | RGBA16F write noise | 3.4710 | 3.4723 | +0 % |
| write | RGBA32F write noise | 7.2532 | 7.2545 | +0 % |
| copy | copy Sample RGBA8 | 0.1595 | 1.9537 | +1125 % |
| half | half bilinear RGBA8 | 0.0955 | 0.4894 | +412 % |
| copy | copy Sample RGB10A2 | 0.1911 | 1.8314 | +858 % |
| half | half bilinear RGB10A2 | 0.0960 | 0.4588 | +378 % |
| copy | copy Sample RGBA16F | 0.4618 | 3.4723 | +652 % |
| half | half bilinear RGBA16F | 0.1936 | 0.8690 | +349 % |
| copy | copy Sample RGBA32F | 1.1343 | 7.2545 | +540 % |
| half | half bilinear RGBA32F | 0.3869 | 1.8146 | +369 % |
| blend | RGBA8 add blend | 1.2068 | 1.2081 | +0 % |
| blend | RGB10A2 add blend | 1.2349 | 1.2362 | +0 % |
| blend | RG11B10F add blend | 3.7716 | 3.7729 | +0 % |
| blend | RGBA16F add blend | 2.6115 | 2.6128 | +0 % |
| blend | RGBA32F add blend | 0.7485 | 0.7498 | +0 % |

## RTX 4090 (NVIDIA Ada)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0246 | 0.0259 | +5 % |
| write | RG8 write noise | 0.0223 | 0.0236 | +6 % |
| write | R16F write noise | 0.0259 | 0.0272 | +5 % |
| write | RGBA8 write noise | 0.0364 | 0.0377 | +4 % |
| write | RGB10A2 write noise | 0.0394 | 0.0407 | +3 % |
| write | RG11B10F write noise | 0.0378 | 0.0391 | +3 % |
| write | RG16F write noise | 0.0392 | 0.0405 | +3 % |
| write | R32F write noise | 0.0393 | 0.0406 | +3 % |
| write | RGBA16F write noise | 0.0873 | 0.0886 | +1 % |
| write | RGBA32F write noise | 0.1508 | 0.1521 | +1 % |
| copy | copy Sample RGBA8 | 0.0610 | 0.0623 | +2 % |
| half | half bilinear RGBA8 | 0.0092 | 0.0394 | +328 % |
| copy | copy Sample RGB10A2 | 0.0662 | 0.0623 | -6 % |
| half | half bilinear RGB10A2 | 0.0074 | 0.0394 | +433 % |
| copy | copy Sample RGBA16F | 0.1479 | 0.1233 | -17 % |
| half | half bilinear RGBA16F | 0.0748 | 0.0775 | +4 % |
| copy | copy Sample RGBA32F | 0.2923 | 0.2453 | -16 % |
| half | half bilinear RGBA32F | 0.1839 | 0.1538 | -16 % |
| blend | RGBA8 add blend | 0.0437 | 0.0623 | +43 % |
| blend | RGB10A2 add blend | 0.0456 | 0.0623 | +37 % |
| blend | RG11B10F add blend | 0.0514 | 0.0623 | +21 % |
| blend | RGBA16F add blend | 0.1447 | 0.1460 | +1 % |
| blend | RGBA32F add blend | 0.3830 | 0.3843 | +0 % |

## RTX 4090 Laptop GPU (NVIDIA Ada)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0389 | 0.0436 | +12 % |
| write | RG8 write noise | 0.0400 | 0.0436 | +9 % |
| write | R16F write noise | 0.0399 | 0.0436 | +9 % |
| write | RGBA8 write noise | 0.0590 | 0.0599 | +2 % |
| write | RGB10A2 write noise | 0.0594 | 0.0602 | +1 % |
| write | RG11B10F write noise | 0.0593 | 0.0601 | +1 % |
| write | RG16F write noise | 0.0595 | 0.0603 | +1 % |
| write | R32F write noise | 0.0591 | 0.0599 | +1 % |
| write | RGBA16F write noise | 0.1195 | 0.1203 | +1 % |
| write | RGBA32F write noise | 0.2412 | 0.2420 | +0 % |
| copy | copy Sample RGBA8 | 0.1183 | 0.1191 | +1 % |
| half | half bilinear RGBA8 | 0.0118 | 0.0747 | +533 % |
| copy | copy Sample RGB10A2 | 0.1187 | 0.1191 | +0 % |
| half | half bilinear RGB10A2 | 0.0118 | 0.0747 | +533 % |
| copy | copy Sample RGBA16F | 0.2660 | 0.2374 | -11 % |
| half | half bilinear RGBA16F | 0.1182 | 0.1487 | +26 % |
| copy | copy Sample RGBA32F | 0.5292 | 0.4740 | -10 % |
| half | half bilinear RGBA32F | 0.2999 | 0.2965 | -1 % |
| reads | 1 read | 0.1177 | 0.1191 | +1 % |
| reads | 2 reads | 0.1157 | 0.1191 | +3 % |
| reads | 3 reads | 0.1186 | 0.1191 | +0 % |
| reads | 4 reads | 0.0554 | 0.1191 | +115 % |
| reads | 6 reads | 0.1046 | 0.1191 | +14 % |
| reads | 8 reads | 0.1281 | 0.1332 | +4 % |
| reads | 10 reads | 0.1536 | 0.1555 | +1 % |
| reads | 12 reads | 0.1858 | 0.1779 | -4 % |
| reads | 16 reads | 0.2195 | 0.2227 | +1 % |
| reads | 24 reads | 0.3106 | 0.3122 | +1 % |
| size | 1/4 (1920 x 1080) | 0.0119 | 0.0747 | +528 % |
| size | 1/16 (960 x 540) | 0.0115 | 0.0636 | +453 % |
| size | 1/64 (480 x 270) | 0.0059 | 0.0165 | +180 % |
| size | 1/256 (240 x 135) | 0.0024 | 0.0047 | +96 % |
| size | 1/1024 (120 x 67) | 0.0007 | 0.0018 | +152 % |
| chain | 1/64, 2 passes | 0.0032 | 0.0031 | -3 % |
| chain | 1/64, 8 passes | 0.0118 | 0.0125 | +6 % |
| chain | 1/64, 32 passes | 0.0500 | 0.0499 | -0 % |
| chain | 1/256, 2 passes | 0.0020 | 0.0020 | -2 % |
| chain | 1/256, 8 passes | 0.0073 | 0.0078 | +7 % |
| chain | 1/256, 32 passes | 0.0314 | 0.0314 | -0 % |
| quad | 4 reads + 12 exchanges | 0.1252 | 0.1260 | +1 % |
| quad | 16 reads | 0.2195 | 0.2227 | +1 % |
| blend | RGBA8 add blend | 0.0669 | 0.1191 | +78 % |
| blend | RGB10A2 add blend | 0.0743 | 0.1191 | +60 % |
| blend | RG11B10F add blend | 0.0739 | 0.1191 | +61 % |
| blend | RGBA16F add blend | 0.2560 | 0.2568 | +0 % |
| blend | RGBA32F add blend | 0.5952 | 0.5960 | +0 % |

## RTX 5080 (NVIDIA Blackwell)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0255 | 0.0268 | +5 % |
| write | RG8 write noise | 0.0258 | 0.0271 | +5 % |
| write | R16F write noise | 0.0262 | 0.0275 | +5 % |
| write | RGBA8 write noise | 0.0398 | 0.0411 | +3 % |
| write | RGB10A2 write noise | 0.0413 | 0.0426 | +3 % |
| write | RG11B10F write noise | 0.0418 | 0.0431 | +3 % |
| write | RG16F write noise | 0.0412 | 0.0425 | +3 % |
| write | R32F write noise | 0.0406 | 0.0419 | +3 % |
| write | RGBA16F write noise | 0.0827 | 0.0840 | +2 % |
| write | RGBA32F write noise | 0.1588 | 0.1601 | +1 % |
| copy | copy Sample RGBA8 | 0.0792 | 0.0805 | +2 % |
| half | half bilinear RGBA8 | 0.0070 | 0.0508 | +625 % |
| copy | copy Sample RGB10A2 | 0.0800 | 0.0805 | +1 % |
| half | half bilinear RGB10A2 | 0.0070 | 0.0508 | +625 % |
| copy | copy Sample RGBA16F | 0.1669 | 0.1597 | -4 % |
| half | half bilinear RGBA16F | 0.0912 | 0.1003 | +10 % |
| copy | copy Sample RGBA32F | 0.3309 | 0.3181 | -4 % |
| half | half bilinear RGBA32F | 0.1960 | 0.1993 | +2 % |
| blend | RGBA8 add blend | 0.0634 | 0.0805 | +27 % |
| blend | RGB10A2 add blend | 0.0882 | 0.0895 | +1 % |
| blend | RG11B10F add blend | 0.0701 | 0.0805 | +15 % |
| blend | RGBA16F add blend | 0.1720 | 0.1733 | +1 % |
| blend | RGBA32F add blend | 0.4146 | 0.4159 | +0 % |

## NVS 310 (NVIDIA)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 8.1372 | 8.1449 | +0 % |
| write | RG8 write noise | 8.1623 | 8.1700 | +0 % |
| write | R16F write noise | 8.1553 | 8.1630 | +0 % |
| write | RGBA8 write noise | 8.2775 | 8.2852 | +0 % |
| write | RGB10A2 write noise | 8.2932 | 8.3009 | +0 % |
| write | RG11B10F write noise | 8.2699 | 8.2776 | +0 % |
| write | RG16F write noise | 8.2323 | 8.2400 | +0 % |
| write | R32F write noise | 8.2259 | 8.2336 | +0 % |
| write | RGBA16F write noise | 8.6086 | 8.6163 | +0 % |
| write | RGBA32F write noise | 16.7312 | 16.7389 | +0 % |
| copy | copy Sample RGBA8 | 6.0059 | 8.2852 | +38 % |
| half | half bilinear RGBA8 | 3.4292 | 3.7614 | +10 % |
| copy | copy Sample RGB10A2 | 5.9979 | 8.3009 | +38 % |
| half | half bilinear RGB10A2 | 3.4494 | 3.7614 | +9 % |
| copy | copy Sample RGBA16F | 10.9442 | 12.0195 | +10 % |
| half | half bilinear RGBA16F | 6.7428 | 7.5150 | +11 % |
| reads | 1 read | 6.0098 | 8.2852 | +38 % |
| reads | 2 reads | 6.9847 | 8.2852 | +19 % |
| reads | 3 reads | 7.3726 | 8.2852 | +12 % |
| reads | 4 reads | 8.4342 | 8.9017 | +6 % |
| reads | 6 reads | 12.3866 | 13.2481 | +7 % |
| reads | 8 reads | 17.5147 | 17.5944 | +0 % |
| reads | 10 reads | 22.2496 | 21.9408 | -1 % |
| reads | 12 reads | 26.6534 | 26.2871 | -1 % |
| reads | 16 reads | 34.0014 | 34.9798 | +3 % |
| reads | 24 reads | 52.7099 | 52.3652 | -1 % |
| size | 1/4 (1920 x 1080) | 3.4745 | 3.7614 | +8 % |
| size | 1/16 (960 x 540) | 2.9005 | 3.1983 | +10 % |
| size | 1/64 (480 x 270) | 1.4357 | 1.4510 | +1 % |
| size | 1/256 (240 x 135) | 0.3721 | 0.3685 | -1 % |
| size | 1/1024 (120 x 67) | 0.2065 | 0.2065 | +0 % |
| chain | 1/64, 2 passes | 0.2089 | 0.2202 | +5 % |
| chain | 1/64, 8 passes | 0.8490 | 0.8808 | +4 % |
| chain | 1/64, 32 passes | 3.5119 | 3.5232 | +0 % |
| chain | 1/256, 2 passes | 0.0616 | 0.0666 | +8 % |
| chain | 1/256, 8 passes | 0.2614 | 0.2662 | +2 % |
| chain | 1/256, 32 passes | 1.0600 | 1.0650 | +0 % |
| quad | 4 reads + 12 exchanges | 30.2613 | 30.2690 | +0 % |
| quad | 16 reads | 34.0014 | 34.9798 | +3 % |
| blend | RGBA8 add blend | 9.6993 | 9.7070 | +0 % |
| blend | RGB10A2 add blend | 9.6241 | 9.6318 | +0 % |
| blend | RG11B10F add blend | 9.6264 | 9.6341 | +0 % |
| blend | RGBA16F add blend | 12.0974 | 12.1051 | +0 % |

## Quadro M5000M (NVIDIA Maxwell)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.3471 | 0.3484 | +0 % |
| write | RG8 write noise | 0.3717 | 0.3730 | +0 % |
| write | R16F write noise | 0.3717 | 0.3730 | +0 % |
| write | RGBA8 write noise | 0.3724 | 0.3737 | +0 % |
| write | RGB10A2 write noise | 0.3727 | 0.3740 | +0 % |
| write | RG11B10F write noise | 0.3729 | 0.3742 | +0 % |
| write | RG16F write noise | 0.3726 | 0.3739 | +0 % |
| write | R32F write noise | 0.3730 | 0.3743 | +0 % |
| write | RGBA16F write noise | 0.4676 | 0.4924 | +5 % |
| write | RGBA32F write noise | 0.9534 | 0.9835 | +3 % |
| copy | copy Sample RGBA8 | 0.4911 | 0.4924 | +0 % |
| half | half bilinear RGBA8 | 0.2942 | 0.3083 | +5 % |
| copy | copy Sample RGB10A2 | 0.4912 | 0.4924 | +0 % |
| half | half bilinear RGB10A2 | 0.2941 | 0.3083 | +5 % |
| copy | copy Sample RGBA16F | 0.9813 | 0.9835 | +0 % |
| half | half bilinear RGBA16F | 0.5880 | 0.6152 | +5 % |
| copy | copy Sample RGBA32F | 1.9632 | 1.9657 | +0 % |
| half | half bilinear RGBA32F | 1.1740 | 1.2291 | +5 % |
| reads | 1 read | 0.4916 | 0.4924 | +0 % |
| reads | 2 reads | 0.4938 | 0.4924 | -0 % |
| reads | 3 reads | 0.4976 | 0.4924 | -1 % |
| reads | 4 reads | 0.4098 | 0.4924 | +20 % |
| reads | 6 reads | 0.6188 | 0.5537 | -11 % |
| reads | 8 reads | 0.7391 | 0.7103 | -4 % |
| reads | 10 reads | 0.8617 | 0.8668 | +1 % |
| reads | 12 reads | 1.0196 | 1.0234 | +0 % |
| reads | 16 reads | 1.2852 | 1.3365 | +4 % |
| reads | 24 reads | 1.9874 | 1.9627 | -1 % |
| size | 1/4 (1920 x 1080) | 0.2945 | 0.3083 | +5 % |
| size | 1/16 (960 x 540) | 0.2445 | 0.2622 | +7 % |
| size | 1/64 (480 x 270) | 0.1155 | 0.1126 | -3 % |
| size | 1/256 (240 x 135) | 0.0285 | 0.0291 | +2 % |
| size | 1/1024 (120 x 67) | 0.0084 | 0.0084 | +0 % |
| chain | 1/64, 2 passes | 0.0082 | 0.0083 | +2 % |
| chain | 1/64, 8 passes | 0.0354 | 0.0333 | -6 % |
| chain | 1/64, 32 passes | 0.1331 | 0.1332 | +0 % |
| chain | 1/256, 2 passes | 0.0039 | 0.0041 | +4 % |
| chain | 1/256, 8 passes | 0.0147 | 0.0163 | +11 % |
| chain | 1/256, 32 passes | 0.0649 | 0.0651 | +0 % |
| quad | 4 reads + 12 exchanges | 0.8703 | 0.8716 | +0 % |
| quad | 16 reads | 1.2852 | 1.3365 | +4 % |
| blend | RGBA8 add blend | 0.4820 | 0.4924 | +2 % |
| blend | RGB10A2 add blend | 0.4841 | 0.4924 | +2 % |
| blend | RG11B10F add blend | 0.4861 | 0.4924 | +1 % |
| blend | RGBA16F add blend | 0.9729 | 0.9835 | +1 % |
| blend | RGBA32F add blend | 2.0101 | 2.0114 | +0 % |

## T600 (NVIDIA Turing (TU10x, TU117))

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.3334 | 0.3347 | +0 % |
| write | RG8 write noise | 0.3343 | 0.3356 | +0 % |
| write | R16F write noise | 0.3344 | 0.3357 | +0 % |
| write | RGBA8 write noise | 0.3599 | 0.3612 | +0 % |
| write | RGB10A2 write noise | 0.3600 | 0.3613 | +0 % |
| write | RG11B10F write noise | 0.3602 | 0.3615 | +0 % |
| write | RG16F write noise | 0.3598 | 0.3611 | +0 % |
| write | R32F write noise | 0.3603 | 0.3616 | +0 % |
| write | RGBA16F write noise | 0.3985 | 0.4334 | +9 % |
| write | RGBA32F write noise | 0.8930 | 0.8943 | +0 % |
| copy | copy Sample RGBA8 | 0.4321 | 0.4334 | +0 % |
| half | half bilinear RGBA8 | 0.2329 | 0.2713 | +17 % |
| copy | copy Sample RGB10A2 | 0.4287 | 0.4334 | +1 % |
| half | half bilinear RGB10A2 | 0.2327 | 0.2713 | +17 % |
| copy | copy Sample RGBA16F | 0.7858 | 0.8655 | +10 % |
| half | half bilinear RGBA16F | 0.4678 | 0.5414 | +16 % |
| copy | copy Sample RGBA32F | 1.5741 | 1.7297 | +10 % |
| half | half bilinear RGBA32F | 0.9321 | 1.0815 | +16 % |
| blend | RGBA8 add blend | 0.4166 | 0.4334 | +4 % |
| blend | RGB10A2 add blend | 0.4292 | 0.4334 | +1 % |
| blend | RG11B10F add blend | 0.4305 | 0.4334 | +1 % |
| blend | RGBA16F add blend | 0.7929 | 0.8655 | +9 % |
| blend | RGBA32F add blend | 2.4882 | 2.4895 | +0 % |

