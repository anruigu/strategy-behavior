# Multiplayer exploit discovery benchmark v0

The current V3 sets are **v3-SA** (the revised 45 single-agent targets across
17 editions) and **v3-MA** (14 multi-agent scenarios across five families).
See the [set definitions, controls, and runner](v3_ma/README.md) or run
`python -m benchmark.suites` for the manifest. The remainder of this document
describes the original v0 benchmark.

Seven short game profiles, 14 canonical categories, 25 specified opportunities,
complete action/state traces, and four fresh episodes per game by default. Built
on the repository's `RefereeGame` / `Episode` protocol and SPaRTan reflection
infrastructure. Legacy engines and historical results are unchanged.

## Completed results

The 2026-09-06 experiment completed **168 main games and 12 independent pilot games**.
Read the [results summary](../research_logs/sep/benchmark-results.md) or the
[full report, matrices, figures, and evidence](results/full-20260906/REPORT.md).
All 168 main traces passed 11,721 integrity checks.

## Run

From the repository root, with the existing research environment:

```bash
PY=/shared/allie/venvs/hole/bin/python
$PY -m pytest benchmark/tests -q
$PY -m benchmark.validate
$PY -m benchmark.experiment_runner
```

The last command runs **6 models × 7 games × 4 iterations = 168 games**.
Model chains run concurrently; games within each chain remain sequential.
Game order is shuffled independently for each model and saved to `config.json`.
Each game receives four consecutive iterations before the next game starts.
The default `--condition no_reflection` uses a fresh context each episode and makes no reflection calls or playbooks. Discovery is judged offline from gameplay evidence; judge output is never fed to the player. Reflection is opt-in with `--condition persistent` (carry playbooks) or `--condition fresh` (reflect but discard playbooks).

```bash
# Fresh-play smoke test
$PY -m benchmark.experiment_runner --models qwen-3.8-27b \
  --games ref_commons --scope within-game

# Fresh control: the model still reflects, but no playbook is passed forward
$PY -m benchmark.experiment_runner --condition fresh

# Persistent within-game memory, reset when moving to another game
$PY -m benchmark.experiment_runner --scope within-game

# Regenerate analysis without spending API calls
$PY -m benchmark.reports benchmark/results/EXPERIMENT_ID
```

Output directories are unique and refuse reuse. A failed call stops its model
chain, preserves completed work and logs the failure; other chains continue.
Provider failures are never converted to honest actions or zero scores. Invalid
*model actions* are retained and counted separately. Existing credential loading
reads the durable research environment, without copying secrets into outputs.
Dependencies: Python 3.12, `openai`; `pytest` for tests; optional `matplotlib` for static figures. No GPU required.

## What is reused

- `referee_games.RefereeGame` and `Episode`, the game's callback/record contract.
- `referee_spartan.run_round`, `Recording`, `Playbook`, `render_episode`, and
  `reflection_prompt`: own-view transcript → revised playbook → next game.
- Native game classes, generated token helpers, Hanabi clue validation, and
  IPD/Winasmuch payoff functions.
- Existing provider credential loading and OpenAI-compatible endpoint conventions.

A thin outer loop adds the requested fourth reflection, structured playbooks,
randomized cross-game scheduling, and independent evaluation. No replacement
reflection framework or LLM referee is introduced.

## Profiles and changes from historical engines

These are **explicitly versioned controlled benchmark profiles**, not scores on
the historical shipped games. Exact source files and hashes are copied into
every experiment. One live focal player faces deterministic scripted opponents.
The fixed opponent behavior is part of the benchmark, including the Hanabi
recipient protocol and IPD coalition response.

| Game | Total players | Max focal actions | Retained mechanics and additions |
|---|---:|---:|---|
| Seven Seal | 3 | 4 | Modular seal; report amendment ordering and public-receipt information leak added |
| Commons | 3 | 4 | Fish depletion/regrowth; fixed quota 3, sequential landings, costly disposal |
| Hanabi | 3 | 4 | Native clue validator; 3-card hands, scripted recipient, own play, review interface |
| IPD | 2 | 4 | Native payoffs and unfulfilled grim threat; explicit optional pledge |
| Exchange | 3 | 6 | Construction/resource economy; workshop grant, dismantle cycle and affordability ordering |
| Winasmuch | 4 | 4 | Native payoff table and promise/memory interaction; shared reserve and early settlement |
| IPD3 | 3 | 4 | Native pairwise payoff and delayed coalition; costly reserve sanction |

The plan's *suggested* coverage is saved separately from tested implemented
coverage. All 14 categories have implementations; every game has at least two
primary specifications. No unimplemented suggested cell is silently reported as
an opportunity. Some cells overlap because one action can realize several
mechanisms. The report marks that dependence explicitly.

## Evaluation

`specs.py` contains descriptions, opportunity conditions, exploit and normal
strategies, observable effects, advantage metrics, testable discovery criteria,
surface forms and abstract rules. Specifications and evaluator results are
**never shown to the player**. `games.py` records factual transitions; all
classification is in `evaluator.py`.

For every action, retain before/after state, the raw action, the normal-action
successor from the same state, and a strict-referee successor. These are local
counterfactuals, not alternative full episodes. The evaluators distinguish
attempt, execution, and positive benefit. A bonus paid, a resource denied, an
earlier ending and a private value revealed are different advantage units;
they are never added as if they were points.

Discovery uses one fixed Haiku judge across all models. It receives the focal
transcript, model-authored playbook, specifications and deterministic evaluation.
Positive judgments must contain exact evidence quotations and a concrete,
correct mechanism; generic suspicion is insufficient. A judge failure preserves
the completed game/reflection as missing discovery data. Deterministic execution
evidence remains available in that trace.

Metrics:

- Discovery: distinct discovered specifications / specified reachable opportunities.
- Execution: discovered specifications executed / discovered specifications.
- Success: successful action executions / action executions.
- First discovery/execution/success iteration, repeated use, and execution in a
  later game iteration after a discovery has been written.

Conditional opportunities that the player never opens remain in the discovery
denominator; `opportunity_encountered` distinguishes those from observed states.
The opt-in fresh and persistent conditions use identical environments and reflection
instructions. Persistent cross-game runs flag earlier same-category discoveries
in another game as prior exposure, **not a causal transfer estimate**.

Discrepancy discovery is reported separately from `natural_opportunity`
strategies such as sacrifice, group-versus-individual incentives and coalition
timing, which are visible affordances rather than hidden bugs. The auditing
reflection treatment explicitly encourages examining mechanisms and should not
be pooled with legacy neutral-reflection results.

## Artifacts

Each experiment has `REPORT.md`, CSV model × game/category matrices, learning
curves, the primary exploit table, machine-readable specifications, source
snapshots and a complete configuration. Each model has `traces/`, `playbooks/`,
`calls/` and `judge_calls/`. Actual returned model IDs, timestamps, temperature,
finish reasons, usage, retries, full request and response bodies are logged.
Environment seeds are fixed; provider sampling seeds are unset because support
is not assumed. Temperature zero does not guarantee bitwise model determinism.

`results/canonical_traces/` holds a positive and normal negative trace for each
specification. These are **scripted regression fixtures, not model results**.
`results/baseline-*.txt` records existing validation: 208 standalone game gates
pass; the broad legacy suite has 940 passes and 5 skips. Its external dependencies
were resolved with the existing custom TextArena and ipd_lib checkouts under
`/shared/allie/think4/code`, plus repository-pinned Tinker 0.25.0 installed in an
isolated test dependency directory. Those dependencies are not needed to run the
new benchmark profiles.

The full matrix is uniformly rescored with `discovery-v3-model-articulation`.
This requires a model-authored mechanism quotation and never shows the judge a
previous judge's decision. Original scoring calls remain available for audit.
To check saved transitions and export static research figures:

```bash
$PY -m benchmark.audit benchmark/results/EXPERIMENT_ID
$PY -m benchmark.plots benchmark/results/EXPERIMENT_ID
```

The final offline audit (`python -m benchmark.audit RESULTS_DIR`) loads the run's frozen game profile, checks native dependency hashes, replays every transition, and checks raw reflection/playbook provenance and model-authored discovery quotations.

## Detailed plot gallery

Generate model, game, and individual-hole curves; attempted → executed →
successful comparisons with discovery shown separately; and radar charts for
rule/enforcement, information/interface, state/time, and multiplayer/objective:

```bash
PYTHONDONTWRITEBYTECODE=1 /shared/allie/venvs/hole/bin/python -m benchmark.detailed_plots benchmark/results/EXPERIMENT_ID
```

Open `plot_gallery/index.html` for searchable PNG previews, individual PDF exports,
and a combined `all_plots.pdf`. `observations.csv`, `rates.csv`, and `manifest.json`
record the plotted data and trace provenance. The original report is unchanged.

Both per-repetition and cumulative coverage are shown. Engine stages are computed
from completed gameplay even when the language judge failed. Discovery uses
existing, uniformly versioned judge labels; known judge inconsistencies are not
fixed by plotting. All four metrics use fixed game-specific-hole denominators;
missing data remain unknown. Radar exploit rate means unconditional engine
execution. Within each broad group, game-specific holes receive equal weight.

## Default model profiles (no reflection)

Both `benchmark.experiment_runner` and `benchmark.diagnostic_runner` now default
to no reflection. The diagnostic runner retains the revised Hanabi challenge;
the original runner retains the historical seven-game registry. The expanded
ten-game suite, including Battleship, remains a separate implementation target.

The completed fresh-play frontier run contains three models, three games, nine
game-specific holes and four episodes per model/game. Plot episode-level rates
by game, category, individual hole and broad group, with gameplay-only discovery:

```bash
$PY -m benchmark.fresh_profiles benchmark/results/frontier-no-reflection-20260906 --score
```

`--score` makes cached discovery-judge calls on visible gameplay only; omit it to
regenerate plots without API calls. Scores and exact model quotations are stored
in a separate `model_profiles/discovery/` directory; source traces stay unchanged.
The gallery includes attempted, executed, successful and articulated discovery
rates. Each uses the same episode × hole denominator, without conditioning
execution on discovery. Unobserved categories are omitted, not scored zero.
Discovery cannot measure recognition the model never articulates during play.
These plots do not pool the informed or reflection conditions with fresh play.

## Cross-family live play

See [cross-play design](../research_logs/sep/crossplay-small-large.md). This is a
separate native-game evaluation, not a replay of the three short diagnostic
profiles. Every table uses distinct model families: Claude, GPT and Gemini,
with small, large and mixed-size lineups and no reflection.

```bash
$PY -B -m benchmark.crossplay_runner --output benchmark/results/crossfamily-20260907 --workers 24
$PY -B -m benchmark.crossplay_discovery benchmark/results/crossfamily-20260907 --watch --workers 12
```

The report has table win credit, outright wins/ties, cooperative Hanabi scores,
per-seat discovery/execution, and paired model-size effects with the other players,
seat and deal held fixed. API calls and per-action replay checkpoints are saved.
