Frozen forecasts generalized to the 21 new games: numerical payoff predictors and few-shot Kimi forecasts substantially improved on the game-blind ordered-context baseline. Few-shot clearly improved on zero-shot, but its broad-target differences from combined logistic were uncertain. A family-rate baseline already matched learned mutual cooperation and coordination, and payoff-dominant equilibrium selection captured most of the broad Brier improvement. These results support useful prediction within familiar archetypes; they provide limited evidence that this requires model-specific or detailed strategic modeling.

The prospective cohort tests forecasts made before play on **21 new payoff shapes sampled from the same seven archetypes** used in training. It tests new-game prediction within familiar archetypes, separately from family holdout and the global parameter-region holdouts reported in [numerical-interpretation.md](numerical-interpretation.md). It is not a test of an eighth strategic family.

The independent [launch audit](results/overnight-20260910/independent-analysis/prospective-launch-audit.json) verified all 17 primary and 17 secondary frozen input/artifact hashes. The primary freeze was completed at **2026-09-10 08:20:37.770974 UTC**; the earliest observed actual completed trace started at **08:20:42.355208 UTC**, a lead of **4.584234 seconds**. Every individual numerical/LLM forecast creation time also preceded that trace. Secondary forecasts were frozen at **07:19:57.430168 UTC**. The completed [main scoring audit](results/overnight-20260910/prospective/evaluation/audit.json) independently verified all actual trace times and outcome identities, with no issues, and recovered the same earliest start. All four primary evaluations and all three secondary comparison scopes passed their prospective audits. Independent final checks verified all secondary scientific output hashes and preservation of the original 135 full, 102 pair-focused and 102 model-focused method/target score cells. The evidence consists of saved local timestamps and byte hashes, not external notarization.

The [manifest](results/overnight-20260910/prospective/manifest.json) preserves the primary player configurations and runtime sources: Claude Haiku 4.5, Kimi K3, Qwen 3.8 27B and GPT-OSS 20B; eight simultaneous rounds, temperature 0.7, complete public action/payoff history, a 4,096-token cap and at most two attempts per action. Players optimize their own cumulative points and do not receive the opponent's model identity. There are three new games per family, ten unordered pairs including self-play, and two trials with opposite display labels: **420 planned episodes / 840 focal rows**. All 21 canonical groups are disjoint from the 72 training groups.

The full numerical fit uses 1,918 training episodes. The excluded-pair fit removes all GPT-OSS/Kimi interactions in both roles, leaving **1,727 episodes**, then scores the **42 prospective episodes** of that pair. The excluded-model fit removes every interaction containing GPT-OSS in either role, leaving **1,151 episodes**, then scores the **168 prospective episodes** containing that model. These focused evaluations still include both focal perspectives, including the familiar model facing the held model. All three training snapshots retain 72 game groups, and primary/secondary filtered snapshots match exactly. The later prospective games are new to every fit. The prompted LLM baselines use full training, so they are not an independently excluded-model/pair comparator.

Kimi K3 generated **336 queries per mode**—21 games × 16 ordered focal/opponent contexts—for zero-shot, few-shot and numerical game-theory prompts. All **1,008 queries completed**, one with a retry, and were exported before play. Each query supplies probabilities for 11 defined measurements, retaining null where the game does not support a target. The core numerical evaluation specifies seven targets; any additional LLM-only conditional diagnostics must remain separate from comparisons with numerical methods. The [prompt audit](results/overnight-20260910/independent-analysis/prospective-prompt-audit.json) checked all query message hashes against the frozen forecast rows and confirmed that every few-shot query has three examples selected only from training. Those examples use 41 of the 72 training groups and none of the 21 query groups. Conditional forecasts predict success given an opportunity, not whether that opportunity will occur.

The original numerical methods, the three prompted modes, and the explicitly post-pilot secondary comparators were fixed before prospective play. The payoff-dominant and event-weighted context controls remain secondary because their design followed pilot inspection. Reporting a low-scoring method after seeing these outcomes will not convert it into a prespecified sole winner. The planned comparisons retain equal-game weighting, shared supported observations, episode clustering and fixed-forecast bootstrap uncertainty; model refitting, a population of new game families, and multiplicity uncertainty are not covered.

All **420/420 episodes completed**, with no reported collection-integrity errors. The [numerical-only scores](results/overnight-20260910/prospective/evaluation-numerical/scores.json) and [numerical-plus-LLM scores](results/overnight-20260910/prospective/evaluation/scores.json) use exactly the same core supported observations: all **102 numerical method/target score cells** retain identical row, game, episode and opportunity counts, Brier, log loss and ECE. Adding the prompted forecasts therefore does not improve the numerical results by dropping difficult rows. The [secondary full comparison](results/overnight-20260910/secondary-baselines/full/prospective-comparison/scores.json) adds the previously frozen secondary methods; its [supervisor audit](results/overnight-20260910/secondary-baselines/full/prospective-comparison/supervisor-audit.json) binds the input/source/output bytes and independently verifies chronology.

The following table reports event Brier, with lower values indicating better probability forecasts. All methods within a target share supported observations. “Combined” and “MLP” include both player IDs; “derived” uses normalized incentive/equilibrium/dominance/welfare features. These are fixed available methods, not a newly selected single winner.

| Method | Action 0: 21 games | Mutual cooperation: 14 games | Coordination: 12 games |
|---|---:|---:|---:|
| Ordered context | 0.2514 | 0.2144 | 0.1932 |
| Original Nash selector | 0.2267 | 0.2177 | 0.2132 |
| Family rate | 0.2585 | 0.0609 | 0.1388 |
| Raw-payoff logistic | 0.1557 | 0.2022 | 0.1586 |
| Derived logistic | 0.1375 | 0.0608 | 0.1399 |
| Combined logistic | 0.1383 | 0.0582 | 0.1395 |
| Combined MLP | 0.1321 | 0.0588 | 0.1400 |
| Kimi zero-shot | 0.1764 | 0.2025 | 0.2209 |
| Kimi few-shot | 0.1313 | 0.0618 | 0.1415 |
| Kimi game-theory prompt | 0.1786 | 0.2144 | 0.2164 |
| Secondary payoff-dominant | 0.1436 | 0.0662 | 0.1441 |
| Secondary event-aligned context | 0.2514 | 0.2144 | 0.1932 |

Combined logistic improves Brier over the ordered-context baseline by **0.1131 [0.0660, 0.1562]** for action, **0.1562 [0.1103, 0.2214]** for mutual cooperation and **0.0537 [0.0405, 0.0702]** for coordination. Few-shot gains are comparable: 0.1202 [0.0730, 0.1642], 0.1526 [0.1056, 0.2148] and 0.0517 [0.0342, 0.0726]. These contrasts establish ex-ante predictability beyond a baseline that ignores the game. They do not establish that the extra signal requires fine-grained strategic behavior models.

The stronger baselines narrow the interpretation. Family rate gives cooperation/coordination Brier **0.0609 / 0.1388**, versus combined logistic **0.0582 / 0.1395**. Paired combined improvements over family are only **0.0027 [−0.0002, 0.0067]** and **−0.0008 [−0.0035, 0.0017]**. Action needs information beyond the family label, but the generator randomly reverses the encoded actions while preserving the label: identifying which encoded action is dominant or cooperative is already payoff-dependent. Removing both model IDs barely changes action (0.1381 game-only versus 0.1383 with IDs); cooperation changes from 0.0608 to 0.0582 and coordination from 0.1400 to 0.1395. This is mainly evidence for shared payoff responses and broad family regularities, with limited evidence that model identities are necessary.

The [independent prompt contrasts](results/overnight-20260910/independent-analysis/prospective-prompt-comparisons.json) compare modes on the exact combined-evaluation supported rows, using the existing game/episode bootstrap. Positive entries below favor the first-named method. Intervals are descriptive 95% intervals, conditional on the frozen forecasts and unadjusted for the many comparisons.

| Brier improvement | Action 0 | Mutual cooperation | Coordination |
|---|---|---|---|
| Few-shot over zero-shot | **0.0452 [0.0141, 0.0868]** | **0.1407 [0.0764, 0.2116]** | **0.0794 [0.0452, 0.1197]** |
| Game-theory prompt over zero-shot | −0.0022 [−0.0197, 0.0213] | −0.0119 [−0.0481, 0.0258] | 0.0045 [−0.0297, 0.0383] |
| Few-shot over combined logistic | 0.0071 [−0.0073, 0.0240] | −0.0036 [−0.0141, 0.0060] | −0.0020 [−0.0097, 0.0056] |

Behavioral examples clearly help this forecaster on the broad targets. Supplying numerical game-theory features by itself does not show a clear improvement over zero-shot. Few-shot has a slightly better action point score than combined logistic and the MLP, but its paired comparison with combined logistic does not establish superiority. Zero-shot and the game-theory prompt have worse Brier and log loss than combined logistic on all three broad targets, with paired intervals excluding zero. The study evaluated one forecasting model, Kimi K3; these results do not generalize automatically to all LLM forecasters or prompting procedures.

Log loss and calibration explain part of the difference. The table reports log loss and ten-bin ECE separately; lower is better for each, but ECE alone does not measure discrimination.

| Method | Action log loss / ECE | Cooperation log loss / ECE | Coordination log loss / ECE |
|---|---:|---:|---:|
| Family rate | 0.7103 / 0.2037 | 0.2157 / 0.0090 | 0.4087 / 0.0248 |
| Combined logistic | 0.4185 / 0.0746 | 0.2070 / 0.0208 | 0.4111 / 0.0384 |
| Combined MLP | 0.4073 / 0.0358 | 0.2363 / 0.0151 | 0.4129 / 0.0403 |
| Kimi zero-shot | 0.5339 / 0.0604 | 0.6057 / 0.2754 | 0.7132 / 0.2330 |
| Kimi few-shot | 0.3909 / 0.0371 | 0.2217 / 0.0458 | 0.4228 / 0.0504 |
| Kimi game-theory prompt | 0.5353 / 0.0626 | 0.6438 / 0.3044 | 0.6822 / 0.2112 |
| Secondary payoff-dominant | 0.7449 / 0.0656 | 0.5504 / 0.0548 | 0.5390 / 0.0455 |

Zero-shot and game-theory prompts substantially **underpredict cooperation and coordination**. Their game-equal mean cooperation forecasts are 0.409 and 0.380 against an observed 0.684; their mean coordination forecasts are 0.504 and 0.525 against 0.736. Few-shot moves those forecasts to 0.667 and 0.750. The corresponding cooperation rate MAE falls from about 0.347–0.350 to 0.111; combined logistic is 0.091. Thus the few-shot benefit includes correcting probability levels, alongside improved discrimination. It is not evidence that simply adding formal incentive features teaches accurate behavior. Family rate itself is particularly well calibrated for cooperation (ECE 0.0090).

Payoff-dominant equilibrium selection remains a strong secondary comparator. Combined-logistic Brier improvements over it are **0.0053 [−0.0121, 0.0203]** for action, **0.0080 [0.0006, 0.0179]** for cooperation and **0.0046 [−0.0043, 0.0165]** for coordination. Few-shot's improvements are 0.0124 [−0.0013, 0.0272], 0.0044 [−0.0109, 0.0222] and 0.0026 [−0.0088, 0.0163]. Only combined cooperation's Brier interval excludes zero here, and its improvement over the empirical family baseline remains uncertain. Both combined logistic and few-shot improve log loss over the equilibrium rule on all three broad targets: combined gains **0.3265 [0.0450, 0.6608] / 0.3435 [0.1377, 0.5959] / 0.1280 [0.0330, 0.2583]**. The theory rule sometimes assigns 0/1 probabilities to outcomes with real exceptions, so a softer predictor can reduce log-loss exposure. No smoothed equilibrium comparator was specified; these gains do not isolate detailed learned strategy from generic probability smoothing. This prospective evidence is legitimate for the frozen secondary rule while retaining its post-pilot origin.

First-action prediction confirms that substantial signal exists before any interaction history. Brier is 0.1213 for few-shot, 0.1237 for combined logistic, 0.1261 for the MLP, 0.1433 for payoff-dominant equilibrium, 0.1562 for zero-shot and 0.1465 for the game-theory prompt. Few-shot improves over zero-shot by 0.0349 [0.0122, 0.0588], but its gain over combined logistic is 0.0024 [−0.0127, 0.0182]. The broad repeated-action results should therefore not be attributed automatically to adaptation within the eight-round episode.

The [excluded-pair evaluation](results/overnight-20260910/prospective/evaluation-pair/scores.json) and [excluded-model evaluation](results/overnight-20260910/prospective/evaluation-model/scores.json) use their separately filtered numerical fits and new prospective payoff shapes. Their [pair secondary comparison](results/overnight-20260910/secondary-baselines/excluded_pair/prospective-comparison/scores.json) and [model secondary comparison](results/overnight-20260910/secondary-baselines/excluded_model/prospective-comparison/scores.json) also passed independent supervisor audits. All game counts are the same as in the main target-specific table, but fewer episodes contribute to each game.

| Focus / target | Episodes | Ordered context Brier | Family rate Brier | Combined logistic Brier | Payoff-dominant Brier |
|---|---:|---:|---:|---:|---:|
| Held GPT-OSS/Kimi pair: action | 42 | 0.2509 | 0.2614 | 0.1396 | 0.1485 |
| Held GPT-OSS/Kimi pair: cooperation | 28 | 0.2422 | 0.0768 | 0.0739 | 0.0709 |
| Held GPT-OSS/Kimi pair: coordination | 24 | 0.2092 | 0.1809 | 0.1791 | 0.1835 |
| Held GPT-OSS model: action | 168 | 0.2516 | 0.2594 | 0.1442 | 0.1485 |
| Held GPT-OSS model: cooperation | 112 | 0.2336 | 0.0791 | 0.0749 | 0.0734 |
| Held GPT-OSS model: coordination | 96 | 0.1986 | 0.1561 | 0.1536 | 0.1601 |

Combined logistic improves action/cooperation over the context baseline in both focus tests: pair gains 0.1113 [0.0657, 0.1581] / 0.1683 [0.0763, 0.2598], and model gains 0.1074 [0.0630, 0.1552] / 0.1587 [0.0836, 0.2555]. Coordination is uncertain for the pair, 0.0301 [−0.0168, 0.0722], and positive for the model, 0.0451 [0.0216, 0.0740]. However, **all six broad-target focused Brier intervals against payoff-dominant equilibrium include zero**. Learned log loss is lower in all six focused contrasts, again with the unsmoothed-theory limitation. Combined ECE for action/cooperation/coordination is 0.0715 / 0.0763 / 0.0510 in the pair test and 0.0737 / 0.0684 / 0.0354 in the model test. These findings support transfer of a shared payoff response to an excluded matchup/model among the tested roster, rather than demonstrating that a learned representation of a new agent is required.

Conditional targets require a separate reading. The full cohort supplies **960 retaliation opportunities in 11 games/107 episodes**, **86 forgiveness opportunities in eight games/63 episodes**, and **705 exploitation opportunities in six games/114 episodes**. The table keeps those opportunity-defined populations; it does not score the occurrence of opportunities themselves.

| Method | Retaliation Brier | Forgiveness Brier | Exploitation Brier |
|---|---:|---:|---:|
| Ordered context | 0.2457 | 0.2098 | 0.2262 |
| Event-aligned context | 0.2553 | 0.2158 | 0.2146 |
| Family rate | 0.2067 | 0.1780 | 0.2525 |
| Combined logistic | 0.1959 | 0.1698 | 0.2110 |
| Combined MLP | 0.2167 | 0.1532 | 0.2461 |
| Kimi zero-shot | 0.2321 | 0.2237 | 0.2756 |
| Kimi few-shot | 0.1999 | 0.2110 | 0.2308 |
| Kimi game-theory prompt | 0.1752 | 0.2242 | 0.2629 |

The game-theory prompt has a useful **retaliation-rate** result despite its poor broad-target performance. It improves over event-aligned context by **0.0800 [0.0286, 0.1278]** Brier and **0.1756 [0.0671, 0.2784]** log loss. This is a conditional defection rate after an opponent's defection; an always-defect policy can also score highly on the measured event. The result is not evidence of intentional punishment or a causal response. Combined logistic and few-shot have positive retaliation point improvements over that baseline, but their intervals include zero.

Forgiveness is too sparse for a strong general claim. Combined logistic improves over event-aligned context by 0.0460 [0.00007, 0.1034] Brier and 0.1146 [0.0016, 0.2494] log loss, but the lower bounds barely exceed zero among many inspected contrasts and only 86 opportunities. The MLP has the lowest listed Brier point score but worse ECE (0.1434 versus combined 0.0347). Few-shot's forgiveness improvement is only 0.0047 [−0.1915, 0.2000]. Pair-focused forgiveness has just **14 opportunities**, model-focused forgiveness 43; those are especially weak bases for claiming trait transfer. All rates describe observed transition patterns, not forgiving intentions.

For exploitation, the event-aligned context baseline scores **0.2146**, close to combined logistic's **0.2110**; the paired gain is **0.0036 [−0.0176, 0.0397]**, with log-loss gain 0.0073 [−0.0375, 0.0861]. The original context baseline scores 0.2262, illustrating why conditional weighting matters. There is no clear prospective residual improvement once objectives are aligned. Few-shot and game-theory conditional exploitation point scores are worse. These forecasts concern a specified payoff-extraction opportunity, not evidence of deception, coercion or an agent's motives.

Support and uncertainty bound the conclusion. Action has 840 focal rows / 6,720 round opportunities; first action has 840 opportunities. Mutual cooperation has 560 focal rows / 4,480 opportunities across **14** games: besides the six equal-diagonal coordination/anti-coordination games, one chicken game lacks a cooperative action under the fixed welfare definition (its best diagonal welfare is 6.66, below the off-diagonal sum 6.73). This is structural inapplicability, not a missing rollout. Coordination has 480 focal rows / 3,840 opportunities across 12 games. The two focal perspectives of a shared episode are clustered; duplicated event counts are not independent trajectories. All intervals use 500 game-then-episode bootstrap resamples of fixed forecasts, with no refitting or multiplicity adjustment. They do not establish transfer to a population of unseen strategic families, different model rosters or provider versions. Additional LLM-only diagnostic targets are available in the saved scores and remain outside the seven-target numerical comparison. Any subsequent payoff/representation controls should be reported as their own sensitivity analysis.
