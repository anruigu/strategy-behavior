# 0901 — what is trainable, and which knobs are actually knobs

Three questions settled by measurement overnight, before committing the next
wave: which cells can be learned at all, whether temperature is a usable
exploration knob, and whether the token budget is doing damage nobody logged.

## ref_estate was never a discovery problem

It was an instrumentation one. MARSHAL's estimator needs a score at each turn;
`ref_estate` settled once at the end, so `referee_env` refused it and it sat
out three waves. Wiring `RefereeGame._snap` into it — a running
`declared cash + deed value`, mirroring the `final` expression branch for
branch so the deltas sum to the settled score — makes it decompose exactly
under the TURN-SCORES gate (72 seat-episodes, one entry per decision).

It is now the strongest cell in the atlas:

| | neutral | ceiling | headroom | single-deviator payoff | invalid |
|---|---:|---:|---:|---:|---:|
| ref_estate | 0.009 | 0.607 | **0.598** | **+431.65** | 0.000 |

A one-step trainer smoke confirmed the credit reaches the estimator:
`advantage_std` 1.000 and `raw_reward_mean` 37.4, which is 2.5x the next cell
on the roster. Observed exploit rate 0.01, matching the 0.009 measured base
rate.

`ref_exchange`, `ref_sidebar` and `ref_hanabi` gained snapshots in the same
change. Only exchange is even arguably trainable (+7.70), and its score moves
from 7.2 to 7.3 across the whole ceiling, so there is nothing for a gradient
to follow. It stays out.

Roster is now seven: ref_estate, gen_frontline_depot, gen_quiet_sonar,
gen_sovereign_vaults, ref_auction, ref_commons, gen_antiquities.

## Temperature is not a knob on this model — NEGATIVE

The proposal was to widen exploration with temperature 2-3. Measured instead,
neutral prompts, top_p 0.95, `reasoning_effort low`, invalid rate:

| cell | T=1.0 | T=1.5 | T=2.0 |
|---|---:|---:|---:|
| gen_antiquities | 0.025 | 0.208 | **0.992** |
| gen_sovereign_vaults | 0.117 | 0.575 | — |
| ref_commons | 0.222 | 0.620 | — |

At T=2.0 essentially every reply is unparseable. The important detail is that
this is NOT truncation that a bigger budget would fix: at T=1.5 on
sovereign_vaults invalid is 0.575 against truncation 0.258, so the majority of
failures are replies that finished and still did not contain a well-formed
bracketed token. And the exploit rate goes the wrong way — sovereign_vaults
0.033 at T=1.0 to 0.000 at T=1.5 — because a broken reply is scored by the
referee's own fallback, which is honest by construction.

So the arms run at T=1.0 and group size is the only knob left standing. That
is where the 0831 evidence pointed anyway, once its magnitude was retracted.

## Budget is not hygiene, it is the discovery knob — POSITIVE

`--max-new-tokens` defaulted to 768 for every cell not explicitly overridden.
Sweeping it at T=1.0 on neutral prompts, 8 seeds, the invalid rate behaves as
expected and the EXPLOIT rate does not:

| cell | 512 | 768 | 1024 | 2048 |
|---|---:|---:|---:|---:|
| gen_sovereign_vaults | 0.163 | 0.175 | 0.150 | **0.425** |
| ref_commons | 0.042 | 0.181 | **0.306** | |
| gen_frontline_depot | 0.016 | 0.000 | 0.000 | **0.109** |
| ref_estate | 0.000 | 0.008 | 0.019 | 0.016 |
| ref_auction | 0.000 | 0.000 | 0.000 | |
| gen_antiquities | 0.000 | 0.000 | 0.000 | 0.000 |

and the corresponding invalid rates:

| cell | 512 | 768 | 1024 | 2048 |
|---|---:|---:|---:|---:|
| gen_frontline_depot | 0.914 | 0.805 | 0.672 | **0.141** |
| ref_commons | 0.361 | 0.111 | 0.042 | |
| gen_sovereign_vaults | 0.237 | 0.200 | 0.087 | 0.025 |
| ref_auction | 0.196 | 0.067 | 0.004 | |
| ref_estate | 0.090 | 0.014 | 0.000 | 0.007 |
| gen_antiquities | 0.000 | 0.000 | 0.000 | 0.006 |

`gen_frontline_depot` at the default budget: 0.914 invalid, score 0.3. At 2048:
0.141 invalid, score 9.2, and an exploit rate that exists at all. That cell has
been read as "flat, `advantage_std` 0.107, almost no reward variance" in two
previous waves. Those waves were measuring truncation.

THE CONSEQUENTIAL PART. The ceiling probe that produced the roster table ran at
2048 tokens. Training ran at 768. So every base rate the roster was selected on
was measured on a policy with room to reason, and every training step was run
on a starved one -- and the gap is not small, since sovereign_vaults exploits
2.8x more often at 2048 than at 1024. An unknown share of "the policy never
discovers this" was "the policy was cut off mid-reasoning".

This is not a knob to screen, it is a bug to fix: more budget is strictly
better for the exploit rate and costs only wall-clock. Budgets are now set per
cell from this table, and the group-size screen runs on top of the fix rather
than confounded with it.

`gen_antiquities` is the exception in both directions -- clean at 512 and never
exploiting at any budget. Its 0.000 neutral rate is real, not truncation.

HOW MUCH OF THIS TO BELIEVE. The invalid rates are solid -- they are ratios over
hundreds of decisions per row and they move monotonically. The exploit rates are
n=8 episodes and are not. Specifically, the ceiling probe measured
`gen_sovereign_vaults` neutral at 0.212 with the same 2048 budget and the same
effort setting that this sweep reads as 0.425, so that cell's spread is at least
as large as the effect claimed for it. `gen_frontline_depot` and `ref_commons`
are the two that survive scepticism: depot's is corroborated by invalid
0.914 -> 0.141 and score 0.3 -> 9.2 moving together, and commons is monotone
across three budgets on both measures at once.

So the defensible claim is the weaker one, and it is enough: budgets are set to
where the invalid rate falls below ~0.05, which is a criterion that does not
depend on the noisy column at all. Whether budget also lifts discovery per se is
a real question this does not settle, and the wave will answer it incidentally
now that every cell is sampled with room to finish.

## Capacity

36 samplers across five pods (was 28). One further idle node was claimed by
another user's job seconds before the pod spec applied; that pod was dropped
rather than contend for it.

## Group size is not the lever either — NEGATIVE

Two arms, identical but for `--group-size`, six cells, T=1.0, measured budgets,
18 samplers each. First half vs second half of the run, neutral groups:

| cell | g16 Δ | g32 Δ |
|---|---:|---:|
| ref_estate | -0.003 | -0.002 |
| gen_frontline_depot | +0.018 | -0.023 |
| gen_sovereign_vaults | -0.032 | +0.064 |
| ref_auction | -0.001 | -0.002 |
| ref_commons | +0.041 | +0.062 |
| gen_antiquities | -0.000 | -0.000 |

Indistinguishable, and the signs disagree on the two cells with any movement at
all, which is what noise looks like. `behavior_drift` sits at 0.0083 in both and
does not move. Doubling the group doubles the compute for nothing.

The 0831 log proposed group size on the reasoning that at a ~0.1 base rate most
groups of 4 contain no exploit, so GRPO has nothing to contrast. That argument
was sound but it is no longer the binding constraint: with budgets fixed,
`gen_sovereign_vaults` and `ref_commons` sample at 0.27-0.37 unprompted, so even
a group of 4 would contain plenty of contrast. The premise moved out from under
the hypothesis.

## What IS binding: the update is too small, and the window is narrow

The adapter moves, but barely. Over 24 steps at the 1e-5 default,
`|A_step - A_0|` reaches 1.05 against `|A_0|` = 52.25, and `lora_B` -- which
initialises to ZERO and is the half that produces the delta -- reaches 0.64
against `lora_A`'s 3.27. Adam moves each parameter about `lr` per step, so the
whole run is ~2.5e-4 of travel. Nothing in the behaviour changes.

Bracketing the learning rate, six cells, same everything else:

| lr | steps | \|dA\| | \|B\| | mean invalid | verdict |
|---|---:|---:|---:|---:|---|
| 1e-5 | 24 | 1.05 | 0.64 | 0.02 | policy does not move |
| 3e-5 | 9 | 1.23 | 0.98 | 0.016 | moves, stable |
| 1e-4 | 6 | 2.88 | 2.48 | **0.16** | collapse |

At 1e-4 the invalid rate rises 5-100x on ALL SIX cells simultaneously within
five steps and scores fall. THE TRAP: the exploit rate goes UP while this
happens -- `gen_frontline_depot` +0.102, `ref_estate` +0.017 -- because the
referee scores an unparseable reply with its own fallback. Read off the headline
metric alone that is a discovery curve. It is structurally the same artefact as
the retracted 0831 result, and `episode/invalid_rate` -- which did not exist
before 2026-09-01 -- is the only reason it was caught.

At 3e-5 the one clean signal so far is `gen_sovereign_vaults`: exploit +0.116,
score +5.4, invalid DOWN 0.020 -> 0.013. Rate up, score up, validity improving
is the signature that cannot be faked by the fallback.

## The cold-start problem is still open

No arm has moved a zero-base-rate cell. Across 1e-5 g16, 1e-5 g32 and 3e-5,
`gen_antiquities` sits at 0.001, `ref_auction` at 0.002, `ref_estate` at 0.008,
and none of them has a trend. Every cell that moves at all was already sampling
the behaviour at 0.27+ unprompted, so what has been demonstrated is
AMPLIFICATION, not discovery -- the same conclusion the 0831 log reached, now on
a roster whose budgets and instrumentation are actually correct.

That matters for `ref_estate` in particular: it has the largest payoff in the
atlas (+431.65), a 0.607 prompted ceiling, a 0.000 invalid rate and healthy
gradient signal (`raw_reward_mean` 37.4, `advantage_std` 1.000). Nothing is
broken about it. The policy simply never samples the move, and no knob tried so
far -- prompt rung, group size, temperature, budget, learning rate -- changes
that.

## 3e-5 works, and it is the first real learning in this project

18 steps, six cells, group 16, T=1.0, measured budgets. First half vs second:

| cell | first | last | Δ | score Δ | invalid |
|---|---:|---:|---:|---:|---|
| gen_sovereign_vaults | 0.394 | 0.647 | **+0.252** | **+14.0** | 0.016 → 0.012 |
| ref_commons | 0.376 | 0.605 | **+0.229** | −5.5 | 0.005 → 0.011 |
| gen_frontline_depot | 0.050 | 0.089 | +0.038 | +3.8 | 0.052 → 0.050 |
| ref_auction | 0.001 | 0.010 | +0.009 | −2.4 | 0.000 → 0.001 |
| ref_estate | 0.007 | 0.014 | +0.007 | −1.5 | 0.007 → 0.002 |
| gen_antiquities | 0.001 | 0.003 | +0.001 | −0.0 | 0.014 → 0.015 |

Last three steps reached `sovereign_vaults` 0.62/0.76/0.75 and `ref_commons`
0.61/0.66/0.71 against base rates near 0.35. Forfeits 0 throughout, invalid
rates flat or falling, and `behavior_drift` moved for the first time in any run
here (0.0082 → 0.0104).

WHY THIS IS BELIEVABLE WHERE 0831 WAS NOT. The failure mode that invalidated the
earlier result raises the exploit rate by BREAKING the policy — the referee
scores an unparseable reply with its own fallback, so garbage reads as a
discovery curve. That artefact necessarily comes with a rising invalid rate and
falling scores, which is exactly what 1e-4 showed. Here validity IMPROVES while
the rate climbs, and on sovereign_vaults the score climbs +14.0 alongside. The
`ref_commons` score falling is not a counterexample but a prediction of the
game: it is a commons tragedy, so when every seat over-harvests the stock
collapses for all of them, and own-score falling while the violation rate rises
is what a working exploit looks like there.

## Cold start: suggestive, not settled

The three cells that sit near zero all moved, and all by amounts too small to
call: `ref_auction` 0.001 → 0.010, `ref_estate` 0.007 → 0.014, `gen_antiquities`
0.001 → 0.003. Multiplicatively that is 10x, 2x, 3x; in absolute terms it is
nothing, and at n=1 seed it is not distinguishable from drift. The wave runs
four seeds precisely so this question gets a real answer rather than another
three-seed table that turns out to be an artefact.

## Standing risk in the wave

`lora_B` reached 1.44 at 18 steps and grows ~0.08/step. 1e-4 collapsed at
roughly 2.5, so a 30-step run at 3e-5 lands near that magnitude and may fail
late. The wave checkpoints every 5 steps and a watcher kills any single seed
whose mean invalid rate crosses 0.12 twice, leaving the rest running. If the
collapse threshold really is a magnitude rather than a rate, the answer is a
shorter run or a decaying schedule, not a smaller lr.
