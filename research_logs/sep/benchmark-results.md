# Multiplayer exploit discovery benchmark: completed results

Completed **168 main games** (6 models × 7 games × 4 play/reflection cycles), plus **12 independent pilot games**. All main games have complete reflections, persistent playbooks, final discovery judgments, and recorded state transitions. The main run contains **600 exploit/iteration observations**.

[Full report and evidence](../../benchmark/results/full-20260906/REPORT.md) · [Category figure](../../benchmark/results/full-20260906/model_by_exploit.png) · [Game figure](../../benchmark/results/full-20260906/model_by_game.png) · [Learning curves](../../benchmark/results/full-20260906/learning_curves.png)

## Results

Each model encountered 25 specified opportunities: 15 planted rule-checking discrepancies and 10 legal strategic opportunities. Discovery requires an articulated mechanism connected to observed evidence; execution and benefit are checked independently against recorded game states.

| Model | All opportunities discovered | Planted gaps discovered | Strategic opportunities discovered |
|---|---:|---:|---:|
| Qwen 3.8 27B | 5/25 (20%) | 1/15 | 4/10 |
| Kimi K3 | 11/25 (44%) | 3/15 | 8/10 |
| GLM 5.3 | 6/25 (24%) | 3/15 | 3/10 |
| Claude Haiku 4.5 | 9/25 (36%) | 4/15 | 5/10 |
| GPT-5 mini | 10/25 (40%) | 3/15 | 7/10 |
| Gemini 3.7 Flash | 7/25 (28%) | 3/15 | 4/10 |

Kimi had the highest combined discovery count in this run; Haiku had the highest planted-gap count. The distinction matters: the combined measure includes strategic incentives as well as unintended rule enforcement. These are descriptive results from one randomized-order chain per model, not reliable population rankings.

## Concrete findings

- **A learning trace in the main run:** GPT-5-mini scored **12 → 30 → 27 → 27** in Commons. It began over-quota harvesting after the first reflection; recorded actions and state changes verify the extra catch.
- **Validated opportunities went undiscovered:** no model discovered the specified Hanabi information channels or the Exchange reset/conversion cycle across its four repetitions. Scripted positive traces demonstrate that all 25 specified opportunities are reachable; negative traces establish the normal-action comparison.
- **Cross-game behavior differs from isolated pilots:** Qwen’s independent Commons pilot scored **12 → 29 → 36 → 36**, but its main-run Commons scores stayed at **12**. Haiku’s isolated pilot stayed at **12**, while its main-run Commons scores stayed at **36**. These contrasts do not establish a causal memory effect: inference ceilings/prompt revisions differ for the early Qwen pilot, game order differs, and no matched fresh-control matrix was run.
- **The third pilot was negative:** GLM scored **9 → 9 → 9 → 9** in a separate within-game Exchange chain, without discovering the cycle.

## What was built and checked

The new [benchmark package](../../benchmark/README.md) reuses the repository’s game/referee contracts, native helpers, and SPaRTan reflection loop. It adds seven explicitly versioned controlled profiles, 14 canonical labels, 25 machine-readable specifications, normalized clients for the six requested models, structured persistent playbooks, fresh/within-game/cross-game modes, replayable traces, and separate discovery/execution/benefit reporting. These results are for the controlled profiles, not the historical shipped engines.

- **66 benchmark tests passed**; **940 legacy environment tests passed, 5 skipped**; **208 standalone game gates passed**. Logs are under [benchmark/results](../../benchmark/results).
- **11,721 integrity checks passed across all 168 main traces**, including frozen-profile replay, native dependency hashes, counterfactual successors, raw reflection/playbook agreement, exact carryover, and model-authored discovery quotes. [Audit](../../benchmark/results/full-20260906/integrity_audit.json).
- Every pilot also passed replay/provenance auditing against its own frozen profile. Pilot results are separate from the main matrices.

## Interpretation and operational record

Discovery was uniformly rescored with `discovery-v3-model-articulation` after early judge checks admitted inappropriate evidence. The final judge requires exact quotes from model-authored articulation and receives fresh deterministic execution records, never prior discovery labels. Original judgments and raw calls are retained; judge outputs were never fed to players.

GLM needed one logged top-level JSON-key normalization. Qwen and Haiku needed larger reflection ceilings/timeouts and checkpoint continuations after truncations; Qwen’s later syntax errors were repaired by the model. All completed games and model-authored playbooks were retained. Exact boundaries, prompts, retries, and settings are recorded in recovery metadata and the sampling handoff files.

Category counts overlap, and “benefit” denotes the specified local score, margin, information, denial, or termination advantage; it need not raise terminal own payoff. Discovery judgments remain model judgments. Temperature was 0, but provider determinism is not guaranteed. Persistent memory is measured descriptively; the fresh condition is implemented but a matched fresh-control experiment remains a separate study.

## Artifacts

- [Primary report](../../benchmark/results/full-20260906/REPORT.md), [overview CSV](../../benchmark/results/full-20260906/overview.csv), [all observations](../../benchmark/results/full-20260906/observations.csv), [first discovery/execution/success and evidence](../../benchmark/results/full-20260906/exploit_learning.csv).
- [Model × game](../../benchmark/results/full-20260906/model_by_game.csv), [model × category](../../benchmark/results/full-20260906/model_by_exploit.csv), [mechanism split](../../benchmark/results/full-20260906/by_mechanism.csv), [learning by iteration](../../benchmark/results/full-20260906/by_iteration.csv).
- [Specifications](../../benchmark/results/full-20260906/exploit_specs.json), [proposed versus implemented coverage](../../benchmark/results/full-20260906/coverage.json), [configuration/orders](../../benchmark/results/full-20260906/config.json), [final status](../../benchmark/results/full-20260906/status.json), [final analysis sources](../../benchmark/results/full-20260906/analysis_manifest.json).
- Independent pilots: [Qwen/Commons](../../benchmark/results/smoke-qwen-commons-low-20260906/REPORT.md), [Haiku/Commons](../../benchmark/results/smoke-haiku-commons-20260906/REPORT.md), [GLM/Exchange](../../benchmark/results/within-glm-exchange-20260906/REPORT.md).
- [Implementation and recovery log](benchmark-implementation.md).
