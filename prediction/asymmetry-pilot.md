# Mixing different payoff schedules across players

Completed 2026-09-10. This is a separate exploratory follow-up to the [core report](REPORT.md), not an addition to its training set or prospective scores.

A subsequent [few-shot versus learned comparison](asymmetry-predictors.md) trains on allowed subsets of this pilot and evaluates 64 fresh matches. The results below describe the initial zero-shot pilot.

**The original study did not include independently chosen payoff schedules. The new 64-match pilot does. Mixing payoffs produced stronger differences between player roles and some difficult switching games, but no clear increase in average prediction error.**

## What the original study allowed

The original [payoff implementation](games.py) constructs every game from four shared numbers:

| Player 0 / Player 1 | Action 0 | Action 1 |
|---|---|---|
| Action 0 | (R, R) | (S, T) |
| Action 1 | (T, S) | (P, P) |

Unequal off-diagonal outcomes and different model identities were allowed. Independently setting each player's four payoffs was not. The original renderer also relies on this symmetry to show both players the same self/other table. The separate pilot uses eight payoff entries and correctly transposes and reverses the payoff pair when presenting Player 1's perspective. Each move still has two choices; the expanded space is the space of incentives and resulting strategies.

## Design and completion

Four schedules were selected before play. In the following table, a schedule's four entries are indexed by **own action, other action**:

| Schedule | 00 | 01 | 10 | 11 |
|---|---:|---:|---:|---:|
| Prisoner's Dilemma (PD) | 3 | 0 | 5 | 1 |
| Harmony | 3 | 2 | 1 | 0 |
| Stag Hunt | 3 | 0 | 2 | 1 |
| Chicken | 3 | 1 | 5 | 0 |

Crossing the schedules gives **16 ordered payoff pairings: four symmetric controls and 12 asymmetric pairings**, or ten games up to swapping player roles. Each player's marginal schedule distribution is balanced across conditions. For instance, PD × Harmony gives `(3,3), (0,1), (5,2), (1,0)` in canonical 00, 01, 10, 11 order.

Each pairing received Qwen 3.8 27B versus GPT-OSS-20B in both seat orders and both A/B label orientations: **64/64 completed matches, 512 rounds, 1,024 player decisions**. The protocol retained eight simultaneous rounds, full public history, own-total-points objectives, temperature 0.7, low reasoning effort, a 4,096-token cap, and at most two attempts per response. Both players saw both players' payoffs; opponent model identities were withheld. No private-payoff or incomplete-information condition was tested.

Kimi K3 supplied 64 zero-shot forecasts of the four joint action frequencies, one per episode context. All forecasts were frozen at **19:34:03.444839 UTC**, before the first player call at **19:34:04.056052 UTC**. No predictor was trained on these outcomes. Two fixed comparators predict a uniform joint distribution or a highest-total-payoff pure stage Nash outcome; tied optimal pure equilibria share joint mass. If there is no pure equilibrium, the latter uses the unique interior mixed equilibrium. This is a restricted stage-game comparator, not a complete account of repeated-game behavior.

## Prediction results

Action Brier scores evaluate the probability of each player's canonical action 0 against individual decisions. Joint Brier scores sum squared probability errors across four joint outcomes. Lower is better. Every method uses all completed matches, with equal weight per ordered payoff pairing.

| Predictor | Symmetric action Brier | Asymmetric action Brier | Symmetric joint Brier | Asymmetric joint Brier |
|---|---:|---:|---:|---:|
| Kimi zero-shot | 0.1432 | 0.1342 | 0.4262 | 0.4254 |
| Stage-equilibrium selector | 0.0781 | 0.0961 | 0.2500 | 0.3275 |
| Uniform | 0.2500 | 0.2500 | 0.7500 | 0.7500 |

Kimi's asymmetric-minus-symmetric action Brier difference is **−0.0090**, with a descriptive 95% bootstrap interval **[−0.1389, +0.1093]**. The equilibrium comparator's difference is +0.0179 [−0.1133, +0.1296]. Neither establishes a direction. Kimi's joint error is almost unchanged, and the equilibrium comparator has lower point error than Kimi in both conditions.

To distinguish mistakes in average behavior from variation in individual actions, forecasts and outcomes were also pooled across the two label orientations within each game × player role × model cell. Kimi's average-rate MSE is **0.0695 symmetric versus 0.0444 asymmetric**; average-rate MAE is 0.2239 versus 0.1854. The MSE difference is −0.0252 [−0.1046, +0.0340]. These noisy cell averages also provide no evidence that the asymmetric condition is harder overall.

## Which mixes changed behavior?

![Prediction error and differences between player roles across the 4×4 payoff grid](results/asymmetry-20260910-openrouter/payoff-grid.png)

- **PD × Harmony produced completely consistent opposite actions.** The PD player chose canonical action 1 and the Harmony player chose action 0 in all 64 rounds across the eight matches covering both payoff role orientations. Kimi Brier was 0.026–0.052, and the equilibrium comparator's error was zero. Different incentives can make roles easier to predict.
- **Stag Hunt × Chicken created a matching-versus-mismatching conflict.** These games have no pure stage Nash outcome. Action switching occurred on 39.3–46.4% of adjacent-round player transitions; Kimi Brier was 0.265–0.290. The equilibrium comparator scored 0.259–0.269, also slightly worse than a 0.5 action forecast in these particular samples. Their difficulty is comparable to the symmetric Chicken control, where Kimi scored 0.280; it is not unique to asymmetry.
- **PD × Stag Hunt was also difficult for Kimi:** Brier 0.218–0.221, despite a unique pure equilibrium. The symmetric PD control scored 0.229. Absence of a pure equilibrium is therefore not the only source of forecast error.
- Across the grid, the average absolute difference between the two roles' action-0 rates grew from **6.25 to 47.66 percentage points**. Overall action switching rose from 9.38% to 14.29%. These are descriptive differences in this selected grid, not independently estimated causal effects or evidence of more complex internal reasoning.

## Limits and implication

This is a smoke test of feasibility and behavior, with four hand-chosen schedules, two player models, four matches per ordered pairing, and one zero-shot forecaster. The bootstrap resamples four symmetric schedule groups or six unordered asymmetric schedule-pair groups, retaining role reversals together. Groups reuse the same four schedules; with so few groups, the intervals are rough descriptive summaries of this grid, not reliable population-level uncertainty. No equivalence claim follows from intervals crossing zero.

The old learned predictors were not evaluated: their four-payoff features, symmetric equilibrium rules, and cooperation definitions do not encode this task. This pilot therefore does not establish whether asymmetry is harder for a trained predictor, or how accurately a model trained only on symmetric games transfers. Its scores also should not be compared directly with the core study's larger four-model cohort or few-shot results.

The useful next extension is to represent both players' payoff schedules, derive each role's incentives, and hold out entire payoff combinations while grouping role-swapped copies together. The present result supports that expansion as a way to obtain different roles and interaction patterns. It does not support assuming that asymmetry alone makes prediction harder.

## Audit, cost, and artifacts

All 64 forecasts and 64 matches completed. Eight offline tests cover independent payoffs, column-player perspective, label reversal, symmetric compatibility, equilibrium calculations, forecast validation, schedule balance, and recorded episode payoffs. The completed-run audits checked source hashes, forecast chronology, prompt and raw-call provenance, exact payouts, role/label coverage, and independently recomputed action Brier scores. There were 1,089 inference requests: 1,088 valid responses and one truncated response recovered by the bounded retry. **Reported charges were $1.1522**, with no outstanding reservations; Qwen used the existing hosted allocation.

The initial FLT Kimi route returned 404 errors. Its 128 failed forecast requests, original manifest, and source snapshot are preserved under `results/asymmetry-20260910/`; no matches started there. The completed pilot uses Kimi via OpenRouter for both conditions. Its separate $20 budget ceiling was an accounting cap, not the amount spent.

- [Frozen design and model configurations](results/asymmetry-20260910-openrouter/manifest.json)
- [Forecast freeze](results/asymmetry-20260910-openrouter/forecast-freeze.json)
- [Aggregate scores and descriptive intervals](results/asymmetry-20260910-openrouter/summary.json)
- [Per-game behavior and scores](results/asymmetry-20260910-openrouter/game-summary.json)
- [Independent audit](results/asymmetry-20260910-openrouter/AUDIT.json)
- [Runner](asymmetry_smoke.py), [readout and figure](asymmetry_readout.py), [offline tests](test_asymmetry_smoke.py), and [reproduction commands](README.md#asymmetric-payoff-pilot)
