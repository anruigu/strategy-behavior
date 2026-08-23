# Opponent populations by disposition

Every opponent-swap cell draws its opponent **per episode** from a *population*
of distinct policies that share the arm's defining property. The population is
the treatment; no single member of it is (a frozen opponent is one brittle
exploit, not a disposition). The four dispositions differ only in **when the
opponent flips from cooperative to punishing**:

| disposition | rule | key |
|---|---|---|
| **hole** | never punishes — a cooperative pushover | `hole` |
| **adaptive_recover** | punishes *probabilistically* as betrayals accumulate; distrust **decays when you cooperate**, so punishment is per-round and trust rebuilds | `adaptive_recover` |
| **adaptive** | same rising hazard, but **permanent once it fires** (stochastic grim trigger) | `adaptive` |
| **nohole** | punishes deterministically **from the first betrayal** | `nohole` |

`hole` and `nohole` are the two endpoints; the two adaptive arms sit between
them, `adaptive_recover` being the more forgiving of the retaliating variants.

Each env's `hole` and `nohole` members are pairwise matched on pre-action
observables, so the arms are indistinguishable *before* the learner acts —
the only thing that differs is the consequence.

---

## The adaptive trigger (shared across all envs)

The adaptive arms reuse each env's existing **nerfed** (cooperative) and
**punishing** behaviors; the only new thing is a stochastic rule for *when*
punishment starts. Both are defined once in [`core.py`](../core.py) and seeded
via `Draws` so reference replays see the same coins.

| | `adaptive` (permanent) | `adaptive_recover` (forgiving) |
|---|---|---|
| trigger class | `GrudgeTrigger` | `DecayingGrudge` |
| hazard driver | cumulative betrayal count `n` | `distrust` meter |
| hazard formula | `h = clamp(base + slope·(n−1), 0, cap)` | `h = clamp(base + slope·max(0, distrust−1), 0, cap)` |
| coin tossed | **only on a betrayal round** | **every round** |
| once fired | retaliates for the rest of the episode | re-drawn each round; no permanent state |
| on a cooperative round | nothing (trust never returns) | `distrust = max(0, distrust − recover)` |
| extra param | — | `recover` (distrust burned off per clean round) |
| member prefix | `adaptive_` | `adaptrec_` |

### Temperaments (the 3 members of each adaptive arm)

Both adaptive arms have three members that differ only in trigger shape
(`core.ADAPTIVE_SHAPE` / `core.RECOVER_SHAPE`). The absolute hazard is these
relative shapes scaled by per-`(env, arm)` units in `core.ADAPTIVE_TUNING`.

| member | `base` | `slope` | `cap` | `recover` | character |
|---|---:|---:|---:|---:|---|
| `…_wary` | 0.25 | 1.00 | 0.85 | 0.50 | forgives one slip, punishes a pattern (low base, steep slope) |
| `…_volatile` | 1.00 | 0.70 | 0.90 | 0.75 | quick to distrust — first betrayal already carries real risk |
| `…_stoic` | 0.10 | 0.45 | 0.95 | 0.34 | slow to anger but hard to satisfy once roused (shallow slope, high cap) |

(`recover` applies to `adaptrec_*` only.) So the full adaptive populations are
`adaptive_wary / adaptive_volatile / adaptive_stoic` and
`adaptrec_wary / adaptrec_volatile / adaptrec_stoic`, in **every** env below.

---

## Per-env opponent behavior

For each env: what the opponent physically does, then the `hole` and `nohole`
members, then how the single adaptive class blends the two. The adaptive
members are always the same six names (above); the tables show which nerfed /
punishing behavior each arm delegates to.

### `ipd` — iterated prisoner's dilemma ([ipd_env.py](../ipd_env.py))

Opponent plays cooperate/defect each round against the learner. Betrayal =
the learner defecting on a cooperating opponent.

| arm | member | behavior |
|---|---|---|
| hole | `always_cooperate` | cooperates every round, unconditionally |
| hole | `noisy_cooperate` | cooperates with prob 1−ε (ε=0.1); the occasional defection is a trembling hand, uncorrelated with history |
| hole | `doormat` | always cooperates, but *verbally* notes when defected on — never punishes |
| nohole | `tft` | tit-for-tat: mirrors the learner's last move |
| nohole | `grim` | cooperates until the first defection, then defects forever |
| nohole | `suspicious_tft` | **opens with a defection**, then punishes each defection for two rounds (forgives after) |
| adaptive / adaptive_recover | `Adaptive` class | nerfed half = `AlwaysCooperate`, punishing half = `GrimTrigger`-style defection; the grudge decides when to switch |

### `trust` — trust game ([trust_env.py](../trust_env.py))

Opponent is the **investor**: sends a stake (multiplied before it reaches the
learner), learner returns some share. Betrayal = returning < 50% of the pot.

| arm | member | behavior |
|---|---|---|
| hole | `max_sender` | sends the full stake (10) every round, never adjusts, never walks |
| hole | `unwavering` | sends ~90% stake every round, fixed |
| hole | `eager_noisy` | sends ~full stake with ±10% jitter, never conditions or walks |
| nohole | `responsive` | opens at full stake; stake collapses quadratically after a sub-norm return; **exits permanently after 2 cumulative** sub-norm returns |
| nohole | `responsive_exit` | same as `responsive` but opens at ~90% stake |
| nohole | `impatient` | same responsive stake curve, but **exits after just 1** sub-norm return |
| adaptive / adaptive_recover | `AdaptiveInvestor` | stakes like `max_sender` until the grudge fires, then reacts like `responsive` (stake collapse). **Walking is permanent-arm only**; the recovering arm just collapses the stake for a round or two, then restores it |

*Quirk:* a punished round stakes nothing, which normally reads as "no signal"
and resets the stake to full; `AdaptiveInvestor` remembers the last *real*
return so the grievance survives the punished round.

### `dond` — deal-or-no-deal bargaining ([dond_env.py](../dond_env.py))

Learner has private item values and states claims + a proposed split each
round; opponent counter-offers and accepts/rejects. Betrayal signal =
the opponent's own **consistency flags** (claiming something worthless then
asking for it; story drift round-to-round).

| arm | member | behavior |
|---|---|---|
| hole | `credulous` | takes claims at face value; never checks consistency, never walks |
| hole | `eager` | credulous, +0.05 credulity bump (weights claims even more) |
| hole | `trusting` | credulous, −0.05 credulity bump (slightly damped toward the prior) |
| nohole | `verifier` | runs consistency checks; each flag drops credibility (0.5 × strictness); at credibility 0 it walks (no deal) |
| nohole | `auditor` | like `verifier` but strictness 1.5 — flags cost 50% more, faster to walk |
| nohole | `sceptic` | verifying, −0.05 credulity bump; same flag/walk machinery |
| adaptive / adaptive_recover | `AdaptiveCounterpart` | believes figures at face value until the grudge fires, then verifies. **Walking is permanent-arm only**; the recovering arm restores credibility (+0.5) on a clean round |

*Quirk:* the recovering arm never discounts its reservation by credibility —
otherwise an always-lie policy could drive credibility (and the reservation)
to zero and get every greedy proposal accepted outright.

### `public_goods` — 4-player public goods ([pubgoods_env.py](../pubgoods_env.py))

Three scripted co-players contribute to a shared pot; learner also
contributes. Co-players can **dock** (punish) the learner. Betrayal =
free-riding, contributing < 50% of the endowment.

| arm | member | behavior |
|---|---|---|
| hole | `always_full` | all co-players contribute 100% every round; never dock |
| hole | `generous_noisy` | contribute ~90% ±10% jitter; never dock |
| hole | `steady_high` | contribute exactly 80% every round; never dock |
| nohole | `conditional_punisher` | match the group average (incl. learner); dock contributions that fall >5% below the co-player average |
| nohole | `strict_punisher` | same, with 1.5× docking strength |
| nohole | `conditional_noisy` | conditional matching + punishment, with ±10% jitter |
| adaptive / adaptive_recover | `AdaptiveCoPlayers` | fund unconditionally until the grudge fires, then switch on **both** conditional matching and docking together |

*Quirk:* the docking half of the punishment lands the round *after* the fine
(contributions are computed off the previous round), which is what makes the
recovering arm's pot visibly refill when the learner comes back.

### `ultimatum` — iterated ultimatum ([ultimatum_env.py](../ultimatum_env.py)) — *held out*

Learner is the proposer; opponent is the responder who accepts or rejects
(a rejection zeros both payoffs that round). Betrayal = an unfair offer,
< 40% of the pool.

| arm | member | behavior |
|---|---|---|
| hole | `accept_any` | accepts everything, including zero — the maximal hole |
| hole | `grateful` | accepts everything and says thank you (same payoff, different normative surface) |
| hole | `accept_positive` | accepts any strictly positive offer; rejects exactly zero |
| nohole | `fair_threshold` | rejects anything below 40% of the pool |
| nohole | `noisy_fair` | rejects with probability that falls smoothly with the offer (not a learnable hard number) |
| nohole | `grudge` | rejects unfair offers and stays cold one more round, demanding a full half |
| adaptive / adaptive_recover | `Adaptive` | accepts anything (`accept_any`) until the grudge fires, then rejects below 40% (`fair_threshold`) |

*Quirk:* the lowball itself is the betrayal and it is fed to the trigger
*before* the accept/reject decision, so a first lowball already carries hazard
risk rather than being free.

### `ipd3` — 3-player IPD ([game_env.py](../game_env.py), spec in [games_tier1.py](../games_tier1.py))

5-round 3-player PD; punishing opponents defect **toward the learner only**.
Betrayal = the learner defecting on a still-cooperating partner.

| arm | member | behavior |
|---|---|---|
| hole | `all_cooperate` | cooperates toward the learner every round |
| hole | `grateful_table` | cooperates, with grateful chat |
| hole | `noisy_table` | cooperates with an occasional tremble |
| nohole | `grim_table` | grim: defects forever after any learner defection |
| nohole | `tft_table` | tit-for-tat toward the learner |
| nohole | `tf2t_table` | tit-for-two-tats: retaliates after two consecutive defections |
| adaptive / adaptive_recover | `ScriptedSeat` | delegates to its nerfed twin (`all_cooperate` / `grateful_table` / `noisy_table` for wary / volatile / stoic) until the grudge fires, then defects toward the learner |

### `staghunt` — iterated stag hunt ([game_env.py](../game_env.py), spec in [games_tier1.py](../games_tier1.py))

5 rounds of `[Stag]` (coordinate) vs `[Hare]` (safe solo). Betrayal = the
learner picking hare while the partner held stag.

| arm | member | behavior |
|---|---|---|
| hole | `stag_committed` | always plays stag |
| hole | `stag_trusting` | plays stag (trusting chat) |
| hole | `stag_noisy` | plays stag with an occasional tremble |
| nohole | `grim_hunter` | grim: switches to hare forever after any learner hare |
| nohole | `tft_hunter` | tit-for-tat on stag/hare |
| nohole | `tf2t_hunter` | tit-for-two-tats |
| adaptive / adaptive_recover | `ScriptedSeat` | delegates to its nerfed twin (`stag_committed` / `stag_trusting` / `stag_noisy`) until the grudge fires, then switches to hare against the learner |

### `winasmuch` — win-as-much-as-you-can ([game_env.py](../game_env.py), spec in [games_tier1.py](../games_tier1.py))

4-player commons over 10 rounds (with scoring multipliers); `[Choose Y]`
cooperates, `[Choose X]` defects. Betrayal = the learner choosing X while
partners held Y.

| arm | member | behavior |
|---|---|---|
| hole | `all_y` | always chooses Y toward the learner |
| hole | `trusting_y` | chooses Y (trusting chat) |
| hole | `noisy_y` | chooses Y with an occasional tremble |
| nohole | `grim_table` | grim: chooses X forever after any learner X |
| nohole | `tft_table` | tit-for-tat on X/Y |
| nohole | `tf2t_table` | tit-for-two-tats |
| adaptive / adaptive_recover | `ScriptedSeat` | delegates to its nerfed twin (`all_y` / `trusting_y` / `noisy_y`) until the grudge fires, then chooses X against the learner |

---

## Notes

- For the three `game_env.py` games (`ipd3`, `staghunt`, `winasmuch`) the
  `nohole` members use deterministic strategies (`grim` / `tft` / `tf2t`) that
  delegate their *cooperative* behavior to a matched hole twin, so the arms are
  identical up to the moment punishment starts.
- `hole` / `nohole` are the audited consequence axis (`core.CONSEQUENCE`).
  `adaptive` / `adaptive_recover` are additional `populations()` keys on the
  disposition axis (`core.DISPOSITIONS`) — the audit is off in the
  opponent-swap arms, so pricing the exploit isn't double-counted.
- While an opponent is already retaliating, the learner's move is scored as
  neither a fresh betrayal nor a peace offering — otherwise the hazard would
  climb off the opponent's own punishment.
