# Single-pass pinwheel blurs fused into the composite (1080p model)

Largest sigma per fetch count that meets each profile. Taps: one per 90-degree
group (the other three are its rotations) and the centre (if any) last.

| fetches | profile | max sigma | marginal us | leak | tv | curv | taps (per group) |
|---:|---|---:|---:|---:|---:|---:|---|
| 5 | strict | 0.6 | 0 | 0.000 | 0.007 | 0.02 | (1.026, 0.200) w 0.1401; (0.000, 0.000) w 0.4395 |
| 5 | medium | 0.8 | 0 | 0.002 | 0.037 | 0.21 | (1.113, 0.302) w 0.1893; (0.000, 0.000) w 0.2429 |
| 5 | loose | 0.9 | 0 | 0.016 | 0.060 | 0.39 | (0.340, 1.180) w 0.2026; (0.000, 0.000) w 0.1895 |
| 8 | strict | 0.7 | 11 | 0.009 | 0.011 | 0.05 | (1.104, 0.378) w 0.0931; (0.370, 0.181) w 0.1569 |
| 8 | medium | 0.9 | 11 | 0.000 | 0.044 | 0.23 | (2.159, 0.415) w 0.0347; (0.458, 0.579) w 0.2153 |
| 8 | loose | 0.9 | 11 | 0.000 | 0.044 | 0.23 | (2.159, 0.415) w 0.0347; (0.458, 0.579) w 0.2153 |
| 9 | strict | 0.9 | 24 | 0.004 | 0.011 | 0.07 | (1.259, 1.903) w 0.0136; (1.136, 0.343) w 0.1878; (0.000, 0.000) w 0.1945 |
| 9 | medium | 1.0 | 24 | 0.007 | 0.034 | 0.15 | (0.358, 1.179) w 0.1821; (1.658, 1.267) w 0.0298; (0.000, 0.000) w 0.1526 |
| 9 | loose | 1.1 | 24 | 0.017 | 0.059 | 0.37 | (0.396, 1.165) w 0.1750; (2.270, 0.616) w 0.0427; (0.000, 0.000) w 0.1289 |
| 13 | strict | 0.9 | 77 | 0.004 | 0.011 | 0.07 | (0.050, 1.167) w 0.1052; (1.279, 1.259) w 0.0439; (0.875, 0.599) w 0.0550; (0.000, 0.000) w 0.1834 |
| 13 | medium | 1.3 | 77 | 0.011 | 0.046 | 0.27 | (2.212, 1.287) w 0.0420; (0.421, 2.191) w 0.0658; (0.831, -0.476) w 0.1318; (0.000, 0.000) w 0.0414 |
| 13 | loose | 1.4 | 77 | 0.017 | 0.071 | 0.48 | (0.432, 2.227) w 0.0725; (2.249, 1.318) w 0.0506; (0.972, 0.454) w 0.1102; (0.000, 0.000) w 0.0667 |

## LumaSharpen patterns as blurs (single pass in the composite, 0 us marginal)

| pattern | fetches | sigma | aniso | tv | curv | note |
|---|---:|---:|---:|---:|---:|---|
| Fast: +-(1/3, 1/3) | 2 | 0.58 | 0.41 | 0.084 | 0.35 | a 1D blur along one diagonal; 2 taps cannot be isotropic |
| Fast + centre 0.2 | 3 | 0.52 | 0.41 | 0.061 | 0.17 | |
| Normal: (+-0.5, +-0.5) | 4 | 0.71 | 0 | 0.109 | 0.56 | exactly the 3x3 binomial |
| Normal + centre 0.2 | 5 | 0.63 | 0 | 0.072 | 0.44 | passes loose |
| Normal, offset 0.34 | 4 | 0.60 | 0 | 0.038 | 0.15 | best 4-fetch fit to a Gaussian |

The optimiser's best 4-fetch pattern (no centre) is always the Normal diagonal
pattern; its offset (LumaSharpen's offset bias) sets sigma: 0.34 -> 0.60,
0.44 -> 0.70, 0.5 -> 0.71. Beyond sigma ~0.75 a centre tap (5+ fetches,
pinwheel) is needed. Note: below sigma 1 "Gaussian" is ambiguous (sampled vs
pixel-integrated), so tv is harsh on e.g. the binomial; leak, aniso and curv
remain meaningful.
