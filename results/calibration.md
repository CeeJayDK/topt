# Cost model vs TexBench

Model (topt/cost.py, profile from topt/gpu_profiles.json) against the TexBench report the profile
was made from, 3840 x 2160, ms. err = model / measured - 1.

| GPU | report | tests | median abs err | worst |
|---|---|---|---|---|
| GTX 860M | nvidia-gtx-860m-4.csv | 41 | 0 % | -7 % (6 reads) |
| GTX 1080 | nvidia-gtx-1080.csv | 18 | 2 % | +9 % (RGBA8 write noise) |
| GTX 1660 | nvidia-gtx-1660-21.csv | 41 | 1 % | +34 % (1/256, 8 passes) |
| RTX 2070 | nvidia-rtx-2070-3.csv | 41 | 7 % | +461 % (1/1024 (120 x 67)) |
| RTX 3060 | nvidia-rtx-3060.csv | 18 | 1 % | +2 % (half bilinear RGBA8) |
| RTX 4070 | nvidia-rtx-4070.csv | 41 | 3 % | +213 % (1/16 (960 x 540)) |
| RTX 5070 | nvidia-rtx-5070.csv | 41 | 5 % | +446 % (1/4 (1920 x 1080)) |
| RX 590 | amd-radeon-rx-590.csv | 18 | 2 % | +11 % (half bilinear RGBA16F) |
| RX 5500 XT | amd-radeon-rx-5500-xt.csv | 18 | 0 % | -7 % (half bilinear RGB10A2) |
| RX 6600 | amd-radeon-rx-6600.csv | 41 | 3 % | +176 % (1/16 (960 x 540)) |
| RX 7900 XTX | amd-radeon-rx-7900-xtx.csv | 18 | 3 % | +107 % (half bilinear RGBA8) |
| RX 9070 XT | amd-radeon-rx-9070-xt-4.csv | 18 | 2 % | +83 % (half bilinear RGBA8) |
| Radeon 680M | amd-radeon-0x1681.csv | 41 | 4 % | +210 % (R8 write noise) |
| UHD 630 | intel-uhd-630-25.csv | 41 | 1 % | +44 % (1/16 (960 x 540)) |
| Iris Xe | intel-iris-xe-3.csv | 41 | 4 % | +196 % (R8 write noise) |
| Arc B580 | intel-arc-b580-2.csv | 41 | 3 % | +50 % (1/256 (240 x 135)) |

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

## GTX 1080 (NVIDIA Pascal)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0733 | 0.0743 | +1 % |
| write | RG8 write noise | 0.0746 | 0.0756 | +1 % |
| write | R16F write noise | 0.0770 | 0.0780 | +1 % |
| write | RGBA8 write noise | 0.1078 | 0.1172 | +9 % |
| write | RGB10A2 write noise | 0.1088 | 0.1172 | +8 % |
| write | RG11B10F write noise | 0.1084 | 0.1172 | +8 % |
| write | RG16F write noise | 0.1079 | 0.1172 | +9 % |
| write | R32F write noise | 0.1078 | 0.1172 | +9 % |
| write | RGBA16F write noise | 0.2151 | 0.2334 | +9 % |
| write | RGBA32F write noise | 0.4345 | 0.4658 | +7 % |
| copy | copy Sample RGBA8 | 0.2324 | 0.2334 | +0 % |
| half | half bilinear RGBA8 | 0.1440 | 0.1463 | +2 % |
| copy | copy Sample RGB10A2 | 0.2328 | 0.2334 | +0 % |
| half | half bilinear RGB10A2 | 0.1439 | 0.1463 | +2 % |
| copy | copy Sample RGBA16F | 0.4632 | 0.4658 | +1 % |
| half | half bilinear RGBA16F | 0.2880 | 0.2915 | +1 % |
| copy | copy Sample RGBA32F | 0.9358 | 0.9306 | -1 % |
| half | half bilinear RGBA32F | 0.5752 | 0.5820 | +1 % |

## GTX 1660 (NVIDIA Turing)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.2817 | 0.2828 | +0 % |
| write | RG8 write noise | 0.2815 | 0.2826 | +0 % |
| write | R16F write noise | 0.2813 | 0.2824 | +0 % |
| write | RGBA8 write noise | 0.2954 | 0.2965 | +0 % |
| write | RGB10A2 write noise | 0.2953 | 0.2964 | +0 % |
| write | RG11B10F write noise | 0.2953 | 0.2964 | +0 % |
| write | RG16F write noise | 0.2954 | 0.2965 | +0 % |
| write | R32F write noise | 0.2962 | 0.2973 | +0 % |
| write | RGBA16F write noise | 0.4419 | 0.4430 | +0 % |
| write | RGBA32F write noise | 0.8606 | 0.8617 | +0 % |
| copy | copy Sample RGBA8 | 0.4278 | 0.4289 | +0 % |
| half | half bilinear RGBA8 | 0.2498 | 0.2685 | +7 % |
| copy | copy Sample RGB10A2 | 0.4243 | 0.4289 | +1 % |
| half | half bilinear RGB10A2 | 0.2527 | 0.2685 | +6 % |
| copy | copy Sample RGBA16F | 0.8656 | 0.8567 | -1 % |
| half | half bilinear RGBA16F | 0.5001 | 0.5358 | +7 % |
| copy | copy Sample RGBA32F | 1.6982 | 1.7123 | +1 % |
| half | half bilinear RGBA32F | 1.0001 | 1.0706 | +7 % |
| reads | 1 read | 0.4229 | 0.4289 | +1 % |
| reads | 2 reads | 0.4251 | 0.4289 | +1 % |
| reads | 3 reads | 0.4278 | 0.4289 | +0 % |
| reads | 4 reads | 0.3531 | 0.4309 | +22 % |
| reads | 6 reads | 0.4922 | 0.5289 | +7 % |
| reads | 8 reads | 0.6166 | 0.6270 | +2 % |
| reads | 10 reads | 0.7340 | 0.7251 | -1 % |
| reads | 12 reads | 0.8297 | 0.8231 | -1 % |
| reads | 16 reads | 1.0078 | 1.0192 | +1 % |
| reads | 24 reads | 1.4124 | 1.4115 | -0 % |
| size | 1/4 (1920 x 1080) | 0.2504 | 0.2685 | +7 % |
| size | 1/16 (960 x 540) | 0.2134 | 0.2283 | +7 % |
| size | 1/64 (480 x 270) | 0.1012 | 0.0996 | -2 % |
| size | 1/256 (240 x 135) | 0.0254 | 0.0257 | +1 % |
| size | 1/1024 (120 x 67) | 0.0114 | 0.0114 | +0 % |
| chain | 1/64, 2 passes | 0.0084 | 0.0068 | -19 % |
| chain | 1/64, 8 passes | 0.0305 | 0.0273 | -11 % |
| chain | 1/64, 32 passes | 0.1106 | 0.1090 | -1 % |
| chain | 1/256, 2 passes | 0.0026 | 0.0033 | +28 % |
| chain | 1/256, 8 passes | 0.0099 | 0.0133 | +34 % |
| chain | 1/256, 32 passes | 0.0524 | 0.0531 | +1 % |
| quad | 4 reads + 12 exchanges | 0.5348 | 0.5359 | +0 % |
| quad | 16 reads | 1.0078 | 1.0192 | +1 % |

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

## RTX 3060 (NVIDIA Ampere)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.1459 | 0.1469 | +1 % |
| write | RG8 write noise | 0.1314 | 0.1324 | +1 % |
| write | R16F write noise | 0.1301 | 0.1311 | +1 % |
| write | RGBA8 write noise | 0.1302 | 0.1312 | +1 % |
| write | RGB10A2 write noise | 0.1300 | 0.1310 | +1 % |
| write | RG11B10F write noise | 0.1300 | 0.1310 | +1 % |
| write | RG16F write noise | 0.1298 | 0.1308 | +1 % |
| write | R32F write noise | 0.1297 | 0.1307 | +1 % |
| write | RGBA16F write noise | 0.2020 | 0.2030 | +1 % |
| write | RGBA32F write noise | 0.4035 | 0.4045 | +0 % |
| copy | copy Sample RGBA8 | 0.1947 | 0.1957 | +1 % |
| half | half bilinear RGBA8 | 0.1209 | 0.1227 | +2 % |
| copy | copy Sample RGB10A2 | 0.1940 | 0.1957 | +1 % |
| half | half bilinear RGB10A2 | 0.1210 | 0.1227 | +1 % |
| copy | copy Sample RGBA16F | 0.3889 | 0.3904 | +0 % |
| half | half bilinear RGBA16F | 0.2420 | 0.2444 | +1 % |
| copy | copy Sample RGBA32F | 0.7815 | 0.7798 | -0 % |
| half | half bilinear RGBA32F | 0.4813 | 0.4878 | +1 % |

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

## RTX 5070 (NVIDIA Blackwell)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0384 | 0.0413 | +7 % |
| write | RG8 write noise | 0.0383 | 0.0413 | +8 % |
| write | R16F write noise | 0.0383 | 0.0413 | +8 % |
| write | RGBA8 write noise | 0.0485 | 0.0512 | +6 % |
| write | RGB10A2 write noise | 0.0482 | 0.0512 | +6 % |
| write | RG11B10F write noise | 0.0482 | 0.0512 | +6 % |
| write | RG16F write noise | 0.0483 | 0.0512 | +6 % |
| write | R32F write noise | 0.0482 | 0.0512 | +6 % |
| write | RGBA16F write noise | 0.0969 | 0.1018 | +5 % |
| write | RGBA32F write noise | 0.1938 | 0.2029 | +5 % |
| copy | copy Sample RGBA8 | 0.1011 | 0.1018 | +1 % |
| half | half bilinear RGBA8 | 0.0138 | 0.0639 | +363 % |
| copy | copy Sample RGB10A2 | 0.1013 | 0.1018 | +0 % |
| half | half bilinear RGB10A2 | 0.0156 | 0.0639 | +309 % |
| copy | copy Sample RGBA16F | 0.2022 | 0.2029 | +0 % |
| half | half bilinear RGBA16F | 0.1167 | 0.1271 | +9 % |
| copy | copy Sample RGBA32F | 0.4065 | 0.4051 | -0 % |
| half | half bilinear RGBA32F | 0.2395 | 0.2534 | +6 % |
| reads | 1 read | 0.1009 | 0.1018 | +1 % |
| reads | 2 reads | 0.1022 | 0.1018 | -0 % |
| reads | 3 reads | 0.1025 | 0.1018 | -1 % |
| reads | 4 reads | 0.0894 | 0.1048 | +17 % |
| reads | 6 reads | 0.1344 | 0.1366 | +2 % |
| reads | 8 reads | 0.1666 | 0.1683 | +1 % |
| reads | 10 reads | 0.1965 | 0.2001 | +2 % |
| reads | 12 reads | 0.2315 | 0.2318 | +0 % |
| reads | 16 reads | 0.3012 | 0.2954 | -2 % |
| reads | 24 reads | 0.4187 | 0.4224 | +1 % |
| size | 1/4 (1920 x 1080) | 0.0117 | 0.0639 | +446 % |
| size | 1/16 (960 x 540) | 0.0100 | 0.0544 | +444 % |
| size | 1/64 (480 x 270) | 0.0101 | 0.0141 | +40 % |
| size | 1/256 (240 x 135) | 0.0027 | 0.0040 | +50 % |
| size | 1/1024 (120 x 67) | 0.0008 | 0.0015 | +91 % |
| chain | 1/64, 2 passes | 0.0027 | 0.0027 | -1 % |
| chain | 1/64, 8 passes | 0.0101 | 0.0107 | +6 % |
| chain | 1/64, 32 passes | 0.0428 | 0.0428 | -0 % |
| chain | 1/256, 2 passes | 0.0017 | 0.0017 | +0 % |
| chain | 1/256, 8 passes | 0.0063 | 0.0068 | +8 % |
| chain | 1/256, 32 passes | 0.0273 | 0.0273 | +0 % |
| quad | 4 reads + 12 exchanges | 0.1505 | 0.1512 | +0 % |
| quad | 16 reads | 0.3012 | 0.2954 | -2 % |

## RX 590 (AMD GCN 4)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.1798 | 0.1808 | +1 % |
| write | RG8 write noise | 0.1786 | 0.1796 | +1 % |
| write | R16F write noise | 0.1810 | 0.1820 | +1 % |
| write | RGBA8 write noise | 0.1799 | 0.1809 | +1 % |
| write | RGB10A2 write noise | 0.1891 | 0.1901 | +1 % |
| write | RG11B10F write noise | 0.2012 | 0.2022 | +1 % |
| write | RG16F write noise | 0.2004 | 0.2014 | +1 % |
| write | R32F write noise | 0.1862 | 0.1872 | +1 % |
| write | RGBA16F write noise | 0.3027 | 0.3284 | +9 % |
| write | RGBA32F write noise | 0.6042 | 0.6558 | +9 % |
| copy | copy Sample RGBA8 | 0.3274 | 0.3284 | +0 % |
| half | half bilinear RGBA8 | 0.1892 | 0.2057 | +9 % |
| copy | copy Sample RGB10A2 | 0.3162 | 0.3284 | +4 % |
| half | half bilinear RGB10A2 | 0.1896 | 0.2057 | +8 % |
| copy | copy Sample RGBA16F | 0.6198 | 0.6558 | +6 % |
| half | half bilinear RGBA16F | 0.3693 | 0.4103 | +11 % |
| copy | copy Sample RGBA32F | 1.2358 | 1.3106 | +6 % |
| half | half bilinear RGBA32F | 0.7662 | 0.8195 | +7 % |

## RX 5500 XT (AMD RDNA 1)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.3121 | 0.3131 | +0 % |
| write | RG8 write noise | 0.2987 | 0.2997 | +0 % |
| write | R16F write noise | 0.2961 | 0.2971 | +0 % |
| write | RGBA8 write noise | 0.2970 | 0.2980 | +0 % |
| write | RGB10A2 write noise | 0.3122 | 0.3132 | +0 % |
| write | RG11B10F write noise | 0.3200 | 0.3210 | +0 % |
| write | RG16F write noise | 0.2967 | 0.2977 | +0 % |
| write | R32F write noise | 0.2971 | 0.2981 | +0 % |
| write | RGBA16F write noise | 0.3357 | 0.3367 | +0 % |
| write | RGBA32F write noise | 0.6525 | 0.6542 | +0 % |
| copy | copy Sample RGBA8 | 0.3266 | 0.3276 | +0 % |
| half | half bilinear RGBA8 | 0.2181 | 0.2052 | -6 % |
| copy | copy Sample RGB10A2 | 0.3265 | 0.3276 | +0 % |
| half | half bilinear RGB10A2 | 0.2205 | 0.2052 | -7 % |
| copy | copy Sample RGBA16F | 0.6623 | 0.6542 | -1 % |
| half | half bilinear RGBA16F | 0.4274 | 0.4093 | -4 % |
| copy | copy Sample RGBA32F | 1.3470 | 1.3074 | -3 % |
| half | half bilinear RGBA32F | 0.8108 | 0.8175 | +1 % |

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

## RX 7900 XTX (AMD RDNA 3)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0429 | 0.0439 | +2 % |
| write | RG8 write noise | 0.0328 | 0.0338 | +3 % |
| write | R16F write noise | 0.0313 | 0.0323 | +3 % |
| write | RGBA8 write noise | 0.0337 | 0.0347 | +3 % |
| write | RGB10A2 write noise | 0.0334 | 0.0344 | +3 % |
| write | RG11B10F write noise | 0.0327 | 0.0337 | +3 % |
| write | RG16F write noise | 0.0323 | 0.0333 | +3 % |
| write | R32F write noise | 0.0315 | 0.0325 | +3 % |
| write | RGBA16F write noise | 0.0797 | 0.0807 | +1 % |
| write | RGBA32F write noise | 0.1563 | 0.1573 | +1 % |
| copy | copy Sample RGBA8 | 0.0397 | 0.0407 | +3 % |
| half | half bilinear RGBA8 | 0.0125 | 0.0259 | +107 % |
| copy | copy Sample RGB10A2 | 0.0377 | 0.0407 | +8 % |
| half | half bilinear RGB10A2 | 0.0125 | 0.0259 | +107 % |
| copy | copy Sample RGBA16F | 0.1551 | 0.0807 | -48 % |
| half | half bilinear RGBA16F | 0.0256 | 0.0507 | +98 % |
| copy | copy Sample RGBA32F | 0.3125 | 0.1598 | -49 % |
| half | half bilinear RGBA32F | 0.2100 | 0.1003 | -52 % |

## RX 9070 XT (AMD RDNA 4)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0430 | 0.0440 | +2 % |
| write | RG8 write noise | 0.0416 | 0.0426 | +3 % |
| write | R16F write noise | 0.0417 | 0.0427 | +2 % |
| write | RGBA8 write noise | 0.0502 | 0.0512 | +2 % |
| write | RGB10A2 write noise | 0.0502 | 0.0512 | +2 % |
| write | RG11B10F write noise | 0.0501 | 0.0511 | +2 % |
| write | RG16F write noise | 0.0502 | 0.0512 | +2 % |
| write | R32F write noise | 0.0502 | 0.0512 | +2 % |
| write | RGBA16F write noise | 0.1026 | 0.1036 | +1 % |
| write | RGBA32F write noise | 0.2082 | 0.2092 | +1 % |
| copy | copy Sample RGBA8 | 0.0551 | 0.0561 | +2 % |
| half | half bilinear RGBA8 | 0.0194 | 0.0355 | +83 % |
| copy | copy Sample RGB10A2 | 0.0522 | 0.0561 | +8 % |
| half | half bilinear RGB10A2 | 0.0194 | 0.0355 | +83 % |
| copy | copy Sample RGBA16F | 0.1093 | 0.1112 | +2 % |
| half | half bilinear RGBA16F | 0.0385 | 0.0699 | +82 % |
| copy | copy Sample RGBA32F | 0.3464 | 0.2214 | -36 % |
| half | half bilinear RGBA32F | 0.1797 | 0.1388 | -23 % |

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

## UHD 630 (Intel Gen9.5)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 1.0749 | 1.0787 | +0 % |
| write | RG8 write noise | 1.0754 | 1.0792 | +0 % |
| write | R16F write noise | 1.0756 | 1.0794 | +0 % |
| write | RGBA8 write noise | 1.4044 | 1.4082 | +0 % |
| write | RGB10A2 write noise | 1.3713 | 1.3751 | +0 % |
| write | RG11B10F write noise | 1.4264 | 1.4302 | +0 % |
| write | RG16F write noise | 1.4031 | 1.4069 | +0 % |
| write | R32F write noise | 1.3244 | 1.3282 | +0 % |
| write | RGBA16F write noise | 2.7822 | 2.7860 | +0 % |
| write | RGBA32F write noise | 5.6026 | 5.6064 | +0 % |
| copy | copy Sample RGBA8 | 2.2680 | 2.2718 | +0 % |
| half | half bilinear RGBA8 | 1.2134 | 1.4213 | +17 % |
| copy | copy Sample RGB10A2 | 2.3095 | 2.2718 | -2 % |
| half | half bilinear RGB10A2 | 1.3426 | 1.4213 | +6 % |
| copy | copy Sample RGBA16F | 5.1813 | 4.5398 | -12 % |
| half | half bilinear RGBA16F | 2.3221 | 2.8388 | +22 % |
| copy | copy Sample RGBA32F | 10.4440 | 9.0758 | -13 % |
| half | half bilinear RGBA32F | 4.5334 | 5.6738 | +25 % |
| reads | 1 read | 2.4254 | 2.2718 | -6 % |
| reads | 2 reads | 2.2067 | 2.2718 | +3 % |
| reads | 3 reads | 2.3033 | 2.2718 | -1 % |
| reads | 4 reads | 2.4367 | 2.3641 | -3 % |
| reads | 6 reads | 3.7194 | 3.4769 | -7 % |
| reads | 8 reads | 4.5969 | 4.5896 | -0 % |
| reads | 10 reads | 5.7011 | 5.7024 | +0 % |
| reads | 12 reads | 6.8033 | 6.8151 | +0 % |
| reads | 16 reads | 9.0225 | 9.0406 | +0 % |
| reads | 24 reads | 13.4968 | 13.4917 | -0 % |
| size | 1/4 (1920 x 1080) | 1.1350 | 1.4213 | +25 % |
| size | 1/16 (960 x 540) | 0.8384 | 1.2086 | +44 % |
| size | 1/64 (480 x 270) | 0.7707 | 0.7926 | +3 % |
| size | 1/256 (240 x 135) | 0.2067 | 0.2010 | -3 % |
| size | 1/1024 (120 x 67) | 0.0883 | 0.0883 | -0 % |
| chain | 1/64, 2 passes | 0.0325 | 0.0369 | +13 % |
| chain | 1/64, 8 passes | 0.1355 | 0.1475 | +9 % |
| chain | 1/64, 32 passes | 0.5856 | 0.5900 | +1 % |
| chain | 1/256, 2 passes | 0.0133 | 0.0149 | +12 % |
| chain | 1/256, 8 passes | 0.0573 | 0.0594 | +4 % |
| chain | 1/256, 32 passes | 0.2362 | 0.2378 | +1 % |
| quad | 4 reads + 12 exchanges | 6.6743 | 6.6781 | +0 % |
| quad | 16 reads | 9.0225 | 9.0406 | +0 % |

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

## Arc B580 (Intel Xe2)

| section | test | measured | model | err |
|---|---|---:|---:|---:|
| write | R8 write noise | 0.0591 | 0.0616 | +4 % |
| write | RG8 write noise | 0.0682 | 0.0707 | +4 % |
| write | R16F write noise | 0.0709 | 0.0734 | +4 % |
| write | RGBA8 write noise | 0.0822 | 0.0890 | +8 % |
| write | RGB10A2 write noise | 0.0821 | 0.0890 | +8 % |
| write | RG11B10F write noise | 0.1742 | 0.1767 | +1 % |
| write | RG16F write noise | 0.0771 | 0.0890 | +15 % |
| write | R32F write noise | 0.0754 | 0.0890 | +18 % |
| write | RGBA16F write noise | 0.1654 | 0.1754 | +6 % |
| write | RGBA32F write noise | 0.3233 | 0.3483 | +8 % |
| copy | copy Sample RGBA8 | 0.1729 | 0.1754 | +1 % |
| half | half bilinear RGBA8 | 0.1074 | 0.1106 | +3 % |
| copy | copy Sample RGB10A2 | 0.1728 | 0.1754 | +2 % |
| half | half bilinear RGB10A2 | 0.1075 | 0.1106 | +3 % |
| copy | copy Sample RGBA16F | 0.3329 | 0.3483 | +5 % |
| half | half bilinear RGBA16F | 0.2069 | 0.2187 | +6 % |
| copy | copy Sample RGBA32F | 0.7009 | 0.6941 | -1 % |
| half | half bilinear RGBA32F | 0.4108 | 0.4348 | +6 % |
| reads | 1 read | 0.1773 | 0.1754 | -1 % |
| reads | 2 reads | 0.1824 | 0.1754 | -4 % |
| reads | 3 reads | 0.1796 | 0.1754 | -2 % |
| reads | 4 reads | 0.1906 | 0.1754 | -8 % |
| reads | 6 reads | 0.2376 | 0.2234 | -6 % |
| reads | 8 reads | 0.2873 | 0.2867 | -0 % |
| reads | 10 reads | 0.3491 | 0.3500 | +0 % |
| reads | 12 reads | 0.4066 | 0.4133 | +2 % |
| reads | 16 reads | 0.5342 | 0.5399 | +1 % |
| reads | 24 reads | 0.7929 | 0.7931 | +0 % |
| size | 1/4 (1920 x 1080) | 0.1076 | 0.1106 | +3 % |
| size | 1/16 (960 x 540) | 0.0855 | 0.0944 | +10 % |
| size | 1/64 (480 x 270) | 0.0783 | 0.0571 | -27 % |
| size | 1/256 (240 x 135) | 0.0108 | 0.0162 | +50 % |
| size | 1/1024 (120 x 67) | 0.0048 | 0.0059 | +23 % |
| chain | 1/64, 2 passes | 0.0084 | 0.0085 | +1 % |
| chain | 1/64, 8 passes | 0.0336 | 0.0341 | +1 % |
| chain | 1/64, 32 passes | 0.1362 | 0.1363 | +0 % |
| chain | 1/256, 2 passes | 0.0059 | 0.0059 | +1 % |
| chain | 1/256, 8 passes | 0.0237 | 0.0237 | +0 % |
| chain | 1/256, 32 passes | 0.0949 | 0.0949 | +0 % |
| quad | 4 reads + 12 exchanges | 1.0374 | 1.0399 | +0 % |
| quad | 16 reads | 0.5342 | 0.5399 | +1 % |

