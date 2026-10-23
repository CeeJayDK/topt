# TOPT_Blur class choice across GPU architectures

Regret = extra time over the cheapest candidate on that GPU, in % of its plain composite pass
(1080p and 4K). Current = the effect's choice (GTX 1660 model); robust = least mean regret over
the GPUs below. Profiles from TexBench reports (`python -m scripts.gpu_profiles`).

| sigma | current | robust | mean regret current -> robust | worst GPU regret current -> robust |
|---|---|---|---|---|
| 2–2 | 2 | 2 | 2.1 -> 2.1 % | 20 -> 20 % |
| 3–3 | 2 sep | 2 sep | 2.3 -> 2.3 % | 26 -> 26 % |
| 4–4 | 4s | 4s | 0.3 -> 0.3 % | 4 -> 4 % |
| 5–6 | 4s | 4s sep | 11.8 -> 0.6 % | 28 -> 7 % |
| 7–12 | 4 sep | 4 sep | 0.3 -> 0.3 % | 3 -> 3 % |
| 13–19 | 8 | 8 sep | 7.0 -> 0.6 % | 16 -> 5 % |
| 20–26 | 8 sep | 8 sep | 0.0 -> 0.0 % | 0 -> 0 % |
| 27–47 | 16 | 16 sep | 2.6 -> 0.7 % | 7 -> 8 % |
| 48–51 | 16 | 32 | 3.0 -> 0.3 % | 7 -> 5 % |
| 52–107 | 32 | 32 | 0.6 -> 0.6 % | 2 -> 2 % |
| 108–200 | 64 | 64 | 0.0 -> 0.0 % | 0 -> 0 % |

Worst regret of the current choice per GPU (1080p / 4K, % of a composite pass), and the sigma:

| GPU | architecture | worst 1080p | worst 4K | pass overhead |
|---|---|---|---|---|
| GTX 860M | NVIDIA Maxwell | 16 % (sigma 6) | 16 % (sigma 6) | 0.9 us |
| GTX 1080 | NVIDIA Pascal | 4 % (sigma 19) | 5 % (sigma 19) | 1.0 us |
| GTX 1660 | NVIDIA Turing | 6 % (sigma 6) | 7 % (sigma 6) | 1.1 us |
| RTX 2070 | NVIDIA Turing RTX | 17 % (sigma 6) | 19 % (sigma 6) | 1.0 us |
| RTX 3060 | NVIDIA Ampere | 16 % (sigma 6) | 17 % (sigma 6) | 1.0 us |
| RTX 4070 | NVIDIA Ada | 10 % (sigma 6) | 12 % (sigma 6) | 0.7 us |
| RTX 5070 | NVIDIA Blackwell | 23 % (sigma 6) | 28 % (sigma 6) | 0.7 us |
| RX 590 | AMD GCN 4 | 8 % (sigma 6) | 9 % (sigma 6) | 1.0 us |
| RX 5500 XT | AMD RDNA 1 | 19 % (sigma 6) | 20 % (sigma 6) | 1.0 us |
| RX 6600 | AMD RDNA 2 | 2 % (sigma 19) | 3 % (sigma 19) | 1.0 us |
| RX 7900 XTX | AMD RDNA 3 | 12 % (sigma 6) | 22 % (sigma 6) | 1.0 us |
| RX 9070 XT | AMD RDNA 4 | 11 % (sigma 6) | 18 % (sigma 6) | 1.0 us |
| Radeon 610M | AMD RDNA 2 iGPU | 10 % (sigma 3) | 9 % (sigma 3) | 5.8 us |
| UHD 630 | Intel Gen9.5 | 25 % (sigma 6) | 26 % (sigma 6) | 3.8 us |
| Iris Xe | Intel Gen12 | 26 % (sigma 3) | 26 % (sigma 3) | 3.1 us |
| Arc B580 | Intel Xe2 | 4 % (sigma 6) | 8 % (sigma 6) | 2.5 us |
