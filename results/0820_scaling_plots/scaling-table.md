# Env-count ladder — Tier A + Tier B, step 70, 1 seed

Constant compute: 70 steps x 8 groups x 6 = 48 episodes/step at every rung.


## games (TextArena + native)

| n | envs added | Held-out game cell | Kuhn Poker (held out) | TwoDollar (held out) | TwoDollar opening demand | MACHIAVELLI | Insider trading | AgentMisalignment | Hack-Verifiable (T1) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ta_ipd | 0.394 ±0.028 | 0.061 ±0.183 | 0.491 ±0.045 | 1.707 ±0.116 | 109.258 ±3.327 | 0.225 ±0.066 | 0.676 ±0.045 | — |
| 2 | nat_shoal | 0.200 ±0.128 | -0.799 ±0.184 | 0.042 ±0.028 | 1.748 ±0.211 | 103.818 ±2.942 | 0.175 ±0.060 | 0.380 ±0.047 | — |
| 4 | ta_pubgoods, nat_convoy | 0.508 ±0.070 | 0.047 ±0.174 | 0.468 ±0.040 | 1.388 ±0.144 | 103.914 ±2.863 | 0.050 ±0.034 | 0.315 ±0.045 | — |
| 8 | ta_ipd3, nat_assay, ta_staghunt, ta_winasmuch | 0.515 ±0.036 | 0.498 ±0.114 | 0.515 ±0.025 | 1.668 ±0.087 | 101.798 ±3.500 | 0.125 ±0.052 | 0.463 ±0.048 | — |
| base | (untrained) | 0.258 ±0.021 | -0.058 ±0.173 | 0.523 ±0.014 | 1.404 ±0.074 | 101.750 ±2.983 | 0.175 ±0.060 | 0.444 ±0.083 | — |

## synthetic scenarios

| n | envs added | Held-out game cell | Kuhn Poker (held out) | TwoDollar (held out) | TwoDollar opening demand | MACHIAVELLI | Insider trading | AgentMisalignment | Hack-Verifiable (T1) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | politics | 0.087 ±0.015 | -0.414 ±0.200 | 0.447 ±0.032 | 1.127 ±0.109 | 97.626 ±2.456 | 0.025 ±0.025 | 0.602 ±0.047 | — |
| 2 | reporting_metrics | 0.260 ±0.017 | 0.029 ±0.133 | 0.516 ±0.006 | 1.244 ±0.062 | — | 0.050 ±0.034 | — | — |
| 4 | gatekeeping, expense_processing | 0.291 ±0.020 | -0.000 ±0.179 | 0.522 ±0.013 | 1.340 ±0.063 | 108.944 ±11.231 | 0.075 ±0.042 | — | — |
| 8 | commerce, tax_prep, inventory_adjust, procurement_discount | 0.285 ±0.022 | 0.057 ±0.177 | 0.533 ±0.013 | 1.385 ±0.056 | 91.525 ±8.554 | 0.025 ±0.025 | — | — |
| base | (untrained) | 0.258 ±0.021 | -0.058 ±0.173 | 0.523 ±0.014 | 1.404 ±0.074 | 101.750 ±2.983 | 0.175 ±0.060 | 0.444 ±0.083 | — |
