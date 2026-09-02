# Handoff — resuming the `think4` endgame wave

**Written:** 2026-08-28 20:20 UTC.
**Audience:** the next agent picking up these training runs.
**Companion docs:** [`research_logs/0826-endgame-by-opponent.md`](research_logs/0826-endgame-by-opponent.md)
(what the runs are for and what they have shown so far),
[`results/0826_think_curves/README.md`](results/0826_think_curves/README.md) (figure pipeline).
[`HANDOFF.md`](HANDOFF.md) is a *different, older* doc about porting this work to
this box — that port is finished; don't re-do it.

> **If you are short on time:** §1 → §2 → §3. §3 is the one that will cost you a
> run if you skip it.

---

## 0. What this wave is

Six runs, `{grim, tft} × {nohole, endgame-penalty, hidden-horizon}`, on
Qwen3.8-27B with thinking on. Splits the 0824 endgame arms by the opponent that
punishes, instead of pooling them over a `{tft, grim, tf2t}` roster.
tit-for-2-tats is in **neither** arm, by request and because
`sim_endgame_timing.py` shows it is the member that fails `early_punished` — it
forgives the first defection, so an N-1 betrayal costs it nothing and it cancels
the contrast the wave exists to measure.

Run directories, all under `hole_exp/runs/`:

```
mixed_think4_nohole-think-grim_d1_s0        mixed_think4_nohole-think-tft_d1_s0
mixed_think4_nohole-think-grim_d1_s0_eg2    mixed_think4_nohole-think-tft_d1_s0_eg2
mixed_think4_nohole-think-grim_d1_s0_inf    mixed_think4_nohole-think-tft_d1_s0_inf
```

---

## 1. State right now

**All six are STOPPED.** Target is 150 steps.

| run | last step | max `invalid_rate` | last clean step | safe resume ckpt | health |
|---|---|---|---|---|---|
| grim | 38 | 0.093 | 38 | 35 | OK |
| grim + eg | 40 | 0.080 | 40 | 40 | OK |
| tft | 42 | 0.083 | 42 | 40 | OK |
| tft + eg | 50 | 0.120 | 50 | 50 | OK |
| tft + inf | 52 | 0.048 | 52 | 50 | OK |
One new training arm, if you spend one at all
Your disposition axis has two points and both are punishers. The cheapest genuine third point is the hole population — always-cooperate, doormat, noisy-cooperate — as a zero-consequence anchor, giving you no punishment, recoverable punishment, terminal punishment. It requires no new code because --consequence hole is fully wired across all seven envs, whereas a third --nohole-shape needs a named member registered in each of the four split envs. Against a non-punisher, endgame timing has no strategic content at all, so any endgame behaviour there is pure "the end is near" rather than "the relationship is over" — which is exactly the contrast your section needs to separate the two readings.

Two operational things bear on whether you can afford it. Both inf cells are currently dead, not from the step-50 collapse in §3 of your handoff but from a Triton compile failure where gcc reads the specs/ subdirectory in the working directory as a spec file, and the supervisor has backfilled their slots with seed-1 jobs. Since the hidden-horizon arm carries most of the endgame-reasoning story, that is worth fixing before anything else. And sampler capacity, not trainer capacity, is the binding constraint — about two spare slots against an eighteen-job seed queue. The seeds are the right thing to be spending on given that the log itself flags the within-run standard error as the wrong error bar, so I would not displace them for a third arm until the free analyses above tell you which arm is worth it.

Support processes are UP and harmless while training is down: watchdog, refresh
loop, trace sweep, and the viewer on `:8792`.

## 3. DO NOT blindly resume `grim + inf`

`mixed_think4_nohole-think-grim_d1_s0_inf` **degenerated into incoherent text**
between steps ~51 and 77. Resuming it from its latest state checkpoint (step 75)
would continue a broken policy and burn budget producing garbage.

The evidence, in order:

```
step 50  invalid=0.023  reward=+0.822
step 55  invalid=0.138  reward=+0.739
step 60  invalid=0.293  reward=+0.674
step 70  invalid=0.444  reward=+0.589
step 77  invalid=0.819  reward=+0.401
```

`train/think_truncated_rate` tracks `train/invalid_rate` almost exactly at every
step (0.817 vs 0.819 at step 77), which normally points at the token budget. **It
is not the budget.** `sampled_tokens_p90` *falls* from 571 to 157 against a
1024-token limit — the outputs got shorter, not longer. Reading the dumped
episodes at `runs/.../traces/step_0075.jsonl` settles it:

```
'Pickinggoddly to bet, gradegy waithas sumo current yeahimatelyites pefire
 tonesei playwright pragmaserverggillerenceastilation teaterright smart'
```

Word salad that never closes `</think>`, so `split_think` returns no answer and
`ipd_lib` substitutes its fallback (`[Cooperate]` on decisions, `(no comment)`
in chat). That is why `endgame_rate` reads a beautiful `0.000` at step 70+ —
**it is forced cooperation from a broken policy, not learned restraint.** Do not
report it as a result.

Note this is *related to* but distinct from the degenerate solution documented
in `core.py` (where garbage is scored as the honest branch and reward stays
flat). Here reward **falls** — `core.INVALID_COST` is charging it correctly — so
the policy is not being rewarded for this. It is a collapse, not a reward hack.
Cause is not diagnosed; that is open work.

**Recommended handling** (pick one, and say which in the log):

1. Resume from `state0050`, the last checkpoint with `invalid < 0.05`, and
   watch `invalid_rate` every step. If it climbs past ~0.15 again by step 60,
   the collapse is reproducible and worth treating as a finding rather than an
   accident.
2. Treat that arm as ending at step 50 and analyse it truncated. The other five
   arms are unaffected and the §4 result does not depend on it.

Whatever you choose, **trim `metrics.jsonl` to `step <= 50` first** (see §5) or
the collapsed rows stay in every figure.

## 4. What the runs have shown (preliminary)

Mean `train/endgame_rate` over steps ≥ 8, at the time of the first billing halt:

| | baseline | + endgame penalty | Δ | + hidden horizon | Δ |
|---|---|---|---|---|---|
| vs grim | 0.229 | 0.279 | **+0.050** | 0.028 | −0.201 |
| vs tft | 0.308 | 0.251 | **−0.057** | 0.061 | −0.246 |

**The hidden endgame penalty flips sign with the opponent** — it suppresses late
betrayal against tit-for-tat and fails to against grim. Pooled over both, the
deltas nearly cancel, so the 0824-style single curve would have called the
penalty inert. That is the wave's reason to exist.

Caveats that must survive into any write-up: one seed, ~40 steps of 150, and the
quoted SE is *within-run across adjacent steps*, which bounds "is this
step-to-step noise" and not "is this the effect of the knob".

Two clean validity results, on 192 reasoning blocks per point:
`shaping_awareness` ≈ 0 in every arm (structurally expected), and
`notices_unknown` is exactly `0.000` in all four finite arms vs `0.104–0.146` in
both `inf` arms — the marker measures the manipulation, not the vocabulary.

## 5. How to resume

```bash
cd /home/ubuntu/strategy-behavior/hole_exp
./resume_think4.sh --check     # billing probe + plan, launches nothing
./resume_think4.sh --all       # resume all six from their last state ckpt
setsid nohup ./watchdog_think4.sh >> logs/think4/watchdog.log 2>&1 &
```

`resume_think4.sh` rebuilds each cell's flags from **that run's own
`config.json`** rather than re-typing them, so a resumed run cannot silently
change condition, and it refuses to launch while the API returns 402.

**It does not know about §3.** To resume `grim + inf` from step 50 instead of 75,
either delete the state entries above 50 from its `checkpoints_state.json`, or
launch that one by hand with `--resume-from <state0050 uri> --start-step 50`.

**The overlap trim.** State is saved at the *start* of a checkpoint step, so a
run can log metrics past its last state (e.g. metrics reach 38, state at 35).
`train_mixed.py` only ever appends, so a naive resume leaves two rows for the
same step — and since the plot reads rows in file order, that renders as a curve
doubling back on itself rather than as an error anyone notices.
`resume_think4.sh` trims `step >= start_step` first and keeps a
`metrics.jsonl.pre-resume` backup; `behaviour()` in the plot script also dedupes
by step (last write wins) as a second line of defence.

## 6. This box has four traps in it

Everything here is already fixed — this is so you don't "fix" it back.

1. **TextArena must be the 0.7.3 checkout at `/workspace/allie/TextArena`**, not
   a pip install. PyPI 0.6.4 uses `is_decision_phase`/`current_round` where
   `ipd_lib` expects `phase`/`round`, and its `close()` returns a bare dict that
   crashes every game cell. The pip package is uninstalled and a
   `zz_textarena_checkout.pth` in the `tinker-ipd` venv pins the checkout, so the
   binding no longer depends on import order.
2. **`WANDB_API_KEY` in `~/.research_env` is the wrong key.** It authenticates as
   `anrui0706`, who has no `thefleet` entity, and `--wb-entity thefleet` then
   fails with a bare `permission denied` *after* the run has started.
   `FLEET_WANDB_API_KEY` is the right one. The launchers prefer it and probe auth
   up front. Worth fixing at the source, but other things may use the personal key.
3. **Two venvs, on purpose.** `venvs/tinker-ipd` has the env stack and *no*
   matplotlib; `venvs/tools` has matplotlib and nothing else. The plot scripts
   only read JSONL, so they run in the small one. Don't merge them —
   `endgame_awareness.py` documents why importing `to_viewer` in the plotting
   venv is fatal.
4. **`/workspace/allie/*` are compatibility symlinks.** ~100 hardcoded
   `/workspace/allie` paths across the repo resolve through them to
   `/home/ubuntu/...`. `SkyRL-Fleet` is canonical at `/home/ubuntu/SkyRL-Fleet`
   on branch **`backup/2026-08-25`** — `main` lacks the opponent-filter dropdown
   these pages need. `/workspace/allie/SkyRL-Fleet.old` (108M) is a redundant
   clone, safe to delete.

**And one trap for you, not the box:** `pkill -f think4` / `pgrep -f` will match
your *own shell's* command line and kill it mid-script. It cost two incidents
here — a half-finished migration, and a watchdog that reported the viewer
healthy while it was down. Kill by PID from a script file, or probe the port
(`curl`) instead of the process name.

## 7. Monitoring you should re-arm

The `grim + inf` collapse happened while nothing was watching for it. There was
an `invalid_rate > 0.30` alert, but it was retired during the billing halt and
never re-armed after the resume — which is exactly when it would have earned its
keep. **Re-arm it.**

```bash
tail -n 0 -F logs/think4/*.log | grep -E --line-buffered "invalid=0\.[3-9]|invalid=1\.0"
```

`watchdog_think4.sh` (5-min loop) restarts the sweep, refresh loop and viewer,
and logs a per-run step line. It deliberately does **not** restart dead training
runs: a relaunch without `--resume-from` starts at step 0 and appends a second
trajectory under the same label, which is the mixed-provenance mess the
`think3` directories are already in.

## 8. File map

| path | what |
|---|---|
| `hole_exp/run_think4_endgame.sh` | original launcher (fresh runs) |
| `hole_exp/resume_think4.sh` | `--check` / `--all`, resume from state ckpts |
| `hole_exp/refresh_think4.sh` | viewer pages + figure; `--loop N` to keep going |
| `hole_exp/watchdog_think4.sh` | keepalive for the support processes |
| `hole_exp/logs/think4/` | per-cell logs, `watchdog.log`, `traces-sweep.log` |
| `results/0826_think_curves/plot_reasoning_markers_by_opponent.py` | the figure |
| `results/0826_think_curves/reasoning_markers.{png,json}` | current output |
| `research_logs/0826-endgame-by-opponent.md` | findings + the billing halt |

**Two viewer feeds, and only one can be scored.** `traces-t4-*` are the episodes
actually trained on, lifted free from `--dump-traces` — but they carry **no
reasoning**, because `train_mixed.py` splits `<think>` off before the env parses
the action and records only the answer. The marker curves are scored off
`traces-think-t4-*`, which are fresh episodes re-sampled from each frozen
checkpoint with thinking on, written by the long-running
`traces_over_training.py --think` sweep. That sweep needs Tinker, so it is dead
whenever billing is.
