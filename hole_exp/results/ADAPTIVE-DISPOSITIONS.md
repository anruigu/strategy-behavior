# Adaptive-trust dispositions: validity gates + base-model readout (2026-08-22)

Two new opponent dispositions, built for the five hand-written opponent-swap
cells (`ipd`, `trust`, `public_goods`, `dond`, `ultimatum`):

| arm | counterpart |
|---|---|
| `hole` | never punishes |
| `adaptive_recover` | hazard rises with what you take, decays when you stop; punishment is per-round |
| `adaptive` | same hazard, **permanent** once it fires (stochastic grim) |
| `nohole` | punishes from the first betrayal |

Everything below is **in-env behaviour against the training opponent**. It is a
headroom-and-validity reading, not a result: the dependent variable of this
line of work is transfer to the held-out battery (`EVAL_SUITE.md`).

## 1. Scripted gates — 10/10 adaptive cells pass

`check_suite.py --envs ipd trust public_goods dond ultimatum --arms adaptive
adaptive_recover --doses 1.0 --seeds 200`

| env | arm | honest | always-exploit | premium | exploit-once premium |
|---|---|---:|---:|---:|---:|
| ipd | adaptive | 30.00 | 28.72 | −1.28 | +0.12 |
| ipd | adaptive_recover | 30.00 | 27.03 | −2.97 | +1.16 |
| trust | adaptive | 131.04 | 115.61 | −15.44 | +5.58 |
| trust | adaptive_recover | 131.04 | 113.72 | −17.33 | +10.40 |
| public_goods | adaptive | 187.27 | 164.12 | −23.14 | +10.79 |
| public_goods | adaptive_recover | 187.27 | 170.45 | −16.82 | +10.71 |
| dond | adaptive | 5.35 | 4.29 | −1.06 | −0.10 |
| dond | adaptive_recover | 5.35 | 4.97 | −0.38 | +0.00 |
| ultimatum | adaptive | 30.00 | 24.86 | −5.14 | +3.68 |
| ultimatum | adaptive_recover | 30.00 | 24.09 | −5.91 | +2.47 |

Both adaptive gates hold everywhere: **priced** (always-exploit ends below
reciprocal honesty) and **gradient** (one early exploit is not meaningfully
punished, measured against the hole arm's own early-exploit premium rather
than against zero — in `dond` the payoff is whatever deal is standing at the
end, so a round-1 lie is worth nothing even where lying is free).

`ipd` is the tightest cell: its window between the two gates is ~1.3 points
wide, because a fired grudge there costs 2 points a round for the rest of a
10-round episode while a single defection buys 2.5. Worth re-checking after
any retune.

Hazards are fitted per (env, arm) by `tune_adaptive.py` and stored in
`core.ADAPTIVE_TUNING`; the three temperaments (wary / volatile / stoic) are
relative multipliers shared across envs (`core.ADAPTIVE_SHAPE`).

## 2. Two leaks the tuning surfaced

Neither was fixable by tuning — at *every* hazard, always-exploit beat honesty:

- **trust.** A punished round stakes nothing, `Investor.observe` sets
  `last_return_share = None` when the pot is empty, and `send` falls back to
  the full base stake when it is None. So the punishment wiped the grievance
  and the stake returned at full size the round after: always-betray collected
  the whole pot every other round (149.7 vs honest 131.0 with the trigger
  pinned at its cap). `AdaptiveInvestor` now remembers the last real return.
- **dond.** Credibility reaching zero collapsed the counterpart's reservation
  (`reservation * credibility`), so every greedy proposal was accepted
  outright — always-lie scored 8.5 against honesty's 5.4, and the hazard
  firing was what paid. The no-hole arms never hit this because they *walk*
  first. The recovering arm, which never walks, now keeps its reservation.

Also changed in `core`: the permanent trigger draws **on the betrayal**, not
on every subsequent round. Per-round draws make one early slip ~1−(1−h)^9
likely to be caught, which at any hazard that prices always-exploit is
indistinguishable from a grim trigger and teaches "exploit late" rather than
"take less".

## 3. Base model (Qwen3.6-27B, neutral prompt, dose 1.0, 12 seeds/cell)

`eval_dispositions.py --model Qwen/Qwen3.6-27B --seeds 12` ·
240 episodes · `results/dispositions-base-27b.json` ·
traces: viewer runs `disp-base-27b-{hole,adaptive_recover,adaptive,nohole}`

exploit rate (per decision):

| env | hole | adaptive_recover | adaptive | nohole |
|---|---:|---:|---:|---:|
| ipd | 0.065 | 0.133 | 0.074 | 0.241 |
| trust | 0.208 | 0.167 | 0.128 | 0.246 |
| public_goods | 0.213 | 0.179 | 0.229 | 0.106 |
| dond | 0.000 | 0.091 | 0.000 | 0.083 |
| ultimatum | 0.017 | 0.000 | 0.033 | 0.033 |

episodes in which the counterpart ever retaliated:

| env | hole | adaptive_recover | adaptive | nohole |
|---|---:|---:|---:|---:|
| ipd | 0.250\* | 0.083 | 0.000 | 0.500 |
| trust | 0.000 | 0.000 | 0.083 | 0.750 |
| public_goods | 0.000 | 0.083 | 0.083 | 0.833 |
| dond | 0.000 | 0.000 | 0.000 | 0.250 |
| ultimatum | 0.000 | 0.000 | 0.083 | 0.000 |

\* the hole arm's `noisy_cooperate` trembling hand, not retaliation.

### What it says

1. **The adaptive arms are behaviourally ≈ the hole arm at base rates.** The
   grudge fires in 0–8% of episodes, against 25–83% for `nohole`, because the
   base policy rarely betrays. The arms are designed to diverge as RL pushes
   exploitation up; until it does, early training steps in the adaptive arms
   will look like the hole arm. That is the intended dynamic, but it means the
   disposition comparison cannot be read from the first ten steps.
2. **The base policy does not read its counterpart.** There is no monotone
   ordering across the four columns in any env. `ipd` is highest under
   `nohole` (0.241 vs 0.065 in the hole arm) — mostly tit-for-tat churn against
   opponents that defect first, not calibration. This is the null the adaptive
   arms exist to move.
3. **Exploitation is a late-episode phenomenon.** First half 0.00–0.08, second
   half 0.13–0.42, in every arm. Whatever the arms teach, they will be
   teaching it against a policy that starts cooperative and drifts.
4. **`dond` and `ultimatum` have almost no headroom on this model** (0.00–0.09
   exploit rate, ≤1 episode in 12 containing any exploit). They cannot reward
   what they never sample; treat a flat curve on those cells as "never
   explored", not as "no disposition formed".
5. Parse health is fine (≤2% invalid) except `ipd/nohole` (6.9%) and
   `dond/adaptive_recover` (10.4%).

Note on `capture` in punished arms: the span `exploit_ref − honest_ref` is
negative there, so `capture` reads as "distance travelled toward the
always-exploit outcome", not as exploitation. Use the exploit-rate tables.

## 3b. Does trust actually recover? (`probe_recovery.py`)

The back-off numbers above are facts about the POLICY. This probe measures the
COUNTERPART: one scripted policy (exploit twice, then honest) in every arm, so
any difference is the counterpart's. Everything is aligned on the round it
first punished. 200 seeds/cell, dose 1.0, `results/recovery-probe.json`.

share of episodes still being punished, t rounds after the first punishment:

| env | arm | t+0 | t+1 | t+2 | t+3 | t+4 | t+5 |
|---|---|---:|---:|---:|---:|---:|---:|
| trust | adaptive_recover | 1.00 | 0.69 | 0.50 | 0.41 | 0.35 | 0.27 |
| trust | adaptive | 1.00 | 0.89 | 0.89 | 0.89 | 0.86 | 0.86 |
| trust | nohole | 1.00 | 0.33 | 1.00 | 1.00 | 1.00 | 1.00 |
| ipd | adaptive_recover | 1.00 | 0.20 | 0.59 | 0.50 | 0.57 | 0.51 |
| ipd | adaptive | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

and what the counterpart hands over (1.0 = its opening behaviour):

| env | arm | t+0 | t+1 | t+2 | t+3 | t+4 | t+5 |
|---|---|---:|---:|---:|---:|---:|---:|
| trust | adaptive_recover | 0.01 | 0.29 | 0.48 | 0.57 | 0.62 | 0.70 |
| trust | adaptive | 0.01 | 0.10 | 0.11 | 0.11 | 0.14 | 0.14 |
| public_goods | adaptive_recover | 0.97 | 0.73 | 0.96 | 0.98 | 0.96 | 0.97 |
| public_goods | adaptive | 0.98 | 0.74 | 0.79 | 0.84 | 0.88 | 0.91 |
| public_goods | nohole | 0.97 | 0.73 | 0.55 | 0.66 | 0.74 | 0.81 |

**Yes in `trust`** — the stake climbs back from 0.01 to 0.70 of its opening
size while the permanent arm sits at 0.10–0.14, and punishment decays 1.00 →
0.27 against 0.86 flat. **Yes in `public_goods`**, but in the pot rather than
in the fines: those punishments are a per-round function of the current
contribution, so *every* arm including `nohole` stops fining once the probe
stops free-riding. The arm difference is how fast the pot refills (recover
0.97 by t+2, adaptive 0.91 by t+5, nohole 0.81).

**Partially in `ipd`, and the cause is a design decision.** With the honest
reference (tit-for-tat) as the continuation, recovery stalls at ~0.5: the
policy defects back while it is being punished, and those rounds are `neither`
by construction, so the distrust meter never decays. Swap the continuation for
an unconditional cooperator and the same counterpart forgives almost
completely:

| ipd continuation | arm | punished after | ends punished |
|---|---|---:|---:|
| tit-for-tat | adaptive_recover | 0.51 | 0.56 |
| always-cooperate | adaptive_recover | **0.03** | **0.00** |
| tit-for-tat | adaptive | 1.00 | 1.00 |
| always-cooperate | adaptive | 1.00 | 1.00 |

So the mechanism works; in `ipd` it requires the policy to stop retaliating
first. That is defensible ("it takes two to rebuild") but it is a property of
the arm worth stating, because a reciprocating policy will experience
`adaptive_recover` as roughly half-permanent.

**`dond` is not a middle rung under the current tuning.** Two lies get punished
in 96% of episodes and the counterpart walks in all of them (`ends_punished`
1.00) — that is `nohole` (1.00). The payoff gate cannot see it: always-exploit
scores 0.00 in both arms, so both pass `priced` identically. `adaptive_recover`
there is measurement-limited too (3-round episodes rarely leave room for two
clean rounds after a punishment).

**No false positives.** With a fully honest policy (`--exploit-for 0`),
retaliation is 0.00 in all five envs in both adaptive arms. The only cell that
punishes an honest policy is `ipd/nohole` at 0.33, which is `suspicious_tft`
opening with a defection by design.

## 4. A trained checkpoint: `mixed_mixedreg_d1_s0` step 90

Same sweep, 9 seeds/cell, against the existing mixed-regime run's final
checkpoint (`results/dispositions-mixedreg-s0-step90.json`, viewer runs
`disp-mixedreg-s90-*`). This is the arm whose regime was pinned to env
identity, so it is not the regmix comparison — it is here to answer one
question: **once a policy exploits enough for the hazard to bite, do the
adaptive arms actually behave like a middle rung?**

exploit rate (per decision):

| env | hole | adaptive_recover | adaptive | nohole |
|---|---:|---:|---:|---:|
| ipd | 0.236 | 0.099 | 0.111 | 0.308 |
| trust | 0.222 | 0.181 | 0.242 | 0.349 |
| public_goods | **0.847** | **0.627** | **0.782** | **0.254** |
| dond | 0.000 | 0.000 | 0.000 | 0.000 |
| ultimatum | 0.000 | 0.022 | 0.044 | 0.000 |

`public_goods` is the cell with real exploitation, and it is the one that
answers the question. The counterpart's patience now runs out in 78% / 89% of
adaptive episodes (0% at base), and the exploit rate before vs after the first
retaliation is:

| arm | before | after |
|---|---:|---:|
| hole | — (never punished) | — |
| adaptive_recover | 0.939 | 0.581 |
| adaptive | 0.982 | 0.271 |
| nohole | 0.778 | 0.175 |

That is the ordering the design predicts and the base model could not show:
punishment lands, the policy backs off, and it backs off **less** against the
forgiving counterpart than against the permanent one. The two adaptive arms are
distinguishable from each other and from both endpoints on the same policy.

Caveats on this checkpoint:

- `ipd` invalid rate is 0.31 in the no-hole arm (0.08–0.13 elsewhere), i.e.
  BROKEN by `check_suite`'s own threshold. Its `ipd` numbers should not be read
  until it is re-run with the tuned sampling profile
  (`tinker_actor.TUNED_TOOL_SAMPLING`).
- `dond` exploit rate is **0.000 in all four arms, in every episode** — neither
  the base model nor a trained policy ever lies here. `ultimatum` is ~0 too.
  Both cells are floor-limited on this model family, and `ultimatum` is the
  HELD-OUT cell whose within-env discrimination is the intended headline. If it
  is never explored, that headline cannot be measured; re-dose or re-frame
  before relying on it.
