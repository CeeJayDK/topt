# Hybrid down/blur/up search (GTX 1660 model, 1920x1080, RGB10A2)

Profiles: **strict** leak<=0.02, tv<=0.05, aniso<=0.03, phase<=0.01, sigma_err<=0.02; **medium** leak<=0.02, tv<=0.05, aniso<=0.03, phase<=0.03, sigma_err<=0.02; **loose** leak<=0.03, tv<=0.08, aniso<=0.05, phase<=0.06, sigma_err<=0.03

## Cheapest design per profile

| sigma | profile | us | passes | leak | tv | phase | design | best baseline |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 16 | strict | 142 | 4 | 0.008 | 0.040 | 0.010 | down 4x2 e5 | direct 2s | up 8 e1 | none |
| 16 | medium | 142 | 4 | 0.009 | 0.049 | 0.017 | down 4x2 e3 | direct 2s | up 8 e1 | dual_filter 270 us |
| 16 | loose | 136 | 4 | 0.011 | 0.012 | 0.046 | down 4x4 e5 | direct 2s | up 16 e1 | dual_filter 270 us |

## Cost vs shift-variance Pareto front (candidates also meeting leak/tv/aniso of 'medium')

**sigma 16**: 136 us / phase 0.217 (down 4x4 e1 | direct 2s | up 16 e2), 136 us / phase 0.046 (down 4x4 e5 | direct 2s | up 16 e1), 141 us / phase 0.044 (down 4x4 e5 | sep 2s | up 16 e1), 142 us / phase 0.010 (down 4x2 e5 | direct 2s | up 8 e2)

