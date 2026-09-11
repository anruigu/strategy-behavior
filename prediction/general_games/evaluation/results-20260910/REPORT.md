# General games: five diagnostic checks

This diagnostic adds 48 parameter-sweep episodes to the balanced 96-episode coverage pilot. It evaluates parameter effects, model differences, native label reliability, four-shot prompting versus fixed learned baselines, and representation ablations. The full 1,360-episode catalog plan remains uncollected.

[Interactive viewer](http://localhost:42329/general#checks) · [Machine-readable results](summary.json) · [Frozen prediction protocol and exact prompts](manifest.json) · [Scored forecasts](predictions.json) · [Evaluation rows](records.evaluator.json)

- **Behavior versus parameters: Modest variation; preliminary.** PD cooperation is 54%, 54%, 46% across higher defection payoffs. Pig episodes lengthen. Blotto concentration is not monotonic. Only eight episodes per setting.
- **Model differences: Family-dependent, no clear overall winner.** Qwen wins/solves 28 of 48; GLM 25 of 48. Qwen is stronger in Connect Four here; GLM in Pig Dice. The paired overall interval spans zero.
- **Label reliability: Operational labels reproduce.** 144 episodes and 1,404 native transitions replay; 72 PD payoff rounds independently match. This validates native outcomes/actions, not intent or unmeasured traits.
- **Few-shot competitiveness: Yes for wins; mixed for behavior.** Four-shot win Brier is .146 versus linear .174 on new parameters, and .221 versus .299 on new families. Learned models do better on some behavior rates.
- **Representation sufficiency: Useful, but incomplete.** Full inputs improve win forecasts over structured inputs in both holdouts. Engine facts help held-out-family wins, but not parameter-holdout wins. Hidden state and future randomness remain unknown.

## Behavior versus parameters

Each setting has eight episodes: two models × two prompts × two seed/seat blocks. Means weight episodes equally. In contrast, the coverage viewer’s supported-rate chart pools decision opportunities; those estimands need not agree. The three selected axes are a small targeted sweep, not a random sample of parameter effects.

| Family / parameter | Value | Episodes | Mean behavior | Win / solved | Mean focal actions |
|---|---:|---:|---:|---:|---:|
| Prisoner’s Dilemma / defect_reward | 4 | 8 | 0.542 | 8/8 | 6.00 |
| Prisoner’s Dilemma / defect_reward | 5 | 8 | 0.542 | 8/8 | 6.00 |
| Prisoner’s Dilemma / defect_reward | 7 | 8 | 0.458 | 8/8 | 6.00 |
| Pig Dice / winning_score | 15 | 8 | 0.700 | 5/8 | 6.88 |
| Pig Dice / winning_score | 20 | 8 | 0.696 | 5/8 | 9.00 |
| Pig Dice / winning_score | 35 | 8 | 0.734 | 3/8 | 13.25 |
| Colonel Blotto / num_total_units | 9 | 8 | 0.431 | 1/8 | 2.75 |
| Colonel Blotto / num_total_units | 12 | 8 | 0.490 | 1/8 | 2.75 |
| Colonel Blotto / num_total_units | 20 | 8 | 0.476 | 2/8 | 2.88 |

Behaviors are PD cooperation, Pig rolling with unbanked points, and Blotto largest-field allocation share. PD cooperation drops from .542 at defection rewards 4 and 5 to .458 at 7. Pig episodes grow as the target rises (6.88, 9.00, 13.25 focal actions), while risk rates remain close (.700, .696, .734). Blotto concentration is not monotonic (.431, .490, .476). These observations support collecting response curves, but do not establish robust causal parameter effects.

Comparisons match model, prompt, seed and seat. However, seed and seat are coupled; only two seed/seat blocks are repeated across conditions, the base and new variants were collected in different batches, and LLM sampling seeds are unavailable. There is no independent repeated rollout of exactly the same complete condition.

## Model differences

Use only the original balanced 12-family pilot (48 episodes per model); the extra sweep does not overweight its three families. Strict wins include full single-player solutions, with ties counted separately from wins.

| Model | Wins / solutions | Episodes with invalid actions | Mean episode invalid-action rate |
|---|---:|---:|---:|
| qwen-3.8-27b | 28/48 | 4/48 | 0.031 |
| glm | 25/48 | 8/48 | 0.041 |

Win difference, Qwen minus GLM: +0.062; paired 95% family-bootstrap interval [-0.229, +0.354] (12 families, 48 paired episodes).

Invalid difference, Qwen minus GLM: -0.083; paired 95% family-bootstrap interval [-0.229, +0.062] (12 families, 48 paired episodes).

Family-specific behavior differs, but the overall intervals do not establish a consistent winner. Family resampling describes uncertainty across these sampled families, not all games; within-condition sampling noise remains unresolved.

## Label reliability

All 144 complete model episodes and 1,404 native transitions replay exactly against the frozen engine and raw model calls. An additional independent calculation matched all 72 PD rounds’ score changes from joint decisions and actual payoff parameters. Rewards, native invalid actions, raw response linkage, retry accounting and both budget ledgers reconcile.

These checks support reproducibility of operational labels. They do not validate intention, deception, exploitation, exploration or semantic rule adherence. Native acceptance can differ from the written rules: PD defaults to cooperation without a defect token, Hanoi can parse several moves in one response, and installed Kuhn betting does not add chips to the pot. Unsupported traits remain null. Native terminal completion may include losses or forfeits, and partial puzzle reward is not a solved task.

## Few-shot versus learned prediction

Two grouped holdouts were fixed before predictor calls: (1) higher parameter values in PD, Pig and Blotto, with lower/base values in training (120 train, 24 test); (2) three entire catalog test families—Kuhn Poker, Tower of Hanoi and Liar’s Dice (96 train, 24 test). No opening group crosses a train/test boundary. Player episodes already existed at preparation time, so this is a held-out evaluation, not a forecast timestamped before gameplay. Query labels and future states never enter predictor prompts or fitted features.

Kimi K3 uses zero or four retrieved training examples. Retrieval uses public structured metadata only, with the same four examples in all representation ablations. Numerical baselines use train-fitted structured features, optionally 384 TF–IDF features, and fixed logistic/Ridge or 16-unit MLP models. All scaling/vocabulary fitting is training-only; no hyperparameters or methods were selected on test results. The primary comparison is four-shot/full versus linear/full. These are small fixed baselines, not the mature learned predictor trained on the earlier matrix-game dataset.

Lower is better. Win and any-invalid use Brier scores; other targets use MSE of the observed episode rate. Scores macro-average families within a target. No undefined behavior rate is converted to zero.

### Parameter holdout

| Method | Win Brier | Any-invalid Brier | Cooperation MSE | Pig risk MSE | Blotto concentration MSE |
|---|---:|---:|---:|---:|---:|
| Training mean | 0.2485 | 0.0100 | 0.0608 | 0.0463 | 0.0022 |
| Linear · structured | 0.1742 | 0.0000 | 0.0296 | 0.0070 | 0.0172 |
| Linear · full | 0.1741 | 0.0000 | 0.0296 | 0.0069 | 0.0140 |
| MLP · structured | 0.2073 | 0.0000 | 0.0330 | 0.0120 | 0.0022 |
| MLP · full | 0.2175 | 0.0000 | 0.0330 | 0.0119 | 0.0022 |
| Kimi zero-shot · full | 0.2554 | 0.0021 | 0.0605 | 0.0586 | 0.0038 |
| Kimi four-shot · full | 0.1456 | 0.0007 | 0.0472 | 0.0113 | 0.0035 |
| Kimi four-shot · structured | 0.1851 | 0.0011 | 0.0360 | 0.0116 | 0.0032 |
| Kimi four-shot · engine facts | 0.1718 | 0.0007 | 0.0315 | 0.0136 | 0.0046 |

Primary paired win-Brier difference (four-shot minus linear): -0.0285, 95% family-bootstrap interval [-0.0621, +0.0188]. Only three test families contribute; this interval and ranking are preliminary.

### Family holdout

| Method | Win Brier | Any-invalid Brier | Cooperation MSE | Pig risk MSE | Blotto concentration MSE |
|---|---:|---:|---:|---:|---:|
| Training mean | 0.2413 | 0.1104 | — | — | — |
| Linear · structured | 0.2990 | 0.1175 | — | — | — |
| Linear · full | 0.2986 | 0.1175 | — | — | — |
| MLP · structured | 0.2733 | 0.1179 | — | — | — |
| MLP · full | 0.2509 | 0.1294 | — | — | — |
| Kimi zero-shot · full | 0.2324 | 0.1162 | — | — | — |
| Kimi four-shot · full | 0.2212 | 0.1082 | — | — | — |
| Kimi four-shot · structured | 0.2332 | 0.1151 | — | — | — |
| Kimi four-shot · engine facts | 0.2056 | 0.1023 | — | — | — |

Primary paired win-Brier difference (four-shot minus linear): -0.0774, 95% family-bootstrap interval [-0.1133, -0.0308]. Only three test families contribute; this interval and ranking are preliminary.

Four-shot/full beats both fitted full baselines on win Brier in both holdouts. It is competitive, but not uniformly better: linear/full has lower PD-cooperation and Pig-risk MSE, while the MLP and training mean have lower Blotto-concentration MSE. Extra engine facts produce the best win Brier among the tested methods on held-out families (.2056), but worsen parameter-holdout win Brier relative to four-shot/full (.1718 versus .1456).

All parameter-holdout episodes contain no native invalid actions, so the validity score there mainly rewards forecasts close to zero. It does not test sensitivity to invalid actions. Each family-specific behavior target has only eight test episodes from one family, so a family-level uncertainty interval is unavailable. See summary.json for every paired ablation and prediction coverage count.

## Does the representation contain enough information?

The structured condition includes game family, objective, action format, public parameters, model identity, seat and prompt label. Full adds exact initial actor-visible messages and an opponent-policy description. This joint ablation cannot separate the value of rules, own private opening information and opponent context. The engine-facts condition additionally supplies source-verified parser, payoff and numerical opponent details to the predictor only; the original players did not receive those extra facts. It never supplies hidden opponent values or future random draws.

The current concise representation is not a complete executable specification. In particular, installed Kuhn and auction accounting differs from common game conventions, and concise opponent descriptions omit some thresholds/probabilities. Exact native observations help establish what the player saw; versioned engine and opponent specifications are needed to establish what determines the outcome. Even an exact specification cannot reveal future stochastic actions or private states unavailable at forecast time. Ablation scores measure practical utility here, not a proof of informational sufficiency.

## Provenance, usage and reproduction

Prediction completion: 192/192 requested forecasts; missing forecasts remain missing. Fixed baselines produce 240 predictions across five methods and two suites. No training convergence warnings were recorded.

| Collection | Inference attempts | Reported cost | Unknown billing calls |
|---|---:|---:|---:|
| pilot-20260910 | 490 | $1.1363 | 0 |
| parameter-check-20260910 | 303 | $0.3922 | 0 |
| Kimi predictor comparisons | 193 | $3.4871 | 0 |

The original 96-episode distributions remain a balanced coverage cohort in the viewer; the separate validation panel shows all 144 study episodes and 48 held-out prediction queries. This general-games diagnostic does not establish relative prediction difficulty against Gameable Games, which uses different opponents, horizons and labels.

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.evaluation.checks fit
/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.evaluation.readout
/shared/allie/venvs/hole/bin/python -B -m pytest prediction/general_games/evaluation/test_checks.py -q
```

The existing frozen manifest and raw calls preserve the original 192 requests. `checks collect` resumes that manifest and skips completed forecasts; do not run `prepare` over the existing output. Player collection source and native engine archives live in the dataset release. Learned models, numeric predictions, full prompts, evaluator rows, all raw responses and budget ledgers live beside this report.
