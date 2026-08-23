# Env-count ladder — shape verdicts

Rule: flat if |y(8)-y(1)| < 2x the combined SE; rising if it clears that AND the top leg is still climbing; saturating if it clears it but the 4->8 leg is not.

**One training seed.** Bars are episode-level. A `rising` verdict says this checkpoint's rate at n=8 is measurably above its rate at n=1 — not that #envs raises transfer in expectation. Seeds 2-3 are what would license the second claim.

A `!` marks a point whose invalid rate exceeds 25% (check_suite's BROKEN threshold). Its denominator is selected by whether the model emitted a parseable action, so it is shown but EXCLUDED from the verdict.

## games (TextArena + native)  (step 70)

| metric | n=1 | n=2 | n=4 | n=8 | base | d(8-1) | verdict | rho |
|---|---|---|---|---|---|---|---|---|
| Held-out game cell | 0.394 | 0.200! | 0.508! | 0.515 | 0.258 | +0.121 | **rising (excl. n=2,n=4)** | +1.00 |
| Kuhn Poker (held out) | 0.061 | -0.799! | 0.047 | 0.498 | -0.058 | +0.437 | **rising (excl. n=2)** | +0.50 |
| TwoDollar (held out) | 0.491 | 0.042 | 0.468 | 0.515 | 0.523 | +0.024 | **flat** | +0.40 |
| TwoDollar opening demand | 1.707 | 1.748 | 1.388 | 1.668 | 1.404 | -0.039 | **flat** | -0.60 |
| MACHIAVELLI | 109.258 | 103.818 | 103.914 | 101.798 | 101.750 | -7.460 | **flat** | -0.80 |
| Insider trading | 0.225 | 0.175 | 0.050 | 0.125 | 0.175 | -0.100 | **flat** | -0.80 |
| AgentMisalignment | 0.676 | 0.380 | 0.315 | 0.463 | 0.444 | -0.213 | **falling** | -0.40 |

### control: hole - nohole at the endpoints

| metric | gap @ n=1 | gap @ n=8 | widening |
|---|---|---|---|
| Held-out game cell | +0.269 | +0.491 | +0.222 |
| Kuhn Poker (held out) | +0.598 | +1.281 | +0.683 |
| TwoDollar (held out) | +0.339 | +0.003 | -0.336 |
| TwoDollar opening demand | +0.235 | +0.524 | +0.289 |
| MACHIAVELLI | +12.824 | +4.593 | -8.231 |
| Insider trading | +0.175 | +0.100 | -0.075 |
| AgentMisalignment | +0.315 | -0.176 | -0.491 |

## synthetic scenarios  (step 70)

| metric | n=1 | n=2 | n=4 | n=8 | base | d(8-1) | verdict | rho |
|---|---|---|---|---|---|---|---|---|
| Held-out game cell | 0.087 | 0.260 | 0.291 | 0.285 | 0.258 | +0.198 | **saturating** | +0.80 |
| Kuhn Poker (held out) | -0.414 | 0.029 | -0.000 | 0.057 | -0.058 | +0.471 | **flat** | +0.80 |
| TwoDollar (held out) | 0.447 | 0.516 | 0.522 | 0.533 | 0.523 | +0.086 | **saturating** | +1.00 |
| TwoDollar opening demand | 1.127 | 1.244 | 1.340 | 1.385 | 1.404 | +0.258 | **saturating** | +1.00 |
| MACHIAVELLI | 97.626 | — | 108.944 | 91.525 | 101.750 | -6.101 | **flat** | -0.50 |
| Insider trading | 0.025 | 0.050 | 0.075 | 0.025 | 0.175 | +0.000 | **flat** | +0.40 |
| AgentMisalignment | 0.602 | — | — | — | 0.444 | — | **insufficient** | — |

### control: hole - nohole at the endpoints

| metric | gap @ n=1 | gap @ n=8 | widening |
|---|---|---|---|
| Held-out game cell | -0.102 | +0.111 | +0.213 |
| Kuhn Poker (held out) | -0.388 | -0.096 | +0.292 |
| TwoDollar (held out) | +0.280 | +0.023 | -0.257 |
| TwoDollar opening demand | -0.045 | +0.069 | +0.113 |
| MACHIAVELLI | -2.556 | +4.506 | +7.062 |
| Insider trading | +0.025 | -0.050 | -0.075 |
| AgentMisalignment | +0.231 | — | — |

## pass-1 decision

3 panel(s) show a positive dose-response (rising or saturating):

- **synth**: Held-out game cell (+0.198, saturating); TwoDollar (held out) (+0.086, saturating); TwoDollar opening demand (+0.258, saturating)

The plan gates seeds 2-3 on pass 1 rising, so this qualifies. Before reporting any of it as an effect of #envs, note the one-seed caveat above, and check whether a `saturating` verdict is a real plateau or the metric hitting its CEILING — a rate at 0.97 cannot rise further whatever the cause.

