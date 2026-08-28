# 0826 — endgame curves, split by opponent

A new iteration of `results/0824_think_curves/reasoning_markers.png`, on the
fixed simulator, with the roster split by punishment shape instead of pooled.

## What changed from 0824

| | 0824 (`think2`) | 0826 (`think4`) |
|---|---|---|
| arms | 3 (nohole / eg / inf) | 6 = {grim, tft} × (nohole / eg / inf) |
| opponent | rotating `{tft, grim, tf2t}` | one pinned shape per run, **no tf2t** |
| horizon cue | total stated once, 20 turns before the decision | `core.annotate_horizon` restates "round i of N" on every finite cue |
| checkpoints | every 22, then every 10 | every 5 from step 0 |

**Why tf2t had to go.** `hole_exp/results/SIM-ENDGAME-TIMING.md` (regenerated on
this box, 2026-08-26) replays every nohole cell three ways — honest, betray at
N-1, betray at N — and reads off whether the last round is really the only safe
place to defect. grim and tft pass `early_punished` in every cross-round cell.
tf2t **fails** it in `ipd`, `ipd3` and `staghunt`: it forgives the first
defection by construction, so an N-1 betrayal costs nothing and the endgame
stops being special. A curve averaged over all three shapes was averaging in a
counterpart that cancels the contrast.

## The six runs

`hole_exp/runs/mixed_think4_nohole-think-{grim,tft}_d1_s0[_eg2|_inf]`

Qwen3.8-27B, thinking on at effort `low`, 7 envs
(`ipd public_goods dond trust ipd3 staghunt winasmuch`, `ultimatum` held out),
dose 1.0, seed 0, 14 groups × 6, t0.7 / top_p 0.9 / 1024 tokens.

Only `core.SHAPE_ENVS` — ipd, ipd3, staghunt, winasmuch — carry a matched
grim/tft pair, so the two arms differ in **4 of 7** envs and the other three are
shared ballast. That is deliberate: it keeps the roster identical to the rest of
the wave, and because every metric is logged per-env the clean 4-env contrast is
recoverable from the same runs without retraining.

Launch: `hole_exp/run_think4_endgame.sh --all`

## Regenerating the figure

```bash
cd hole_exp && ./refresh_think4.sh          # viewer pages + figure, one pass
```

The figure venv is `/home/ubuntu/venvs/tools` (matplotlib only); the suite venv
`/home/ubuntu/venvs/tinker-ipd` has the env stack and no matplotlib.

## Two viewer feeds, and why only one can be scored

| page | source | has reasoning? |
|---|---|---|
| `traces-t4-<arm>` | `runs/<arm>/traces/` — the episodes actually trained on | **no** |
| `traces-think-t4-<arm>` | fresh episodes re-sampled from each frozen checkpoint | **yes** |

`train_mixed.py` splits `<think>` off the sample before the env parses the
action, and records only the answer — so the dumped training traces carry no
reasoning and cannot be scored for markers. The marker panels are therefore
scored off the re-sampled pages, exactly as the 0824 figure was, written by:

```bash
python traces_over_training.py --runs "mixed_think4_*" \
  --envs ipd trust ipd3 staghunt winasmuch \
  --seeds 3 --temperature 0.7 --max-tokens 1024 --think --watch
```

Those five envs are the ones that HAVE an endgame; `sim_endgame_timing` reports
`public_goods`, `dond` and `ultimatum` as `no_endgame_hole` (their consequence
lands within the round), so backward-induction markers there would be scored
against episodes with no endgame to reason about. The behaviour panels come from
the training log and still span all seven trained envs — the two panels are not
the same denominator, and the panel notes say so.

Viewer: `SkyRL-Fleet/tools/trace-viewer/serve.sh 8792 0.0.0.0`
