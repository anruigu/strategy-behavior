# Improving prediction with transformer representations

Started 2026-09-10. User authorization: write this plan and execute it. **All experiment training, including baseline calibration and prediction-head fitting, must be submitted through the [Fleet Training API](https://api.ft.flt.build/v1/docs).** Local work prepares data, audits artifacts, scores saved forecasts, and renders the report. The earlier authorization for economical evaluation spending and independent agents continues to apply.

## Question and starting evidence

Can a pretrained transformer representation, or supervised adaptation of that representation, improve pre-interaction forecasts of repeated-game behavior beyond numerical features, family averages, calibrated equilibrium selection, and few-shot prompting?

The [first study](../../prediction/REPORT.md) establishes predictable behavior but weak structural transfer. Its 72 training shapes contain 1,918 valid matches. Its later 21 shapes and seven-shape control panel have already been inspected; results on them are development evidence for this follow-up, not a fresh confirmatory test. We will preserve the original run and report.

The promising observation is that three behavioral examples substantially improved prompted forecasts. The limitation is that family averages and equilibrium selection explain much of the broad-target signal. More expressive predictors should therefore be judged against those stronger baselines. Four player models and weak identity effects currently provide insufficient motivation for a separate agent-embedding research program; this run concentrates on representations of the game and prediction context.

## Fixed experimental scope

- Retain the original four players, eight simultaneous rounds, public history, own-total-points objective, sampling settings, neutral labels, and mechanical measurements.
- Primary targets: canonical action0, mutual cooperation where defined, and strict-equilibrium coordination where defined. Predict probabilities/rates, with observed successes and opportunity counts as supervision. No-opportunity targets remain missing. Conditional retaliation/forgiveness/extraction remain outside the primary improvement claim.
- Primary training data remain the original fixed 72-shape snapshot. Both focal rows and all repetitions of a canonical shape stay together in game splits. Existing later outcomes may diagnose the frozen candidate set, but will not silently become a new test.
- Inputs contain the payoff matrix, fixed decision protocol, and declared focal/opponent identities. They omit outcomes from the target encounter, game IDs, and named family labels. The family label is permitted only in the explicit taxonomy baseline and split construction.
- Start with the publicly available **Qwen/Qwen3-4B** pretrained/post-trained checkpoint, pinning its exact revision before extraction or fitting. Its documented decoder architecture is supported by Transformers; [model card](https://huggingface.co/Qwen/Qwen3-4B). A technical availability or memory failure may justify a smaller checkpoint, recorded before inspecting comparative results.

## Candidate predictors

| Candidate | Purpose |
|---|---|
| Ordered-context and game-family rates | Preserve the strong empirical comparators. |
| Original and payoff-dominant equilibrium selectors | Retain interpretable mathematical references. |
| Training-calibrated payoff-dominant selector | Give generic probability smoothing credit; fit calibration using training data only. |
| Normalized-feature and combined-feature logistic predictors | Reproduce the useful numerical comparators, including the known raw-offset weakness. |
| Frozen transformer embeddings + a regularized probability head | Test whether pretrained representations improve prediction without changing the transformer. |
| The same transformer with a small LoRA adapter and probability head | Test supervised representation adaptation. Fit fractional binomial targets directly rather than rounding empirical probabilities into synthetic labels. |
| Kimi three-example few-shot forecasts | Retain the strong prompted comparator with examples restricted to the relevant training partition. |

The LoRA predictor is a fine-tuned language-model backbone with supervised probability outputs. It is not an experiment in fine-tuning the game-playing agents. Architecture, pooling, adapter targets/rank, optimization, seeds, epoch/checkpoint rule, and training-only tuning grids will be fixed in a machine-readable protocol after a technical preflight and before comparative improvement scores are examined. Use a compact candidate set; do not launch an open-ended architecture search. Frozen feature extraction may share a cache across folds because it never uses behavioral labels; any learned scaling, dimension reduction, calibration, or head must be fitted within the training fold.

## Corrected evaluation

1. **Leave-one-family-out:** all seven families, with every shape and interaction from the held family excluded from training. This is the central structural test.
2. **Within-family interpolation:** define payoff-coordinate regions separately inside each family; train outer regions and test the middle. Each scored family must be present in training and bracket the test coordinate. Coordinate selection and boundaries use payoff metadata only, including a documented nondegenerate coordinate for equal-diagonal families.
3. **Within-family extrapolation:** for each family, train the lower and middle thirds and test the upper third of the same declared coordinate. Preserve family coverage rather than mixing the previous global-region composition shift into the test.
4. **Existing 21-shape development cohort:** apply the full 72-shape fits without calling it a new prospective experiment.
5. **Fresh prospective cohort:** generate **28 new canonical shapes, four per family**, disjoint from all 93 shapes already observed. Run all ten unordered player pairs and two opposite-label trials: **560 matches**. Freeze full-training forecasts and family-excluded forecasts before any new player rollout. The same outcomes support those two distinct prediction settings. Family-excluded few-shot forecasts must also exclude that family's examples.

Save exact folds, row/group memberships, training-only statistics, fitting source, checkpoint hashes, forecasts, and timing evidence. Fresh player rollouts cannot begin until every required forecast is complete or an explicit technical exclusion has been recorded without viewing fresh outcomes. Never replace missing/invalid forecasts with a favorable fallback silently. Preserve numerical-only and all-method common-support scores when supports differ.

## Scoring and decisions

Use game-equal event Brier and log loss, calibration summaries, and rate error. Preserve entire episodes and both focal roles in uncertainty calculations. Bootstrap intervals condition on the fitted predictors and are descriptive; one or two optimization seeds do not quantify unrestricted training uncertainty. Report target-specific shape/episode/opportunity counts and all fixed candidates.

Before fresh collection, require valid forecasts, intact provenance, sufficient training support, and successful optimization diagnostics. A fixed fresh cohort is justified by positive **or inconclusive** comparative development results. Stop additional inference if both transformer approaches are consistently worse than the strongest applicable baselines and descriptive upper bounds exclude a practically useful gain across the broad targets. An interval crossing zero alone is not a negative result.

For a positive improvement claim, look for a prespecified meaningful paired gain (reference threshold **0.005 Brier**) on structural holdouts over strong empirical and calibrated-theory baselines, supported by log loss/calibration rather than an extreme-probability artifact. Compare the frozen and adapted representations directly. Separate useful within-family prediction, structural transfer, and model-specific characterization; success at the first does not establish the others. Report a negative or inconclusive outcome without escalating capacity to search for a positive result.

## Execution and resources

Use the training service's authenticated identity check and manifest preview, then submit custom jobs through `POST /v1/runs`. Save the exact submissions, assigned names, image, resource requests, status history, logs, and artifacts. Use a single GPU initially, backfill priority, no privileged containers, checkpointed work, and explicit runtime limits. Training may be batched within a job to avoid repeated weight loading and idle GPU reservations. Cancel only this experiment's jobs if they exceed limits or cannot make useful progress.

Start with a **six GPU-hour ceiling** for the bounded training comparison, including technical retries. Record actual GPU allocation/time separately: the API does not currently expose dollar billing in its public schema. Keep metered evaluation calls within a **$200 initial stage cap**, with the prior $42.21 commitment counted when checking the existing $3,000 overall spending authorization. The ceiling is not a spending target. Any training-dollar estimate is a planning estimate, not a quoted service price.

All durable code, data, caches, job output, downloads, and temporary artifacts belong under `/shared/allie`. The training cluster may mount that same storage as `/mnt/sfs`; use its `allie/` subtree and record the path mapping. Never use the default `/mnt/sfs/jobs` output directory for this task or write task state under `/home`. Keep credentials out of commands, logs, reports, and source bundles.

Run root: `prediction/results/improve-20260910/`. New implementation: `prediction/improve/`. The first study's scientific sources, forecasts, scores, and completion audit remain intact. Separate agents may implement transformer training, design/baseline evaluation, and independent audits; the root agent owns API submission and the final study disposition.

## Deliverables and completion

- This plan and a frozen machine-readable protocol with any technical amendments.
- Actual Fleet training jobs, reusable checkpoints/embedding caches, and complete status/cost-time records.
- Corrected split and baseline analyses; frozen versus adapted transformer comparisons.
- Audited fresh prospective results if the stated gate proceeds.
- `prediction/IMPROVEMENT-REPORT.md`, with inline figures, all candidate results, uncertainty, failed or unrun conditions, and a decision about further work.

Writing code or submitting a job does not complete this task. Continue through training, evaluation, the stated prospective gate, and final reporting, unless a technical dependency prevents progress or the explicit negative-result rule warrants stopping expansion.

## Frozen implementation choices

The model snapshot is pinned to Qwen/Qwen3-4B revision `1cfa9a7208912126459214e8b04321603b3df60c`, with every downloaded file hashed. The [transformer protocol](../../prediction/results/improve-20260910/transformer-protocol.json) specifies last-token representations, no generated reasoning/output tokens, a 512-token limit that rejects overflow, training-only standardization, and a regularized three-probability head. LoRA uses rank 8 on query/value projections, two epochs, adapter learning rate 0.0002, and the final checkpoint. It starts from the same fold's frozen head. One optimization seed means that confidence intervals do not measure training-seed variability.

The [baseline protocol](../../prediction/results/improve-20260910/baseline-protocol.json) fixes a compact, training-only regularization grid and monotone calibration of the payoff-dominant selector. The [data audit](../../prediction/results/improve-20260910/data/provenance.json) records 1,152 training contexts and 336 earlier development contexts; aggregation preserves original counts and episode mappings.

All new prompted forecasts and player calls share one **$150** inference ledger, a stricter operational limit than the initial $200 cap. A separate authorization ledger imports the prior $42.21 commitment without changing the earlier study's ledger. GPU allocations have explicit watchdog deadlines; startup/queue time is conservatively included when enforcing the six-hour bound.
