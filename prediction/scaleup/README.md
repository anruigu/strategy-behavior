# Parameterized behavioral dataset

Open the [interactive dataset viewer](http://localhost:42329) for distributions,
collection summaries, and browsable game/trajectory samples. Its
[usage notes](viewer/README.md) explain filtering, paired variants, and JSON export.
The generated design is in [data/20260910-v1](data/20260910-v1/DATASET_CARD.md);
the live smoke pilot is in `runs/pilot-20260910/`.

The [five-check pilot assessment](assessments/pilot-checks-20260910/REPORT.md)
quantifies reward sensitivity, model differences, label consistency,
family-held-out few-shot baselines, and representation limits. These findings
and their plots are also in the viewer. [Reproduction notes](assessment/README.md)
describe the matched comparisons and prediction protocol.

The pilot is **complete: 144/144 episodes and 864 decisions**, with 72 episodes
per model. It retains 77 completed FLT episodes and collected the other 67
through OpenRouter, using `qwen/qwen3.8-27b` and `z-ai/glm-5.3`.
The FLT gateway returned generic HTTP 403 responses for both models and its
catalog; access subsequently recovered, but the response did not disclose the
cause. Each restarted episode begins from its original opening state. Provider
is recorded per episode and shown separately in the viewer; assignment followed
prior completion and was not randomized. See the [audited pilot report](runs/pilot-20260910/export/REPORT.md)
for collection coverage, distributions, and limitations.

All 144 episodes passed raw-call, protocol, deterministic replay, and export
join checks. Five of the 864 recorded actions were invalid under the game rules;
they remain in the dataset as observed model behavior. The 26 automated tests and Chromium
viewer checks passed. OpenRouter reported $1.984484 for the continuation,
including unsuccessful calls and upstream BYOK charges; preflight cost is
separate. This is a two-model collection pilot within the larger generated
design, with one trial per cell.

This implements the dataset-building part of [the September 10 plan](../../research_logs/sep/0910-prediction-scale-up.md): playable game instances, controlled dose changes, trajectory collection, observable labels, and grouped evaluation splits. It is a new versioned suite; historical Gameable Games and matrix-game experiments retain their original engines and results.

There are **24 compact families**: 20 distinct state-transition mechanisms using the original taxonomy from `benchmark/scaleup/taxonomy.py`, plus public goods, threshold coordination, trust exchange, and sealed-bid competition. Every game has three actors: one focal model and two explicitly scripted rivals. Models and prompt conditions get fresh context each episode. This version does not implement LLM opponents, autonomous all-player cross-play, human data, or large-scale encoder training; the pilot assessment includes small numerical predictors and LLM forecasting baselines.

The canonical schema is in `schema.py`. Game records carry complete player-facing rules, structured mechanics, role, parameters, construction, and separate research annotations. The same generated rules are used by the player runner. Exploit witnesses and evaluator facts are never put in player prompts. Structured predictor inputs include the experimental control assignment; remove it for an observer-blind prediction ablation.

## Build and collect

Run from `/shared/allie/strategy-behavior`, using the existing environment:

```bash
export TMPDIR=/shared/allie/home/.codex/tmp
export PYTHONDONTWRITEBYTECODE=1
PY=/shared/allie/venvs/hole/bin/python

$PY -B -m prediction.scaleup build \
  --out prediction/scaleup/data/new-build --blocks 8 --validation-seeds 3

$PY -B -m prediction.scaleup plan \
  --dataset prediction/scaleup/data/new-build \
  --out prediction/scaleup/pilot-manifest.json \
  --pilot --provider openrouter --budget-usd 50 \
  --models qwen-3.8-27b,glm --trials 1 --max-tokens 16384 \
  --families certificate_office,shared_fishery,inspection_dock,sealed_archive,conversion_market,workshop_grants,voucher_bank,escrow_partnership,public_works,launch_coordination

$PY -B -m prediction.scaleup run \
  --manifest prediction/scaleup/pilot-manifest.json \
  --out prediction/scaleup/runs/new-pilot --workers 12

$PY -B -m prediction.scaleup export \
  --run prediction/scaleup/runs/new-pilot \
  --out prediction/scaleup/runs/new-pilot/export
```

`build`, `plan`, and `export` make no inference calls. `run` uses the existing research credential loader and logged client. New plans default to **OpenRouter**, a 16,384-token cap, and a $50 budget ceiling; set `--budget-usd` to choose a different ceiling. Conservative per-call reservations can pause collection before actual spending reaches the ceiling. Qwen 3.8 27B and GLM 5.3 passed OpenRouter catalog and generation preflight on September 10. Candidate model names in the research note are not assumed to be available. `--provider configured` explicitly opts into the historical shared routing registry. Existing run manifests keep their original provider configuration.

The provider continuation has a separate manifest, call log, budget ledger, and
source snapshot in `runs/openrouter-continuation-20260910/`. The original FLT
manifest and traces remain intact. The viewer follows `provider-continuation.json`
and selects exactly one run per episode. To resume this continuation and regenerate
the combined, independently audited export:

```bash
$PY -B -m prediction.scaleup run \
  --manifest prediction/scaleup/openrouter-continuation-20260910-manifest.json \
  --out prediction/scaleup/runs/openrouter-continuation-20260910 --workers 12
$PY -B -m prediction.scaleup.viewer.export_collection
$PY -B -m prediction.scaleup.viewer.report
```

The combined export records each row's source run and manifest hash. Its
`collection.json` indexes the selected source of every planned episode, and
`audit.json` contains separate source audits plus the combined coverage check.

The first 2,048-token calibration pass completed 82/144 episodes and left 62 incomplete, predominantly because reasoning exhausted the cap. It is retained separately in `runs/token-cap-calibration-20260910/` and excluded from the final pilot/viewer. The pilot was restarted from fresh contexts with a uniform 16,384-token limit for all conditions. This avoids selectively combining short completions with larger-budget retries. Within that fixed final protocol, transport failures can resume from their saved decision context.

Omit `--pilot` and `--families` to include the entire design. `--trials`, `--models`, `--prompts normal,active_exploration`, and `--opponents ordinary,defensive` specify the episode cross-product. Defensive policies differ only where the game rules define them. They must not be interpreted as a globally effective defense. Output counts include the condition multipliers; these can dominate collection size.

Build and plan destinations refuse overwrite. Repeating `run` with the same manifest resumes missing actions and skips completed episodes after replay verification. Each completed provider response is checkpointed before applying its action. A provider failure leaves an incomplete episode; a malformed model action consumes a turn and remains in the trace. There are at most three inference attempts per decision across resumptions. Completion requires a terminal state and matching raw-call provenance. The runner freezes source hashes and copies its runtime sources into each run. Changes to the runtime require a new manifest/run.

## Controlled construction

Each family gets eight public opening-endowment constructions by default. Construction zero uses default parameter values; later anchors use independently sampled parameter backgrounds. Every anchor has a one-variable sweep over every declared parameter grid. All parameter edges differ in exactly one value; each mechanism-bearing game also has a paired intervention that changes only the control flag.

Implementation-discrepancy controls close a specific transition without changing the visible rules. Strategic-affordance controls change incentives or rival responses and are explicitly described to the player as ablations. They are not called bug patches. The families differ in mechanics (inventory cycles, shared stocks, grants, escrow, hidden signals, queue order, terminal requests, etc.), not just prose or payoff matrices.

The `reward` parameter is a family-specific payment or effect magnitude; it is **not a comparable expected exploit value across families**. Parameter descriptions and rules specify its units. Zero-advantage and costly doses remain in the dataset; an opportunity need not be profitable. Audit risks are supplied only to families with programmatically identifiable prohibited requests. Inspection shows the public ledger at a cost; it is an observable information-seeking action, not proof of discovery. Exploit complexity and number of players are not varied in this first version.

Environment seeds and seat permutations are matched across all parameter/control variants, models, and framing conditions in a group and trial. Audit draws are keyed by episode seed and turn, so different action paths cannot shift the random-number stream. Seat IDs are permuted independently from fixed strategic roles; internal actor 0 remains focal. Role names and rival-to-seat mappings are shown in the observation. Construction changes public initial endowments, not the underlying family.

## Files and measurements

| File | Contents |
|---|---|
| `families.json` | Family mechanics, action contracts, parameter grids, taxonomy, witness definitions |
| `games.jsonl` | Playable instances with natural-language and structured representations |
| `counterfactual_pairs.jsonl` | Single-parameter interventions and patch/ablation pairs |
| `splits.json` | Game-to-fold assignments for each evaluation regime |
| `validation.json`, `design_audit.json` | Coverage and executed deterministic checks |
| `validation_fixtures.jsonl` | Scripted witness trajectories, explicitly marked `scripted_fixture` |
| `runs/.../episodes/*/trace.json` | Raw responses, exact prompts, every before/after state, rival actions, labels, local counterfactuals |
| `runs/.../calls/` | Raw provider requests/responses, returned model IDs, usage, statuses |
| `runs/.../export/episodes.jsonl` | Verified model episodes with separate `inputs` and `labels` |
| `runs/.../export/actions.jsonl` | Exact pre-action contexts and action targets; no future trajectory in inputs |
| `runs/.../export/missing.jsonl` | Planned episodes that are missing or incomplete |

Observed cooperation, defection, communication, coordination, information seeking, exploitation, free riding, generosity, sacrifice, risk-taking action classes, and rule adherence have explicit family support. Rates count tagged focal actions divided by focal decisions; unsupported measurements are null, not zero. These are operational action classes, not psychological traits or intention judgments. `coordination_success` is conditional on recorded coordination attempts and carries its denominator. Inventory, hidden-information, termination, and rival-damage effects retain separate units in transition facts.

`discovered`, intent-based `tested`/`abandoned`, deception, exploration, retaliation, and commitment remain null where no defensible observation rule exists. Mechanism execution and repetition are programmatic. Successful execution means the specified effect occurred, regardless of recognition, net reward, or winning. Strategic affordances are tagged separately from implementation exploitation. A requested probe that has no effect is distinct from an executed effect.

Scores, ranks, shared win credit, opponent scores and social welfare are secondary outcomes. Every action stores a same-state honest-action successor and a same-state controlled successor with the same exogenous draw. These are local one-action comparisons. Their score-difference sum is labeled as such and is not an honest-policy episode counterfactual. Full-episode counterfactual payoff, causal regret and efficiency remain null. `benefit_observed` reports a positive local honest-action score contrast on a mechanism-executing action; it does not establish an episode-level benefit.

## Splits and interpretation

Random-group, construction, family, and mechanism splits retain entire intervention groups. All players, trials, and framing conditions inherit their game's assignment. The interpolation split holds out reward 6 (validation 8); the extrapolation split holds out reward 12 (validation 8). Those dose splits deliberately separate values within a response curve while keeping patch pairs and replications together. They test dose transfer and must not be interpreted as structural transfer. Cross-environment evaluation is explicitly deferred.

There is one family per mechanism in this version. Consequently a held-out-mechanism test is also a family holdout; this design cannot independently identify mechanism transfer versus family transfer. Multiple structurally different families per mechanism are needed for that claim. A two-model, one-trial smoke pilot can verify collection and visible behavioral variation but cannot establish stable model phenotypes or estimate response thresholds reliably.

Validation runs honest, witness and malformed policies across generated variants and seeds, verifies every transition and derived label, checks nonmutation, and tests patch closure. A positive scripted witness proves an effect is reachable, not that an uninformed model will discover it. Information witnesses may be uninformative when the default guess already matches the hidden target. The catalog's visible action menus expose possible requests; this version measures exploration among those affordances rather than open-ended command invention.

```bash
$PY -B -m pytest prediction/scaleup/test_scaleup.py -q \
  --basetemp=/shared/allie/home/.codex/tmp/scaleup-pytest
```
