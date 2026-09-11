**SA incentive dose built — 2026-09-11**

**Live launch:** September 11, 02:18 UTC. The 400-episode campaign is running from the frozen source with a shared $50 paid-API ceiling. It runs reward, audit and control phases, performs the allowed recovery pass, refreshes plots, and verifies accepted API contexts automatically. [Live status](../../benchmark/results/sa-dose-20260911/STATUS.md) · [Launch record](../../benchmark/results/sa-dose-20260911/process.json).

The [engine](../../hole_exp/hackable_games/engines_v3_sa_dose.py) and
[experiment package](../../benchmark/v3_sa_dose/README.md) implement the first two
mechanisms from the [plan](0910-sa-incentive-dose-plan.md): Seven Seal self-report
and Commons over-quota landings. The new version is `v3-SA-dose.1`.

The five reward settings give a fixed complete exploit policy a final
score-margin advantage of **−1, 0, +1, +3, +7** relative to a strong legal policy.
These are measured by scripted engine rollouts, not inferred from model behavior.
The same grid passes for all five environment seeds. Commons uses an exact
optimal legal catch policy and includes the effect of stock depletion on rivals.
The audit sweep enumerates every combination of eight independent audit flags
and includes the resulting changes in future stock and opportunities.

![Scripted SA payoff calibration](../../benchmark/results/sa-dose-20260911/plots/payoff_calibration.png)

The isolated variants have fixed action ranges and patched companion mechanisms.
Seven Seal retains its modular seal, bounds reports to 0–10 and gives each rival
a fixed three-point initial endowment. That endowment makes the calibrated
ladder cross a win/loss boundary instead of increasing an already certain win.
Commons retains stock 40, regrowth 3 and rotating landing order, with a catch
menu of 0–6 and fixed over-quota handling cost 2. Its isolated menu removes
trawling and damage claims. These versioned restrictions are held constant
across doses; they are not historical SA observations.

The [prepared manifest](../../benchmark/results/sa-dose-20260911/plan.json)
contains 400 tasks: four models × two targets × five episode replicates × ten
cells. Five reward cells give the first 200 episodes. Four additional audit
cells and one patched anchor add 200; the audit figure reuses the existing
zero-audit reward anchor. The manifest freezes model settings, prompts,
261 source files and the hash of 100 target/cell/seed calibration records.

The runner reserves from a dedicated SA budget before each request, accounts
for upstream BYOK cost, checkpoints accepted replies and replays completed
traces. Dose and complete context are included in resume identity. One explicit
recovery pass can resume transport/truncation failures while preserving the
accepted prefix. Refusals and provider failures stay missing. Invalid game
actions consume a turn and are recorded separately. Attempts precede enforcement;
physical execution remains detectable even when the reward is zero.

Validation completed:

- **29 tests passed** across the new dose package, existing public-SA tests and
  budget tests. These cover calibrated payoff and win transitions, honest-policy
  invariance, full inspection, zero-reward execution, bounded menus, hidden audit
  draws, task balance, historical-engine preservation, resumability, refusal
  handling, missing-data plots and BYOK accounting.
- Both new games also completed the existing `RefereeGame.run` interface with
  eight recorded decisions and versioned dose metadata.
- The full preparation and figure pipeline completed without model calls, and
  preparation/plotting was reproduced from the frozen source directory.
- PNG/PDF/SVG exports were generated; the calibration and empty response figures
  were visually inspected.

Reproduce the test run:

```bash
/shared/allie/venvs/hole/bin/python -m pytest \
    benchmark/v3_sa_dose \
    hole_exp/hackable_games/test_v3_public.py \
    benchmark/fullscale/test_budget.py -q
```

**Model data status at build completion: 0/400 episodes.** No model API calls were made during this
build. The [behavior figures and exact cell tables](../../benchmark/results/sa-dose-20260911/plots/README.md)
explicitly show that no observations exist yet. The subsequent live campaign uses its own $50 SA cap; the MA campaign's budget is not reused. The build
does not yet estimate model thresholds, slopes, exploration-cost sensitivity,
or human curves.


**Plotting repair and resume — September 11, 04:03 UTC.** The first campaign stopped at 63 completed reward episodes and $9.09586495 paid usage when floating-point roundoff produced a tiny negative Matplotlib error-bar length for a zero-success cell. Wilson interval endpoints now include the observed proportion exactly; nine focused tests passed. The monitor records plotting errors without terminating inference. The corrected renderer is frozen separately in [the analysis manifest](../../benchmark/results/sa-dose-20260911/analysis-manifest.json), preserving the original engine/evaluator source hashes, plan identity, budget ledger and accepted replies. [The resumed process](../../benchmark/results/sa-dose-20260911/process.json) continues the original phases and recovery allowance. Qwen had transient NotFound responses; its frozen route was present again in the read-only route check before resumption.
