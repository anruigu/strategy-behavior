# Replicated general-game study

This version implements the next study after the 12-family diagnostic: complete executable game specifications, crossed world seeds and seats, repeated independent model play, expanded operational behavior labels, learning curves against 4/8/16-shot prompting, and four prospective new-family tests.

[Live viewer](http://localhost:42329/general/replicated) · [Study protocol](study/protocol.json) · [Final report](study/REPORT.md) · [Machine-readable results](study/summary.json)

**Completed:** 592 new episodes, 736 including historical data, and 3,755 focal actions. Few-shot remains ahead on win prediction: at 440 training episodes, four-shot Brier is .1867/.2165 on parameter/new-family tests, versus linear .2073/.2909 and learned correction .2087/.3039. A secondary pooled four-shot control reaches .1657/.2170. The current learning curves favor fixing transfer and testing training-family breadth before increasing collection volume. All 5,608 new native transitions and 3,607 inference attempts are audited; cost was $27.9994 with no unresolved billing.

The catalog has 16 families / 57 configurations, adding native Iterated Ultimatum, Two-Thirds Average, Secretary and Memory. The 114 fresh seeded instances have 85 distinct openings. Scripted validation covers 983 transitions and is never counted as observed model behavior. The historical v1 artifacts remain separate and unchanged.

| Cohort | Families | New episodes | Repetitions per exact condition |
|---|---:|---:|---:|
| Lower/base training parameters | PD, Pig, Blotto, Auction | 320 | 5 |
| Higher-parameter prospective test | Same four anchors | 160 | 5 |
| Prospective family transfer | Four new families | 112 | 2 |

Each condition specifies configuration, world seed, focal seat, model and prompt. Seeds 6200 and 6201 cross every focal seat and both player models independently. Fresh collection uses the normal prompt. Independent LLM calls supply the repetitions; an LLM sampling seed is not set. Each model plays against the frozen scripted policy using only that policy's allowed observations. Single-player games have no opponent.

Learning curves use 120 eligible historical episodes, then 248 and 440 total training episodes. All higher anchor configurations and all four new families are excluded from training and retrieval at every size. Training growth adds depth in four anchors, not a controlled increase in family breadth. The 88 prospective conditions are fixed across all three sizes. Test predictions and fitted artifacts must be frozen before any test-player call.

Eight methods are retained at each size: training mean; fixed structured + TF–IDF logistic/Ridge learner; 4-, 8-, and 16-shot Kimi forecasts; and a learned Ridge correction to each shot count. The primary comparison is corrected-4 versus few-4. Corrections train on family-excluded calibration forecasts of normal-prompt condition means. Fixed hyperparameters and family-balanced weights are recorded in `predict.py`; no test-outcome tuning or language-encoder fine-tuning is performed. Example sets are nested and contain distinct observable inputs. Shared batches contain up to four queries; each query has its own examples and supported targets.

A primary demonstration reports one exact world's repeated mean/count. If several seeds have identical visible inputs, retrieval keeps one such condition. A separate control in `pooled_fewshot.py` pools every training label/count for each identical visible input at 440 episodes, preserving the exact original demonstration IDs/order for 4/8/16-shot prompting. Its 264 forecasts are explicitly secondary: the pooling rule and requests were introduced after test play began, using training inputs/labels only. The 2,112 original test predictions and their prospective freeze remain unchanged. Even with pooling, the learner uses all groups while each prompt contains at most 16 examples; this comparison does not isolate architecture from label access.

The player environment is unchanged TextArena 0.7.4. Forecasters receive public constructor values, exact focal opening messages, and normalized mechanics/opponent descriptions. The complete native engine and collection source are archived in `data/`; hidden opponent realizations and future events stay in evaluator files. The normalized specification is a compact rendering, not a claim that prose alone reproduces every engine detail.

`data/mechanics.v2.json` corrects the initial auction-bid wording, value distributions, Liar's Dice invalid-action handling and Pig horizon timing. Every final stage uses this same revision. Earlier 120-episode forecasts are retained under `study/prediction/preflight/spec-v1-n120`, excluded from scores and included in cost accounting. Collection code and original data manifest did not change. The correction preceded all prospective test play.

Operational labels have explicit family support and opportunity counts. They include win/full solution, native invalidity, PD cooperation, Pig risk, Blotto concentration, auction capital use, dice challenges, negotiation offers/acceptance, ultimatum offers/acceptance, normalized guesses, secretary selection timing and public-memory use. Invalid or ineligible decisions do not silently become zero behavioral rates. Fixed-role Ultimatum support is masked before outcomes. Incomplete/censored episodes have no completed-episode target. These labels do not measure intent or a general psychological trait.

Reproduction from the repository root:

```bash
PY=/shared/allie/venvs/hole/bin/python
# Read-only/native audit and report rebuild; no inference calls:
$PY -B -m prediction.general_games.scaleup_v2.readout
$PY -B -m pytest prediction/general_games/scaleup_v2 -q

# Collection order used for this study (do not duplicate active collectors):
$PY -B -m prediction.general_games.scaleup_v2.collection collect --phase training --workers 8
$PY -B -m prediction.general_games.scaleup_v2.collection export --phase training
# For each size 120, 248 and 440, once its training rows are complete:
$PY -B -m prediction.general_games.scaleup_v2.predict prepare --size 120
$PY -B -m prediction.general_games.scaleup_v2.predict collect --size 120 --workers 4
$PY -B -m prediction.general_games.scaleup_v2.predict fit --size 120
# After all three sizes are fitted:
$PY -B -m prediction.general_games.scaleup_v2.predict freeze
$PY -B -m prediction.general_games.scaleup_v2.collection collect --phase test --workers 8
$PY -B -m prediction.general_games.scaleup_v2.collection export --phase test
# Separate secondary pooling control; its own manifest refuses overwrite:
$PY -B -m prediction.general_games.scaleup_v2.pooled_fewshot prepare
$PY -B -m prediction.general_games.scaleup_v2.pooled_fewshot collect --workers 4
$PY -B -m prediction.general_games.scaleup_v2.pooled_fewshot export
```

`prepare` and `freeze` deliberately refuse to overwrite their frozen artifacts. Collection resumes checkpoints through native replay and raw-call checks, with at most three inference attempts per decision or forecast batch. Actor requests cap output at 16,384 tokens; Kimi forecasts cap at 8,192. All new calls share a $75 global ledger, with $50 ceilings for training, prediction and test stages. Native invalid submissions remain observed actions. Transport/empty/truncated calls are retained as inference failures. The 128-total/64-focal action cap is external censoring, never a relabeled native loss.

`study/all-episodes.jsonl` and `all-actions.jsonl` combine the 144 historical episodes with this study's 592 new episodes. Use the `inputs` object for pre-episode learning; outer fields, `*.evaluator.json`, raw calls, native checkpoints and viewer state inspectors contain outcomes or hidden evaluator information. Exact-condition groups and opening groups must remain together in any further split. Comparing absolute scores with Gameable Games is not a controlled comparison because opponents, horizons and supported targets differ.
