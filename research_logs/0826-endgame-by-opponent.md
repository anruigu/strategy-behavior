# 0826 — endgame arms, split by the opponent that punishes

Fresh `think4` wave on the fixed simulator. Six runs, `{grim, tft} × {nohole,
endgame-penalty, hidden-horizon}`, tit-for-2-tats dropped from both arms.
Figure: `results/0826_think_curves/reasoning_markers.png`.

**Status when these numbers were taken (2026-08-26 06:30Z): step 12–18 of 150,
one seed.** Everything below is preliminary and the reasoning panels in
particular are not yet separated. Runs are still going.

---

## 1. Why tf2t had to go — the simulator says so, not just the complexity budget

`sim_endgame_timing.py`, regenerated on this box, replays every nohole cell
three ways (honest / betray at N-1 / betray at N) and asks whether the last
round is really the only safe place to defect:

| opponent | `endgame_paid` | `early_punished` |
|---|---|---|
| grim (all 4 cross-round cells) | PASS | **PASS** |
| tft  (all 4 cross-round cells) | PASS | **PASS** |
| tf2t (ipd, ipd3, staghunt) | PASS | **FAIL** |

tf2t forgives the first defection by construction, so betraying at N-1 costs it
nothing and the endgame stops being special. A curve averaged over
`{tft, grim, tf2t}` was averaging in a counterpart that cancels the contrast.

`check_suite.py`: 70/70 cells pass.

## 2. The step-0 row is a wiring check, and it passes

Step 0 is the untrained base policy, so each knob may only move what its design
says it can reach:

| arm | R | exploit | endgame |
|---|---|---|---|
| grim | +0.639 | 0.422 | 0.280 |
| grim + eg | +0.573 | 0.391 | 0.252 |
| grim + inf | +0.646 | 0.282 | **0.048** |
| tft | +0.677 | 0.357 | 0.266 |
| tft + eg | +0.666 | 0.267 | 0.262 |
| tft + inf | +0.718 | 0.164 | **0.012** |

- `eg` matches its baseline on behaviour (0.252 vs 0.280; 0.262 vs 0.266) — correct,
  the penalty is reward-only and cannot reach the observation. Its reward IS
  docked (+0.573 vs +0.639), which is the knob proving it is live.
- `inf` diverges immediately — correct, scrubbing the round count is an
  observation change and bites with no learning at all.
- grim ≈ tft at step 0 — correct, the two counterparts are indistinguishable
  until the learner first defects.

## 3. Two clean validity results on the reasoning side

Both hold at every step, in every arm, on 192 reasoning blocks per point:

- **`shaping_awareness` ≈ 0 everywhere** (a single hit, tft/nohole step 0).
  As `endgame_awareness.py` argues, this is close to structurally impossible:
  the penalty is applied after the episode to a scalar the policy never
  observes, and there is no cross-episode memory. Nothing to condition on.
- **`notices_unknown` fires only where the horizon is actually missing** —
  exactly `0.000` in all four finite arms, `0.104–0.146` in both `inf` arms.
  The marker is measuring the manipulation and not the vocabulary.

## 4. The finding worth watching: the endgame penalty flips sign with the opponent

Mean `train/endgame_rate` over steps ≥ 8:

| | baseline | + endgame penalty | Δ | + hidden horizon | Δ |
|---|---|---|---|---|---|
| **vs grim** | 0.229 | 0.279 | **+0.050** | 0.028 | −0.201 |
| **vs tft** | 0.308 | 0.251 | **−0.057** | 0.061 | −0.246 |

Against tit-for-tat the hidden penalty does what it was built to do — it pushes
late betrayal down. Against grim it does not; late betrayal sits *above* the
matched control.

Relative to step-to-step spread inside that window the gaps are ~3.7 SE (grim)
and ~4.4 SE (tft). **That SE is the wrong error bar for the claim** — adjacent
steps of one run are correlated and there is one seed, so it bounds "is this
step-to-step noise" and not "is this the effect of the knob". Treat the
direction as a lead, not a result.

If it holds, it is the thing the split was built to expose: pooled over both
opponents the two deltas nearly cancel (+0.050 and −0.057 → ≈ −0.004), i.e. the
0824-style single curve would have reported the penalty as having no effect.

A mechanism worth testing: under grim the first betrayal ends cooperation for
good, so once the policy has defected there is nothing left to protect and the
marginal cost of *also* betraying late is near zero — the penalty has no
behaviour left to price. Under tft the relationship is recoverable, so late
betrayal still costs something the policy can act on.

**`inf` dominates everything either penalty does**, in both blocks, and also
drops overall exploit_rate (−0.231 grim, −0.148 tft). Removing the cue beats
pricing the behaviour, which reproduces 0824 on the fixed simulator.

## 5. Reasoning panels: no separation yet

`backward_induction` and `endgame_defect_plan` differ between arms by less than
~2 SE (n = 192/point, SE ≈ 0.026 at p ≈ 0.15) apart from `inf` running low. The
one movement above noise is `tft/inf`, where backward induction climbs
0.057 → 0.156 → 0.141 and defect-plan 0.062 → 0.172 → 0.198 while `grim/inf`
stays flat at 0.068–0.109 — the hidden-horizon policy reaching for endgame
reasoning again despite having no stated total. Panel F says it is not because
it learned the length (`assumes_finite` stays ≤ 0.08). Too early to lean on.

## 6. Reproducing

```bash
cd hole_exp
./run_think4_endgame.sh --all     # the six runs
./refresh_think4.sh               # viewer pages + figure, one pass
setsid nohup ./watchdog_think4.sh &   # overnight keepalive
```

Viewer on :8792 from `/home/ubuntu/SkyRL-Fleet/tools/trace-viewer`
(branch `backup/2026-08-25` — `main` lacks the opponent-filter dropdown these
pages need). Env notes for this box are in `results/0826_think_curves/README.md`.

---

## 7. The wave stopped at step 13–20: Tinker billing, not a bug

At **08:04:1x Z on 2026-08-26** every sampling call began returning

```
tinker.APIStatusError: Error code: 402
  {'detail': 'Access for is blocked due to billing status.
              Please add payment at https://tinker.thinkingmachines.ai/billing/balance'}
```

All six training runs and the trace sweep died within four seconds of each
other. Nothing is wrong with the runs, the simulator, the box or the roster --
the account is blocked. `check_suite.py` (70/70) and `sim_endgame_timing.py`
both passed hours earlier on this same tree.

Final state, all six resumable from a saved state checkpoint:

| run | metrics reach | latest state ckpt |
|---|---|---|
| grim | 13 | 10 |
| grim + eg | 13 | 10 |
| grim + inf | 20 | 20 |
| tft | 13 | 10 |
| tft + eg | 14 | 15 |
| tft + inf | 14 | 15 |

Numbers in §4 are recomputed on the final data and unchanged in direction:
`eg − baseline` = **+0.039** vs grim, **−0.069** vs tft.

### Resuming

```bash
cd hole_exp
./resume_think4.sh --check     # probes billing, prints the resume plan
./resume_think4.sh --all       # resumes all six from their last state
```

`resume_think4.sh` recovers each cell's flags from its own `config.json` rather
than re-typing them, so a resumed run cannot silently change condition, and it
refuses to launch while the API still returns 402.

**One wrinkle it handles.** State is saved at the START of a checkpoint step, so
four of the six logged metrics PAST their last state (metrics reach 13, state is
at 10). Since `train_mixed.py` only ever appends, a naive resume would leave two
rows per step for 10–13 — and because the plot reads rows in file order, that
shows up as a curve doubling back on itself rather than as an error. The script
trims rows at `step >= start_step` first, keeping a `.pre-resume` backup;
`behaviour()` in the plot script now also dedupes by step, last write wins, as a
second line of defence for a hand-relaunched run.

Support processes were stopped (they would respawn the sweep every 5 min against
a permanent error). **The viewer is still up on :8792** — it serves static JSONL
and needs no API.
