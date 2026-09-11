# Fixed-budget family breadth versus repetitions

Completed prospective check: **288 training episodes per arm**, **480 unique training episodes**, and **144 fresh test episodes across six unseen families**. Both arms use the same models, fixed learners and pooled 4/8/16-shot controls. All forecasts were frozen before test play.

Broader training improves win-error point estimates, but the six-family intervals include zero. It does not establish that breadth fixes learned transfer. The linear learner improves only 0.0080 Brier; learned correction improves 0.0460, while pooled four-shot improves 0.0491.

The best tested few-shot setting beats both learned methods on win prediction in each arm. However, the training-mean baseline beats all tested predictors on win Brier, and every win predictor is worse than the constant-0.5 arithmetic reference (0.2500). This is a calibration and transfer problem for prompting as well as learning.

For overnight work, use a small representation/calibration experiment with full-family validation inside the training pool. Preserve pooled 4/8/16-shot and constant/prior controls. There are only 68 distinct visible training inputs in the breadth arm. These results do not justify a large run of the current learner, nor prove that neural training cannot help.

| Training arm | Families | Episodes/family | Repetitions/condition |
|---|---:|---:|---:|
| Depth | 4 | 72 | 6 |
| Breadth | 12 | 24 | 2 |

The two arms share 96 anchor episodes. Each family has 12 exact conditions: model × seat × three seeds for two-player games; model × six seeds for single-player games. Training uses one native base configuration per family. Test conditions have two independent actor repetitions.

Held out entirely from training and demonstrations: **GOPS, Stag Hunt, Blackjack, Battleship, Othello and Sokoban**. Unseen means absent from this behavioral training dataset, not necessarily absent from foundation-model pretraining.

## Win prediction

Lower Brier is better. Families receive equal weight after averaging episodes within exact conditions.

| Predictor | Depth: 4 families | Breadth: 12 families | Breadth − depth |
|---|---:|---:|---:|
| training_mean | 0.2840 | 0.2654 | -0.0186 |
| linear | 0.3281 | 0.3201 | -0.0080 |
| few_4 | 0.3331 | 0.2840 | -0.0491 |
| corrected_4 | 0.3367 | 0.2907 | -0.0460 |
| few_8 | 0.3047 | 0.2872 | -0.0174 |
| few_16 | 0.2925 | 0.2668 | -0.0257 |

A constant prediction of 0.5 has Brier **0.2500** for binary labels. This arithmetic reference was added after readout; it is not a newly fitted or pre-registered forecast method.


## Paired comparisons

Negative differences favor the left method/arm. Intervals resample six test families and condition on the fitted forecasts; they do not capture uncertainty across alternative training-family selections.

| Comparison | Difference | Family-bootstrap 95% interval | Families favoring left |
|---|---:|---|---:|
| breadth linear − depth linear | -0.0080 | [-0.0713, +0.0782] | 5/6 |
| breadth corrected_4 − depth corrected_4 | -0.0460 | [-0.1121, +0.0024] | 4/6 |
| breadth few_4 − depth few_4 | -0.0491 | [-0.1516, +0.0312] | 3/6 |
| depth linear − depth few_4 | -0.0050 | [-0.1122, +0.0951] | 3/6 |
| depth corrected_4 − depth few_4 | +0.0035 | [-0.0237, +0.0297] | 2/6 |
| breadth linear − breadth few_4 | +0.0361 | [-0.0033, +0.0781] | 2/6 |
| breadth corrected_4 − breadth few_4 | +0.0067 | [-0.0145, +0.0281] | 3/6 |

## Other shared prediction targets

Any-invalid uses Brier error; normalized native terminal score uses MSE. Lower is better. These targets are scored separately from strict wins.

| Predictor | Depth invalid | Breadth invalid | Depth native score | Breadth native score |
|---|---:|---:|---:|---:|
| training_mean | 0.2153 | 0.1948 | 0.1828 | 0.1784 |
| linear | 0.2491 | 0.2395 | 0.1781 | 0.1858 |
| few_4 | 0.1733 | 0.1420 | 0.1943 | 0.1732 |
| corrected_4 | 0.2709 | 0.1515 | 0.1969 | 0.1779 |
| few_8 | 0.1871 | 0.1216 | 0.1880 | 0.1870 |
| few_16 | 0.1587 | 0.1463 | 0.1772 | 0.1633 |

## Per-family win prediction

| Test family | Depth linear | Breadth linear | Depth 4-shot | Breadth 4-shot | Depth correction | Breadth correction |
|---|---:|---:|---:|---:|---:|---:|
| Battleship | 0.3216 | 0.2556 | 0.2354 | 0.2426 | 0.2572 | 0.2676 |
| Blackjack | 0.3342 | 0.3085 | 0.2170 | 0.2825 | 0.2416 | 0.2707 |
| Game of Pure Strategy | 0.1390 | 0.3263 | 0.3332 | 0.2260 | 0.2860 | 0.2569 |
| Othello | 0.3591 | 0.2422 | 0.2230 | 0.2554 | 0.2675 | 0.2261 |
| Sokoban | 0.2895 | 0.2804 | 0.3113 | 0.2993 | 0.3295 | 0.2831 |
| Stag Hunt | 0.5252 | 0.5078 | 0.6789 | 0.3981 | 0.6382 | 0.4399 |

## Post-readout diagnosis

These descriptive checks were added after inspecting the completed results. They did not change collection, labels, fits or forecasts.

Stag Hunt produced **2 strict wins and 22 draws in 24 episodes**. Mean breadth-arm strict-win forecasts were .723 (linear), .599 (four-shot) and .530 (sixteen-shot), versus .083 observed. Native score correctly gives draws half credit; strict-win labels do not. Broad four-shot improves strongly on this family, but still overestimates wins. This is an observed forecast failure, not proof of its internal cause.

GOPS goes in the opposite direction: 23/24 episodes are wins, while mean breadth forecasts are .430 (linear) and .536 (four-shot). The linear learner improves on five other families, but its GOPS Brier worsens by .1872, offsetting much of those gains.

All **24/24 Sokoban first actions** are rejected for missing brackets. The native opening shows bracketed shorthand but lists available directions as bare words; the parser requires brackets. Every episode therefore has `any_invalid=1`. This signal mixes interface compliance with later planning errors. A separate controlled instruction ablation is warranted before treating invalidity gains as strategic transfer; existing native observations stay unchanged.

Breadth changes the global training win prior from .6042 to .5556, closer to the test rate .3889. The training-mean baseline improves by .0186, more than the linear learner’s .0080. Thus some overall improvement is explainable without richer game-specific prediction.

For the next study, test a clearer action-format reminder and distinguish strict wins, draws/native score and decision-level behavior. Tune representations and calibration only on training-family validation; reserve untouched families or fresh evaluation for prospective claims after this readout.

## Measurements and interpretation

Binary wins are strict two-player wins or full single-player solutions; Blackjack counts a completed five-hand match with more wins than losses. Native score is a separate continuous target, including Blackjack hand-win fraction and Sokoban goal completion. Family-specific action rates are diagnostic observations, not newly learned targets with no training support.

Some aggregates are mechanically uninformative: a player that spends all thirteen GOPS cards must have mean bid-card fraction 7/13, regardless of strategy. Early high-card use retains information about ordering; the aggregate bid fraction should not be read as a strategic preference.

This is a controlled label-budget comparison for two fixed, purposively chosen training sets. It changes both family composition and repetition count. Episode count does not equalize tokens, actions, cost, or the number of distinct actor-visible inputs. It does not establish a general causal effect of adding an arbitrary family.

Each query has complete actor opening messages, public parameters, normalized mechanics, and the scripted-opponent policy. Hidden opponent realizations and future events remain evaluator-only. The installed native engine is unchanged. A compact specification is not proof that the learner can use all represented information.

Sokoban’s native stored board string is stale after reset; the adapter uses the actual latest delivered board observation. Native room arrays are retained separately for exact replay and label audit. Battleship actor histories have an 80KB ceiling; predictor requests retain 40KB. Both arms use the same actor limits.

Only one configuration per family was collected here; this check tests family transfer, not parameter-response curves. Two test repetitions and six families still limit precision. No test-outcome tuning or neural encoder fine-tuning was performed.

## Reliability and model differences

| Test family | Qwen win | GLM win | Conditions with variable wins |
|---|---:|---:|---:|
| Battleship | 0.417 | 0.250 | 4/12 |
| Blackjack | 0.167 | 0.417 | 1/12 |
| Game of Pure Strategy | 1.000 | 0.917 | 1/12 |
| Othello | 0.250 | 0.167 | 3/12 |
| Sokoban | 0.667 | 0.250 | 3/12 |
| Stag Hunt | 0.167 | 0.000 | 2/12 |

All **7,008 native transitions** replayed. Independent checks: `{"battleship_shot_results": 1288, "blackjack_hand_and_reward_accounting": 24, "gops_card_removals": 624, "gops_prize_accounting": 312, "othello_disc_changes": 272, "othello_passes": 16, "sokoban_box_conservation": 323, "sokoban_terminal_fraction": 24, "stag_round_payoffs": 72}`.

All **4,281 inference attempts** link to raw requests/responses and reconciled ledgers. Reported total cost: **$17.6965**; unknown-cost calls: 0. Serialized learners reproduce 864 forecast values within 1e-12.

Forecast freeze: `2026-09-11T03:30:56.194676+00:00`. First test actor call: `2026-09-11T03:31:05.988667+00:00`.

A uniform actor-recovery amendment was specified at `2026-09-11T02:56:54.488060+00:00`, after one training checkpoint produced three blank answers and before any predictor request. It permits at most six total identical-context attempts for empty/truncated/transport responses, excludes explicit refusals, and preserves the original checkpoints and all calls. Additional recovery calls: **1**. No failed trial was replaced or labeled as a native loss.

Full per-family scores, native-score/invalidity forecasts, behavioral opportunity counts, repeated-label variation, input coverage and costs are in `summary.json`. The release includes train-only arm exports and archived sources.
