# Predicting behavior in repeated matrix games

Updated 2026-09-10T09:32:19.888806+00:00. **Study status: Core Gate 1–7 pilot complete.**

The study tests payoff-only predictions made before an eight-round, simultaneous symmetric 2×2 interaction. Players maximize their own total points, see complete public history, and receive neutral A/B labels. The predictor can know the focal and opponent model identities. All rates are computed from actions; no LLM judges are used.

**Payoff-asymmetry follow-ups added 2026-09-10:** The core study did not give players independently chosen payoff schedules. The [payoff-mixing pilot below](#asymmetric-payoff-follow-up) tests this extension, followed by a [few-shot versus learned comparison on 64 fresh matches](#few-shot-versus-learned-predictors-fresh-matches). These results are separate from the core study's counts, fitted predictors, and gate decisions.

**Latest general-game result, 2026-09-11:** the [fixed-budget breadth check below](#fixed-budget-family-breadth-check-2026-09-11) is complete: **624 fresh episodes**, comparing four versus twelve training families on six new holdouts. Broader coverage improves win-error point estimates, but does not establish a learned-predictor advantage. Both prompting and learning need better calibration; training-only exports are ready for a small follow-up experiment.

**General-game coverage follow-up, 2026-09-10:** A separate native TextArena dataset now covers **12 game families and 49 parameter configurations**, with **144 complete model episodes** collected on 18 configurations. The [interactive viewer](http://localhost:42329/general) shows games, distributions and exact trajectories; its [validation panel](http://localhost:42329/general#checks) answers the five diagnostic questions. [Full analysis and frozen prediction artifacts](general_games/evaluation/results-20260910/REPORT.md).

- **Parameters:** modest variation in a three-family sweep, with only eight episodes per setting. PD cooperation was .542, .542 and .458 as the defection payoff rose; Pig episodes lengthened; Blotto concentration was not monotonic.
- **Models:** Qwen won/solved 28/48 balanced coverage episodes, GLM 25/48. Differences depend on family; the overall paired interval includes zero.
- **Labels:** all 144 episodes / 1,404 native transitions replay; 72 PD payoff rounds independently match. This supports native outcome/action labels, not inferred intent or unsupported traits.
- **Few-shot:** four-shot/full win Brier was **.1456 vs linear/full .1741** on higher parameter values and **.2212 vs .2986** on three unseen families. It also beat the small MLP on win Brier; learned models won on some behavior-rate targets. Each holdout has only 24 test episodes. These fixed general-game baselines are newly fitted and separate from the matrix-game learned predictors.
- **Representation:** exact initial player messages plus opponent context improved four-shot win forecasts over structured inputs alone in both holdouts. Added engine facts helped unseen-family win forecasts but hurt parameter-holdout win forecasts. The concise representation omits some parser, payoff and opponent details; sufficiency is not established.

The original 96-episode coverage cohort and the new 48-episode parameter cohort remain separately selectable. This study does not establish relative prediction difficulty against Gameable Games; native opponents, horizons and label support differ.

## Fixed-budget family-breadth check (2026-09-11)

**Completed: broader coverage helps point estimates, but this does not justify a large run of the current learned predictor.** [Viewer](http://localhost:42329/general/breadth) · [Full report](general_games/breadth_v3/study/REPORT.md) · [Machine-readable results](general_games/breadth_v3/study/summary.json) · [Training exports](general_games/breadth_v3/study/overnight/README.md).

Each arm has **288 fresh training episodes**: depth uses four families with six repetitions per exact condition; breadth uses twelve families with two. The arms share 96 episodes, giving **480 unique training episodes**. **GOPS, Stag Hunt, Blackjack, Battleship, Othello and Sokoban** supply **144 fresh test episodes** and are absent from both training and demonstrations. All fitted artifacts and 864 forecast rows were frozen before test play. Historical labels are excluded. This studies learner transfer; no implementation bug was presumed.

Win Brier on the same six test families, lower is better:

| Predictor | Depth: 4 families | Breadth: 12 families |
|---|---:|---:|
| Training mean | .2840 | .2654 |
| Learned linear | .3281 | .3201 |
| Four-shot + learned correction | .3367 | .2907 |
| Pooled four-shot | .3331 | .2840 |
| Pooled eight-shot | .3047 | .2872 |
| Pooled sixteen-shot | .2925 | .2668 |

Linear breadth-minus-depth is **−.0080**, with a paired six-family bootstrap 95% interval **[−.0713,+.0782]**; learned correction is **−.0460 [−.1121,+.0024]**. Both include zero. Four-shot improves by .0491, so the gain is not specific to learning. Linear improves on five families but worsens sharply on GOPS (+.1872 Brier), offsetting most gains. The global training-mean baseline improves by .0186, more than linear; breadth shifts the training win prior from .6042 to .5556, closer to the observed test rate .3889.

**Few-shot remains competitive, but is not a solved baseline.** The best tested few-shot setting beats both learned methods in each arm; the depth linear learner narrowly beats four-shot alone. Every win predictor trails its arm's training-mean baseline. A constant 0.5 forecast scores **.2500**, an arithmetic reference added after readout, below every reported win error. Breadth prompting leads the other shared targets too: best few-shot **.1216 invalidity Brier** (eight-shot) versus **.2395 linear / .1515 correction**, and **.1633 native-score MSE** (sixteen-shot) versus **.1858 / .1779**. These are point comparisons with limited family coverage.

Post-readout diagnosis identifies specific limitations:

- **Strict wins versus draws:** Stag Hunt produces **2 wins and 22 draws in 24 games**. Breadth linear/four-shot/sixteen-shot mean win forecasts are **.723/.599/.530**, versus **.083 observed**. GOPS goes the other way: 23/24 wins are underestimated. These are observable forecast failures; their internal causes have not been established.
- **Action format matters:** every Sokoban episode begins with a rejected unbracketed action. The native opening shows bracketed shorthand but lists available directions as bare words; the parser requires brackets. Its all-positive invalidity target therefore includes interface compliance. Test a clearer format reminder as a separate controlled ablation before reading this signal as strategic transfer.
- **Models differ and labels vary:** Qwen solves Sokoban **8/12**, GLM **3/12**; Blackjack reverses direction (**2/12 versus 5/12** completed majority wins). Win outcomes vary across repeats in **14/72 exact test conditions**. These remain family-specific observations, with only two test repetitions.

**Overnight recommendation:** run a small representation/calibration comparison with full-family validation within the training pool, keeping pooled prompting and constant/prior controls. The breadth arm has only **68 distinct complete visible inputs**, versus 24 for depth. Do not interpret repeated labels as hundreds of independent game descriptions. Large-scale training of the current linear/correction method is not supported; neural fine-tuning was not tested. A newly tuned learner or instruction ablation needs untouched evaluation for a prospective claim. Broader coverage remains a useful experimental direction, but this fixed purposive family composition also changes player-count/information coverage and does not isolate a universal family-count effect. There is one configuration per family here, so this is not a new parameter-response study.

All **624 planned episodes / 4,042 focal actions / 7,008 native transitions** passed the final audit. All **4,281 inference attempts** reconcile at **$17.6965**, with no unknown billing. Saved learners reproduce 864 forecast values within 1e-12. One training checkpoint needed one extra call under the uniform recovery policy specified before forecasting; original failures remain archived. No trial was replaced, censored out of scoring, or relabeled as a loss after an API failure. [Code, source archives and reproduction manifests](general_games/breadth_v3/README.md).

## Replicated general-game follow-up (2026-09-11)

**Implemented and completed: 16 families, 57 configurations, 736 total episodes. Few-shot still leads general win prediction; the current learned predictors do not establish a benefit from scaling training volume.** [Expanded viewer](http://localhost:42329/general/replicated) · [Full study report and learning curves](general_games/scaleup_v2/study/REPORT.md) · [Dataset card](general_games/scaleup_v2/data/DATASET_CARD.md) · [Code and reproduction](general_games/scaleup_v2/README.md).

The new version adds native **Ultimatum, Two-Thirds Average, Secretary and Memory**, without selecting games for gameability. It collects **592 fresh episodes**: 320 lower/base-parameter training episodes, 160 higher-parameter tests and 112 new-family tests. The four anchor families independently cross two world seeds, every focal seat and both models, with **five independent LLM repetitions per exact condition**. New families have two repetitions. All fresh actors use the original normal prompt. The 144 historical episodes remain separate, giving **3,755 focal actions** across 28 actually sampled configurations; other catalog configurations have scripted validation only.

Learning curves use **120 / 248 / 440 training episodes**, holding out the same upper parameter settings and all four new families at every stage. Training-only feature fitting, family-excluded calibration and fixed hyperparameters compare a direct structured/text linear learner, learned corrections, and **4/8/16-shot Kimi prompting**. All **2,112 primary test predictions** and saved models were frozen before the first new test-player call. Added training depth is concentrated in four anchors; this is not a controlled increase in training-family breadth or language-encoder fine-tuning.

Win / full-solution Brier at 440 training episodes, lower is better:

| Predictor | Higher parameters · 160 episodes | Four new families · 112 episodes |
|---|---:|---:|
| Four-shot | 0.1867 | 0.2165 |
| Eight-shot | 0.1718 | 0.2422 |
| Sixteen-shot | 0.1727 | 0.2306 |
| Learned linear | 0.2073 | 0.2909 |
| Four-shot + learned correction | 0.2087 | 0.3039 |
| Pooled four-shot, secondary control | 0.1657 | 0.2170 |

The primary corrected-four-shot minus four-shot difference is **+0.0220** on parameters (paired family-bootstrap 95% interval **[+0.0093,+0.0315]**) and **+0.0874** on new families (**[+0.0187,+0.1524]**). The learned correction's unseen-family error increases with training size: **.2506 → .2952 → .3039**. These intervals condition on fitted forecasts and only four families per holdout; they are not broad population guarantees.

During validation, we identified underused few-shot data: several exact conditions share identical visible inputs, but the original retrieval keeps one condition's labels. A **secondary 264-forecast control** pools all training labels/counts for each identical visible input while preserving the **exact same example IDs and order** for 4/8/16-shot prompts. This control was introduced after test play began, using training data only; it is explicitly separate from the prospective freeze. Pooling strengthens parameter four-shot prediction, including Pig risk-rate MSE (**.0038**, versus learned linear **.0047** and original four-shot **.0160**).

- **Parameter responses are observable:** PD cooperation falls **.567/.533/.492** with increasing defection reward; Blotto allocation concentration falls **.483/.466/.451**; auction capital use falls **.996/.900/.647**. Each setting has 40 episodes; the auction rate is measurable in 30/33/35. Pig episodes lengthen from **5.225 to 14.100** focal actions. The high setting was collected in a later batch, limiting causal interpretation.
- **Models differ by behavior and family:** GLM wins Memory **10/16**, Qwen **5/16**, and selects an available known pair more often (**.943 vs .718**). Auction invalidity affects **30/60 GLM episodes versus 6/60 Qwen**. All 120 fresh PD episodes are wins, yet cooperation differs (**.661 GLM vs .400 Qwen**): win alone misses useful variation.
- **Operational labels reproduce:** all **5,608 new native transitions** replay. Independent checks cover 360 PD rounds, 98 valid auction capital changes, 96 Ultimatum rounds, 96 Two-Thirds rounds, 16 secretary selections and 527 memory moves. Repeated win outcomes vary in **51/152 exact conditions**. Unsupported/ineligible rates stay null; intention and exploitation are not inferred.
- **Representation is more complete:** exact actor openings, corrected parser/payoff/initialization rules, numerical opponent policies and authoritative executable sources are preserved. Earlier specification drafts/forecasts remain auditable preflight artifacts, excluded from scoring. A complete source archive does not establish that the compact predictor rendering is sufficient; hidden realizations and future events remain unavailable.

**Training headroom is narrow in this run.** Linear prediction still beats every tested few-shot variant on auction budget-use MSE (**.0778 vs best few-shot .0911**) and narrowly on Blotto concentration (**.0042 vs .0043**). These are individual-family targets. Remaining error leaves room for better predictors, but the current learners do not capture it broadly. **Keep the improved measurement protocol and pooled few-shot controls; fix learner transfer and test training-family breadth at a fixed label budget before a large scale-up.** Selective family expansion is supported as a controlled next experiment; more repetition of the same anchors is not the evidence-backed next scaling strategy.

All **3,607 inference attempts** reconcile with raw records and ledgers: **$27.9994** total, including preflight and secondary controls, with no unresolved billing. Saved learned models reproduce all checked values and masks exactly. [Full audit and results](general_games/scaleup_v2/study/summary.json).

[Research plan](plan.md) · [Plan coverage and unrun items](plan-coverage.md) · [Execution decisions](execution.md) · [Consolidated literature map](literature.md) · [Predictive-work literature](literature-prediction.md) · [Repeated-game literature](literature-games.md) · [Agent-identification literature](literature-identification.md) · [Measurement formulas](measurements.md) · [Independent audit](audit.md) · [Reproduction and artifact guide](README.md) · [Pilot interpretation](pilot-interpretation.md) · [Prediction interpretation](numerical-interpretation.md) · [Secondary interpretation](secondary-interpretation.md) · [Prospective interpretation](prospective-interpretation.md) · [Control interpretation](controls-interpretation.md)

## Asymmetric-payoff follow-up

**Independently mixing player payoffs produced much larger differences between roles and some difficult switching games, but no clear increase in average prediction error in this small pilot.** The original study used four shared payoff numbers, giving joint outcomes `(R,R), (S,T), (T,S), (P,P)`. It allowed unequal outcomes and different model identities, but not independent payoff schedules. The extension permits eight payoff entries and presents each player with the correct table from their own perspective. Each move still has two actions; the expanded space is the space of incentives and resulting strategies.

### Pilot design

Four fixed schedules—Prisoner's Dilemma, Harmony, Stag Hunt, and Chicken—were crossed independently across the two players. This yields **16 ordered payoff pairings: four symmetric controls and 12 asymmetric pairings**, or ten games up to swapping player roles. Each player's marginal schedule distribution is balanced across conditions. For example, pairing PD with Harmony gives canonical joint payoffs `(3,3), (0,1), (5,2), (1,0)` for outcomes 00, 01, 10, 11.

Qwen 3.8 27B and GPT-OSS-20B played each pairing in both model seat orders and both A/B label orientations: **64/64 completed eight-round matches, 512 rounds, and 1,024 player decisions**. Players saw both players' payoffs and full public history, maximized their own cumulative points, and did not know the opponent model identity. The remaining protocol settings matched the core study: simultaneous actions, temperature 0.7, low reasoning effort, a 4,096-token cap, and at most two attempts per response.

Kimi K3 made 64 zero-shot joint-action forecasts. All forecasts were frozen before the first player request. Fixed comparators predicted uniform play or a highest-total-payoff pure stage Nash outcome, sharing joint mass among tied maximizers; when no pure equilibrium exists, the latter uses the unique interior mixed equilibrium. This comparator is a restricted stage-game rule, not a complete theory of repeated play.

### Is asymmetry harder to predict?

Action Brier scores evaluate the forecast probability of each player's canonical action 0; lower is better. Every method uses all matches with equal weight per ordered payoff pairing.

| Predictor | Symmetric action Brier | Asymmetric action Brier |
|---|---:|---:|
| Kimi zero-shot | 0.1432 | 0.1342 |
| Stage-equilibrium selector | 0.0781 | 0.0961 |
| Uniform | 0.2500 | 0.2500 |

Kimi's asymmetric-minus-symmetric difference is **−0.0090**, with a descriptive 95% bootstrap interval **[−0.1389, +0.1093]**. The equilibrium comparator's difference is +0.0179 [−0.1133, +0.1296]. Neither establishes a direction. The equilibrium comparator has lower point error than Kimi in both conditions.

The conclusion also holds for the other prediction targets. Kimi's four-outcome joint Brier is nearly unchanged: **0.4262 symmetric versus 0.4254 asymmetric**. After pooling the two label orientations within each game × player role × model cell, its average-rate MSE is **0.0695 versus 0.0444**, with difference −0.0252 [−0.1046, +0.0340]. This checks average-behavior prediction separately from error on individual actions; neither result supports an aggregate difficulty increase.

### What payoff mixing changed

![Prediction error and differences between player roles across independently mixed payoff schedules](results/asymmetry-20260910-openrouter/payoff-grid.png)

- **PD × Harmony produced completely consistent opposite actions.** The PD player chose canonical action 1 and the Harmony player chose action 0 in all 64 rounds across the eight matches covering both payoff role orientations. Kimi Brier was 0.026–0.052, and the equilibrium comparator's error was zero. Different incentives can make roles easier to predict.
- **Stag Hunt × Chicken produced a matching-versus-mismatching conflict with no pure stage Nash outcome.** Players switched actions on 39.3–46.4% of adjacent-round transitions. Kimi Brier was 0.265–0.290, and the equilibrium comparator scored 0.259–0.269. This was difficult, but comparable to symmetric Chicken, where Kimi scored 0.280.
- **PD × Stag Hunt was difficult for Kimi despite having a unique pure equilibrium:** Brier 0.218–0.221. The symmetric PD control scored 0.229, so this error is not specific to asymmetry or the absence of a pure equilibrium.
- Across the grid, the mean absolute difference between the two roles' action-0 rates grew from **6.25 to 47.66 percentage points**, while overall action switching rose from **9.38% to 14.29%**. These are descriptive differences in the selected grid, not independently estimated causal effects or evidence of more complex internal reasoning.

### Scope, audit, and implication

This is a small exploratory run with four hand-chosen schedules, two player models, four matches per ordered pairing, and one zero-shot forecaster. Bootstrap intervals resample four symmetric or six unordered asymmetric schedule groups, retaining role reversals together. Those groups reuse the same four schedules, so the intervals are rough descriptive summaries of this grid. They do not establish equivalence or reliable population-level uncertainty.

The initial 64-match pilot did not evaluate learned predictors: the original four-payoff features, symmetric equilibrium rules, and cooperation definitions do not encode independent player payoffs. The follow-up below trains predictors with both players' payoff schedules. Neither experiment measures transfer of the original symmetric fitted weights to asymmetric games, and these scores should not be compared directly with the core study's larger cohort or few-shot results. Both payoff schedules were public; private-payoff games remain untested.

The results support expanding the representation to both players' payoff schedules and testing held-out combinations, with role-swapped copies grouped together. Payoff mixing offers different roles and interaction patterns; it does not automatically make prediction harder.

All forecasts and matches completed. Eight offline tests and the completed-run audits checked role-specific payoffs and prompts, label reversal, equilibrium calculations, source hashes, forecast chronology, raw-call provenance, coverage, and an independent Brier recomputation. **Reported inference charges were $1.15**, with no outstanding reservations; Qwen used the existing hosted allocation. One truncated response was recovered by the bounded retry. Kimi forecasts used OpenRouter after the original FLT route returned 404 errors; that failed forecast-only attempt is preserved separately, and no matches started there.

[Full follow-up and exact payoff schedules](asymmetry-pilot.md) · [Frozen manifest](results/asymmetry-20260910-openrouter/manifest.json) · [Scores and intervals](results/asymmetry-20260910-openrouter/summary.json) · [Per-game results](results/asymmetry-20260910-openrouter/game-summary.json) · [Audit](results/asymmetry-20260910-openrouter/AUDIT.json) · [Reproduction](README.md#asymmetric-payoff-pilot)

### Few-shot versus learned predictors: fresh matches

**Few-shot has a small, inconclusive point lead over learned logistic and MLP predictors on asymmetric games. It barely improves on zero-shot there, and its performance on the symmetric controls is substantially worse. There is no established overall few-shot advantage in this follow-up.**

The first pilot's 64 matches supplied the training pool. For each query, its entire payoff-equivalence group was excluded from numerical fitting and example selection, including role swaps, independent action relabeling, and positive affine utility transformations. Kimi received three nearby examples from distinct allowed groups, matched to the ordered player-model pair. Logistic and a 16-unit tanh MLP used all allowed training matches with both players' raw/normalized payoffs, incentive and equilibrium features, label orientation, and model identities. Logistic regularization was tuned only within allowed training groups; MLP settings were fixed. The methods shared the allowed training pool, but few-shot saw fewer examples. These were newly fitted numerical models, not the old symmetric weights.

All forecasts were frozen before **64/64 fresh eight-round matches** on the same 16-pairing grid, with both model seat orders and label orientations. The test set has 16 symmetric and 48 asymmetric matches. Original zero-shot forecasts were reused unchanged; every method below was scored on these same fresh outcomes. Lower action Brier is better.

| Predictor | Asymmetric | Symmetric controls | All pairings |
|---|---:|---:|---:|
| Kimi three-example few-shot | 0.1419 | 0.2404 | 0.1665 |
| Learned logistic | 0.1524 | 0.1412 | 0.1496 |
| Learned MLP | 0.1468 | 0.1431 | 0.1459 |
| Kimi zero-shot | 0.1434 | 0.1670 | 0.1493 |
| Stage-equilibrium selector | **0.0935** | **0.1094** | **0.0974** |
| Uniform | 0.2500 | 0.2500 | 0.2500 |

On asymmetric games, few-shot-minus-logistic Brier is **−0.0105 [−0.0597, +0.0376]**, and few-shot-minus-MLP is **−0.0049 [−0.0438, +0.0355]**. Both leads are inconclusive. The difference against zero-shot is just −0.0014 [−0.0382, +0.0438]. Few-shot's asymmetric average-rate MSE is also lower in point estimate—0.0511 versus logistic 0.0734 and MLP 0.0680—but separate uncertainty intervals for those MSE differences were not computed.

![Few-shot versus learned prediction scores and paired differences on asymmetric games](results/asymmetry-predictors-20260910/predictor-comparison.png)

The equilibrium selector remains best on action Brier; few-shot-minus-selector is +0.0485 [+0.0061, +0.1045] on asymmetric games. This ranking depends on the metric: asymmetric log loss is 0.8193 for the extreme equilibrium rule versus 0.4297 few-shot, 0.4429 logistic, and 0.4375 MLP. Departures from its zero/one forecasts are costly under log loss, with probabilities clipped at 1e-6.

The few-shot lead also varies by payoff combination. Few-shot beats logistic on two of the six asymmetric groups and MLP on three. Harmony × Stag Hunt favors few-shot (0.0092 versus logistic 0.1050 and MLP 0.0774), while Stag Hunt × Chicken favors the learned models (few-shot 0.2999, logistic 0.2726, MLP 0.2576).

The symmetric **Stag Hunt × Stag Hunt** control is a substantial few-shot failure: Brier **0.4416**, versus zero-shot 0.1119, logistic 0.0937, and MLP 0.2206. Few-shot predicts low canonical action-0 rates in three matches where both players actually choose action 0 throughout. For one such query, nearest examples came from PD × Stag Hunt, Chicken × Stag Hunt, and PD × PD. This is consistent with numerically nearby examples being poor behavioral analogies across incentive regimes, but the cause was not isolated by an ablation. Across the full grid, few-shot's 0.1665 Brier is worse in point estimate than logistic 0.1496 and MLP 0.1459; their paired differences remain inconclusive.

This is a small follow-up designed after seeing the initial pilot, with forecasts frozen before fresh outcomes. It tests held-out payoff combinations on fresh repetitions of the existing grid, not newly sampled payoff shapes. The asymmetric condition has only six equivalence groups and the symmetric condition four. Descriptive intervals use 4,000 paired bootstrap draws over groups and whole fresh episodes, conditional on fixed fits and forecasts; they omit refitting uncertainty and multiplicity correction. The result supports few-shot competitiveness in this setting, not a general lead over learned prediction.

All 1,088 new requests succeeded, with **$1.01 in reported charges** and no outstanding reservations; Qwen used the hosted allocation. Seventeen offline tests passed. Runtime audits verified training/example exclusion, source and artifact hashes, forecast-before-play chronology, role/label coverage, and prompt/action/payoff provenance. An independent readout reproduced all 256 numerical predictions from the saved models and independently recomputed all 18 condition × method Brier scores.

[Full comparison](asymmetry-predictors.md) · [Frozen design](results/asymmetry-predictors-20260910/manifest.json) · [Examples and prompts](results/asymmetry-predictors-20260910/queries.json) · [Fits and forecasts](results/asymmetry-predictors-20260910/numeric.json) · [Scores and intervals](results/asymmetry-predictors-20260910/summary.json) · [Audit](results/asymmetry-predictors-20260910/AUDIT.json) · [Independent recomputation](results/asymmetry-predictors-20260910/independent-audit.json)

## Research readout

Minimum prediction feasibility is supported: game payoffs predict average behavior before play. The stronger case for a transferable, model-specific behavioral representation is not established. Simple family and equilibrium baselines explain much of the signal, few-shot prompting is competitive with learned predictors, and cooperation transfers poorly across families, especially held-out Prisoner’s Dilemma. The bounded study closes at Gate 7 without expanding into embeddings or fine-tuning.

- The study contains 2,758 valid eight-round matches out of 2,760 planned, over 93 distinct payoff shapes and four models. Training uses 1,918 matches over 72 shapes. All 420 new-game matches and all 420 control matches completed; controls reuse seven known shapes. Numerical and all 1,008 prompted forecasts were saved before their prospective player runs. Trace, input, and chronology audits passed. The 21 new shapes come from the same seven archetypes, not an eighth family.
- On new games, combined-logistic Brier scores are 0.138 action choice, 0.058 mutual cooperation, and 0.140 coordination, versus context-only scores 0.251, 0.214, and 0.193. Paired gains are 0.113 [0.066, 0.156], 0.156 [0.110, 0.221], and 0.054 [0.040, 0.070]. This clears the minimum criterion of prediction beyond model/opponent averages.
- Three-example few-shot prompting improves over zero-shot on all three broad targets: Brier gains 0.045 [0.014, 0.087], 0.141 [0.076, 0.212], and 0.079 [0.045, 0.120]. Its differences from combined logistic are inconclusive. Adding a game-theory prompt to zero-shot yields no clear broad-target improvement.
- The prospective family mean already scores 0.061 cooperation and 0.139 coordination; combined logistic has no clear additional Brier gain over it. A stronger equilibrium selector, designed after the pilot and frozen before new-game play, scores 0.144, 0.066, and 0.144. Combined logistic improves cooperation by 0.008 [0.001, 0.018], but its action and coordination residuals are inconclusive. Learned/few-shot log loss improves over the extreme equilibrium rule; a generic smoothed theory comparator was not tested.
- Structural transfer is substantially weaker. In the 72-game family holdouts, combined-logistic Brier is 0.173 action, 0.302 cooperation, and 0.159 coordination; the secondary equilibrium rule scores 0.151, 0.084, and 0.146. Holding out Prisoner’s Dilemma produces cooperation Brier 0.901. Global parameter-region extrapolation also fails for learned action prediction (0.340 versus context 0.257); these region splits change family composition and do not isolate within-family extrapolation.
- Focal/opponent identity adds little to action prediction (prospective game-only 0.1381 versus both identities 0.1383). Joint new-game/excluded-pair and new-game/excluded-GPT-OSS tests beat context means for action and cooperation; coordination is clear only in the model-focused test. All six broad-target Brier residuals against the stronger equilibrium selector are inconclusive. This supports a shared response to payoffs more directly than individualized dispositions.
- Conditional targets remain limited. Prospective forgiveness has 86 opportunities across eight games. Matching the baseline to event weights removes much of the apparent exploitation gain. The game-theory prompt has a positive conditional retaliation result, but these observational rates do not establish intent or causal responses.
- Robustness is qualified. Across the matched historical-pilot comparisons, scale ×3 increases mutual cooperation by 4.35 percentage points [1.06, 9.23] on five shapes; abstract text reduces canonical action0 by 4.47 points [−10.11, −0.29] on seven shapes. Other aggregate broad-target intervals cross zero, which is not an equivalence test. Serving/time changes and independent sampling can contribute because there is no concurrent untransformed baseline. Forecasts that include raw payoffs are themselves sensitive to affine transformations; normalized-feature forecasts are invariant by construction.
- All intervals are descriptive 95% game/episode bootstraps conditional on fixed fitted forecasts, without multiplicity adjustment or model retraining uncertainty. Secondary baselines were added after viewing the pilot. Minimum feasibility does not satisfy the plan’s stronger success criteria or justify a claim of a general behavioral representation.
- Core gate completion is narrower than the full plan checklist. Controlled training-composition and fixed-game label-noise ablations, per-condition confidence intervals, strict within-family interpolation, and joint trajectory-distribution prediction remain unrun or narrower than specified. These gaps are explicit in the plan coverage audit.

### Main prospective comparison

Brier scores on 21 new payoff shapes from the same seven training archetypes; lower is better. Cooperation is supported on 14 shapes and coordination on 12. All methods use the same supported outcomes. Point differences do not establish a winner; paired intervals and calibration appear below.

| Predictor | Action choice | Mutual cooperation | Coordination |
|---|---:|---:|---:|
| Ordered model/opponent mean | 0.2514 | 0.2144 | 0.1932 |
| Game-family mean | 0.2585 | 0.0609 | 0.1388 |
| Original stationary Nash selector | 0.2267 | 0.2177 | 0.2132 |
| Payoff-dominant selector (secondary) | 0.1436 | 0.0662 | 0.1441 |
| Combined logistic + both identities | 0.1383 | 0.0582 | 0.1395 |
| Combined MLP + both identities | 0.1321 | 0.0588 | 0.1400 |
| Kimi zero-shot | 0.1764 | 0.2025 | 0.2209 |
| Kimi three-example few-shot | 0.1313 | 0.0618 | 0.1415 |
| Kimi game-theory prompt | 0.1786 | 0.2144 | 0.2164 |

The secondary selector was designed after the pilot, then frozen before these new games were played. This cohort tests new payoffs within familiar archetypes; family holdouts provide the separate structural-transfer test.

## Progress and spending

Primary players: **Claude Haiku 4.5, Kimi K3, Qwen 3.8 27B, GPT-OSS-20B**.

| Stage | Completed matches | Planned matches | State |
|---|---:|---:|---|
| Primary pilot (24 shapes) | 958 | 960 | Audited; two bounded-retry failures retained as missing |
| development | 960 | 960 | complete |
| prospective | 420 | 420 | complete |
| controls | 420 | 420 | complete |

The pilot combines verified unchanged pairings and GPT-OSS replacement pairings. Gemma calibration traces are preserved and excluded after a response-truncation reliability revision; [the execution record](execution.md#collection-calibration-revision) explains the decision. The 21 control configurations reuse seven known shapes and do not add 21 independent games.

Prompted forecasts: **1008/1008 valid** (complete; 0 failed queries). Zero-shot, few-shot, and game-theory forecasts are completed before new-game player collection.

Reported inference charges: **$33.13**. Including pending/unknown reservations: **$42.21**. 45,871 requests recorded against the **$3,000 ceiling**. Hosted FLT requests count as calls and tokens but use the existing hosted allocation.

## Gate decision history

Decisions are shown in execution order. Later entries and the research readout above describe the final scope and findings.

- **Gate 1 (04:58 UTC): proceed.** Close precedents rule out broad novelty; narrowed to payoff-only preinteraction distributions in autonomous repeated symmetric2x2 crossplay with structural and pair holdouts.
- **Gate 2 (05:01 UTC): proceed.** All four endpoints passed format preflight; 40 tests and 22 subtests passed, including game transformations, measurement opportunities, simultaneous actions, checkpoint provenance and budget accounting. Frozen 24 games and 960 episodes.
- **Gate 2 (05:19 UTC): revise roster and proceed.** Gemma repeatedly truncated and was slow at larger cap. GPTOSS passed identical failed contexts; replace Gemma based only on endpoint reliability. Reuse verified unchanged traces of otherthree players; retain all Gemma calibration data. Primarycohort24games4models960matches.
- **Gate 3 (06:13 UTC): proceed.** Integrity-checked pilot has sufficient completed coverage and nonconstant game-level behavior. Repeatability estimates and sparse conditional support are retained; variation alone is not evidence of prediction.
- **Gate 4 (07:19 UTC): proceed.** Expanded to 72 distinct payoff shapes with the same player protocol. The snapshot is fixed before fitting the final predictors.
- **Gate 5 (07:34 UTC): numerical evaluation complete.** Prespecified numerical predictors were scored against the ordered model/opponent baseline. All methods, missing support and paired uncertainty remain visible. The prompted-LLM comparison is still required.
- **Gate 6 (07:34 UTC): numerical evaluation complete.** Family, random-group and payoff interpolation/extrapolation holdouts completed. These are exploratory grouped validations; prospective forecasts and presentation/affine controls remain separate.
- **Gate 7 (07:34 UTC): numerical evaluation complete.** Focal/opponent identity ablations, held-out unordered pairings and zero-calibration model holdouts completed. Unknown identities use a declared fallback; no Gate8 adaptation or embeddings experiment was run.
- **Gate 5 (07:34 UTC): proceed.** Run the single fixed prospective cohort after positive screening or inconclusive retrospective evidence. No result-driven enlargement of this cohort is permitted.
- **Gate 6 (08:53 UTC): prospective evaluation complete.** All numerical and prompted forecasts were frozen before new-game player episodes. Missing outcomes and LLM failures remain explicit.
- **Gate 7 (08:53 UTC): prospective evaluation complete.** Additional frozen fits excluded the unordered test pair or every test-model interaction; both roles were purged. Unknown identities use declared fallbacks.
- **Gate 6 (08:53 UTC): proceed.** A prespecified numerical predictor improved ordered context by at least .005 Brier prospectively. Paired intervals are reported without requiring their lower bound above zero for this bounded control screen.
- **Gate 6 (09:24 UTC): control evaluation complete.** Seven source games each received scale x3, offset +10 and abstract-text controls, preserving canonical shapes. Original training fit remained frozen; no Gate8 adaptation or narratives.

## Pilot measurement repeatability

The final pilot contains 958 valid matches out of 960 planned. Balanced repeat halves each include both action-label orientations. Game correlations compare aggregate rates; cell correlations compare game × focal model × opponent rates. Opportunity counts are focal measurement denominators, not independent sample sizes. Conditional targets can retain different subsets.

| Target | Eligible games | Paired games | Game r [95% interval] | Cell r | Focal opportunities |
|---|---:|---:|---|---:|---:|
| action0 | 24 | 24 | 0.996 [0.990, 0.999] | 0.878 | 15,328 |
| first_action0 | 24 | 24 | 0.986 [0.974, 0.995] | 0.750 | 1,916 |
| cooperation | 18 | 18 | 0.994 [0.987, 0.999] | 0.949 | 11,488 |
| coordination | 14 | 14 | 0.951 [0.892, 0.990] | 0.737 | 8,928 |
| retaliation | 15 | 12 | 0.633 [-0.081, 0.997] | 0.549 | 2,824 |
| forgiveness | 11 | 9 | 0.936 [0.567, 0.995] | 0.384 | 295 |
| exploitation | 8 | 8 | 0.615 [-0.601, 0.959] | 0.510 | 1,842 |

[Detailed pilot interpretation and support caveats](pilot-interpretation.md). Strong repeatability is not itself a test of prediction accuracy.


## Prediction results

### Pilot grouped validation

| Test | Target | Predictor | Brier ↓ | Rate MAE ↓ | Shape groups |
|---|---|---|---:|---:|---:|
| family | action0 | marginal | 0.252 | 0.402 | 24 |
| family | action0 | pair | 0.253 | 0.402 | 24 |
| family | action0 | nash | 0.213 | 0.279 | 24 |
| family | action0 | family | 0.252 | 0.402 | 24 |
| family | action0 | raw_logistic | 0.205 | 0.297 | 24 |
| family | action0 | combined_mlp_both | 0.211 | 0.287 | 24 |
| family | action0 | combined_logistic_both | 0.172 | 0.290 | 24 |
| family | cooperation | marginal | 0.331 | 0.506 | 18 |
| family | cooperation | pair | 0.331 | 0.504 | 18 |
| family | cooperation | nash | 0.209 | 0.235 | 18 |
| family | cooperation | family | 0.331 | 0.506 | 18 |
| family | cooperation | raw_logistic | 0.354 | 0.514 | 18 |
| family | cooperation | combined_mlp_both | 0.261 | 0.428 | 18 |
| family | cooperation | combined_logistic_both | 0.310 | 0.403 | 18 |
| family | coordination | marginal | 0.221 | 0.302 | 14 |
| family | coordination | pair | 0.223 | 0.303 | 14 |
| family | coordination | nash | 0.231 | 0.329 | 14 |
| family | coordination | family | 0.221 | 0.302 | 14 |
| family | coordination | raw_logistic | 0.204 | 0.268 | 14 |
| family | coordination | combined_mlp_both | 0.155 | 0.185 | 14 |
| family | coordination | combined_logistic_both | 0.162 | 0.190 | 14 |
| family | exploitation | marginal | 0.298 | 0.444 | 8 |
| family | exploitation | pair | 0.304 | 0.445 | 8 |
| family | exploitation | family | 0.298 | 0.444 | 8 |
| family | exploitation | raw_logistic | 0.262 | 0.393 | 8 |
| family | exploitation | combined_mlp_both | 0.298 | 0.444 | 8 |
| family | exploitation | combined_logistic_both | 0.321 | 0.472 | 8 |
| family | first_action0 | marginal | 0.254 | 0.504 | 24 |
| family | first_action0 | pair | 0.255 | 0.504 | 24 |
| family | first_action0 | nash | 0.230 | 0.360 | 24 |
| family | first_action0 | family | 0.254 | 0.504 | 24 |
| family | first_action0 | raw_logistic | 0.165 | 0.318 | 24 |
| family | first_action0 | combined_mlp_both | 0.175 | 0.337 | 24 |
| family | first_action0 | combined_logistic_both | 0.151 | 0.343 | 24 |
| family | forgiveness | marginal | 0.262 | 0.458 | 11 |
| family | forgiveness | pair | 0.262 | 0.404 | 11 |
| family | forgiveness | family | 0.262 | 0.458 | 11 |
| family | forgiveness | raw_logistic | 0.269 | 0.462 | 11 |
| family | forgiveness | combined_mlp_both | 0.400 | 0.555 | 11 |
| family | forgiveness | combined_logistic_both | 0.360 | 0.530 | 11 |
| family | retaliation | marginal | 0.313 | 0.447 | 15 |
| family | retaliation | pair | 0.351 | 0.473 | 15 |
| family | retaliation | family | 0.313 | 0.447 | 15 |
| family | retaliation | raw_logistic | 0.374 | 0.510 | 15 |
| family | retaliation | combined_mlp_both | 0.342 | 0.475 | 15 |
| family | retaliation | combined_logistic_both | 0.323 | 0.452 | 15 |

[All scores, support, calibration and uncertainty](results/overnight-20260910/pilot/evaluation/scores.json).

Transfer tests for the same combined logistic predictor with both model identities (Brier score; lower is better). Pair and model holdouts reuse known game shapes; their accuracy does not establish new-game transfer.

| Test | Target | Ordered context mean | Original Nash selector | Combined logistic | Shape groups |
|---|---|---:|---:|---:|---:|
| family | action0 | 0.253 | 0.213 | 0.172 | 24 |
| family | cooperation | 0.331 | 0.209 | 0.310 | 18 |
| family | coordination | 0.223 | 0.231 | 0.162 | 14 |
| random_group | action0 | 0.263 | 0.213 | 0.192 | 24 |
| random_group | cooperation | 0.244 | 0.209 | 0.075 | 18 |
| random_group | coordination | 0.186 | 0.231 | 0.146 | 14 |
| interpolation | action0 | 0.252 | 0.126 | 0.171 | 6 |
| interpolation | cooperation | 0.225 | 0.146 | 0.066 | 6 |
| interpolation | coordination | 0.098 | 0.248 | 0.031 | 1 |
| extrapolation | action0 | 0.251 | 0.243 | 0.329 | 6 |
| extrapolation | cooperation | 0.551 | 0.172 | 0.209 | 6 |
| extrapolation | coordination | 0.467 | 0.252 | 0.465 | 4 |
| pair | action0 | 0.250 | 0.213 | 0.141 | 24 |
| pair | cooperation | 0.235 | 0.209 | 0.071 | 18 |
| pair | coordination | 0.183 | 0.231 | 0.140 | 14 |
| model | action0 | 0.250 | 0.212 | 0.143 | 24 |
| model | cooperation | 0.237 | 0.206 | 0.080 | 18 |
| model | coordination | 0.181 | 0.232 | 0.141 | 14 |

Paired Brier improvement over the ordered focal/opponent mean (positive is better; descriptive 95% game/episode bootstrap intervals):

| Target | Predictor | Improvement | Interval |
|---|---|---:|---|
| action0 | raw_logistic | 0.048 | [-0.007, 0.097] |
| action0 | combined_mlp_both | 0.042 | [-0.023, 0.108] |
| action0 | combined_logistic_both | 0.081 | [0.050, 0.114] |
| cooperation | raw_logistic | -0.023 | [-0.084, 0.027] |
| cooperation | combined_mlp_both | 0.069 | [0.034, 0.099] |
| cooperation | combined_logistic_both | 0.021 | [-0.066, 0.101] |
| coordination | raw_logistic | 0.019 | [-0.006, 0.041] |
| coordination | combined_mlp_both | 0.068 | [0.055, 0.080] |
| coordination | combined_logistic_both | 0.062 | [0.052, 0.071] |
### Combined training-set grouped validation

| Test | Target | Predictor | Brier ↓ | Rate MAE ↓ | Shape groups |
|---|---|---|---:|---:|---:|
| family | action0 | marginal | 0.252 | 0.406 | 72 |
| family | action0 | pair | 0.252 | 0.406 | 72 |
| family | action0 | nash | 0.221 | 0.288 | 72 |
| family | action0 | family | 0.252 | 0.406 | 72 |
| family | action0 | raw_logistic | 0.197 | 0.294 | 72 |
| family | action0 | combined_mlp_both | 0.187 | 0.271 | 72 |
| family | action0 | combined_logistic_both | 0.173 | 0.243 | 72 |
| family | cooperation | marginal | 0.317 | 0.488 | 52 |
| family | cooperation | pair | 0.316 | 0.486 | 52 |
| family | cooperation | nash | 0.221 | 0.246 | 52 |
| family | cooperation | family | 0.317 | 0.488 | 52 |
| family | cooperation | raw_logistic | 0.352 | 0.513 | 52 |
| family | cooperation | combined_mlp_both | 0.243 | 0.398 | 52 |
| family | cooperation | combined_logistic_both | 0.302 | 0.364 | 52 |
| family | coordination | marginal | 0.220 | 0.308 | 42 |
| family | coordination | pair | 0.221 | 0.308 | 42 |
| family | coordination | nash | 0.231 | 0.338 | 42 |
| family | coordination | family | 0.220 | 0.308 | 42 |
| family | coordination | raw_logistic | 0.186 | 0.235 | 42 |
| family | coordination | combined_mlp_both | 0.150 | 0.177 | 42 |
| family | coordination | combined_logistic_both | 0.159 | 0.175 | 42 |
| family | exploitation | marginal | 0.314 | 0.458 | 22 |
| family | exploitation | pair | 0.308 | 0.450 | 22 |
| family | exploitation | family | 0.314 | 0.458 | 22 |
| family | exploitation | raw_logistic | 0.268 | 0.405 | 22 |
| family | exploitation | combined_mlp_both | 0.317 | 0.461 | 22 |
| family | exploitation | combined_logistic_both | 0.285 | 0.434 | 22 |
| family | first_action0 | marginal | 0.253 | 0.502 | 72 |
| family | first_action0 | pair | 0.253 | 0.502 | 72 |
| family | first_action0 | nash | 0.232 | 0.358 | 72 |
| family | first_action0 | family | 0.253 | 0.502 | 72 |
| family | first_action0 | raw_logistic | 0.161 | 0.304 | 72 |
| family | first_action0 | combined_mlp_both | 0.162 | 0.319 | 72 |
| family | first_action0 | combined_logistic_both | 0.178 | 0.284 | 72 |
| family | forgiveness | marginal | 0.220 | 0.388 | 30 |
| family | forgiveness | pair | 0.237 | 0.367 | 30 |
| family | forgiveness | family | 0.220 | 0.388 | 30 |
| family | forgiveness | raw_logistic | 0.233 | 0.397 | 30 |
| family | forgiveness | combined_mlp_both | 0.228 | 0.388 | 30 |
| family | forgiveness | combined_logistic_both | 0.232 | 0.412 | 30 |
| family | retaliation | marginal | 0.321 | 0.456 | 38 |
| family | retaliation | pair | 0.354 | 0.471 | 38 |
| family | retaliation | family | 0.321 | 0.456 | 38 |
| family | retaliation | raw_logistic | 0.373 | 0.499 | 38 |
| family | retaliation | combined_mlp_both | 0.292 | 0.432 | 38 |
| family | retaliation | combined_logistic_both | 0.334 | 0.472 | 38 |

[All scores, support, calibration and uncertainty](results/overnight-20260910/development/evaluation/scores.json).

Transfer tests for the same combined logistic predictor with both model identities (Brier score; lower is better). Pair and model holdouts reuse known game shapes; their accuracy does not establish new-game transfer.

| Test | Target | Ordered context mean | Original Nash selector | Combined logistic | Shape groups |
|---|---|---:|---:|---:|---:|
| family | action0 | 0.252 | 0.221 | 0.173 | 72 |
| family | cooperation | 0.316 | 0.221 | 0.302 | 52 |
| family | coordination | 0.221 | 0.231 | 0.159 | 42 |
| random_group | action0 | 0.252 | 0.221 | 0.147 | 72 |
| random_group | cooperation | 0.232 | 0.221 | 0.075 | 52 |
| random_group | coordination | 0.184 | 0.231 | 0.137 | 42 |
| interpolation | action0 | 0.250 | 0.114 | 0.106 | 17 |
| interpolation | cooperation | 0.208 | 0.135 | 0.077 | 17 |
| interpolation | coordination | 0.201 | 0.252 | 0.148 | 4 |
| extrapolation | action0 | 0.257 | 0.249 | 0.340 | 17 |
| extrapolation | cooperation | 0.610 | 0.167 | 0.184 | 17 |
| extrapolation | coordination | 0.410 | 0.257 | 0.256 | 9 |
| pair | action0 | 0.250 | 0.221 | 0.141 | 72 |
| pair | cooperation | 0.228 | 0.221 | 0.074 | 52 |
| pair | coordination | 0.183 | 0.231 | 0.138 | 42 |
| model | action0 | 0.250 | 0.219 | 0.142 | 72 |
| model | cooperation | 0.231 | 0.217 | 0.075 | 52 |
| model | coordination | 0.179 | 0.232 | 0.137 | 42 |

Paired Brier improvement over the ordered focal/opponent mean (positive is better; descriptive 95% game/episode bootstrap intervals):

| Target | Predictor | Improvement | Interval |
|---|---|---:|---|
| action0 | raw_logistic | 0.056 | [0.027, 0.085] |
| action0 | combined_mlp_both | 0.065 | [0.038, 0.092] |
| action0 | combined_logistic_both | 0.079 | [0.049, 0.109] |
| cooperation | raw_logistic | -0.036 | [-0.065, -0.006] |
| cooperation | combined_mlp_both | 0.073 | [0.054, 0.089] |
| cooperation | combined_logistic_both | 0.014 | [-0.047, 0.062] |
| coordination | raw_logistic | 0.035 | [0.016, 0.050] |
| coordination | combined_mlp_both | 0.071 | [0.063, 0.079] |
| coordination | combined_logistic_both | 0.062 | [0.052, 0.072] |
### New games: numerical and prompted forecasts on common support

| Test | Target | Predictor | Brier ↓ | Rate MAE ↓ | Shape groups |
|---|---|---|---:|---:|---:|
| prospective | action0 | marginal | 0.251 | 0.405 | 21 |
| prospective | action0 | pair | 0.251 | 0.406 | 21 |
| prospective | action0 | nash | 0.227 | 0.281 | 21 |
| prospective | action0 | family | 0.258 | 0.410 | 21 |
| prospective | action0 | raw_logistic | 0.156 | 0.241 | 21 |
| prospective | action0 | combined_mlp_both | 0.132 | 0.180 | 21 |
| prospective | action0 | combined_logistic_both | 0.138 | 0.196 | 21 |
| prospective | action0 | llm_zero_shot | 0.176 | 0.260 | 21 |
| prospective | action0 | llm_few_shot | 0.131 | 0.167 | 21 |
| prospective | action0 | llm_game_theory | 0.179 | 0.266 | 21 |
| prospective | cooperation | marginal | 0.217 | 0.405 | 14 |
| prospective | cooperation | pair | 0.214 | 0.399 | 14 |
| prospective | cooperation | nash | 0.218 | 0.241 | 14 |
| prospective | cooperation | family | 0.061 | 0.091 | 14 |
| prospective | cooperation | raw_logistic | 0.202 | 0.360 | 14 |
| prospective | cooperation | combined_mlp_both | 0.059 | 0.091 | 14 |
| prospective | cooperation | combined_logistic_both | 0.058 | 0.091 | 14 |
| prospective | cooperation | llm_zero_shot | 0.203 | 0.347 | 14 |
| prospective | cooperation | llm_few_shot | 0.062 | 0.111 | 14 |
| prospective | cooperation | llm_game_theory | 0.214 | 0.350 | 14 |
| prospective | coordination | marginal | 0.195 | 0.274 | 12 |
| prospective | coordination | pair | 0.193 | 0.273 | 12 |
| prospective | coordination | nash | 0.213 | 0.321 | 12 |
| prospective | coordination | family | 0.139 | 0.152 | 12 |
| prospective | coordination | raw_logistic | 0.159 | 0.197 | 12 |
| prospective | coordination | combined_mlp_both | 0.140 | 0.157 | 12 |
| prospective | coordination | combined_logistic_both | 0.140 | 0.155 | 12 |
| prospective | coordination | llm_zero_shot | 0.221 | 0.302 | 12 |
| prospective | coordination | llm_few_shot | 0.141 | 0.160 | 12 |
| prospective | coordination | llm_game_theory | 0.216 | 0.298 | 12 |
| prospective | defection_after_cooperation | llm_zero_shot | 0.120 | 0.234 | 14 |
| prospective | defection_after_cooperation | llm_few_shot | 0.081 | 0.130 | 14 |
| prospective | defection_after_cooperation | llm_game_theory | 0.103 | 0.211 | 14 |
| prospective | defection_after_mutual_cooperation | llm_zero_shot | 0.098 | 0.211 | 14 |
| prospective | defection_after_mutual_cooperation | llm_few_shot | 0.084 | 0.134 | 14 |
| prospective | defection_after_mutual_cooperation | llm_game_theory | 0.100 | 0.203 | 14 |
| prospective | exploitation | marginal | 0.253 | 0.394 | 6 |
| prospective | exploitation | pair | 0.226 | 0.369 | 6 |
| prospective | exploitation | family | 0.253 | 0.323 | 6 |
| prospective | exploitation | raw_logistic | 0.249 | 0.396 | 6 |
| prospective | exploitation | combined_mlp_both | 0.246 | 0.309 | 6 |
| prospective | exploitation | combined_logistic_both | 0.211 | 0.318 | 6 |
| prospective | exploitation | llm_zero_shot | 0.276 | 0.408 | 6 |
| prospective | exploitation | llm_few_shot | 0.231 | 0.324 | 6 |
| prospective | exploitation | llm_game_theory | 0.263 | 0.370 | 6 |
| prospective | first_action0 | marginal | 0.251 | 0.501 | 21 |
| prospective | first_action0 | pair | 0.251 | 0.501 | 21 |
| prospective | first_action0 | nash | 0.223 | 0.341 | 21 |
| prospective | first_action0 | family | 0.276 | 0.518 | 21 |
| prospective | first_action0 | raw_logistic | 0.158 | 0.319 | 21 |
| prospective | first_action0 | combined_mlp_both | 0.126 | 0.260 | 21 |
| prospective | first_action0 | combined_logistic_both | 0.124 | 0.240 | 21 |
| prospective | first_action0 | llm_zero_shot | 0.156 | 0.348 | 21 |
| prospective | first_action0 | llm_few_shot | 0.121 | 0.240 | 21 |
| prospective | first_action0 | llm_game_theory | 0.147 | 0.336 | 21 |
| prospective | forgiveness | marginal | 0.196 | 0.394 | 8 |
| prospective | forgiveness | pair | 0.210 | 0.371 | 8 |
| prospective | forgiveness | family | 0.178 | 0.364 | 8 |
| prospective | forgiveness | raw_logistic | 0.195 | 0.398 | 8 |
| prospective | forgiveness | combined_mlp_both | 0.153 | 0.330 | 8 |
| prospective | forgiveness | combined_logistic_both | 0.170 | 0.360 | 8 |
| prospective | forgiveness | llm_zero_shot | 0.224 | 0.434 | 8 |
| prospective | forgiveness | llm_few_shot | 0.211 | 0.367 | 8 |
| prospective | forgiveness | llm_game_theory | 0.224 | 0.440 | 8 |
| prospective | individual_cooperation | llm_zero_shot | 0.168 | 0.288 | 14 |
| prospective | individual_cooperation | llm_few_shot | 0.081 | 0.109 | 14 |
| prospective | individual_cooperation | llm_game_theory | 0.172 | 0.288 | 14 |
| prospective | retaliation | marginal | 0.253 | 0.410 | 11 |
| prospective | retaliation | pair | 0.246 | 0.380 | 11 |
| prospective | retaliation | family | 0.207 | 0.295 | 11 |
| prospective | retaliation | raw_logistic | 0.270 | 0.430 | 11 |
| prospective | retaliation | combined_mlp_both | 0.217 | 0.303 | 11 |
| prospective | retaliation | combined_logistic_both | 0.196 | 0.303 | 11 |
| prospective | retaliation | llm_zero_shot | 0.232 | 0.331 | 11 |
| prospective | retaliation | llm_few_shot | 0.200 | 0.265 | 11 |
| prospective | retaliation | llm_game_theory | 0.175 | 0.291 | 11 |
| prospective | retaliation_after_exploitation | llm_zero_shot | 0.256 | 0.382 | 11 |
| prospective | retaliation_after_exploitation | llm_few_shot | 0.206 | 0.292 | 11 |
| prospective | retaliation_after_exploitation | llm_game_theory | 0.199 | 0.337 | 11 |

[All scores, support, calibration and uncertainty](results/overnight-20260910/prospective/evaluation/scores.json).

Paired Brier improvement over the ordered focal/opponent mean (positive is better; descriptive 95% game/episode bootstrap intervals):

| Target | Predictor | Improvement | Interval |
|---|---|---:|---|
| action0 | raw_logistic | 0.096 | [0.053, 0.137] |
| action0 | combined_mlp_both | 0.119 | [0.074, 0.161] |
| action0 | combined_logistic_both | 0.113 | [0.066, 0.156] |
| cooperation | raw_logistic | 0.012 | [-0.037, 0.053] |
| cooperation | combined_mlp_both | 0.156 | [0.109, 0.221] |
| cooperation | combined_logistic_both | 0.156 | [0.110, 0.221] |
| coordination | raw_logistic | 0.035 | [0.020, 0.049] |
| coordination | combined_mlp_both | 0.053 | [0.040, 0.069] |
| coordination | combined_logistic_both | 0.054 | [0.040, 0.070] |
### New games: numerical forecasts on their full common support

| Test | Target | Predictor | Brier ↓ | Rate MAE ↓ | Shape groups |
|---|---|---|---:|---:|---:|
| prospective | action0 | marginal | 0.251 | 0.405 | 21 |
| prospective | action0 | pair | 0.251 | 0.406 | 21 |
| prospective | action0 | nash | 0.227 | 0.281 | 21 |
| prospective | action0 | family | 0.258 | 0.410 | 21 |
| prospective | action0 | raw_logistic | 0.156 | 0.241 | 21 |
| prospective | action0 | combined_mlp_both | 0.132 | 0.180 | 21 |
| prospective | action0 | combined_logistic_both | 0.138 | 0.196 | 21 |
| prospective | cooperation | marginal | 0.217 | 0.405 | 14 |
| prospective | cooperation | pair | 0.214 | 0.399 | 14 |
| prospective | cooperation | nash | 0.218 | 0.241 | 14 |
| prospective | cooperation | family | 0.061 | 0.091 | 14 |
| prospective | cooperation | raw_logistic | 0.202 | 0.360 | 14 |
| prospective | cooperation | combined_mlp_both | 0.059 | 0.091 | 14 |
| prospective | cooperation | combined_logistic_both | 0.058 | 0.091 | 14 |
| prospective | coordination | marginal | 0.195 | 0.274 | 12 |
| prospective | coordination | pair | 0.193 | 0.273 | 12 |
| prospective | coordination | nash | 0.213 | 0.321 | 12 |
| prospective | coordination | family | 0.139 | 0.152 | 12 |
| prospective | coordination | raw_logistic | 0.159 | 0.197 | 12 |
| prospective | coordination | combined_mlp_both | 0.140 | 0.157 | 12 |
| prospective | coordination | combined_logistic_both | 0.140 | 0.155 | 12 |
| prospective | exploitation | marginal | 0.253 | 0.394 | 6 |
| prospective | exploitation | pair | 0.226 | 0.369 | 6 |
| prospective | exploitation | family | 0.253 | 0.323 | 6 |
| prospective | exploitation | raw_logistic | 0.249 | 0.396 | 6 |
| prospective | exploitation | combined_mlp_both | 0.246 | 0.309 | 6 |
| prospective | exploitation | combined_logistic_both | 0.211 | 0.318 | 6 |
| prospective | first_action0 | marginal | 0.251 | 0.501 | 21 |
| prospective | first_action0 | pair | 0.251 | 0.501 | 21 |
| prospective | first_action0 | nash | 0.223 | 0.341 | 21 |
| prospective | first_action0 | family | 0.276 | 0.518 | 21 |
| prospective | first_action0 | raw_logistic | 0.158 | 0.319 | 21 |
| prospective | first_action0 | combined_mlp_both | 0.126 | 0.260 | 21 |
| prospective | first_action0 | combined_logistic_both | 0.124 | 0.240 | 21 |
| prospective | forgiveness | marginal | 0.196 | 0.394 | 8 |
| prospective | forgiveness | pair | 0.210 | 0.371 | 8 |
| prospective | forgiveness | family | 0.178 | 0.364 | 8 |
| prospective | forgiveness | raw_logistic | 0.195 | 0.398 | 8 |
| prospective | forgiveness | combined_mlp_both | 0.153 | 0.330 | 8 |
| prospective | forgiveness | combined_logistic_both | 0.170 | 0.360 | 8 |
| prospective | retaliation | marginal | 0.253 | 0.410 | 11 |
| prospective | retaliation | pair | 0.246 | 0.380 | 11 |
| prospective | retaliation | family | 0.207 | 0.295 | 11 |
| prospective | retaliation | raw_logistic | 0.270 | 0.430 | 11 |
| prospective | retaliation | combined_mlp_both | 0.217 | 0.303 | 11 |
| prospective | retaliation | combined_logistic_both | 0.196 | 0.303 | 11 |

[All scores, support, calibration and uncertainty](results/overnight-20260910/prospective/evaluation-numerical/scores.json).

Paired Brier improvement over the ordered focal/opponent mean (positive is better; descriptive 95% game/episode bootstrap intervals):

| Target | Predictor | Improvement | Interval |
|---|---|---:|---|
| action0 | raw_logistic | 0.096 | [0.053, 0.137] |
| action0 | combined_mlp_both | 0.119 | [0.074, 0.161] |
| action0 | combined_logistic_both | 0.113 | [0.066, 0.156] |
| cooperation | raw_logistic | 0.012 | [-0.037, 0.053] |
| cooperation | combined_mlp_both | 0.156 | [0.109, 0.221] |
| cooperation | combined_logistic_both | 0.156 | [0.110, 0.221] |
| coordination | raw_logistic | 0.035 | [0.020, 0.049] |
| coordination | combined_mlp_both | 0.053 | [0.040, 0.069] |
| coordination | combined_logistic_both | 0.054 | [0.040, 0.070] |
### New games and excluded Kimi/GPT-OSS pairing

| Test | Target | Predictor | Brier ↓ | Rate MAE ↓ | Shape groups |
|---|---|---|---:|---:|---:|
| prospective_pair | action0 | marginal | 0.251 | 0.379 | 21 |
| prospective_pair | action0 | pair | 0.251 | 0.379 | 21 |
| prospective_pair | action0 | nash | 0.233 | 0.275 | 21 |
| prospective_pair | action0 | family | 0.261 | 0.386 | 21 |
| prospective_pair | action0 | raw_logistic | 0.148 | 0.218 | 21 |
| prospective_pair | action0 | combined_mlp_both | 0.136 | 0.173 | 21 |
| prospective_pair | action0 | combined_logistic_both | 0.140 | 0.181 | 21 |
| prospective_pair | cooperation | marginal | 0.242 | 0.418 | 14 |
| prospective_pair | cooperation | pair | 0.242 | 0.418 | 14 |
| prospective_pair | cooperation | nash | 0.182 | 0.215 | 14 |
| prospective_pair | cooperation | family | 0.077 | 0.117 | 14 |
| prospective_pair | cooperation | raw_logistic | 0.215 | 0.369 | 14 |
| prospective_pair | cooperation | combined_mlp_both | 0.076 | 0.120 | 14 |
| prospective_pair | cooperation | combined_logistic_both | 0.074 | 0.113 | 14 |
| prospective_pair | coordination | marginal | 0.209 | 0.240 | 12 |
| prospective_pair | coordination | pair | 0.209 | 0.240 | 12 |
| prospective_pair | coordination | nash | 0.225 | 0.278 | 12 |
| prospective_pair | coordination | family | 0.181 | 0.153 | 12 |
| prospective_pair | coordination | raw_logistic | 0.192 | 0.203 | 12 |
| prospective_pair | coordination | combined_mlp_both | 0.179 | 0.159 | 12 |
| prospective_pair | coordination | combined_logistic_both | 0.179 | 0.154 | 12 |
| prospective_pair | exploitation | marginal | 0.216 | 0.371 | 6 |
| prospective_pair | exploitation | pair | 0.216 | 0.371 | 6 |
| prospective_pair | exploitation | family | 0.231 | 0.366 | 6 |
| prospective_pair | exploitation | raw_logistic | 0.243 | 0.401 | 6 |
| prospective_pair | exploitation | combined_mlp_both | 0.223 | 0.352 | 6 |
| prospective_pair | exploitation | combined_logistic_both | 0.224 | 0.360 | 6 |
| prospective_pair | first_action0 | marginal | 0.251 | 0.501 | 21 |
| prospective_pair | first_action0 | pair | 0.251 | 0.501 | 21 |
| prospective_pair | first_action0 | nash | 0.221 | 0.339 | 21 |
| prospective_pair | first_action0 | family | 0.284 | 0.525 | 21 |
| prospective_pair | first_action0 | raw_logistic | 0.150 | 0.311 | 21 |
| prospective_pair | first_action0 | combined_mlp_both | 0.124 | 0.259 | 21 |
| prospective_pair | first_action0 | combined_logistic_both | 0.117 | 0.235 | 21 |
| prospective_pair | forgiveness | marginal | 0.144 | 0.321 | 6 |
| prospective_pair | forgiveness | pair | 0.144 | 0.321 | 6 |
| prospective_pair | forgiveness | family | 0.112 | 0.262 | 6 |
| prospective_pair | forgiveness | raw_logistic | 0.149 | 0.332 | 6 |
| prospective_pair | forgiveness | combined_mlp_both | 0.115 | 0.259 | 6 |
| prospective_pair | forgiveness | combined_logistic_both | 0.122 | 0.279 | 6 |
| prospective_pair | retaliation | marginal | 0.256 | 0.405 | 8 |
| prospective_pair | retaliation | pair | 0.256 | 0.405 | 8 |
| prospective_pair | retaliation | family | 0.199 | 0.273 | 8 |
| prospective_pair | retaliation | raw_logistic | 0.274 | 0.426 | 8 |
| prospective_pair | retaliation | combined_mlp_both | 0.209 | 0.287 | 8 |
| prospective_pair | retaliation | combined_logistic_both | 0.211 | 0.286 | 8 |

[All scores, support, calibration and uncertainty](results/overnight-20260910/prospective/evaluation-pair/scores.json).

Paired Brier improvement over the ordered focal/opponent mean (positive is better; descriptive 95% game/episode bootstrap intervals):

| Target | Predictor | Improvement | Interval |
|---|---|---:|---|
| action0 | raw_logistic | 0.103 | [0.063, 0.144] |
| action0 | combined_mlp_both | 0.115 | [0.072, 0.159] |
| action0 | combined_logistic_both | 0.111 | [0.066, 0.158] |
| cooperation | raw_logistic | 0.027 | [-0.036, 0.085] |
| cooperation | combined_mlp_both | 0.166 | [0.072, 0.257] |
| cooperation | combined_logistic_both | 0.168 | [0.076, 0.260] |
| coordination | raw_logistic | 0.017 | [-0.010, 0.043] |
| coordination | combined_mlp_both | 0.031 | [-0.015, 0.071] |
| coordination | combined_logistic_both | 0.030 | [-0.017, 0.072] |
### New games and excluded GPT-OSS model

| Test | Target | Predictor | Brier ↓ | Rate MAE ↓ | Shape groups |
|---|---|---|---:|---:|---:|
| prospective_model | action0 | marginal | 0.252 | 0.390 | 21 |
| prospective_model | action0 | pair | 0.252 | 0.390 | 21 |
| prospective_model | action0 | nash | 0.229 | 0.275 | 21 |
| prospective_model | action0 | family | 0.259 | 0.394 | 21 |
| prospective_model | action0 | raw_logistic | 0.158 | 0.229 | 21 |
| prospective_model | action0 | combined_mlp_both | 0.138 | 0.177 | 21 |
| prospective_model | action0 | combined_logistic_both | 0.144 | 0.191 | 21 |
| prospective_model | cooperation | marginal | 0.234 | 0.395 | 14 |
| prospective_model | cooperation | pair | 0.234 | 0.395 | 14 |
| prospective_model | cooperation | nash | 0.207 | 0.229 | 14 |
| prospective_model | cooperation | family | 0.079 | 0.102 | 14 |
| prospective_model | cooperation | raw_logistic | 0.219 | 0.350 | 14 |
| prospective_model | cooperation | combined_mlp_both | 0.075 | 0.102 | 14 |
| prospective_model | cooperation | combined_logistic_both | 0.075 | 0.098 | 14 |
| prospective_model | coordination | marginal | 0.199 | 0.259 | 12 |
| prospective_model | coordination | pair | 0.199 | 0.259 | 12 |
| prospective_model | coordination | nash | 0.218 | 0.306 | 12 |
| prospective_model | coordination | family | 0.156 | 0.156 | 12 |
| prospective_model | coordination | raw_logistic | 0.167 | 0.195 | 12 |
| prospective_model | coordination | combined_mlp_both | 0.153 | 0.156 | 12 |
| prospective_model | coordination | combined_logistic_both | 0.154 | 0.154 | 12 |
| prospective_model | exploitation | marginal | 0.240 | 0.378 | 6 |
| prospective_model | exploitation | pair | 0.240 | 0.378 | 6 |
| prospective_model | exploitation | family | 0.221 | 0.319 | 6 |
| prospective_model | exploitation | raw_logistic | 0.270 | 0.404 | 6 |
| prospective_model | exploitation | combined_mlp_both | 0.205 | 0.303 | 6 |
| prospective_model | exploitation | combined_logistic_both | 0.215 | 0.332 | 6 |
| prospective_model | first_action0 | marginal | 0.252 | 0.501 | 21 |
| prospective_model | first_action0 | pair | 0.252 | 0.501 | 21 |
| prospective_model | first_action0 | nash | 0.216 | 0.334 | 21 |
| prospective_model | first_action0 | family | 0.283 | 0.524 | 21 |
| prospective_model | first_action0 | raw_logistic | 0.163 | 0.320 | 21 |
| prospective_model | first_action0 | combined_mlp_both | 0.132 | 0.259 | 21 |
| prospective_model | first_action0 | combined_logistic_both | 0.127 | 0.236 | 21 |
| prospective_model | forgiveness | marginal | 0.191 | 0.383 | 8 |
| prospective_model | forgiveness | pair | 0.191 | 0.383 | 8 |
| prospective_model | forgiveness | family | 0.196 | 0.368 | 8 |
| prospective_model | forgiveness | raw_logistic | 0.203 | 0.392 | 8 |
| prospective_model | forgiveness | combined_mlp_both | 0.166 | 0.346 | 8 |
| prospective_model | forgiveness | combined_logistic_both | 0.183 | 0.371 | 8 |
| prospective_model | retaliation | marginal | 0.257 | 0.390 | 11 |
| prospective_model | retaliation | pair | 0.257 | 0.390 | 11 |
| prospective_model | retaliation | family | 0.355 | 0.440 | 11 |
| prospective_model | retaliation | raw_logistic | 0.262 | 0.399 | 11 |
| prospective_model | retaliation | combined_mlp_both | 0.277 | 0.366 | 11 |
| prospective_model | retaliation | combined_logistic_both | 0.295 | 0.352 | 11 |

[All scores, support, calibration and uncertainty](results/overnight-20260910/prospective/evaluation-model/scores.json).

Paired Brier improvement over the ordered focal/opponent mean (positive is better; descriptive 95% game/episode bootstrap intervals):

| Target | Predictor | Improvement | Interval |
|---|---|---:|---|
| action0 | raw_logistic | 0.093 | [0.051, 0.133] |
| action0 | combined_mlp_both | 0.114 | [0.073, 0.160] |
| action0 | combined_logistic_both | 0.107 | [0.063, 0.155] |
| cooperation | raw_logistic | 0.014 | [-0.038, 0.062] |
| cooperation | combined_mlp_both | 0.158 | [0.082, 0.256] |
| cooperation | combined_logistic_both | 0.159 | [0.084, 0.256] |
| coordination | raw_logistic | 0.031 | [0.012, 0.052] |
| coordination | combined_mlp_both | 0.046 | [0.022, 0.075] |
| coordination | combined_logistic_both | 0.045 | [0.022, 0.074] |
### Frozen forecasts under payoff and presentation controls

| Test | Target | Predictor | Brier ↓ | Rate MAE ↓ | Shape groups |
|---|---|---|---:|---:|---:|
| prospective_controls | action0 | marginal | 0.251 | 0.409 | 7 |
| prospective_controls | action0 | pair | 0.251 | 0.409 | 7 |
| prospective_controls | action0 | nash | 0.183 | 0.249 | 7 |
| prospective_controls | action0 | family | 0.227 | 0.376 | 7 |
| prospective_controls | action0 | raw_logistic | 0.195 | 0.278 | 7 |
| prospective_controls | action0 | combined_mlp_both | 0.130 | 0.193 | 7 |
| prospective_controls | action0 | combined_logistic_both | 0.153 | 0.226 | 7 |
| prospective_controls | cooperation | marginal | 0.225 | 0.397 | 5 |
| prospective_controls | cooperation | pair | 0.224 | 0.393 | 5 |
| prospective_controls | cooperation | nash | 0.159 | 0.199 | 5 |
| prospective_controls | cooperation | family | 0.067 | 0.086 | 5 |
| prospective_controls | cooperation | raw_logistic | 0.206 | 0.354 | 5 |
| prospective_controls | cooperation | combined_mlp_both | 0.067 | 0.095 | 5 |
| prospective_controls | cooperation | combined_logistic_both | 0.066 | 0.092 | 5 |
| prospective_controls | coordination | marginal | 0.185 | 0.255 | 4 |
| prospective_controls | coordination | pair | 0.185 | 0.254 | 4 |
| prospective_controls | coordination | nash | 0.254 | 0.361 | 4 |
| prospective_controls | coordination | family | 0.140 | 0.138 | 4 |
| prospective_controls | coordination | raw_logistic | 0.200 | 0.242 | 4 |
| prospective_controls | coordination | combined_mlp_both | 0.141 | 0.145 | 4 |
| prospective_controls | coordination | combined_logistic_both | 0.141 | 0.143 | 4 |
| prospective_controls | exploitation | marginal | 0.244 | 0.370 | 2 |
| prospective_controls | exploitation | pair | 0.243 | 0.367 | 2 |
| prospective_controls | exploitation | family | 0.218 | 0.291 | 2 |
| prospective_controls | exploitation | raw_logistic | 0.248 | 0.377 | 2 |
| prospective_controls | exploitation | combined_mlp_both | 0.214 | 0.305 | 2 |
| prospective_controls | exploitation | combined_logistic_both | 0.224 | 0.329 | 2 |
| prospective_controls | first_action0 | marginal | 0.251 | 0.501 | 7 |
| prospective_controls | first_action0 | pair | 0.251 | 0.500 | 7 |
| prospective_controls | first_action0 | nash | 0.178 | 0.301 | 7 |
| prospective_controls | first_action0 | family | 0.256 | 0.498 | 7 |
| prospective_controls | first_action0 | raw_logistic | 0.174 | 0.295 | 7 |
| prospective_controls | first_action0 | combined_mlp_both | 0.124 | 0.257 | 7 |
| prospective_controls | first_action0 | combined_logistic_both | 0.129 | 0.236 | 7 |
| prospective_controls | forgiveness | marginal | 0.242 | 0.309 | 3 |
| prospective_controls | forgiveness | pair | 0.261 | 0.312 | 3 |
| prospective_controls | forgiveness | family | 0.229 | 0.266 | 3 |
| prospective_controls | forgiveness | raw_logistic | 0.256 | 0.336 | 3 |
| prospective_controls | forgiveness | combined_mlp_both | 0.301 | 0.354 | 3 |
| prospective_controls | forgiveness | combined_logistic_both | 0.242 | 0.300 | 3 |
| prospective_controls | retaliation | marginal | 0.250 | 0.391 | 4 |
| prospective_controls | retaliation | pair | 0.245 | 0.368 | 4 |
| prospective_controls | retaliation | family | 0.176 | 0.233 | 4 |
| prospective_controls | retaliation | raw_logistic | 0.260 | 0.396 | 4 |
| prospective_controls | retaliation | combined_mlp_both | 0.167 | 0.239 | 4 |
| prospective_controls | retaliation | combined_logistic_both | 0.162 | 0.245 | 4 |

[All scores, support, calibration and uncertainty](results/overnight-20260910/controls/evaluation/scores.json).

Paired Brier improvement over the ordered focal/opponent mean (positive is better; descriptive 95% game/episode bootstrap intervals):

| Target | Predictor | Improvement | Interval |
|---|---|---:|---|
| action0 | raw_logistic | 0.055 | [-0.045, 0.148] |
| action0 | combined_mlp_both | 0.120 | [0.050, 0.183] |
| action0 | combined_logistic_both | 0.098 | [0.023, 0.166] |
| cooperation | raw_logistic | 0.018 | [-0.109, 0.100] |
| cooperation | combined_mlp_both | 0.157 | [0.092, 0.268] |
| cooperation | combined_logistic_both | 0.158 | [0.091, 0.269] |
| coordination | raw_logistic | -0.015 | [-0.094, 0.040] |
| coordination | combined_mlp_both | 0.045 | [0.027, 0.067] |
| coordination | combined_logistic_both | 0.044 | [0.027, 0.068] |

## Secondary baseline checks

These methods were designed after viewing the pilot and are separate from the original 15 methods and gate criteria. The payoff-dominant selector chooses a highest-payoff symmetric pure stage equilibrium when available; tied choices form a joint mixture of coordinated conventions. The event-weighted context mean matches the event-scoring objective for conditional targets. Prospective labels below require both a forecast-before-play audit and unchanged inputs throughout analysis. [Definitions and audit interfaces](secondary-baselines-cli.md).

### Pilot saved-fold sensitivity; retrospective

| Test | Target | Predictor | Brier ↓ | Log loss ↓ | Calibration ECE ↓ | Shape groups |
|---|---|---|---:|---:|---:|---:|
| extrapolation | action0 | nash | 0.243 | 1.318 | 0.160 | 6 |
| extrapolation | action0 | combined_mlp_both | 0.404 | 2.020 | 0.389 | 6 |
| extrapolation | action0 | combined_logistic_both | 0.329 | 1.021 | 0.230 | 6 |
| extrapolation | action0 | secondary_payoff_dominant | 0.243 | 1.318 | 0.160 | 6 |
| extrapolation | action0 | secondary_pair_event | 0.251 | 0.694 | 0.036 | 6 |
| extrapolation | cooperation | nash | 0.172 | 0.799 | 0.111 | 6 |
| extrapolation | cooperation | combined_mlp_both | 0.226 | 0.624 | 0.216 | 6 |
| extrapolation | cooperation | combined_logistic_both | 0.209 | 0.600 | 0.185 | 6 |
| extrapolation | cooperation | secondary_payoff_dominant | 0.172 | 0.799 | 0.111 | 6 |
| extrapolation | cooperation | secondary_pair_event | 0.551 | 1.451 | 0.623 | 6 |
| extrapolation | coordination | nash | 0.252 | 0.697 | 0.048 | 4 |
| extrapolation | coordination | combined_mlp_both | 0.465 | 1.852 | 0.464 | 4 |
| extrapolation | coordination | combined_logistic_both | 0.465 | 1.851 | 0.463 | 4 |
| extrapolation | coordination | secondary_payoff_dominant | 0.252 | 0.697 | 0.048 | 4 |
| extrapolation | coordination | secondary_pair_event | 0.467 | 3.475 | 0.464 | 4 |
| family | action0 | nash | 0.213 | 0.957 | 0.173 | 24 |
| family | action0 | combined_mlp_both | 0.211 | 0.744 | 0.137 | 24 |
| family | action0 | combined_logistic_both | 0.172 | 0.525 | 0.151 | 24 |
| family | action0 | secondary_payoff_dominant | 0.146 | 0.815 | 0.079 | 24 |
| family | action0 | secondary_pair_event | 0.253 | 0.699 | 0.049 | 24 |
| family | cooperation | nash | 0.209 | 0.859 | 0.220 | 18 |
| family | cooperation | combined_mlp_both | 0.261 | 0.723 | 0.201 | 18 |
| family | cooperation | combined_logistic_both | 0.310 | 1.087 | 0.244 | 18 |
| family | cooperation | secondary_payoff_dominant | 0.079 | 0.566 | 0.059 | 18 |
| family | cooperation | secondary_pair_event | 0.330 | 0.881 | 0.432 | 18 |
| family | coordination | nash | 0.231 | 0.655 | 0.255 | 14 |
| family | coordination | combined_mlp_both | 0.155 | 0.469 | 0.109 | 14 |
| family | coordination | combined_logistic_both | 0.162 | 0.485 | 0.128 | 14 |
| family | coordination | secondary_payoff_dominant | 0.146 | 0.569 | 0.066 | 14 |
| family | coordination | secondary_pair_event | 0.223 | 0.676 | 0.238 | 14 |

Combined-logistic Brier improvement over the payoff-dominant selector (positive is better):

| Test | Target | Improvement | Descriptive 95% interval |
|---|---|---:|---|
| extrapolation | action0 | -0.086 | [-0.204, 0.010] |
| extrapolation | cooperation | -0.038 | [-0.092, 0.005] |
| extrapolation | coordination | -0.213 | [-0.265, -0.169] |
| family | action0 | -0.025 | [-0.046, -0.005] |
| family | cooperation | -0.231 | [-0.385, -0.100] |
| family | coordination | -0.015 | [-0.035, 0.008] |

[Complete secondary scores and support](results/overnight-20260910/independent-analysis/pilot-secondary/scores.json) · [Input stability audit](results/overnight-20260910/independent-analysis/pilot-secondary/supervisor-audit.json).

### Combined training saved-fold sensitivity; retrospective

| Test | Target | Predictor | Brier ↓ | Log loss ↓ | Calibration ECE ↓ | Shape groups |
|---|---|---|---:|---:|---:|---:|
| extrapolation | action0 | nash | 0.249 | 1.642 | 0.206 | 17 |
| extrapolation | action0 | combined_mlp_both | 0.262 | 0.722 | 0.125 | 17 |
| extrapolation | action0 | combined_logistic_both | 0.340 | 1.260 | 0.332 | 17 |
| extrapolation | action0 | secondary_payoff_dominant | 0.249 | 1.642 | 0.206 | 17 |
| extrapolation | action0 | secondary_pair_event | 0.257 | 0.707 | 0.103 | 17 |
| extrapolation | cooperation | nash | 0.167 | 0.894 | 0.133 | 17 |
| extrapolation | cooperation | combined_mlp_both | 0.169 | 0.922 | 0.134 | 17 |
| extrapolation | cooperation | combined_logistic_both | 0.184 | 0.781 | 0.168 | 17 |
| extrapolation | cooperation | secondary_payoff_dominant | 0.167 | 0.894 | 0.133 | 17 |
| extrapolation | cooperation | secondary_pair_event | 0.610 | 1.690 | 0.675 | 17 |
| extrapolation | coordination | nash | 0.257 | 0.708 | 0.074 | 9 |
| extrapolation | coordination | combined_mlp_both | 0.251 | 0.696 | 0.031 | 9 |
| extrapolation | coordination | combined_logistic_both | 0.256 | 0.705 | 0.061 | 9 |
| extrapolation | coordination | secondary_payoff_dominant | 0.257 | 0.708 | 0.074 | 9 |
| extrapolation | coordination | secondary_pair_event | 0.410 | 1.239 | 0.399 | 9 |
| family | action0 | nash | 0.221 | 0.964 | 0.198 | 72 |
| family | action0 | combined_mlp_both | 0.187 | 0.559 | 0.089 | 72 |
| family | action0 | combined_logistic_both | 0.173 | 0.558 | 0.122 | 72 |
| family | action0 | secondary_payoff_dominant | 0.151 | 0.811 | 0.077 | 72 |
| family | action0 | secondary_pair_event | 0.252 | 0.698 | 0.051 | 72 |
| family | cooperation | nash | 0.221 | 0.914 | 0.234 | 52 |
| family | cooperation | combined_mlp_both | 0.243 | 0.685 | 0.140 | 52 |
| family | cooperation | combined_logistic_both | 0.302 | 1.371 | 0.230 | 52 |
| family | cooperation | secondary_payoff_dominant | 0.084 | 0.580 | 0.069 | 52 |
| family | cooperation | secondary_pair_event | 0.316 | 0.859 | 0.477 | 52 |
| family | coordination | nash | 0.231 | 0.656 | 0.262 | 42 |
| family | coordination | combined_mlp_both | 0.150 | 0.447 | 0.096 | 42 |
| family | coordination | combined_logistic_both | 0.159 | 0.463 | 0.105 | 42 |
| family | coordination | secondary_payoff_dominant | 0.146 | 0.544 | 0.070 | 42 |
| family | coordination | secondary_pair_event | 0.221 | 0.663 | 0.248 | 42 |

Combined-logistic Brier improvement over the payoff-dominant selector (positive is better):

| Test | Target | Improvement | Descriptive 95% interval |
|---|---|---:|---|
| extrapolation | action0 | -0.091 | [-0.157, -0.030] |
| extrapolation | cooperation | -0.016 | [-0.028, -0.005] |
| extrapolation | coordination | 0.002 | [-0.005, 0.008] |
| family | action0 | -0.022 | [-0.035, -0.009] |
| family | cooperation | -0.219 | [-0.323, -0.134] |
| family | coordination | -0.013 | [-0.029, 0.002] |

[Complete secondary scores and support](results/overnight-20260910/independent-analysis/development-secondary/scores.json) · [Input stability audit](results/overnight-20260910/independent-analysis/development-secondary/supervisor-audit.json).

### New games; secondary forecasts frozen before play

| Test | Target | Predictor | Brier ↓ | Log loss ↓ | Calibration ECE ↓ | Shape groups |
|---|---|---|---:|---:|---:|---:|
| prospective | action0 | nash | 0.227 | 0.915 | 0.208 | 21 |
| prospective | action0 | combined_mlp_both | 0.132 | 0.407 | 0.036 | 21 |
| prospective | action0 | combined_logistic_both | 0.138 | 0.418 | 0.075 | 21 |
| prospective | action0 | llm_zero_shot | 0.176 | 0.534 | 0.060 | 21 |
| prospective | action0 | llm_few_shot | 0.131 | 0.391 | 0.037 | 21 |
| prospective | action0 | llm_game_theory | 0.179 | 0.535 | 0.063 | 21 |
| prospective | action0 | secondary_payoff_dominant | 0.144 | 0.745 | 0.066 | 21 |
| prospective | action0 | secondary_pair_event | 0.251 | 0.696 | 0.084 | 21 |
| prospective | cooperation | nash | 0.218 | 0.975 | 0.225 | 14 |
| prospective | cooperation | combined_mlp_both | 0.059 | 0.236 | 0.015 | 14 |
| prospective | cooperation | combined_logistic_both | 0.058 | 0.207 | 0.021 | 14 |
| prospective | cooperation | llm_zero_shot | 0.203 | 0.606 | 0.275 | 14 |
| prospective | cooperation | llm_few_shot | 0.062 | 0.222 | 0.046 | 14 |
| prospective | cooperation | llm_game_theory | 0.214 | 0.644 | 0.304 | 14 |
| prospective | cooperation | secondary_payoff_dominant | 0.066 | 0.550 | 0.055 | 14 |
| prospective | cooperation | secondary_pair_event | 0.214 | 0.620 | 0.034 | 14 |
| prospective | coordination | nash | 0.213 | 0.617 | 0.216 | 12 |
| prospective | coordination | combined_mlp_both | 0.140 | 0.413 | 0.040 | 12 |
| prospective | coordination | combined_logistic_both | 0.140 | 0.411 | 0.038 | 12 |
| prospective | coordination | llm_zero_shot | 0.221 | 0.713 | 0.233 | 12 |
| prospective | coordination | llm_few_shot | 0.141 | 0.423 | 0.050 | 12 |
| prospective | coordination | llm_game_theory | 0.216 | 0.682 | 0.211 | 12 |
| prospective | coordination | secondary_payoff_dominant | 0.144 | 0.539 | 0.045 | 12 |
| prospective | coordination | secondary_pair_event | 0.193 | 0.574 | 0.023 | 12 |

Combined-logistic Brier improvement over the payoff-dominant selector (positive is better):

| Test | Target | Improvement | Descriptive 95% interval |
|---|---|---:|---|
| prospective | action0 | 0.005 | [-0.012, 0.020] |
| prospective | cooperation | 0.008 | [0.001, 0.018] |
| prospective | coordination | 0.005 | [-0.004, 0.016] |

[Complete secondary scores and support](results/overnight-20260910/secondary-baselines/full/prospective-comparison/scores.json) · [Input stability audit](results/overnight-20260910/secondary-baselines/full/prospective-comparison/supervisor-audit.json).

### New games and excluded pairing; secondary prospective test

| Test | Target | Predictor | Brier ↓ | Log loss ↓ | Calibration ECE ↓ | Shape groups |
|---|---|---|---:|---:|---:|---:|
| prospective_pair | action0 | nash | 0.233 | 0.947 | 0.239 | 21 |
| prospective_pair | action0 | combined_mlp_both | 0.136 | 0.475 | 0.073 | 21 |
| prospective_pair | action0 | combined_logistic_both | 0.140 | 0.430 | 0.072 | 21 |
| prospective_pair | action0 | secondary_payoff_dominant | 0.148 | 0.856 | 0.083 | 21 |
| prospective_pair | action0 | secondary_pair_event | 0.251 | 0.695 | 0.086 | 21 |
| prospective_pair | cooperation | nash | 0.182 | 0.980 | 0.211 | 14 |
| prospective_pair | cooperation | combined_mlp_both | 0.076 | 0.571 | 0.077 | 14 |
| prospective_pair | cooperation | combined_logistic_both | 0.074 | 0.310 | 0.076 | 14 |
| prospective_pair | cooperation | secondary_payoff_dominant | 0.071 | 0.900 | 0.080 | 14 |
| prospective_pair | cooperation | secondary_pair_event | 0.242 | 0.678 | 0.053 | 14 |
| prospective_pair | coordination | nash | 0.225 | 0.643 | 0.188 | 12 |
| prospective_pair | coordination | combined_mlp_both | 0.179 | 0.547 | 0.050 | 12 |
| prospective_pair | coordination | combined_logistic_both | 0.179 | 0.558 | 0.051 | 12 |
| prospective_pair | coordination | secondary_payoff_dominant | 0.184 | 1.080 | 0.095 | 12 |
| prospective_pair | coordination | secondary_pair_event | 0.209 | 0.610 | 0.051 | 12 |

Combined-logistic Brier improvement over the payoff-dominant selector (positive is better):

| Test | Target | Improvement | Descriptive 95% interval |
|---|---|---:|---|
| prospective_pair | action0 | 0.009 | [-0.015, 0.039] |
| prospective_pair | cooperation | -0.003 | [-0.014, 0.005] |
| prospective_pair | coordination | 0.004 | [-0.017, 0.027] |

[Complete secondary scores and support](results/overnight-20260910/secondary-baselines/excluded_pair/prospective-comparison/scores.json) · [Input stability audit](results/overnight-20260910/secondary-baselines/excluded_pair/prospective-comparison/supervisor-audit.json).

### New games and excluded model; secondary prospective test

| Test | Target | Predictor | Brier ↓ | Log loss ↓ | Calibration ECE ↓ | Shape groups |
|---|---|---|---:|---:|---:|---:|
| prospective_model | action0 | nash | 0.229 | 0.942 | 0.210 | 21 |
| prospective_model | action0 | combined_mlp_both | 0.138 | 0.470 | 0.043 | 21 |
| prospective_model | action0 | combined_logistic_both | 0.144 | 0.440 | 0.074 | 21 |
| prospective_model | action0 | secondary_payoff_dominant | 0.148 | 0.838 | 0.067 | 21 |
| prospective_model | action0 | secondary_pair_event | 0.252 | 0.696 | 0.087 | 21 |
| prospective_model | cooperation | nash | 0.207 | 1.011 | 0.208 | 14 |
| prospective_model | cooperation | combined_mlp_both | 0.075 | 0.546 | 0.063 | 14 |
| prospective_model | cooperation | combined_logistic_both | 0.075 | 0.316 | 0.068 | 14 |
| prospective_model | cooperation | secondary_payoff_dominant | 0.073 | 0.755 | 0.059 | 14 |
| prospective_model | cooperation | secondary_pair_event | 0.234 | 0.660 | 0.046 | 14 |
| prospective_model | coordination | nash | 0.218 | 0.627 | 0.208 | 12 |
| prospective_model | coordination | combined_mlp_both | 0.153 | 0.466 | 0.030 | 12 |
| prospective_model | coordination | combined_logistic_both | 0.154 | 0.470 | 0.035 | 12 |
| prospective_model | coordination | secondary_payoff_dominant | 0.160 | 0.740 | 0.067 | 12 |
| prospective_model | coordination | secondary_pair_event | 0.199 | 0.587 | 0.024 | 12 |

Combined-logistic Brier improvement over the payoff-dominant selector (positive is better):

| Test | Target | Improvement | Descriptive 95% interval |
|---|---|---:|---|
| prospective_model | action0 | 0.004 | [-0.012, 0.020] |
| prospective_model | cooperation | -0.001 | [-0.008, 0.005] |
| prospective_model | coordination | 0.007 | [-0.007, 0.023] |

[Complete secondary scores and support](results/overnight-20260910/secondary-baselines/excluded_model/prospective-comparison/scores.json) · [Input stability audit](results/overnight-20260910/secondary-baselines/excluded_model/prospective-comparison/supervisor-audit.json).

### Payoff and presentation controls; secondary prospective test

| Test | Target | Predictor | Brier ↓ | Log loss ↓ | Calibration ECE ↓ | Shape groups |
|---|---|---|---:|---:|---:|---:|
| prospective_controls | action0 | nash | 0.183 | 0.737 | 0.200 | 7 |
| prospective_controls | action0 | combined_mlp_both | 0.130 | 0.404 | 0.077 | 7 |
| prospective_controls | action0 | combined_logistic_both | 0.153 | 0.459 | 0.147 | 7 |
| prospective_controls | action0 | secondary_payoff_dominant | 0.140 | 0.643 | 0.116 | 7 |
| prospective_controls | action0 | secondary_pair_event | 0.251 | 0.695 | 0.145 | 7 |
| prospective_controls | cooperation | nash | 0.159 | 0.622 | 0.185 | 5 |
| prospective_controls | cooperation | combined_mlp_both | 0.067 | 0.228 | 0.031 | 5 |
| prospective_controls | cooperation | combined_logistic_both | 0.066 | 0.227 | 0.027 | 5 |
| prospective_controls | cooperation | secondary_payoff_dominant | 0.073 | 0.457 | 0.058 | 5 |
| prospective_controls | cooperation | secondary_pair_event | 0.224 | 0.641 | 0.013 | 5 |
| prospective_controls | coordination | nash | 0.254 | 0.703 | 0.289 | 4 |
| prospective_controls | coordination | combined_mlp_both | 0.141 | 0.460 | 0.028 | 4 |
| prospective_controls | coordination | combined_logistic_both | 0.141 | 0.426 | 0.036 | 4 |
| prospective_controls | coordination | secondary_payoff_dominant | 0.163 | 0.640 | 0.094 | 4 |
| prospective_controls | coordination | secondary_pair_event | 0.185 | 0.558 | 0.006 | 4 |

Combined-logistic Brier improvement over the payoff-dominant selector (positive is better):

| Test | Target | Improvement | Descriptive 95% interval |
|---|---|---:|---|
| prospective_controls | action0 | -0.013 | [-0.056, 0.019] |
| prospective_controls | cooperation | 0.007 | [-0.003, 0.022] |
| prospective_controls | coordination | 0.021 | [-0.004, 0.063] |

[Complete secondary scores and support](results/overnight-20260910/secondary-baselines/full/controls-comparison/scores.json) · [Input stability audit](results/overnight-20260910/secondary-baselines/full/controls-comparison/supervisor-audit.json).


## Payoff and presentation sensitivity

Changes are percentage points in the observed event rate. Label swaps compare balanced pilot trials after undoing the action permutation. Scale, offset, and text variants compare later trials with historical pilot anchors, matching game and ordered model/opponent context. There is no concurrent untransformed baseline or shared random seed, so calendar or serving changes can contribute. Intervals resample whole source shapes; an interval spanning zero does not establish invariance.

| Comparison | Target | Change (pp) | Descriptive 95% interval | Shapes | Matched contexts |
|---|---|---:|---|---:|---:|
| Swapped − unswapped labels | action0 | -8.15 | [-16.87, -1.35] | 24 | 381 |
| Swapped − unswapped labels | cooperation | -1.52 | [-4.24, +1.70] | 18 | 285 |
| Swapped − unswapped labels | coordination | +0.23 | [-2.63, +3.06] | 14 | 221 |
| Payoffs ×3 − original | action0 | +0.01 | [-3.46, +4.15] | 7 | 110 |
| Payoffs ×3 − original | cooperation | +4.35 | [+1.06, +9.23] | 5 | 78 |
| Payoffs ×3 − original | coordination | -3.71 | [-8.35, +0.94] | 4 | 62 |
| Payoffs +10 − original | action0 | -1.77 | [-5.15, +0.42] | 7 | 110 |
| Payoffs +10 − original | cooperation | -1.39 | [-4.22, +0.87] | 5 | 78 |
| Payoffs +10 − original | coordination | +0.49 | [-1.64, +3.75] | 4 | 62 |
| Abstract text − matrix | action0 | -4.47 | [-10.11, -0.29] | 7 | 110 |
| Abstract text − matrix | cooperation | -0.04 | [-4.50, +4.72] | 5 | 78 |
| Abstract text − matrix | coordination | -1.10 | [-7.83, +5.62] | 4 | 62 |

The controls reuse seven known shapes; mutual cooperation is supported on five and coordination on four. Full forecast scores and matched behavioral changes use different support rules. Conditional-rate changes can also reflect different opportunity sets. [Control interpretation, predictor sensitivity, and per-variant accuracy](controls-interpretation.md).

### Forecast accuracy by control variant

Descriptive Brier point scores from the saved forecasts, preserving the original common supported observations. This breakdown was added after collection; it does not refit predictors or supply new significance tests. Seven source shapes support action choice, five cooperation, and four coordination.

| Target | Predictor | Scale ×3 | Offset +10 | Abstract text |
|---|---|---:|---:|---:|
| action0 | Game-family mean | 0.2285 | 0.2259 | 0.2275 |
| action0 | Normalized-feature logistic | 0.1398 | 0.1411 | 0.1364 |
| action0 | Combined logistic + identities | 0.1483 | 0.1760 | 0.1348 |
| action0 | Combined MLP + identities | 0.1245 | 0.1375 | 0.1293 |
| action0 | Payoff-dominant selector (secondary) | 0.1488 | 0.1354 | 0.1347 |
| cooperation | Game-family mean | 0.0691 | 0.0632 | 0.0679 |
| cooperation | Normalized-feature logistic | 0.0717 | 0.0637 | 0.0698 |
| cooperation | Combined logistic + identities | 0.0660 | 0.0618 | 0.0700 |
| cooperation | Combined MLP + identities | 0.0684 | 0.0622 | 0.0699 |
| cooperation | Payoff-dominant selector (secondary) | 0.0802 | 0.0652 | 0.0741 |
| coordination | Game-family mean | 0.1389 | 0.1398 | 0.1403 |
| coordination | Normalized-feature logistic | 0.1416 | 0.1390 | 0.1416 |
| coordination | Combined logistic + identities | 0.1409 | 0.1418 | 0.1411 |
| coordination | Combined MLP + identities | 0.1395 | 0.1395 | 0.1428 |
| coordination | Payoff-dominant selector (secondary) | 0.1471 | 0.1693 | 0.1716 |

[Complete per-variant scores, support, and derivation](results/overnight-20260910/independent-analysis/control-variant-breakdown/scores.json).


## Inline figures

The transfer heatmaps show the same fixed combined-logistic predictor against the ordered context mean. Green means improvement over that baseline; comparisons with the original and secondary equilibrium selectors are reported separately. Intervals are descriptive and conditional on fixed fitted forecasts. Different holdouts answer different transfer questions.

![primary-transfer-development](results/overnight-20260910/report-figures/primary-transfer-development.png)

![primary-transfer-overview](results/overnight-20260910/report-figures/primary-transfer-overview.png)

![primary-transfer-pilot](results/overnight-20260910/report-figures/primary-transfer-pilot.png)

![primary-transfer-prospective](results/overnight-20260910/report-figures/primary-transfer-prospective.png)

![model family](results/overnight-20260910/primary-pilot/diagnostics/model_family.png)

![model opponent](results/overnight-20260910/primary-pilot/diagnostics/model_opponent.png)

![replicate agreement cell](results/overnight-20260910/primary-pilot/diagnostics/replicate_agreement_cell.png)

![replicate agreement game](results/overnight-20260910/primary-pilot/diagnostics/replicate_agreement_game.png)

![action labels changes](results/overnight-20260910/primary-pilot/label-analysis/action_labels_changes.png)

![action labels paired games](results/overnight-20260910/primary-pilot/label-analysis/action_labels_paired_games.png)

![comparison](results/overnight-20260910/pilot/evaluation/comparison.png)

![comparison](results/overnight-20260910/development/evaluation/comparison.png)

![abstract text changes](results/overnight-20260910/controls/sensitivity/abstract_text_changes.png)

![abstract text paired games](results/overnight-20260910/controls/sensitivity/abstract_text_paired_games.png)

![action labels changes](results/overnight-20260910/controls/sensitivity/action_labels_changes.png)

![action labels paired games](results/overnight-20260910/controls/sensitivity/action_labels_paired_games.png)

![offset10 changes](results/overnight-20260910/controls/sensitivity/offset10_changes.png)

![offset10 paired games](results/overnight-20260910/controls/sensitivity/offset10_paired_games.png)

![scale3 changes](results/overnight-20260910/controls/sensitivity/scale3_changes.png)

![scale3 paired games](results/overnight-20260910/controls/sensitivity/scale3_paired_games.png)

![brier-overview](results/overnight-20260910/report-figures/secondary/controls/brier-overview.png)

![secondary-uncertainty](results/overnight-20260910/report-figures/secondary/controls/secondary-uncertainty.png)

![brier-overview](results/overnight-20260910/report-figures/secondary/development/brier-overview.png)

![secondary-uncertainty](results/overnight-20260910/report-figures/secondary/development/secondary-uncertainty.png)

![brier-overview](results/overnight-20260910/report-figures/secondary/model/brier-overview.png)

![secondary-uncertainty](results/overnight-20260910/report-figures/secondary/model/secondary-uncertainty.png)

![brier-overview](results/overnight-20260910/report-figures/secondary/pair/brier-overview.png)

![secondary-uncertainty](results/overnight-20260910/report-figures/secondary/pair/secondary-uncertainty.png)

![brier-overview](results/overnight-20260910/report-figures/secondary/pilot/brier-overview.png)

![secondary-uncertainty](results/overnight-20260910/report-figures/secondary/pilot/secondary-uncertainty.png)

![brier-overview](results/overnight-20260910/report-figures/secondary/prospective/brier-overview.png)

![secondary-uncertainty](results/overnight-20260910/report-figures/secondary/prospective/secondary-uncertainty.png)

![broad-target-scores](results/overnight-20260910/report-figures/prospective/controls/broad-target-scores.png)

![broad-target-calibration](results/overnight-20260910/report-figures/prospective/controls/broad-target-calibration.png)

![broad-target-scores](results/overnight-20260910/report-figures/prospective/full/broad-target-scores.png)

![broad-target-calibration](results/overnight-20260910/report-figures/prospective/full/broad-target-calibration.png)

![broad-target-scores](results/overnight-20260910/report-figures/prospective/model/broad-target-scores.png)

![broad-target-calibration](results/overnight-20260910/report-figures/prospective/model/broad-target-calibration.png)

![broad-target-scores](results/overnight-20260910/report-figures/prospective/numerical/broad-target-scores.png)

![broad-target-calibration](results/overnight-20260910/report-figures/prospective/numerical/broad-target-calibration.png)

![broad-target-scores](results/overnight-20260910/report-figures/prospective/pair/broad-target-scores.png)

![broad-target-calibration](results/overnight-20260910/report-figures/prospective/pair/broad-target-calibration.png)

## Interpretation and artifacts

Completion of the core gate sequence does not mean every checklist item in the broader plan was run. Controlled training-composition and fixed-game rollout-label-noise ablations remain unrun; per-condition empirical confidence intervals are not exported. Counts, variances, and aggregate game/episode uncertainty are available. The global parameter-region splits change family composition rather than isolate within-family extrapolation. [The coverage audit](plan-coverage.md) records these limitations and the Gate 8 exclusions.

The literature already contains learned strategic-behavior predictors and few-shot agent identification. The narrower question here is transfer of pre-interaction, payoff-based forecasts in autonomous repeated cross-play. Grouped validation and prospective forecasts are reported separately; conditional rates with no opportunities remain undefined. These predictors estimate expected event probabilities and rates, not a joint distribution of complete phenotype vectors or trajectories. For conditional targets, logistic training weights opportunity counts while the mean baselines and rate regressors weight eligible row rates. Conditional Brier gains can therefore partly reflect different training objectives; they do not alone isolate the added value of game structure. The primary action, mutual-cooperation and coordination targets have fixed eight-round opportunities and avoid this denominator-weighting discrepancy. Retaliation and forgiveness are observational summaries. Exploitation denotes a specified asymmetric payoff-extraction event and does not establish intent.

[Frozen player source](results/overnight-20260910/source-manifest.json) · [Gate records](results/overnight-20260910/gates.json) · [Numerical methods and reproduction](modeling-cli.md).

[Final completion, chronology, and budget audit](results/overnight-20260910/independent-analysis/completion-audit.json).

[Exportable figure inventory: PNG, SVG, and PDF](results/overnight-20260910/report-figures/figure-inventory-final.json).
