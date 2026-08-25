# recovery probe -- every policy measured in the SAME recoverable (`*_nr`) nohole cells

Rounds are bucketed by what has already happened in the episode: `fresh` = no exploit yet, `tempted` = exploited before but never caught, `burned` = exploited before AND caught. `recovery` = tempted - burned, which holds "this is an exploiting episode" fixed and varies only whether the environment's detection coin came up. Positive means the policy stops after being caught (a learned contingency); ~0 means detection is not a cue it conditions on, and any fall in the training curve was a level shift in propensity.

`recovery (strat)` further restricts the comparison to rounds with the SAME number of prior exploits, which is the part of the residual bias that observational rollouts can remove.

| policy (train arm) | seeds | exploit | fresh | tempted | burned | recovery | recovery (strat) | detected eps | capture |
|---|---|---|---|---|---|---|---|---|---|
| base | 1 | 0.377 | 0.169 | 0.626 | 0.850 | -0.224 | -0.115 | 0.354 | 0.349 |
| natural_hole | 3 | 0.951 ±0.004 | 0.914 ±0.012 | 0.951 ±0.003 | 0.968 ±0.002 | -0.017 ±0.005 | 0.000 ±0.003 | 0.910 ±0.005 | 0.932 ±0.002 |
| natural_nohole | 3 | 0.111 ±0.014 | 0.042 ±0.004 | 0.582 ±0.068 | 0.660 ±0.092 | -0.078 ±0.092 | 0.001 ±0.118 | 0.125 ±0.026 | 0.102 ±0.019 |
| natural_norem_nohole | 3 | 0.240 ±0.091 | 0.104 ±0.044 | 0.547 ±0.085 | 0.789 ±0.057 | -0.241 ±0.141 | -0.144 ±0.127 | 0.253 ±0.106 | 0.205 ±0.090 |

## exploit rate by round (mean over seeds)

| policy | r1 | r2 | r3 | r4 | r5 |
|---|---|---|---|---|---|
| base | 0.40 | 0.35 | 0.35 | 0.39 | 0.40 |
| natural_hole | 0.93 | 0.98 | 0.93 | 0.97 | 0.94 |
| natural_nohole | 0.11 | 0.10 | 0.12 | 0.10 | 0.12 |
| natural_norem_nohole | 0.24 | 0.24 | 0.23 | 0.26 | 0.24 |
