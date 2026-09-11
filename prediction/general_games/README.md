# General TextArena games for behavior prediction

**Latest fixed-budget breadth check:** [report](breadth_v3/study/REPORT.md) · [18-family viewer](http://localhost:42329/general/breadth) · [train-only exports](breadth_v3/study/overnight/README.md). This separate study compares 288 training labels in four versus twelve families on six new holdouts, with 624 fresh episodes in total. Breadth improves win-error point estimates, but neither learned method establishes an advantage over pooled prompting or the training-mean baseline. Calibration and interface diagnostics qualify the scaling recommendation; see the completed report.

**Expanded replicated version:** [study tools and protocol](scaleup_v2/README.md) · [16-family viewer](http://localhost:42329/general/replicated) · [study report](scaleup_v2/study/REPORT.md). This version adds four native families, independent seed/seat crossing, five repeated samples per anchor condition, richer operational labels, and prospective 120/248/440-episode comparisons against 4/8/16-shot prompting. It retains the v1 artifacts described below as a separate historical release.

This is the ordinary-game coverage counterpart to [Gameable Games](../scaleup/README.md). Games are selected for distinct strategic structures, using the installed **TextArena 0.7.4 native environments** and their native constructor parameters. They are not selected, modified, or filtered for exploitability. This is a purposive sample, not a representative random sample of all games.

- [Dataset card](data/20260910-v1/DATASET_CARD.md): scope, families, split and label definitions.
- [Catalog](data/20260910-v1/catalog.json): 12 families and 49 parameter configurations.
- [Manifest](data/20260910-v1/manifest.json): 196 seeded instances, 113 distinct opening-state groups, validation and code fingerprints.
- [Pilot plan](runs/pilot-20260910/plan.json): 96 model episodes across both models and prompt conditions.
- [Pilot report and comparison](runs/pilot-20260910/export/REPORT.md): observed coverage and comparison limits.
- [Viewer](http://localhost:42329/general): game families, parameter and behavior distributions, exact native trajectories, and separate coverage / parameter / combined cohorts.
- [Five diagnostic checks](evaluation/results-20260910/REPORT.md): parameter effects, model differences, label reliability, four-shot versus learned prediction, and representation ablations. [Interactive results](http://localhost:42329/general#checks).
- Prediction rows: [episodes](runs/pilot-20260910/export/episodes.jsonl), [actions](runs/pilot-20260910/export/actions.jsonl), [aligned comparison rows](runs/pilot-20260910/export/comparison-episodes.jsonl).

The catalog and scripted validation are complete. The first live pilot samples each family's base configuration. A separate parameter study adds six configurations in PD, Pig Dice and Colonel Blotto: **48/48 complete episodes and 302 focal actions**. Total collection is **144 episodes, 779 focal actions and 18 native invalid actions across 18 configurations**; the remaining 31 configurations await model collection. Scripted fixtures are never substituted for LLM observations.

Final pilot: **96/96 complete episodes, 477 focal actions, 18 native invalid actions**. All 803 native transitions replayed; all 490 inference attempts were reconciled with raw calls and both budget ledgers. Eight empty responses and five truncated responses were retried and are excluded from action labels. Reported API cost was **$1.1363**. See the [independent audit](runs/pilot-20260910/export/audit.json).

A separate [full-catalog collection plan](runs/full-catalog-v1/plan.json) is prepared but **not collected in full**: 1,360 episodes crossing all 49 configurations, four seeds, every focal seat, both models and both prompt conditions. The small parameter study copies 48 selected episodes into its own plan; it does not complete this larger collection or remove seed/seat confounding. Create a fresh copy with `python -B -m prediction.general_games.plans --run /path/to/full-run`; collection requires explicitly running the runner against that path.

The diagnostic compares 192 valid Kimi forecasts with five fixed numerical baselines on two grouped 24-episode holdouts. Four-shot prompting remains competitive for wins (.146 versus linear .174 on new parameter values; .221 versus .299 on new families), while learned models do better on some behavior rates. All 144 native trajectories replay; raw calls and both ledgers reconcile. Additional collection cost was $0.3922 and predictor cost $3.4871, with no unresolved billing. The diagnostic report records limitations and reproduction commands.

From the repository root, using the existing environment:

```bash
/shared/allie/venvs/hole/bin/python -B -m unittest prediction.general_games.test_general_games -v
/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.runner --workers 6
/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.export
/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.audit
```

The runner resumes completed checkpoints by replaying native actions and checking raw calls, skips complete/censored episodes, and makes at most three inference attempts per decision. Run one collector for a given plan at a time. Do not resume it while another collector owns those episodes. Transport, refusal, truncation, and empty-response failures are retained as inference failures rather than submitted game actions. Native invalid model actions remain observed behavior. An incomplete episode remains incomplete when its attempt allowance is exhausted.

To construct a separate catalog and plan without overwriting this version:

```bash
/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.dataset build --data /path/to/new-data
/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.dataset plan --data /path/to/new-data --run /path/to/new-run
/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.runner --run /path/to/new-run --workers 6
/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.export --run /path/to/new-run
```

Collection uses the existing credential loader, never credentials embedded in the dataset. Model routes are `qwen/qwen3.8-27b` and `z-ai/glm-5.3` on OpenRouter, temperature 0.7, requested reasoning low, output cap 16,384, and a $50 ledger ceiling. This ceiling is a fail-closed reservation bound, not expected spend. Each episode has at most 128 total submitted actions and 64 focal model actions; hitting either external limit is censored. Actual usage is recorded in the report and raw calls.

Use only the `inputs` object for pre-episode prediction, and `inputs` plus `messages` for next-action prediction. The surrounding row carries targets, split metadata and trace links. The `*.evaluator.json`, episode checkpoints, and raw provider responses contain hidden state and future outcomes. They are for auditing and analysis, not prediction features. Always group entire opening instances and all repeated model/prompt/seat trajectories together when splitting.

Source: [official TextArena repository](https://github.com/TextArena/TextArena). Installed engine code is unchanged, fingerprinted in `native-source-hashes.json`, and archived with its MIT license in `native-source.tar.gz`. The 11 fingerprinted collection/dependency files are preserved in `collection-source.tar.gz`; archive checksums and installed package versions are in `runtime.json`. Wordle lexicon and validity dictionaries are separately fingerprinted in evaluator opening snapshots. The local installed version, not current upstream main, defines this dataset's behavior.
