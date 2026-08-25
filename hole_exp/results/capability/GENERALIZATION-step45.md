# Out-of-distribution transfer (step 45)

`exploit_rate` on cells no disposition arm trained on. The in-env numbers are not the finding; these are.

## audit twins (same games, invisible audit)

| arm | exploit (free) | exploit (priced) | gap | skill (priced) |
|---|---|---|---|---|
| base | 0.381 ±0.065 | 0.407 ±0.058 | -0.026 ±0.087 | -0.311 |
| adaptive_s0 | 0.475 ±0.057 | 0.475 ±0.054 | +0.000 ±0.079 | -0.289 |
| adaptrec_s0 | 0.623 ±0.054 | 0.553 ±0.050 | +0.069 ±0.074 | -0.353 |
| nohole_s0 | 0.292 ±0.047 | 0.260 ±0.047 | +0.032 ±0.066 | -0.177 |
| regmix_s0 | 0.669 ±0.054 | 0.596 ±0.054 | +0.073 ±0.076 | -0.456 |

## held-out games

Pooled over 0 of 2 cells. Excluded: `ta_kuhn` (at ceiling), `ta_negotiation` (unreliable) -- reported separately below, not averaged in.

| arm | exploit (free) | exploit (priced) | gap | skill (priced) |
|---|---|---|---|---|

### `ta_kuhn` (excluded from the pool)

| arm | exploit (free) | exploit (priced) | capture (priced) |
|---|---|---|---|
| base | 0.469 | 0.656 | +1.875 |
| adaptive_s0 | 0.627 | 0.490 | +1.608 |
| adaptrec_s0 | 0.385 | 0.604 | +2.604 |
| nohole_s0 | 0.668 | 0.750 | +2.149 |
| regmix_s0 | 0.460 | 0.458 | +1.382 |

### `ta_negotiation` (excluded from the pool)

| arm | exploit (free) | exploit (priced) | capture (priced) |
|---|---|---|---|
| base | 0.244 | 0.125 | +0.241 |
| adaptive_s0 | 0.456 | 0.219 | +0.260 |
| adaptrec_s0 | 0.281 | 0.292 | +0.393 |
| nohole_s0 | 0.248 | 0.227 | +0.479 |
| regmix_s0 | 0.073 | 0.260 | +0.297 |

## synthetic scenarios (Suite 2)

| arm | exploit (free) | exploit (priced) | gap | skill (priced) |
|---|---|---|---|---|
| base | 0.587 ±0.046 | 0.546 ±0.047 | +0.041 ±0.066 | -0.263 |
| adaptive_s0 | 0.550 ±0.046 | 0.619 ±0.044 | -0.069 ±0.063 | -0.348 |
| adaptrec_s0 | 0.602 ±0.042 | 0.571 ±0.044 | +0.031 ±0.061 | -0.416 |
| nohole_s0 | 0.575 ±0.044 | 0.486 ±0.046 | +0.089 ±0.063 | -0.183 |
| regmix_s0 | 0.610 ±0.044 | 0.601 ±0.044 | +0.009 ±0.062 | -0.333 |

## Reading it

The **audit twins** are the mechanism control. They are the same games the arms trained on, priced by an invisible audit rather than a counterpart who visibly changes -- so there is nothing in the observation to condition on. A policy that learned *where* to exploit carries over here; one that learned to read a counterpart cannot, and should look like base.

The **synthetic scenarios** are the real test. Different suite, different prompt, different action grammar, not a game. Movement there is a disposition; movement only on the twins is a map.

`skill` is printed beside every pool because a rise in exploitation that comes with a fall in competence is the collapse the all-hole arm showed, not a disposition.

