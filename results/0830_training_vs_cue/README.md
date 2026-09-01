# 0830_training_vs_cue

`0830-endgame-summary.md` §7 argues "the endgame is a cue, not a disposition" from
three strands — §7.1 a training-log window (steps 8–16), §7.2 a within-checkpoint
prompt swap at step 35, §7.3 marker counts at that same checkpoint. The last two
are single-checkpoint by construction. So which of it is actually a **training**
effect?

**Almost all of it is present at step 0.** In `hole_exp/train_mixed.py` the loop
samples rollouts, then calls `tc.optim_step(...)`, then logs the step's metrics from
the PRE-UPDATE rollouts, so **step 0 is the untrained policy** and anything already
present at step 0 was not installed by training. The `inf` endgame collapse, the
concentration inversion, and §7.3's `notices_unknown` manipulation check are all
already true before the first gradient step. Training does three things: overall
defection roughly halves in every arm; final-window defection does not fall with it,
so the concentration index roughly doubles — **training does not teach the endgame,
it prunes everything that is not the endgame**; and the endgame penalty's `tft`
suppression is genuinely trained, indistinguishable at step 0 and clearly separated
by steps 30–37. This does not contradict §7's conclusion — step-0 evidence makes
the "cue, not disposition" case more strongly than §7 does. What it revises is the
attribution to training.

Write-up:
[`research_logs/0830-endgame-summary.md`](../../research_logs/0830-endgame-summary.md)
§7.4. Companion reasoning result:
[`research_logs/0830-endgame-reasoning.md`](../../research_logs/0830-endgame-reasoning.md)
§3.

Scope: dense training log `/shared/allie/think4/runs/*/metrics.jsonl` over all 7
trained envs, six arms × 2–3 seeds, plus a one-seed reasoning panel from
`results/0826_think_curves/reasoning_markers.json`.

## Files

| file | what it is |
|---|---|
| `fig1_training_vs_cue.{py,png,json}` | concentration index (`train/endgame_rate` / `train/exploit_rate`, per seed then averaged, between-seed SE) over training windows step 0, 8–16, 16–19, and 30–37, with a one-seed reasoning-marker panel at step 0 against the pooled 0–35 deltas. |

The figure writes a paired `.json` with the exact numbers behind it. **Read the
JSON rather than the PNG** when quoting a number.

## What the figure shows

Concentration index (`train/endgame_rate` / `train/exploit_rate`, per seed then
averaged, between-seed SE):

| arm | step 0 | 8–16 | 16–19 | 30–37 |
|---|---|---|---|---|
| grim + base | 0.71 ± 0.13 | 1.26 ± 0.14 | 1.46 ± 0.09 | 1.61 ± 0.15 |
| grim + eg | 0.67 ± 0.07 | 0.92 ± 0.17 | 1.30 ± 0.27 | 1.82 ± 0.06 |
| grim + inf | 0.22 ± 0.13 | 0.44 ± 0.05 | 0.70 ± 0.20 | — |
| tft + base | 1.08 ± 0.06 | 1.34 ± 0.14 | 1.76 ± 0.14 | 2.34 ± 0.23 |
| tft + eg | 0.90 ± 0.05 | 1.25 ± 0.15 | 1.41 ± 0.21 | 1.60 ± 0.36 |
| tft + inf | 0.22 ± 0.07 | 0.33 ± 0.07 | 0.62 ± 0.14 | 1.14 (n=1) |

n = 3 seeds base/eg, 2 for `inf`.

### This table is a snapshot — the `inf` cells are still training

The four `inf` runs append to `metrics.jsonl` while this is being read. Both
seeds of both `inf` arms are now past step 19, which freezes every column above
except **30–37**, where `grim/inf` has no cell and `tft/inf` has only s1. That
`1.14` is the one number here that will move: it becomes n=2 once `tft/inf` s0
reaches step 30. **Re-run the figure before quoting the late column.** The
base/eg rows are final. `fig1_training_vs_cue.py` takes `--max-step` to pin the
frontier for an exactly reproducible render, and names the live cells in its
coverage footer.

Already true at step 0: the `inf` endgame collapse (`endgame_rate` 0.068 grim /
0.046 tft at step 0 against the 0.054 / 0.039 §7.1 reports at steps 8–16); the
concentration inversion (`inf` 0.22 against base 0.71 / 1.08); and §7.3's
manipulation check (`notices_unknown` 0.125 grim / 0.115 tft against 0.000 in the
horizon-visible arms).

Three things change over training: (1) overall defection roughly halves in every
arm (`exploit_rate` grim/base 0.386 → 0.169, tft/base 0.307 → 0.159); (2)
final-window defection does not fall with it (`endgame_rate` grim/base 0.269 →
0.267, tft/base 0.332 → 0.371), so the concentration index roughly doubles; (3)
the endgame penalty's `tft` suppression is genuinely trained, indistinguishable at
step 0 (0.332 base vs 0.300 eg) and clearly separated by steps 30–37 (0.371 vs
0.146).

## Regenerating

Run from anywhere; the script resolves its paths from `__file__`.

```bash
PY=/home/allie/venvs/tools/bin/python
cd /home/allie/strategy-behavior/results/0830_training_vs_cue
$PY fig1_training_vs_cue.py   # -> fig1_training_vs_cue.{png,json}
```

## Caveats

`endgame_rate` divides by the exogenous late window while `exploit_rate` is over
all rounds, so the concentration index is an INDEX not a probability and it inherits
`core.py`'s warning that `endgame_rate` is not comparable across counterparts — the
reliable read is the WITHIN-arm change over training.

`inf` has 2 seeds and is shallow: three of its four cells are around step 20 and
still climbing, only `tft/inf` s1 is deep. No `grim/inf` cell reaches the 30–37
window and only `tft/inf` s1 does (so 1.14 is n=1, no error bar).

All reasoning-marker numbers are one seed, 192 blocks/point.
