# Replicating the 49-hole engine audit across small models

Launched September 9 on Qwen 3.8 27B, GLM 5.3, Claude Haiku 4.5, GPT-5 mini, and a new Gemini 3.7 Flash reference. Kimi K3 remains absent from the FLT model catalog and is not silently substituted.

All five use **low reasoning effort**, temperature omitted, and a fixed 16,384-token completion allowance. Qwen does not support the original Gemini run's `high` effort and GLM showed extensive truncation under the earlier live-study configuration. Low-effort game canaries returned usable responses from all five models. Equal effort labels and token ceilings do not imply equal hidden compute across architectures. The original high-effort Gemini audit is retained separately; the comparative plot uses the new low-effort Gemini reference.

The exact source snapshot from the completed Gemini 49-hole audit is reused. Every original Python file's SHA-256 identity is verified; only a model-selection launcher is added. The same 49 target IDs, 11 excluded policy-dependent cells, three seeds (19, 73, 101), game observations, exploration prompt, engine mechanics, scorers, and hint text are retained. No reflection or cross-game memory. Native scripted opponents: this is not live cross-play.

Each model runs 57 blind episodes (19 editions × three seeds), then fresh hinted follow-ups for each valid target/seed miss, up to 147 follow-ups. API failures are incomplete rather than failed discoveries. Up to 285 blind + 735 hinted episodes across the five-model matched cohort. Eight concurrent episodes per model; five model processes run concurrently. All calls, including canaries and other active studies, share the original $500 ledger.

Output: `benchmark/results/small-engine49-20260909/`.

- `plan.json`, `source-identity.json`, target/exclusion lists, per-model launch records.
- Per model: manifest, status, raw calls, turn checkpoints, oracle validation, coverage, and traces.
- `REPORT.md`: live progress and embedded comparative figures.
- `plots/model_star_comparison.{png,svg,pdf}`: separate unaided and hinted profiles across the original four broad groups.
- `plots/model_type_heatmap.{png,svg,pdf}`: unaided execution across the 17 included types.
- `plots/comparison-data.json`: rates and completion denominators behind the figures.

Plots update automatically. A model's unaided curve is drawn only once all 49 × three seed opportunities have valid completed blind episodes. Its hinted curve is drawn only after all scheduled diagnostics complete. Incomplete grids are omitted, never represented as zero. The hinted panel conditions on each model's own missed subset, so it does not compare identical test items across models. Broad-group axes equally weight eligible type rates. Profiles report execution, not verified semantic discovery. Whether the profiles differ is an empirical result; the protocol will not be tuned to produce a spread.

## One bounded recovery pass

At approximately 01:01 UTC, GLM was still completing its hinted phase. Qwen, Haiku, and GPT-5 mini had ended with seven, one, and one failed episodes respectively. A single explicitly logged recovery pass was launched for those three models using the identical frozen source, model settings, prompts and seeds, retaining all valid turn checkpoints. Original status and coverage are preserved in each run's `*-before-recovery1.json`; process records list every original failure. Newly completed blind misses receive the ordinary planned hinted follow-ups. No repeated recovery loop is scheduled; the shared $500 cap remains in force.

## Completed, including bounded recovery

Four models completed all scheduled episodes. Qwen retained two invalid-response blind failures (Commons Neighbours seed 101; Exchange Workshops seed 73) after recovery and is not being retried again. Observed unaided / combined distinct-hole coverage: GLM 28/46, GPT-5 mini 24/36, Haiku 19/40, Gemini low 15/48, Qwen 13/35, all out of 49. The five-model star now uses exactly the same 55 completed blind episodes for every model. Final tables, interpretation and plots are in `benchmark/results/small-engine49-20260909/RESULTS.md`. Original high-reasoning Gemini remains separate (21/49 unaided, 49/49 combined).
