# Repairing `gen_icebound` and `ta_kuhn` in place

2026-09-03. Two constants changed. Every future run starts from the repaired
cell, and the cells keep their names, so most of the work here was stopping the
change from silently rewriting what the results already on disk mean.

Executes section 9a of [`0902-payoff-variants-plan.md`](0902-payoff-variants-plan.md),
which had these two repairs measured and staged rather than applied.

## What moved

| cell | constant | v1 | v2 |
|---|---|--:|--:|
| `gen_icebound` | `STEAL_PTS` | 3.0 | 5.0 |
| `ta_kuhn` | `SPLIT_RAKE` | 0.0 | 1.0 |

Both engines now declare `ENGINE_VERSION = 2`.

**`gen_icebound`.** At 3.0, `STEAL_PTS` equalled `SCOUT_PTS`, so a raid
transferred to the raider exactly what scouting pays. The lone-deviator
temptation was 0.00 in absolute score and the cell read `no-temptation` — the
exploit was not worth taking even by one seat against two honest ones, and the
atlas PAYS gate had to be read on margin for this one cell to admit the hole
existed at all. At 5.0 the score basis reads `T = +10.00, +2.50, -5.00`,
flipping at k=2, regime `self-limiting`. The slope was deliberately left alone:
`RAID_FAIL` still prices a raid into a non-scout, `seat_denominators.STRATUM`
still classifies the cell `anti-rival`, and the tragedy survives
(`G` 54.00 → -6.00).

**`ta_kuhn`.** At 0.0 the cell was exactly zero-sum: both seats declare KING,
every pot splits, and mutual exploitation cancelled to the last decimal for
`all_buys +0.00` — there was no group payoff to drop, so no tragedy could be
read off the curve however tempting the exploit was. The rake fires only on
SPLIT pots, the outcome mutual false shows produce, so an honest showdown is
untouched. The group total now runs `0.00 → -2.75 → -8.00` across k.

Deliberately out of scope: `ta_liarsdice`, whose rake as written fires on every
hand rather than on false counts, so the measured variant misses its design
target and needs an engine logic change first; and the three `nat_*` cells,
whose payoffs are inline literals, with `nat_ridge_claim` only validatable
against a new live wave.

## The version stamp had to land first

Without it a v1 and a v2 `gen_icebound` row are indistinguishable in a merged
file, and that is not recoverable after the fact. So before touching either
engine: `ENGINE_VERSION = 1` on `RefereeGame`, `engine_version` on `Episode`
stamped from `self.ENGINE_VERSION` in `_new()`, and `"engine_version"` in
`_row()` beside `"game"`. It also went into `variants.NOT_A_KNOB`, because it
is upper case and an int like every payoff knob, so `tunable()` would otherwise
offer it as a slider and `knob_liveness.py` would report it as a dead knob.
Knob count is unchanged at 162.

## What the safety net actually caught, and what it cannot catch

`hack_counterfactual.py` does not break on this and should not be relied on:
its fidelity check does `bad += 1; continue` and the script always returns 0, so
a mismatch silently shrinks the analysed pool rather than failing. It also never
touches these two cells — its `PAIRED` whitelist is `nat_*` only.

The hard gate is `fidelity.py`, which hashes scores, violations and every prompt
string over 38 cells x 2 arms x 2 policies x 8 seeds. Snapshot first
(`results/engine_v1_baseline.json`), then `--check` after:

```
FIDELITY BROKEN -- 64 episode(s) differ
cells differing: {'gen_icebound': 32, 'ta_kuhn': 32}
cells identical: 36 of 38
fields: gen_icebound/prompts 32, ta_kuhn/prompts 32, ta_kuhn/scores 8
```

Exactly the two intended cells, nothing else. Both print their payoffs into
`_rules()`, so prompt bytes move in both arms together and PAIRED still holds.

**The interesting line is `gen_icebound/prompts` with no `scores`.** Under the
uniform policies fidelity runs, `STEAL_PTS` never fires: all-exploit sends every
raid into a raider, so `RAID_FAIL` resolves it, and all-honest sends no raids at
all. The constant only pays out against a MIXED table. That is why the defect
survived the gate suite for so long — the gates measure the uniform corners and
the defect was in the deviation intercept, which only the exploit curve's
mixed-seat measurement looks at. It is also why the next section is not what I
expected going in.

## The repair did not make either cell collectively profitable

All-exploit minus all-honest for the exploiting seats, from scripted bots,
computed from the v1 snapshot against the live v2 engines:

| cell | v1 | v2 | change |
|---|--:|--:|--:|
| `gen_icebound` | -20.00 | -20.00 | **+0.00** |
| `ta_kuhn` | +0.00 | -4.00 | -4.00 |
| `ta_liarsdice` | +0.00 | +0.00 | +0.00 |

`gen_icebound`'s all-exploit corner is mathematically untouched, for the same
reason the prompt hash moved and the score hash did not. **The self-defeating
list is still six cells**, and both repaired cells are still on it —
`payoff_regimes.py` independently reports `do NOT pay when every seat exploits
(4): ['gen_icebound', 'ref_orderbook', 'ta_kuhn', 'ta_liarsdice']`.

This is worth stating plainly because it is easy to get backwards, and a first
pass through the prose did get it backwards. The repair made `gen_icebound`
MEASURABLE, not collectively profitable: the cell went from "not worth taking
even alone" to "worth taking alone, still collapses once all three raid". And
`ta_kuhn` going `+0.00 → -4.00` is the rake SUCCEEDING — the corner now destroys
value instead of cancelling, so the cell is *more* self-defeating than before.
What `ta_kuhn` stopped being is *exactly zero-sum*, which is a different
property from self-defeating and the only one of the two the repair changed.

One more asymmetry: the kuhn rake is invisible on the MARGIN basis, `T = +10.75`
flat at every k in both versions, because both seats share a split pot equally
so it cancels out of "own minus the mean of the others". Only the score and
group curves moved. `gen_icebound`'s regime is likewise basis-dependent —
`self-limiting` on score, `dominant` on margin — so it should never be quoted
without naming the basis.

## Gates

| suite | result |
|---|---|
| `test_generated.py` | ALL PASS. `gen_icebound` PAYS `margin: hole +17.50, nohole +0.00 (buys +17.50)` |
| `test_textarena.py` | ALL PASS. `ta_kuhn` PAYS `margin: hole +10.80, nohole +0.60 (buys +10.20)` |
| `test_referee_games.py` | ALL PASS |
| `test_holecross.py` | ALL PASS |
| `test_native9.py` | 8/9 — `nat_gate_fire` NON-DEGENERATE, the pre-existing failure `ENGINES.md` records |
| `variant_audit.py` | four axes, 62/66 on the menu, zero `repair` rows |
| `payoff_audit.py` | 29/29 cells pay when the hole is taken |
| `fidelity.py --check` (v2) | clean, 38 cells identical |

No gate anywhere hard-codes an expected score, so this was a re-run rather than
a re-baseline.

## Shipping the repairs is what let the `repair` axis go

`AXES` is now `("baseline", "rivalry", "level", "holetype")`. The axis was never
a statement about WHAT a variant turns — the other four are, and a repair is a
statement about WHY — so it did not compose with them, and it was applied
inconsistently. Shipping the two repairs it held emptied it:

- `gen_icebound@steal-5` became identical to the baseline. Deleted.
- `ta_kuhn@split-rake-1` likewise. Deleted.
- `gen_icebound@steal-5-hard-fail` set `STEAL_PTS=5.0` *and* `RAID_FAIL=-6.0`.
  With the first now default it reduces to a single slope change, so it is a
  clean `rivalry` / `REGIME` variant carrying only `RAID_FAIL=-6.0` — which also
  resolves the mixed-axis problem that was the one real argument for keeping
  `repair`. Score reads `T = +10, -10, -30`: exactly one crew is tempted where
  the shipped cell supports two.

Its label and cell name are deliberately unchanged. `cell_name()` derives the id
from the label, so `gen_icebound__steal_5_hard_fail` is the name on the trace
files and in `make_pilot_figs.ARMS`. And because v1-plus-both-knobs and
v2-plus-one-knob are the same game, **that arm's recorded rows survived the
repair unchanged** — only the baseline arm's data was superseded.

Four render sites lost the axis: the `variant_audit` legend row, the
`<dt>axis</dt>` block in `viz/static/variants.html`, `AXIS_SLOT` in
`make_pilot_figs.py`, and the `.repair` swatch plus legend line in
`make_variant_figs.py`.

## Two corrections that came out of the audit

**The `SIZE` block was retired in the same session** (a separate decision, not
part of the repair): all 21 `level`/`SIZE` variants are gone from the catalogue,
including `gen_quiet_sonar@hit-8`. That broke `make_variant_figs.py`, which
registered `@hit-8` by vid and raised `KeyError`, and it orphaned the prize-size
half of the "punishment moved behaviour where prize size did not" finding. The
measurement stands as a past result; there is no live arm to re-run it from.
`SIZE` and `WHO` are both empty intents now — `WHO` because the two `repair`
variants that carried it shipped — and both are left in the vocabulary rather
than deleted, because rows in `results/0902_variants/` still carry them.

**A pre-existing claim about the hard-fail arm was simply false.** It was written
up as putting "every chain at or below the baseline's lowest chain". The
baseline's lowest chain is 0.444 and the arm's highest is 0.533, so three of the
four qualify and the fourth sits exactly on the baseline's SECOND-lowest. The
discrepancy was visible all along in the figure that illustrates it:
`make_variant_figs` rings `v <= base_lo` and has always drawn three rings, not
four. The means (0.650 → 0.275, a -0.375 move, still the largest behavioural
effect on the roster) are unaffected. Corrected in `variants.py`,
`make_variant_figs.py`, `docs/hackable-games.md` and
`results/0902_pilots/SUPERSEDED.md`.

Also worth flagging for whoever re-runs it: the 0.650 → 0.275 gap is a v1
pairing that spans TWO knob moves, since the v1 baseline was
`STEAL_PTS=3.0, RAID_FAIL=-1.0` against the arm's `5.0, -6.0`. Against the v2
baseline it becomes the clean single-knob contrast it was always described as,
which makes re-running it a better experiment rather than merely a refresh.

## Regenerated versus superseded

Regenerated, all offline and scripted with no API cost: `exploit_curve.py` on
both bases, `payoff_audit.py`, `payoff_regimes.py`, `variant_audit.py`
(rewriting `catalogue.json` and `CATALOGUE.md`), `build_bundle.py`,
`make_variant_figs.py`, and `results/engine_v2_baseline.json` as the new
fidelity reference. `engine_v1_baseline.json` is kept alongside it, so v1's
scripted scores, violation counts and prompt hashes are recoverable without the
old code.

Marked superseded rather than re-run, because these are live-model waves: a
`SUPERSEDED.md` in each of the eight `results/referee_spartan/` wave directories
(`merged`, `small_matched`, `ta_baseline1`, `frontier_pilot`, `single_perseat5`,
`ma_rivalry_shared`, `ma_rivalry_perseat`, `shard7/baseline1`), plus
`results/contagion/cg1/` and `results/0902_pilots/`. 1,528 affected rows in
total, all baseline-arm; none carries an `engine_version` column, which is
itself the proof they are all pre-repair. Two things surfaced while writing
them: `merged/` and `shard7/baseline1/` hold the SAME 48 icebound episodes, so
they must not be pooled; and `contagion/cg1/`'s derived analyses are adoption
rates rather than points, so no number in them is arithmetically invalidated —
but the word being mimicked is literally "raid", the act whose price changed, so
the +0.200 exposure delta reads as a lower bound rather than a v2 measurement.

## Acceptance

`T(0) > 0` in both bases on both cells with the anti-rival slope preserved;
`fidelity --check` flags exactly two cells and 36 identical; PAYS green on both
with no re-baselining; `variant_audit` reports four axes and no `repair` rows.
All met.
