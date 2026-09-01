# 0830_grim_vs_tft

Did training an RL policy against a `grim` trigger opponent, rather than against
`tit-for-tat`, produce a behaviourally different policy?

**No — the two arms converge on the same strategy, and the mechanism is that the
part of the game where the two opponents differ is essentially never visited.**
Both arms open C in 100% of episodes, run the full 10 rounds, cooperate at
0.908 ± 0.017 (grim) against 0.897 ± 0.010 (tft) late in training, and in every
one of the six cells `ever_defect` equals `defects_last_round` to three decimals:
every defection this policy makes is a final-round defection. A final-round
defection leaves neither opponent a round in which to punish, so grim and
tit-for-tat are observationally the same script there. Rounds 1–7 of the
10-round training episodes carry a defection hazard of **exactly 0.000 in every
seed of both arms**, the share of rounds played after an opponent defection
peaks at **0.0023** (tft/base, the largest value in the late window), and the
repair path that alone separates the two opponents — defect early, be punished,
return to cooperating, see whether the opponent forgives — completes **once in
616 ipd episodes**. Holding the played opponent fixed in crossplay, 1 of 26
testable contrasts clears 2 SE and **0 do so with both sides varying**.

**The one real exception is the interaction with the endgame-penalty arm.** On
the three envs whose opponent populations are identical in both arms, the
baseline pair does not separate (grim − tft `exploit_rate` **+0.010 ± 0.010**,
1.0 SE) while the `eg` pair does (**+0.055 ± 0.022**, 2.5 SE). The same knob
pulls `train/endgame_rate` down **−0.044 ± 0.013** against grim and
**−0.159 ± 0.067** against tft, a factor of 3.6. So the opponent split changed
what the penalty had to work with, not the policy the baseline arms learned.

Scope: `think4`, Qwen3.8-27B, local PEFT LoRA, 7 social-dilemma envs, 3 training
seeds per cell. Training traces cover 16 cells / 850 kept ipd episodes;
frozen-adapter evaluation is at **step 35** only. Every error bar is between
training seed.

Snapshot: `run_state` digest **`d31ee6ab23176486`**, captured **2026-08-30
22:26:53 UTC**, recorded in `train_strategy.json` under `meta.run_state`. The
source runs are live and still appending, so two caches describe the same data
only if their digests match, which is why `build_train_cache.py` writes each
run's `metrics.jsonl` mtime and newest trace-file mtime into that block. Every
number below was read out of the six JSON files in this directory, all
regenerated from that snapshot.

## Reproduce

Run from anywhere; every script resolves its paths from `__file__`. Order
matters — the figures read the two caches.

```bash
PY=/home/allie/venvs/tinker-ipd/bin/python
cd /home/allie/strategy-behavior/results/0830_grim_vs_tft

$PY strategy_stats.py               # optional; prints the pooled ipd table, writes nothing
$PY build_train_cache.py            # -> train_strategy.json
$PY build_eval_cache.py             # -> eval_strategy.json

$PY fig1_strategy_evolution.py      # train cache only
$PY fig2_unreachable_difference.py  # both caches
$PY fig3_opponent_or_policy.py      # both caches
$PY fig4_knob_by_opponent.py        # both caches
```

Options are uneven. `strategy_stats.py` takes **no arguments at all** and writes
beside itself. `build_eval_cache.py` takes `--outdir` only.
`build_train_cache.py` takes `--outdir` and `--update-ground-truth`. The four
figure scripts take `--outdir`, `--dpi` (default 150, the repo's render setting)
and `--stem`. On all six, the *input* caches are always read from the script's
own directory regardless of `--outdir`, so `build_eval_cache.py --outdir /tmp`
produces a cache the figures will not see.

`--help` is free on all six. Every script parses its arguments before it opens a
run directory or draws anything, so usage prints without a build or a render.

`build_train_cache.py` checks what it observes against a `GROUND_TRUTH` table
recorded in its own source. The two halves of that table mean different things.
Episode counts are **informational**: the runs only append, so growth says
nothing about correctness and a count that *falls* is the hard failure. The
rates are the guard: drift above 0.005 warns, and drift above **0.02 fails the
build**. A hard failure there means the live runs moved, not that anything in
this directory is broken — re-derive the numbers, then refresh the table.
Refreshing is a deliberate one-command act, `--update-ground-truth`, which
rewrites the literal in place and prints every cell it changed. The table is
never edited by hand, or it stops being a record of what a build actually saw.

## Files

| file | what it is | reads | writes |
|---|---|---|---|
| `strategy_stats.py` | the single definition site for every behavioural statistic, plus the trace/metrics loaders. Imported by the cache builder so the figures and the cache cannot disagree about what `defect_before_last` means. Run directly, prints the pooled ipd table. | `/shared/allie/think4/runs/<label>/traces/step_*.jsonl` | nothing |
| `build_train_cache.py` | groups, pools and serialises the training-trace statistics; pins the input snapshot as a `run_state` digest and checks a recorded ground-truth table on every build. | the run dirs, via `strategy_stats`; `<label>/metrics.jsonl` | `train_strategy.json` |
| `build_eval_cache.py` | the frozen step-35 evidence: crossplay 2×2, held-out horizons, reasoning markers, and the expanded eval cached only to rule it out. | `hole_exp/results/think4_evals/{B_crossplay,A_endgame_length}.jsonl`, `results/0830_endgame_traces/trace_blocks.jsonl`, `hole_exp/results/eval_grimtft_expanded/*.json` | `eval_strategy.json` |
| `train_strategy.json` | 1.1 MB cache: `by_step`, `pooled_late` (steps ≥ 25), `pooled_all` (steps ≥ 5), `step0`, `hazard`, `funnel`, `shared_opponent_envs`, `metrics_curves`, and a `meta` block pinning provenance and denominators. | — | — |
| `eval_strategy.json` | 343 KB cache: `crossplay` (with an auto-derived `verdict`), `endgame_length` (twice — see below), `reasoning_markers`, `eval_grimtft_expanded`. | — | — |
| `fig1_strategy_evolution.{py,png,json}` | the baseline opponent contrast over training, 8 panels. | `train_strategy.json` | png + json |
| `fig2_unreachable_difference.{py,png,json}` | where in the game the two opponents differ, and whether the policy goes there. | both caches | png + json |
| `fig3_opponent_or_policy.{py,png,json}` | the three handles that break the ipd confound: shared-opponent envs, crossplay, held-out horizons. | both caches | png + json |
| `fig4_knob_by_opponent.{py,png,json}` | the one place the opponent matters — its interaction with the endgame penalty. | both caches | png + json |

Every figure writes a paired `.json` with the exact numbers behind it. **Read the
JSON rather than the PNG** when quoting a number.

## What each figure shows

- **fig1 — strategy evolution.** Panels 3 (`defect_before_last`) and 6
  (`rounds_in_punishment`) are tinted because they are the only place on the page
  where a difference could live; panels 1, 2, 4 and 5 are the agreement. Late
  `defect_before_last` is grim 0.121 ± 0.072 against tft 0.104 ± 0.032. Panel 6
  is empty by construction: grim/base is identically 0.000 at every step and
  every seed.
- **fig2 — the unreachable difference.** Training hazard by round (A) and frozen
  step-35 hazard by distance from the end at N = 6, 10, 14 (B): the spike tracks
  the *end of the game*, not a memorised round number, and beyond two rounds from
  the end every arm is exactly 0.000 at every horizon. (C) exposure, (D) the
  repair funnel: grim/base 14/149 episodes defect before the last round, all 14
  are retaliated against, **0 return to cooperating**; tft/base 22/168, 22
  retaliated, 1 returns, 1 forgiven. That one episode is the entire training
  signal separating the two opponents. grim's forgiveness stage is `n/a` by
  construction, not a measured zero. **Panel D does not share a window with the
  rest of the page.** A and C are steps ≥ 25; D is **steps ≥ 5**
  (`TRAINED_STEP`, not `LATE_STEP`), because the cache builds the funnel at that
  floor and at no other. The 616-episode denominator and the 1-in-616 count are
  therefore steps ≥ 5 numbers, and the wider window is the conservative one for
  this claim. The script says so on the figure and under
  `panels.D_repair_funnel.window`; restricted to steps ≥ 25 the same four cells
  hold 328 episodes and can contain at most the same 1 completion.
- **fig3 — opponent or policy.** The shared-opponent envs over training and as an
  endpoint (A, B), crossplay with the played opponent held fixed (C), and
  held-out horizons (D, all four arms fit slope ≈ +1.0 against N). The forest in
  C is the decisive object: baseline `exploit_rate` contrasts are −0.012 ± 0.013
  and −0.003 ± 0.012. The count over all metrics is **1 of 26 testable contrasts**
  over 2 SE. The cache holds 28 condition × plays × metric contrasts, and 2 of
  them are untestable: `frac_any_defect` for the baseline arms against each
  played opponent pins both arms at 1.000, so the delta and its quadrature SE are
  both zero and |z| is undefined. Those two are excluded from every count rather
  than scored as nulls.
- **fig4 — the knob by opponent.** `train/endgame_rate` over training (A), the
  behavioural decomposition of what the knob moves (B — how often the buzzer-beater
  is taken, not when defection starts), the transfer test with its
  `eg − base` deltas (C), and the reasoning markers (D). Five of the eight markers
  clear the 0.02 floor; `m_endgame_defect_plan` moves `eg − base` by −0.083 ± 0.167
  against grim and −0.288 ± 0.115 against tft, the same asymmetry as the behaviour.

## Data provenance

Training traces come from `/shared/allie/think4/runs/<label>/traces/step_NNNN.jsonl`
and the dense per-step scalars from `<label>/metrics.jsonl`, with the run label

```
mixed_think4_nohole-think-{grim,tft}_d1_s{0,1,2}[_eg2|_inf]
```

— no suffix is the baseline arm, `_eg2` the endgame-defection penalty, `_inf` the
scrubbed round count. Sixteen of the twenty-four surveyed dirs carry traces;
`_s3` was launched for every cell and never produced a rollout, and `grim/inf/s2`
and `tft/inf/s2` are empty.

The `GROUND_TRUTH` table was refreshed at this snapshot, so the current cache
reports **no episode growth, no rate warnings and no rate failures**: all six
cells come in at status `ok` with `n_episodes_delta` 0. Expect that to stop being
true as the `tft` cells keep appending steps. The digest is written into
`train_strategy.json` alone — the figure JSONs and `eval_strategy.json` pin their
input by path, size and mtime instead — and `fig4`'s `caveat.ground_truth_warnings`
still lists the five drift warnings from the build that rendered it, one
`--update-ground-truth` before the table was refreshed. Every statistic in the
figure JSONs matches the current cache; only that bookkeeping block is behind.

Frozen-checkpoint evidence comes from
`hole_exp/results/think4_evals/A_endgame_length.jsonl` (672 rows; 576 after
restricting to the four grim/tft × base/eg arms, 575 after the `invalid_rate`
gate) and `hole_exp/results/think4_evals/B_crossplay.jsonl` (208 rows, 189 kept),
plus `results/0830_endgame_traces/trace_blocks.jsonl` (12,480 reasoning blocks)
for the marker panel. All are opened read-only.

## Four things to know before trusting any number here

**Trace dumps are a sample, not the training log.** They are the *first 24
episodes of every fifth training step*, covering exactly four envs at six
episodes each, so `ipd` contributes roughly 6 episodes per step per seed. The
envs `ipd3`, `staghunt` and `winasmuch` therefore **never appear in the traces at
all**, even though they do feed the pooled `train/*` metrics in
`metrics_curves`. Trace-derived and metrics-derived numbers have different
denominators and must never be divided by one another.

**Only `ipd` pins the grim/tft contrast, and that is exactly why it cannot answer
the question.** In `ipd` the opponent *is* the manipulation, so any difference
measured there confounds a learned-policy difference with the fact that the
opponent itself differs. `public_goods`, `dond` and `trust` draw identical
opponent populations in both arms — public_goods `strict_punisher` /
`conditional_punisher` / `conditional_noisy`; dond `sceptic` / `auditor` /
`verifier`; trust `responsive` / `impatient` / `responsive_exit`, verified
against every trace file and re-asserted at build time under
`meta.opponent_populations`. Those three are the unconfounded transfer test, and
the two groups are kept in separate sections of the cache and never pooled.

**Every error bar is between training seed.** Collapse each seed to one number
first, then take `sd(ddof=1)/sqrt(n)` across seeds. Fewer than two seeds yields a
null SE and draws no bar — never a zero-length one, which would read as a
measured zero spread. Pooling episode seeds instead treats correlated rollouts
from one LoRA as independent draws, and that is what produced the sign flip in
[`research_logs/0826-endgame-by-opponent.md`](../../research_logs/0826-endgame-by-opponent.md)
§4 that three seeds later contradicted. Differences taken within a checkpoint are
paired; differences taken across arms are unpaired quadrature, because train_seed
0/1/2 index different checkpoints in the grim and tft arms.

**Two cells are known bad.** `grim/nohole` train_seed 1 emits an empty decision
answer on **578 of 960 turns (60%)** while its `invalid_rate` reads **0.000**, so
the repo's gate is blind to it — `invalid_rate` counts actions the environment had
to substitute and says nothing about turns that produced no answer text.
`eval_strategy.json` therefore stores every A-file statistic **twice**, under
`all_seeds` and `excl_grim_nohole_s1`, and the figures draw the sensitivity rather
than silently choosing one (dropping it moves the grim/nohole final-round hazard
0.660 → 0.844 on two seeds, so the spike is not an artefact of that checkpoint).
Separately, the `inf` arm has at most two seeds in either opponent and `grim/inf`
stopped by step 20 with zero ipd episodes in the steps ≥ 25 window; it appears
only as a reference line and is never a tested condition.

### Naming gotcha

**The training cache calls the baseline arm `base`; the eval cache calls the same
arm `nohole`.** `train_strategy.json` has `grim/base`, `eval_strategy.json` has
`grim/nohole`, and they are the same runs. fig3 and fig4 both carry the mapping
explicitly (`ARM_TRAIN_TO_EVAL`, `EVAL_ARM`); anything new that joins the two
caches has to do the same.

## Colour encoding, and the inversion

**fig1 through fig3 encode the OPPONENT as colour** — `#00918f` grim, `#b8236f`
tft — because there the opponent is the contrast. **fig4 inverts this** and
encodes the **ARM** as colour using the repo's standing trio (`#7a5bd6` base,
`#eb6834` eg, `#2a78d6` inf), with the opponent carried by panel position, marker
shape (circle grim, square tft) and line style (solid grim, dashed tft), because
there the arm is the contrast. The inversion is stated on fig4 itself. Do not
carry a reading of colour from one figure to the other.

In both conventions colour is redundant, never load-bearing. The grim/tft pair
separates only at the **CVD floor** — `viz/validate_palette.py` gives deutan
dE 6.4 against a target of 8.0 and a floor of 6.0 — which is why every series is
also direct-labelled and given a distinct marker and dash pattern, and why
identity never rests on hue alone. The same rule matters more, not less, in fig4:
the arm trio is the weaker palette of the two — the same validator puts base
against inf at deutan dE 1.0 and normal-vision dE 10.7, below both thresholds —
so in that figure the marker, the line style and the panel are doing the work.

## What this does NOT show

**A wide interval containing zero is a failure to detect a difference, not a
demonstration that none exists.** With three training seeds per arm the
resolvable claim about the baseline arms is an *upper bound* on the size of any
policy difference, not its absence. What makes that bound informative rather than
merely underpowered is that the `eg` arm shows a difference at the same sample
size.

**Nothing here speaks to what happens later in training.** Both the crossplay and
the held-out-length evals are frozen at **step 35**, chosen because it is the
deepest step all the checkpoints share. Separately, the arms did not stop
together: on traces, grim/base holds three seeds only to step 30 and tft/base to
step 40; on the dense metrics, grim/base to step 34 and grim/eg to 37 against
tft/base 44 and tft/eg 46. The rightmost points of every curve rest on fewer
seeds, so late movement there is a change in *which* seeds are averaged. The
3.6× asymmetry in fig4 should be read as an upper bound on the tft side rather
than a calibrated ratio, since the tft knob had more training over which to act.

**`hole_exp/results/eval_grimtft_expanded/` is not a grim-vs-tft comparison.** It
looks like one and it is not usable as one. Its `grim_trained` file is
`mixed_think3_nohole-think-grim_d1_s0_inf-step0040` — the **hidden-horizon** arm
at **step 40** — while its `tft_trained` file is
`mixed_think3_nohole-think-tft_d1_s0-step0030` — the **baseline** arm at **step
30**. Training opponent, manipulation, step *and* model generation (think3, not
the think4 wave analysed everywhere else) all vary at once, with one seed each
and no error bar. It is cached in `eval_strategy.json` only so this comparison
can be explicitly ruled out.

**The reasoning-marker and held-out-length files are diagonal only.** Every row
in `A_endgame_length.jsonl` and `trace_blocks.jsonl` satisfies `opponent ==
arm.split('/')[0]`, so each arm plays only the opponent it trained against and
those files cannot separate the policy from the environment. Any grim-vs-tft gap
in fig2 panel B or fig4 panel D is policy and environment together. The
separation lives in `crossplay.trained_vs_contrast` and nowhere else.

**The largest crossplay contrast is not a result.** The single contrast that
clears 2 SE (`eg`, plays grim, `frac_any_defect`, +0.250 ± 0.072, 3.46 SE) has
**zero between-seed variance on the grim side** — every seed pinned at the same
value — so the quadrature SE carries only the tft arm's spread and understates
the uncertainty. Read that |z| as optimistic.

**`grim/base`'s forgiveness stage is not a measured null**, and neither is the
one-episode `tft/base` cell a rate. grim never forgives by definition of the
opponent, and a funnel stage with a denominator of 1 carries `se: null` and no
error bar.

## Cross-references

- [`research_logs/0830-endgame-summary.md`](../../research_logs/0830-endgame-summary.md)
  — **§10, "Grim vs tit-for-tat across every arm", is this analysis in prose**,
  and carries its own reproduce block; this README is the operational companion
  to it. §6 ("It learned the game, not the opponent") is the crossplay result
  these figures expand on, and §1/§8 carry the 3–4× interaction-of-magnitude
  claim that fig4 quantifies.
- [`research_logs/0830-endgame-traces.md`](../../research_logs/0830-endgame-traces.md)
  — the reasoning-side companion; `trace_blocks.jsonl` from that analysis is an
  input here.
- [`research_logs/0826-endgame-by-opponent.md`](../../research_logs/0826-endgame-by-opponent.md)
  — the one-seed predecessor. Its §4 "flips sign with the opponent" headline is
  superseded; the between-seed error-bar rule above exists because of it.
- [`results/0830_endgame_traces/`](../0830_endgame_traces/) — sibling figures,
  and the source of the `grim/nohole` seed-1 and `tft/inf` duplicate-batch
  hazards documented in its README.
- [`results/0830_endgame_reasoning/`](../0830_endgame_reasoning/) — sibling
  figures on reasoning versus behaviour.
