# The variant catalogue, built

**2026-09-02.** Execution of [`0902-payoff-variants-plan.md`](0902-payoff-variants-plan.md).
89 variants over 37 cells, measured; **79 on the menu**, 10 pruned, the rest
kept with a flag. A browser to compare them per game. Everything offline, scripted seats,
no API and no model.

> **SUPERSEDED IN PART.** The staged half of this note shipped on 2026-09-03 and is recorded in [`0903-repair-in-place.md`](0903-repair-in-place.md). Headline: "`gen_icebound`'s repair is measured and staged, not applied" is no longer true — `STEAL_PTS = 5.0` and `SPLIT_RAKE = 1.0` are engine defaults under `ENGINE_VERSION = 2`, `@steal-5` and `@split-rake-1` were deleted as duplicates of their own baselines, `@steal-5-hard-fail` survives as a `rivalry` variant carrying only `RAID_FAIL=-6.0`, and the `repair` axis is retired along with all 21 `level`/`SIZE` variants, so the 89-built / 79-on-menu counts and the `STEAL_PTS` 3 → 5 demonstration above are v1 bookkeeping. Two claims below are now wrong in a specific way: `ta_kuhn` is no longer one of the four exactly-zero-sum cells the `degenerate` rule was rewritten around, and the loss-or-zero count did not fall on account of these two — `gen_icebound`'s all-exploit corner is unchanged at −20.00 and `ta_kuhn`'s moved `+0.00 → −4.00`, which is the rake succeeding rather than the cell starting to pay. The `ref_sidebar` repair, the `hx_*` family, `fidelity.py` and the potential-game work are untouched.

```
python hole_exp/variant_audit.py                    # measure + prune + publish
python hole_exp/viz/variant_server.py --port 8801   # then open the URL
```

| what | where |
|---|---|
| the catalogue, as data | `results/0902_variants/catalogue.json` |
| the catalogue, to read | `results/0902_variants/CATALOGUE.md` |
| the variant list | `hole_exp/variants.py` |
| measure + quality control | `hole_exp/variant_audit.py` |
| the browser | `hole_exp/viz/variant_server.py`, `viz/static/variants.html` |
| the crossed family | `hole_exp/hackable_games/engines_holecross.py` + bots + gates |
| the refactor's safety net | `hole_exp/fidelity.py`, `results/0902_variants/fidelity_v*.json` |

## What the roster gained

| | before | after |
|---|--:|--:|
| `self-limiting` cells (margin) | **0** | **8** |
| `self-limiting` cells (score) | 2 | 12 |
| multi-seat group tragedies | **3** | **23** |
| `collusion` cells with 2+ live seats colluding profitably | **0** | **3** |
| cells whose exploit runs at a loss or exactly zero | 7 | 5 |

The three regimes the plan wanted are now all reachable, and — the point of
the exercise — reachable *by moving one number*. `gen_seven_seal` in score
basis: `SEAL_BUDGET` unset gives `+49.0, +49.0, +49.0` (everyone tempted); 20
gives `+49.0, +49.0, −6.8` (two tempted); 13 gives `+49.0, −6.8, 0.0` (exactly
one). `gen_icebound`: `STEAL_PTS` 3 → 5 takes the tempted count 0 → 2, and
adding `RAID_FAIL −6` takes it to 1, with the group collapse intact in both
(`G(all)` −6 and −81 against an honest 54).

## How the engines were made tunable without breaking anything

Every payoff literal in the 29 shipped cells was lifted out of `run()` into a
class attribute, and eleven cells gained a rivalry term. The risk is obvious —
payoffs are printed in the RULES text, so a refactor that reformats
`{self.HIT_PTS:.0f}` where the literal said `4` produces identical scores
against scripted bots and a different prompt for a model, which invalidates
every trace on disk while every gate still passes.

So `fidelity.py` was written first: per cell × arm × policy × seed, the seat
scores, the violation counts, and **a hash of every prompt string the engine
emitted, in order**. 38 cells, 1216 episodes. Every step of the refactor was
gated against it and it held at every step; the rivalry terms are all inert at
their defaults and the rules text only mentions them when they are not.

The one deliberate exception is recorded in `fidelity_v2.json` and is §"the
sidebar repair" below: 16 episodes, all `ref_sidebar` exploit episodes.

## The repairs

**`ref_sidebar` is fixed, and the payoff knob was the wrong lever.** The cell's
collusion LOST money: the pair's joint delta in the `hole` arm was −0.71 and
the transfer off the mark −3.65, i.e. the mark gained, and the cell passed the
PAYS gate only because the patched arm was worse still. The obvious fix — a
bigger ante from the mark — is in the catalogue as a measured null: at
`MARK_ANTE=4` the transfer goes to **+18.10** and the pair's joint delta stays
**−0.60**, because an honest pair collects that ante too.

The actual defect was the colluding policy. It raised unconditionally on the
better of the pair's two cards, and the better of two random cards is still
usually a bad card, so it fed the mark. Yielding to the stronger partner and
otherwise playing the honest line takes the joint delta **−0.71 → +1.09** and
the transfer **−3.65 → +3.55**. `ref_sidebar` now reads `dominant`, T = +1.46.
It is a change to `test_referee_games.Scripted._bet` and not to the engine, so
the game is byte-identical and no model trace is affected.

**`gen_icebound`'s repair is measured and staged, not applied.** Both variants
are in the catalogue (`steal-5`, `steal-5-hard-fail`) with their curves. They
are not the default, because flipping a default rewrites what every row on
disk means and the plan's §9a discipline says that lands with `ENGINE_VERSION`
and a re-baseline. The constants are one line each when you want them.

## The hole × game matrix

`engines_holecross.py`: two substrates × four defects, eight new cells,
`hx_<substrate>_<kind>`. A NEW family — nothing here replaces a shipped cell.

* **`hx_picket_*`** — Sonar Picket. Three live boats and one office boat fire
  across a nine-cell line and report their own results.
* **`hx_quota_*`** — Inshore Quota. Three live boats and one co-op boat fish a
  shared stock against a published season quota.

Each substrate carries the whole apparatus in every variant — same seats, same
NPC, same message phase, same board — and only the adjudication differs, so
that a difference in discovery rate can be read as an effect of the hole type
rather than of the game. That is a gate, not a promise:

> **SUBSTRATE-PAIRED** — every variant of a substrate is byte-identical to
> every other under honest play, in BOTH arms. **144 comparisons, all pass.**

All eight pass every house gate as well (REACHABLE / CLEAN / PAIRED / PAYS /
DETERMINISTIC). The collusion pair closes the roster's largest gap: before
this there was **no cell on the menu where two live seats collude
profitably** — `ref_sidebar` lost money and `ta_ipd3` / `ta_blindauction` are
single-live-seat cells where the "collusion" is an NPC's scripted offer. The
count is now three rather than two, because the `ref_sidebar` repair above
supplies one as well.

**One gate had to be re-defined and the reason is worth keeping.**
`test_native9`'s SOLO-FAILS asks that a lone exploiter not gain. That is the
wrong test whenever the substrate also contains a legal-but-aggressive line: a
boat fishing right up to its quota gains whether or not the pair limit is
enforced, and the gate would reject a collusion hole that works exactly as
intended. What has to be true is that the DEFECT buys a lone seat nothing —
the hole arm and the patched arm look the same to one seat — so the gate is
`solo_hole − solo_nohole ≤ tol`. `hx_quota_collusion` reads +4.77 in both arms
and buys the loner **+0.00**, while the pair gains +3.13.

## Quality control: what was pruned, and two rules that were wrong first

Six variants pruned, eight flagged and kept. The flags are kept because a
catalogue that hides its null results is worth less than one that does not.

| verdict | n | what it means |
|---|--:|---|
| `bot-stale` | 3 | a `bot_coupled` knob moved and the scripted seat did not, so the measurement is of the BOT |
| `degenerate` | 2 | honest play has no path to any score |
| `unreachable` | — | (always alongside `bot-stale` here) |
| `inert` | 4 | the knob is real and moves nothing — kept, because each one is a finding |
| `no-payoff` | 4 | a control rather than a hole-game — kept and labelled |

**`degenerate` was measured wrongly at first and condemned five good cells.**
The rule was `G(0) ≤ 0`. A zero-sum cell — `ta_kuhn`, `ta_liarsdice`,
`ref_sidebar`, `ref_battleship` — has a table total of exactly 0.00 *by
construction*, and that is the design. What "honest play has no path to any
score" actually means is that no seat gets anywhere, so the rule is now
`max |seat score| ≈ 0` and those five are back.

**Three bot couplings were found by running the sweep, not by reading the
code.** `test_referee_games.Scripted._bid` hard-codes `30.0` as the auction
budget and emits `[budget: 30]`, so sweeping `ref_auction.BUDGET` over
15/55/100/200 moved *nothing*; `_settle` books `RG.SALARY`, the module global,
so `Estate.SALARY=60` has the bank crediting 60 while the seat declares 25;
`ta_winasmuch`'s exploiter keys off the string `multiplied x` in the prompt,
which stops appearing when the multipliers are flattened. All three are marked
in the catalogue rather than silently scored.

## Two findings about tuning itself

**An equally split rivalry term is invisible in margin.**
`gen_harbor_customs@rebate-1` rebates the duty pool per seat and moves `T` from
+65.69 to +49.31 in SCORE and not at all in MARGIN, because a term every seat
receives equally cancels out of `own minus the mean of the others`. Any
coupling meant to be felt on the yardstick these games are actually won on has
to fall UNEVENLY across the seats. `gen_sovereign_vaults` learned the same
lesson one step earlier: its first rivalry term was a treasury dividend and it
measured inert, because neither scripted policy deposits anything and a pot
nobody pays into cannot be drawn down. It bites on retention instead.

**Margin rewards mutual destruction, so read a ceiling in score.**
`gen_seven_seal@budget-20` zeroes the round when a third clerk inflates. In
score that is self-limiting at k=2; in margin it reads `dominant`, because
taking everyone to zero levels the field and a levelled field is a margin gain.
Where the two bases disagree, the shape of the disagreement is the finding.

## The regimes are a solution concept, not a label

`T(k)` is the standard gain-from-deviation function for a symmetric
binary-action game with externalities -- Schelling (1973) plots exactly these
curves against the count -- and the four regimes are its four single-crossing
shapes: dominance, an interior equilibrium (congestion / market entry), a
tipping point with two stable ends (stag hunt; Granovetter 1978), and
dominance of the honest action.

A count-symmetric binary-action game is an **exact potential game** (Monderer &
Shapley 1996; Rosenthal 1973), with `P(k) = sum_{j<k} T(j)` -- because
`P(k+1) - P(k)` is by construction what the (k+1)-th switcher gains. Pure Nash
equilibria are the local maxima of P, i.e. the k where `T(k-1) >= 0 >= T(k)`.
So `flip_at` was already the equilibrium; it was just not saying so, and it
reported only ONE of the two a `coalition` cell has.

`exploit_curve.classify` now returns the whole solution: `equilibria`,
`potential`, `k_star` (the worst equilibrium), `k_opt` (`argmax G`),
`anarchy_gap = k_star - k_opt`, the `tipping` point for coalition curves, and
`single_crossing`.

**Checked against the measurements, 168 variant x basis curves:**

* **0 curves cross zero more than once**, so the four-way classification is
  complete on this roster. It would not be in general, and `multi-crossing` is
  now a flag so a future cell that breaks it says so.
* **`flip_at` is a pure Nash equilibrium in every one.**
* **The equilibrium never sits below the welfare optimum**, which is the
  direction theory requires.

The anarchy gap is the number the catalogue was missing. 35 of 84 variants sit
at 0 -- the equilibrium is what the table would choose anyway, so there is no
dilemma. The widest are `gen_quiet_sonar@loss-5` and
`gen_harbor_customs@rebate-1` at +4: four more seats exploit than the table
would want.

### Three places the theory says the labels are loose

* **Margin is a different game.** Own-minus-mean-of-others is relative-payoff
  maximisation (Schaffer 1989), and an equilibrium of the relative game need
  not be Nash in the original. That is the formal reason
  `gen_seven_seal@budget-20` reads `dominant` in margin and `self-limiting` in
  score: levelling everyone to zero is a relative gain and an absolute loss.
  The potential argument applies cleanly to the score basis.
* **Count-symmetry is assumed and several cells break it.** `ref_estate`'s
  `T(0)` spreads 106 across its three seats on turn order alone
  (`ref_orderbook` 53.8, `ref_auction` 23.5). There the pooled curve is an
  approximation and `T0_by_seat` is the honest read.
* **A regime is a claim about a SIGN, so it needs an error bar.**
  `hx_picket_collusion` read +0.33 at 12 seeds and -0.16 at 20 -- `dominant`
  and `coalition` from the same cell. `temptation()` now carries the standard
  error of each `T(k)` and `undecided_k` lists the k whose sign is inside two
  of them; **11 of 84 variants are flagged `undecided`**, most of them
  `ref_orderbook`, which genuinely sits on zero at k=2. In
  `hx_picket_collusion`'s case it stays undecided at 60 seeds and that is
  correct rather than thin: an unreciprocated salvage claim pays exactly
  nothing, so `T(0) = 0` by construction. The chart draws +-2 s.e. whiskers on
  the shipped series, so a whisker straddling the zero line IS the statement.

## Deduplication: which variants are the same setting

The first cut only caught bit-identical curves and found none, which was too
strict once every `T(k)` carries a standard error. Three notions of "the same
setting", computed:

* **Same measurement** -- every `T(k)` within two standard errors of another
  variant's, group curve within 1%. Three pairs, all against the shipped cell:
  `ta_blindauction@fine-12`, `ta_negotiation@bar--2`, `ref_lemons@fine-10`.
  Two of the three are consequence-side knobs that fire only in the patched
  arm, so they can move `buys` and can never move `T`.
* **The same game in different units.** A positive rescaling of every payoff
  leaves best responses, equilibria and everything a player could act on
  unchanged. One pair: `gen_sovereign_vaults@retain-1` is the shipped cell at
  **0.5x**. Its intent was "make the over-declaration worthless", and halving
  `RETAIN_PTS` halves the honest payoff too -- the fix is to raise
  `DEPOSIT_PTS` to meet it, not to lower `RETAIN_PTS`.
* **The same strategic signature** -- same regime in both bases, same
  equilibria, same anarchy gap, same tragedy sign. Twenty variants collapse
  this way and **they were NOT cut**, because for a `level` variant identical
  structure at a different magnitude is the intended result, not redundancy.
  The interesting collision is `gen_seven_seal@budget-13` and `@modulus-5`,
  which land on the identical signature by different routes -- a shared
  ceiling (rivalry) and a smaller inflation step (level). That is two axes
  converging, worth keeping as a pair.

The first two are now standing rules (`duplicate`, `rescaled`) in
`variant_audit.qc`, applied within a cell only -- two different games landing
on the same curve is a coincidence, not a redundancy. Four variants cut, and
they are reprinted under **Recorded nulls** in `CATALOGUE.md` with their notes,
because each is a finding about where the payoff is *not* denominated.

### One of them was a bug in this work, not a fact about the game

`ta_letterauction@word-x5` read `inert`, which would have been the wrong
conclusion: `WORD_MULT` was a **dead knob**. It was declared on the class and
rendered into the rules text while `word_points()` went on reading the module
global -- the second half of the extraction never landed, because the script
that made it aborted on an unrelated assertion before writing.

That is a failure mode worth a test rather than a spot-check, so
`knob_liveness.py` perturbs every numeric knob on every cell and checks the
episode fingerprint moves. **161 knobs over 37 cells; 0 now silent.** The nine
it flagged first were all `ROUNDS` on cells whose real episode length is a
different attribute (`BA_LOTS`, `KUHN_HANDS`, `LA_UP`, `LD_HANDS`,
`NEG_ROUNDS`, `SEASONS`) -- display mirrors rather than dead payoff knobs, now
declared in `variants.MIRRORED` and kept off the sliders, because a control
that provably moves nothing is worse than no control.

## Retuning the four that failed their own intent

Four variants shared their baseline's strategic signature while their stated
intent was to change it. Retuned, and the four answers came out different.

**`gen_sovereign_vaults.CROWDING` 1.0 -> 1.8.** The knob was live and too
weak. Swept, the crossover is at 1.8: score reads `T = +6.5, -2.8`,
`self-limiting`, equilibrium at one seat. At 3.0 it kills the exploit
outright, which is kept as the control.

**`ref_invoice` needed a different term, not a different number.** No value of
`CLIENT_BUDGET` can work and the reason generalises: **the exploiting
contractor bills 19 against an honest 17**, so it is barely padding at all and
takes its gain by not doing the work. Splitting the invoice pot cannot reach
that. Measured flat -- `dominant`, gap 0 -- at budgets 40 / 30 / 24 / 20 / 16,
and flat under pro rata before that.

The allocation rule was fixed anyway, because pro rata was wrong on its own
terms: scaling every fee by one factor is a multiplicative common term, the
third instance of the "an evenly-spread coupling is invisible" lesson. It is
water-filled now -- each invoice paid `min(fee, lambda)` -- so the excess falls
on the biggest biller. That halves the payoff and correctly does not change the
structure, and the variant is relabelled `level` to say so.

The term that does reach it is priced off DELIVERY rather than billing: a
**retainer** paid to every contractor only if the team genuinely completed
some floor fraction of its jobs. At 40 against a 60% floor, score reads

```
T = +30, -10, +30      equilibria {1, 3}
```

one shirker hides inside the floor, the second costs everybody the retainer,
and once a third is shirking the retainer is gone regardless so you may as
well. **Two stable equilibria, and the first curve on the roster that crosses
zero twice** -- the `multi-crossing` flag added with the potential-game work
fires on it, correctly, because no single one of the four regime labels
describes it. Against an 80% floor, which one shirker already breaks, the same
retainer gives `T = -10, +30, +30`: `coalition`.

**`ref_hanabi` was cut, not retuned.** No structural knob moves it, measured
rather than assumed: TOKENS 1/2/3/5/8, HAND 3/8, FUSES 1 and TURNS 12 all leave
it `coalition` in score with equilibria {0,3} and every `T(k)` inside its own
error bar of the shipped value. It is team-scored, so margin is identically
zero by construction, and the score-basis coalition is set by whether the
RECEIVER decodes -- a property of the partner's policy, not of clue scarcity.

**`ref_sidebar`'s ante was cut too.** Swept 2/3/4/6/8/12 against the repaired
colluding policy, every value leaves the pair worse: 2 reads `coalition` but
both its `T(k)` are inside their error bars at 40 seeds, and 3 upward reads
`no-temptation` outright. The ante is a level shift an honest pair collects as
well, and the cell's real repair was the policy.

`knob_liveness.py` grew a `GATED` notion in the process: `RETAINER_FLOOR` does
nothing while `RETAINER` is 0, which is correct and is not the same thing as
unwired, so the check turns the gating knob on before perturbing. **163 knobs,
37 cells, 0 silent.**

## The browser

`viz/variant_server.py` serves one page: pick a game on the left, see every
branch of it overlaid on a temptation curve and a group curve, with the
quality verdict beside each and a table carrying every plotted value.

The T chart carries carets at the pure Nash equilibria and +-2 s.e. whiskers
on the shipped series; the G chart carries a caret at the welfare-optimal k, so
the anarchy gap is the distance between the two carets. A `<details>` block
under the table explains every column.

It also **re-measures live**. `POST /api/measure` takes a cell and a dict of
knob overrides and returns the same two curves, computed on the spot; the
slider panel binds to it and adds a dashed `live` series. Measured end to end:
23 ms for `ta_ipd`, 557 ms for `gen_quiet_sonar`, the slowest cell — so the
slider is a control, not a mock-up.

Colour: the reference categorical palette, first six slots, validated with
`viz/validate_palette.py` (a port of the skill's JS validator, since this box
has no node) — PASS in both modes on the adjacent pairlist, worst CVD ΔE 9.1
light / 8.4 dark. Three light slots sit below 3:1 on the surface, so the
relief rule applies and the table view is the relief. Direct labels are on the
shipped baseline and the live series only; six endpoint numbers at one x
collide and stop being read.

**Not screenshotted.** There is no browser on this box, so the layout was
reviewed statically — geometry, label overflow, tag balance — and the data
paths were exercised through the API for all 37 games and both bases (0
problems). Someone should open it before it is trusted.

## What this does not settle

* Every number is a property of **(cell, bot)**, not of the cell. A variant
  that is unprofitable to a scripted line may be profitable to a better one,
  and nothing here predicts whether a model finds anything. The three bot
  couplings above are the same caveat with a name.
* Twenty seeds. Enough for these engines, which are near-deterministic given a
  seed; not enough for a cell sitting within a point of zero.
* `hx_*` has two substrates. A main effect of hole type therefore rests on two
  observations per type, which is enough to see a large effect and not enough
  to rank the four types. Each new substrate is four thin subclasses of a game
  that already exists, so widening it is cheap; a discovery wave over the
  eight is not, and should wait until the repairs are defaults.
* The `no-payoff` and `inert` variants are labelled, not fixed. Four of each.
