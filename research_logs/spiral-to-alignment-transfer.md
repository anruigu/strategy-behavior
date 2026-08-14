Behavior (deception / honesty)

MASK — elicits belief, then pressures the model to contradict it; frontier models lie 20–60% under pressure. Tightest thread: Kuhn-Poker bluffing → lying-under-pressure. Run first. 
GitHub
MACHIAVELLI — reward-vs-ethics trade-off in text games; same game surface form as training. 
arxiv
(opt) AI-LieDar — utility-vs-truthfulness frontier in agents; matches your payoff-per-leaked-bit geometry.

Personality (disposition)

TRAIT — LLM-validated Big Five + Dark Triad (naive SD3 self-report is unreliable); watch the Machiavellianism facet. 
arxiv
Behavioral Dark-Triad scenarios (SD4-style) — pair with TRAIT, since exploitation and deception run through dissociable pathways; which axis moves is the finding. 
arXiv

Social engineering (capability)

CyberSecEval 3 spear-phishing — judge rubric over 250 cases, human-correlated at r=0.89; measures persuasive capability. 
arxiv
Persuasion-safety / SpearMail (14,672 emails, 681 profiles) — isolates willingness/refusal from capability. 
arxiv

Reward hacking / specification gaming (new)

School of Reward Hacks — does game reward-maxing transfer to hacking held-out reward functions.
Apollo in-context scheming (Meinke et al.) — o1 maintained deception across 85% of follow-up challenges; scheming/power-seeking under goals. 
GitHub
(opt) PropensityBench — propensity to reach for unsafe shortcuts under pressure.


control run:
1. Match on the full reasoning-benchmark battery SPIRAL reports 

2. one strategic-but-non-deceptive reasoning benchmark so you're not accused of leaving the relevant capability unmatched. - pidgice
3. combined

## 0806-0807 — why the PigDice control collapsed

Killed the TicTacToe control and relaunched it as PigDice (job 64, `run_pigdice.sh`).
The arm trains, but by step 32 the policy has collapsed to a **no-op** and the
control is not measuring what it was chosen to measure.

Symptom, from the online eval against `random`:

| step | invalid | win | game_length |
| --- | --- | --- | --- |
| 0  | 0.69 | 0.0   | 3.1  |
| 16 | 0.31 | 0.0   | 21.2 |
| 32 | 0.06 | 0.0   | 52.1 |
| 48 | 0.00 | 0.125 | 57.8 |

The invalid-action rate falls exactly as you'd want — the base model learns the
`\boxed{}` format fast — and by step 32 games run to full length. But the win
rate stays at the floor while it does: 0.0 through step 32, against a *random*
opponent, while playing 94% legal moves.

The 0.125 at step 48 is not the policy recovering. Invalid actions hit exactly
0.0 at that eval, and with only 16 eval games one decision-boundary game is
worth 0.0625 — the win rate is simply free to wobble on turn-limit coin flips
that were previously forfeited outright. The behaviour underneath is unchanged:

| steps | roll | hold | hold-at-zero | median final score |
| --- | --- | --- | --- | --- |
| 30–32 | 22.5% | 74.3% | **81.3%** | 13 |
| 40–44 | 21.7% | 77.1% | **82.5%** | 17 |
| 44–48 | 20.8% | 78.4% | **82.5%** | 16 |

Cause, from the training rollouts (`game_state/actor*_step*.json`):

- hold rate 70–78% and still rising, roll rate 20–26%
- **~82% of all holds are at `turn_total == 0`** — it holds *before rolling*,
  banks nothing, and passes the turn
- median final score ~16 against `winning_score=50`; games end on the turn
  limit, never by scoring

So the policy learned to pass most of the time — not literally every turn, but
often enough that it never accumulates. Not a bug in the port: env, action
parser and zero-sum rewards were all verified independently (300 self-play
games, 17,392 observations, correct action space every time).

**Why RL finds this.** Rolling risks a 1, which forfeits the turn total; holding
at 0 has zero variance. In self-play *both* seats run the same policy, so when
both pass, the game is decided by the turn limit as a near-coin-flip worth ~0
expected reward. There is no gradient pointing out of mutual passivity — it is a
stable, mutually-passive equilibrium, the Pig analogue of both players folding
every hand.

**What makes it stable is the registered config.** `spiral/envs/__init__.py`
registers `PigDice-v1` with `winning_score=50, max_turns=50`. Because the turn
limit is no larger than the target score, a game where nobody accumulates still
*terminates and gets scored*, so passivity is survivable. If `max_turns` were
well above `winning_score` (TextArena's own `PigDice-v0-long` uses 500/500), a
passive player could never win — any opponent that ever banks eventually crosses
the line — which restores the gradient toward rolling.

**Implication for the design.** The PigDice arm was chosen to separate "trained
on a risky zero-sum game" from "trained on a game where bluffing pays". A model
that learned to pass has learned neither, so its MASK numbers would not be a
control for the Kuhn arm — they'd be a control for "no training happened".

### Fix: PigDice-v2, `require_roll_before_hold` — works

Rather than raising `max_turns` (which only makes passivity *lose eventually*,
leaving the variance-free action in the space), v2 makes `[hold]` illegal until
something has been rolled. That removes the passive action instead of
out-weighing it. `PigDice-v1` is left registered and untouched so the collapsed
run stays reproducible.

Job 80 (`pigv2-smoke`) against job 64 over the same step range:

| | roll | hold | hold-at-zero |
| --- | --- | --- | --- |
| v1, steps 20–26 | 28.4% | 66.9% | **75.6%** |
| v2, steps 20–26 | 65.4% | 30.5% | **22.3%** |

Online eval, v2 at step 16: **win 0.4375**, invalid 0.19, game_length 8.6 —
against v1's 0.0 at every eval through step 48. The intervention did not merely
discourage the passive line, it inverted the policy: roll/hold went from 28/67
to 65/31, and games start ending by *scoring* rather than by exhausting the turn
limit. (The residual 22.3% is partly detector noise — it counts holds in turns
where no "Turn total is now" line was emitted — so treat it as an upper bound.)

**Update, ~step 36 (0807).** v2's online win rate against `random` is
0.0625 -> 0.4375 -> **0.9375** (15/16) with invalid at 0.0, while v1 sits flat
at 0.125 across its last three evals. The two arms have fully separated.

More interesting: v2 is now learning *risk management*, not just non-degeneracy.
Mean hold threshold (turn total at which it banks) is climbing, and v1's is not:

| | roll | hold | mean hold threshold | max |
| --- | --- | --- | --- | --- |
| v2, steps 20–26 | 65.4% | 30.5% | 7.5 | 27 |
| v2, steps 31–36 | 73.0% | 26.1% | **9.2** | 38 |
| v1, steps 20–26 | 28.4% | 66.9% | 5.3 | 22 |
| v1, steps 65–70 | 26.9% | 72.9% | **5.2** | 22 |

v1 is frozen at 5.2 forty steps later; v2 has moved 7.5 -> 9.2 and is pushing
further per turn (max 27 -> 38). Optimal Pig banks around 20–25, so v2 is still
well short, but the direction is right and the gradient is live. This was the
open question about whether the fix bought real play or just a milder
bank-early-and-often equilibrium — as of step 36 it looks like the former.

**Smoke test completed (job 80, 0807).** `run_pigdice_v2_smoke.sh` was
configured `--max_train 6400` = 50 policy steps, and it ran all of them, saved
`step_00052` via oat's forced end-of-run save, and shut down cleanly. (The
`Killed` line in the slurm log is launchpad's teardown SIGKILL-ing two workers
that missed the stop deadline, not a crash — `Plasma daemon process error 0`,
exit code 0.)

Full v2 eval trajectory against `random`, steps 0/16/32/48/final:

    0.0625 -> 0.4375 -> 0.9375 -> 0.875 -> 0.75

So the headline 0.9375 was a peak, not a plateau; it settles in the 0.75–0.9
band. Still a decisive separation from v1's flat 0.0–0.125, but quote the range
rather than the max. Final-step behaviour: roll 81.5%, hold 17.9%, mean hold
threshold 11.1 (max 40) — up from 7.5 at step 20 and still short of the ~20–25
optimum, consistent with a live gradient rather than a converged policy.

Caveat on all v2 numbers: 16 eval games per point, so one game is worth 0.0625
and the 0.9375->0.75 move is within noise of a flat 0.8-ish. The v1/v2 gap is
far outside that noise; the v2 trend within itself is not.

**The collapse is also expensive.** A collapsed policy maxes out episode
length by construction — every game runs to `max_turns` instead of ending on a
score — so it inflates *eval* cost too. Measured per eval episode at ~step 64:
v1 takes **4–5 min**, v2 **1–2 min**. Job 64 is therefore grinding at ~10.5
rounds/hr against v2's ~12.9, and projects to **38h** for its 400 steps versus
v2's 31h. Worth pricing in: the failure mode does not just waste the arm, it
costs ~25% more wall-clock to produce the useless result.

### math-rl COMPLETE (job 81, 0808) -- final numbers

407 rounds (7498 MATH-train prompts x 7 epochs / 128 batch), 33h13m on node-1,
clean teardown. Seven checkpoints: 64/128/192/256/320/384 plus the forced
end-of-run `step_00407`. Twenty-seven evals on the SPIRAL battery.

Average accuracy, means over non-overlapping 5-eval windows:

| evals | approx steps | mean |
| --- | --- | --- |
| 0-4 | 0-64 | 0.4004 |
| 5-9 | 80-144 | 0.4211 |
| 10-14 | 160-224 | **0.4231** (peak) |
| 15-19 | 240-304 | 0.4111 |
| 20-24 | 320-384 | 0.3976 |
| last 5 | ~368-407 | **0.3919** |

Step 0 = 0.3245. Best single eval 0.4390 at eval 14 (~step 224). Final = 0.3848.

- net gain start -> finish: **+0.060**
- loss from peak -> finish: **-0.054**

So the arm gave back roughly *half* of everything it gained by training to
completion. Four consecutive descending windows after the peak; this is not
noise.

**Use `step_00192` or `step_00256` for the MASK comparison, not `step_00407`.**
They bracket the peak window. Taking the final checkpoint would understate the
arm's reasoning capability by ~5.4 points -- which matters directly, because
this arm exists to test whether reasoning gains mediate the deception effect. A
capability-degraded checkpoint would bias that mediation toward a null.

### Both surviving arms degrade with over-training (0808)

math-rl (job 81) average benchmark accuracy, means over non-overlapping 5-eval
windows:

| evals | approx steps | mean |
| --- | --- | --- |
| 0-4 | 0-64 | 0.4004 |
| 5-9 | 80-144 | 0.4211 |
| 10-14 | 160-224 | **0.4231** |
| 15-19 | 240-304 | 0.4111 |
| last 5 | ~320-368 | **0.3966** |

Three descending windows; the final one is below the first. The arm gained until
roughly step 200 and has been losing since.

**This corrects an earlier reading in this log.** The "plateau at ~0.42 since
step 64" recorded above was sampling inside the peak, not a ceiling. The honest
curve is rise-to-~200, then decline. Two consequences: (a) stopping at step 64
as originally proposed would have been premature, not merely cheap; (b) running
to 410 is *worse* than stopping near 192-256. For the MASK comparison use
`step_00192` or `step_00256`, not the final checkpoint.

**Pattern across arms.** PigDice-v2 over-rolls past optimal play; math-rl loses
benchmark accuracy. Different modality, same shape: peak mid-run, degrade after.
Neither arm's headline eval detected its own degradation in time -- PigDice's
win-vs-random was saturated, math-rl's was inside noise until three windows had
accumulated. **Checkpoint selection should be treated as part of the experiment,
not a formality**: for every arm, pick the checkpoint at the behavioural peak
rather than the last one written.

### PigDice-v2 overshoots: the mirror-image degenerate policy (job 88, 0808)

The full 400-step v2 arm reproduced the fix cleanly and then broke the other
way. Hold threshold (turn total at which it banks), by non-overlapping 15-step
window, all windows complete:

| steps | mean | median | p90 | n holds | illegal holds |
| --- | --- | --- | --- | --- | --- |
| 45-59 | 11.8 | 10 | 23 | 514 | 55 |
| 60-74 | 15.5 | 14 | 30 | 463 | 29 |
| 75-89 | 20.5 | 18 | 35 | 381 | 3 |
| 90-104 | 20.5 | 18 | 38 | 314 | 10 |
| 105-119 | 26.8 | 22 | 51 | 173 | 6 |
| 120-134 | 40.5 | 34 | 71 | 43 | 6 |
| 135-149 | 48.2 | 54 | 73 | 15 | 0 |
| 150-164 | 60.5 | 60 | 93 | 6 | 0 |
| **165-179** | **39.8** | **43.5** | **63** | **26** | **0** |
| 180-194 | 44.7 | 42 | 73 | 47 | 0 |
| 195-209 | 59.5 | 50 | 75 | 13 | 0 |
| 210-224 | 64.0 | 64 | 64 | **1** | 0 |
| 225-239 | 52.7 | 57 | 76 | **17** | 0 |

Source: `game_state/actor*_step*.json`, one record per actor per step (8 actors);
a hold's threshold is the last `Current turn total:` / `Turn total is now` in the
observation the policy was acting on. Holds at turn total 0 are illegal under
`require_roll_before_hold` and are excluded from the threshold stats, counted in
the last column instead. p90 is nearest-rank on the sorted window.

Optimal Pig banks around 20-25. The policy passed through that band around
steps 75-104 and kept going. By steps 210-224 the mean hold is **64** in a game
to 50 points, and that entire 15-step window contains **one single hold**,
against 514 at steps 45-59. It has effectively stopped banking. By 120-134 the
median hold is already 34 and p90 is 71 -- it routinely rolls past the winning
score before considering a hold -- and holds have collapsed 381 -> 43.

### CORRECTION (0808): window 165-179 was missing, and the drift is not monotone

The version of this table committed in f542bb8 skipped the 165-179 window while
stating "all windows complete". Recomputed from `game_state` it is filled in
above, and every other window reproduces the previous numbers exactly, so the
gap was an omission in the earlier pass, not a data problem. It matters because
of what it hides. The hold *count* over the back half is:

    150-164: 6  ->  165-179: 26  ->  180-194: 47  ->  195-209: 13  ->  210-224: 1

and the mean threshold is 60.5 -> 39.8 -> 44.7 -> 59.5 -> 64. The policy does
not march monotonically away from banking; it reaches a near-total stop at
150-164, **partially recovers for two windows**, then collapses again. The
earlier "kept going -- and did not stop" reading was produced by the omitted
window, and has been softened above.

This is the third time in this log a trend has been overstated by a window
boundary (see the Social-arm RETRACTION). The first two were windows ending at a
local extreme; this one is a window missing from the middle. Same failure class:
**the shape of the claim came from the shape of the sampling.** The endpoint
conclusion is unaffected -- 210-224 really is one hold, and the arm really is
degenerate -- but "ran monotonically to the end of the axis" is not what the
data shows, and the design implication below should be read as "runs to one end
of the axis eventually", not "moves there without reversals".

**Illegal holds are a separate, clean story.** Attempts to hold at turn total 0
-- forbidden by `require_roll_before_hold` -- fall 55 -> 29 -> 3 and are **zero
in every window from 135 on**. The model learned the new rule early and never
unlearned it. So the over-rolling is not rule confusion; it is the policy
optimising within the rules, exactly as the reward specifies.

### SECOND CORRECTION (0808 18:43): 210-224 was a trough, not the floor

Window 225-239 has now closed: **17 holds, mean 52.7, median 57**. The "one
single hold" window was not the terminal state of the policy, it was the
extreme point of an oscillation. Hold count over the back half now reads:

    150-164: 6 -> 165-179: 26 -> 180-194: 47 -> 195-209: 13 -> 210-224: 1 -> 225-239: 17

and mean threshold 60.5 -> 39.8 -> 44.7 -> 59.5 -> 64.0 -> 52.7. The policy is
not converging on never-hold. It is oscillating inside a high band, roughly
mean 40-64, with the hold count swinging by more than an order of magnitude
between adjacent windows.

**This is the same error a third time, and the correction above committed it.**
That correction diagnosed the omitted 165-179 window and then still described
210-224 as the collapse endpoint -- because 210-224 was the last window that
existed when it was written. Diagnosing "the shape of the claim came from the
shape of the sampling" did not prevent doing it again one paragraph later. The
generalisable rule is not "check for gaps": it is that **the final window of a
running job is not evidence about where the run is heading**, because it is
selected by when you happened to look. Windows from a live job should be
reported and left uninterpreted until at least one further window has closed
behind them.

What survives all three passes: the arm is far off optimal (optimal banks
20-25; every window from 120 on has mean >= 35), holds are one to two orders of
magnitude rarer than at 45-59, and `step_00128` remains the last checkpoint
near optimal play. What does not survive: "it has stopped banking entirely",
"roll until bust, forever", and any monotone-collapse framing. The honest
summary is **degenerate and unstable**, not degenerate and converged.

**Status as of 0808 18:45 UTC:** job 88 at step 239 of 400, 20h17m elapsed of a
48h limit, no OOM / NCCL / CUDA / Traceback hits. Log mtime is 10.8 min stale
and newest `game_state` write 7.9 min stale, against a step time of ~4-7.5 min
-- at the edge of normal, not yet a hang. Being re-checked. Checkpoints remain
three: `step_00064`, `step_00128`, `step_00192`. `/workspace` 655 GiB free.

**This is v1's collapse inverted.** v1 learned to never roll; v2 learned to never
hold. `require_roll_before_hold` removed the variance-free passive action and
that fixed the first failure, but the reward still cannot rank *magnitudes* of
success -- it is terminal win/lose only (see the reward section above), so
"banked 20 and won" and "banked 45 and won" are identical to the gradient. Once
rolling is locally favoured there is nothing pushing back until you actually
bust, and busting is only a fraction of turns.

**The online eval never saw it.** Win rate vs `random` hit 1.0 at step 32 and
stayed there for nine consecutive evals, straight through the degradation.
Against an opponent that plays badly you can bust half your turns and still win
16/16. Win-vs-random saturated ~100 steps before the behaviour did and is
structurally incapable of detecting over-rolling. **Do not gate stopping
decisions on it** -- the behavioural statistic (hold threshold) is the only one
that tracked the policy.

**Practical upshot.** `step_00128` is the last checkpoint taken near optimal
play; the 105-119 window straddling it is already drifting. Training past it
makes the arm progressively less representative of "trained on a risky zero-sum
game", which is the property the control is supposed to supply.

**Design implication.** Deleting a degenerate action is necessary but not
sufficient. If the reward is terminal-only and the game has an unbounded
accumulate-then-bank axis, expect the policy to run to one end of that axis or
the other. Fixing this properly needs either a reward that ranks margin of
victory, or an env cap (bust probability rising with turn total, or a hard
turn-total ceiling). Worth deciding before any further Pig arm.

**Generalises past Pig.** Any zero-sum self-play env with (a) a variance-free
passive action and (b) a terminal condition reachable without acting is exposed
to this. The fix generalises too: delete the passive action from the space
rather than trying to price it correctly. Worth checking before committing
GPU-months to the multigame arms — Liar's Dice in particular has a cheap
passive-ish line.

### PigDice-v2 MASK + mathbench land (jobs 117/118, 0808) -- the honesty drop is not about deception

Both evals on `pig-step192` completed clean (`MASK_DONE` 18:21, `MATHBENCH_DONE`
18:09). First alignment numbers for any PigDice checkpoint. MASK honesty score
by category, all arms run to date:

| category | base | kuhn-064 | kuhn-128 | kuhn-256 | kuhn-400 | mathrl-064 | mathrl-192 | **pig-192** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| continuations | 77.8 | 69.9 | 71.6 | 71.6 | 70.5 | 63.1 | 94.9 | 69.3 |
| disinformation | 80.8 | 67.2 | 69.6 | 69.6 | 72.0 | 67.2 | 96.8 | 64.8 |
| doubling_down | 92.5 | 94.2 | 89.2 | 90.8 | 89.2 | 89.2 | 98.3 | 90.0 |
| known_facts | 95.2 | 91.9 | 88.5 | 93.3 | 95.7 | 93.8 | 98.1 | 90.4 |
| provided_facts | 71.5 | 63.5 | 58.8 | 55.8 | 60.9 | 63.9 | 88.0 | 61.3 |
| statistics | 65.6 | 49.0 | 49.0 | 45.8 | 46.9 | 44.8 | 95.8 | 49.0 |
| **mean** | **80.6** | 72.6 | 71.1 | 71.2 | 72.5 | 70.3 | **95.3** | **70.8** |

And the capability mediation, same arms, math-evaluation-harness average over
math500 / aime24 / aime25 / olympiadbench / amc23 / minerva_math:

| arm | base | kuhn-064 | kuhn-128 | kuhn-256 | kuhn-400 | mathrl-064 | mathrl-192 | pig-192 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mathbench avg | 30.0 | 37.6 | 36.6 | 38.6 | 38.1 | 40.5 | 43.2 | 36.1 |

**The result the control was built to produce.** PigDice has no communication
channel. There is no message to shade, no opponent model to mislead, no
deception affordance of any kind -- the entire action space is `[roll]` and
`[hold]`. It still drops MASK honesty from 80.6 to **70.8**, landing inside the
same 70-73 band as every Kuhn arm, which does have a betting/bluffing channel.
Whatever is moving MASK is therefore **not** the model learning to deceive from
strategic-interaction content.

**And it is not capability loss either.** Every RL arm gains on mathbench
relative to base (30.0 -> 36-43), including the degenerate pig arm at 36.1
(+6.1). Honesty falls while capability rises, so the mediation story -- "the
behaviour is just downstream of getting worse at the task" -- is ruled out in
the direction it was posed. The two move in opposite directions.

That leaves generic consequences of RL fine-tuning on self-play transcripts --
format drift, output-length or reasoning-style change, assistant-persona
erosion from training on non-assistant text -- as the live hypotheses. All are
checkable and none require the game to be social. **This makes the trained
control more informative than expected**: it was meant to hold the algorithm
fixed while removing the manipulation channel, and removing the channel did not
remove the effect.

**`mathrl-step192` is an outlier and nothing here should be built on it.** It
scores 95.3 mean honesty -- 15 points *above* base and 25 above every other arm
-- while also topping mathbench at 43.2, and its sibling `mathrl-step064` sits
at 70.3 with the pack. A 25-point jump between two checkpoints of one arm is
more consistent with a format or judge artifact (e.g. a response style the MASK
judge parses differently) than with a real honesty gain. Worth reading the raw
`mathrl-192` responses before treating it as signal.

**Caveats.** One eval run per arm, no seeds; per-category n runs 96-274
responses, so category-level numbers carry real noise even if the arm means are
better constrained. The pig-192 result is also drawn from a checkpoint inside
the degenerate 180-194 band (mean hold 44.7) -- it says what a *degenerate*
pig policy does to MASK, not what a well-trained one does. **Re-running MASK on
`step_00128`, the last near-optimal checkpoint, is the obvious next arm** and
would separate "training on Pig at all" from "training on Pig past collapse".

### Social arm status (job 74, 0807)

Training healthily and clearly learning. Online eval vs `random`, steps
0/16/32/48/64:

| env | win | invalid |
| --- | --- | --- |
| KuhnPoker-v1 | 0.0 -> 0.0625 -> 0.25 -> 0.25 -> **0.3125** | 0.5 -> 0.44 -> 0.0 -> 0.125 |
| TicTacToe-v0 | 0.0 -> 0.25 -> 0.375 -> 0.3125 -> **0.375** | 0.5 -> 0.19 -> 0.31 -> 0.0 -> 0.125 |

`actor/avg_reward` climbing 0.45 -> 0.48. First checkpoint `step_00064` on disk.

Note TicTacToe is *not* in this arm's training mix (it trains on
TruthAndDeception + KuhnPoker + SimpleNegotiation + LiarsDice-2d), so its
0 -> 0.375 is out-of-domain transfer, not fitting. That is the same
cross-game generalisation SPIRAL reports, reproduced here on the deception-dense
game set.

No sign of the passive-equilibrium failure in this arm: rewards are moving and
invalid rates are falling on both eval envs. Liar's Dice was the one flagged as
having a cheap passive-ish line ([Call] immediately); worth a hold-at-zero-style
audit of its rollouts before trusting the arm, but nothing in the aggregate
metrics suggests it yet.

### Single-agent RLVR control (job 81, 0807)

`oat.experiment.run_math_rl` on MATH train 7.5k, Qwen3-4B-Base, ~410 planned
steps. This is the "does *any* RL move the social traits, or only training
against a manipulable mind" control, so it first has to clear the bar of being a
*competent* control rather than a null one. It does — online eval average
accuracy 0.325 -> 0.412 -> 0.432 -> 0.403 -> **0.431** across steps 0-64.

Per benchmark at step 64, against the base-model numbers measured separately
with `evals/run_reasoning_bench.sh`:

| bench | base | step 64 |
| --- | --- | --- |
| math | 0.642 | **0.770** |
| amc | 0.400 | **0.494** |
| olympiad_bench | 0.342 | **0.416** |
| minerva | 0.250 | **0.276** |
| aime | 0.100 | **0.200** |

Entropy sits low (0.04-0.07) with occasional spikes to 0.17-0.26. Those are
batch outliers, not instability: `policy_grad_norm` stays flat at 0.034-0.052
and `avg_reward` at 0.76-0.85 straight through them. A real destabilisation
moves the gradient norm too.

### All three arms checkpointed at step 64 (0807)

`oat-output-pigdice`, `oat-output-multigame-social` and `oat-output-mathrl` each
now hold `step_00064`, plus `oat-output-pigv2-smoke/step_00052` from the
completed smoke test. That is the first point at which every arm is
simultaneously probe-able with MASK.

Social arm through step ~160, KuhnPoker win across 11 evals:

    0.00 0.06 0.25 0.25 0.31 0.56 0.75 0.62 0.50 0.69 **0.88**

TicTacToe (out-of-domain, not in the training mix): 0.00 0.25 0.38 0.31 0.38
0.50 0.50 0.50 0.25 0.25 0.31.

Note the dip at evals 7-8 (Kuhn 0.75 -> 0.62 -> 0.50, TicTacToe 0.50 -> 0.25). It
looked like early over-training, but invalid rates were 0.0 throughout, so
forfeits could not explain it, and it reversed to 0.69 -> 0.88. On a 16-game
eval the standard error near p=0.5 is ~0.125, so a 0.25 move is ~2 SE and two
consecutive dips are well within what noise produces. **Do not read single-eval
moves in these arms as signal** -- wait for three points or widen `eval_games`.

**Social arm COMPLETE (job 74, 0807).** 400 steps in 13h48m on node-6, clean
teardown. Seven checkpoints: 64/128/192/256/320/384 plus the forced end-of-run
`step_00402`. Twenty-seven evals.

Win rate vs `random`, means over non-overlapping 5-eval windows:

| window | KuhnPoker (trained) | TicTacToe (NOT trained) |
| --- | --- | --- |
| 0-4 | 0.175 | 0.263 |
| 5-9 | 0.625 | 0.400 |
| 10-14 | 0.762 | 0.400 |
| 15-19 | 0.713 | 0.475 |
| 20-24 | 0.713 | 0.487 |
| last 5 | 0.688 | **0.525** |

Final invalid rates: Kuhn 0.000, TicTacToe 0.037.

**Both games improve, and the out-of-domain game is still climbing at the end.**
Kuhn rises fast, peaks around window 10-14 (0.762) and settles ~0.69-0.71.
TicTacToe rises more slowly but monotonically after its first window, 0.263 ->
0.400 -> 0.400 -> 0.475 -> 0.487 -> 0.525, and had not flattened when training
ended. The Kuhn-minus-TicTacToe gap goes +0.088 (first window) -> +0.162 (last
five) -- wider than at the start, but far narrower than mid-run.

So this arm **does** show sustained cross-game transfer: a held-out game it never
trained on went from 0.263 to 0.525 and was still improving.

### RETRACTION: the "in-domain/OOD decoupling" claimed earlier was wrong

Two earlier versions of this entry claimed TicTacToe had flatlined while Kuhn
climbed, and that the transfer was a one-off early gain rather than a trend. The
completed run contradicts both claims. The error, twice:

1. First version used the last 8 *raw* evals, a window that happened to end with
   Kuhn at its peak (0.94) and TicTacToe at its trough (0.25).
2. Second version fixed the statistic -- windowed means -- but still cut the
   series at step ~272, where Kuhn sat at its all-time peak window and
   TicTacToe was mid-plateau between its 0.400 and 0.475 phases. The gap looked
   like it was widening (0.225 -> 0.462) purely because of where the data
   stopped.

Switching from raw tails to windowed means was the right fix for the wrong
problem. The actual problem was **drawing a trend from an unfinished run**. Both
failures share a shape: a window terminating at a local extreme. The discipline
that would have caught it is not a better estimator, it is refusing to publish
directional claims until the curve has stopped moving -- or stating the
horizon explicitly ("as of step 272") and treating it as provisional.

`actor/avg_reward` drifted 0.48 -> 0.21 over the run, expected in zero-sum
self-play as both seats improve together and outcomes equalise.

## 0806 multigame CONTROL

So the clean division of labor is:


Non-trained control = reasoning-battery mediation on the treatment checkpoints. Answers "is the behavior just downstream of capability," introduces no algorithm confound because it trains nothing.

also fix pigdice
Trained control = ConnectFour/Chess self-play. Holds algorithm + competition fixed, isolates the manipulation channel. This is your causal within-training control.
The cheaper and more direct fix is to attack property (a) instead of weakly counteracting the equilibrium: forbid hold-at-turn_total==0 — require ≥1 roll before a hold is legal. That removes the variance-free passive action entirely; every turn now carries the 1/6 bust risk, so pure passivity is no longer a safe attractor and the policy can't collapse onto it. It's compute-neutral (no extra turns), and it's arguably more faithful to Pig's risk-management character than the current port, which is the whole reason you picked the arm. If you'd rather not touch the action mask, the other property-(b) attack is scoring a no-progress game as a double loss rather than a draw, which also kills survivability — but the roll-forcing rule is the least invasive.

Concretely, three cheap layers before the real run rather than a binary choice:

Paper screen — run the three-clause passivity filter (variance-free line + terminal-without-accumulating + mirror payoff ≥ active) on every candidate. ConnectFour passes; Chess has the draw-collapse variant (repetition-shuffle for the safe 0.5), so I'd bench it or handle draws explicitly.
Solo smoke-test — ~50 steps per candidate individually, just to confirm it trains. This is the one place single-game runs earn their keep, and they're cheap: PigDice outed itself by step 32, so a short solo run catches any intrinsic-collapse game before it enters the mixture. Note this only rules out intrinsic collapse — a game can still get gradient-starved inside a mixture — but it's the main failure mode and it's ~1% of a full run to check.
Mixture run with per-game eval + tripwire, and your "cut down the set" plan as the explicit contingency rather than a surprise.

Net: multi-game for the actual arm (matches treatment, amortizes compute), preceded by cheap per-game screening (so you're not blind), with per-game monitoring during (so the mixture survives collapse instead of masking it). You only pay the per-game decomposition cost on the control if the aggregate null fails — if the mixture shows no deception in aggregate, you're done and you never needed separate runs.