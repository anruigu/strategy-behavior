# SUPERSEDED IN PART -- engine v2 repair, 2026-09-03

Both cells repaired in place on 2026-09-03 are in this wave: 160 of 720 rows.
The cells kept their names and these rows predate the `engine_version` column,
so nothing in a row says which engine produced it. The wave ran against a live
model; it is marked rather than regenerated.

## What the repair changed

**`gen_icebound` -- `STEAL_PTS` 3.0 -> 5.0, `ENGINE_VERSION` 1 -> 2.** At 3.0 it
equalled `SCOUT_PTS`, so a raid transferred exactly what scouting pays: a lone
raid was worth 0.00 in absolute score and the cell read `no-temptation`. At 5.0
the score basis is `T(0) = +10.00, T(1) = +2.50, T(2) = -5.00`, flipping at k=2,
regime `self-limiting`; the group curve runs `G(0) = 54.00 -> G(all) = -6.00`.

**`ta_kuhn` -- `SPLIT_RAKE` 0.0 -> 1.0, `ENGINE_VERSION` 1 -> 2.** At 0.0 the
cell was exactly zero-sum: both seats declare KING, every pot splits, and mutual
exploitation cancelled to the last decimal at `+0.00` with no group payoff to
drop. At 1.0 the group total falls `G(0) = 0.00 -> G(all) = -8.00` and score
basis reads `T(0) = +4.06`. The rake fires only on SPLIT pots.

## Read the RIVALRY framing carefully -- it cuts both ways here

This is a rivalry wave, and the two repairs sit differently against it.

* **`gen_icebound`: the slope you are measuring was NOT changed.** `RAID_FAIL`
  is still -1.0, so a raid into a raid still costs the raider and the cell is
  still the anti-rivalry case `seat_denominators.STRATUM` names it for. The
  repair moved the INTERCEPT -- what a lone raid is worth -- not the penalty for
  colliding. The rivalry structure these rows were run to measure survives the
  repair; the absolute payoff numbers do not.
* **`ta_kuhn`: the repair is exactly a group-level change.** The rake destroys
  value on split pots rather than redistributing it, so the group total moved
  from flat 0.00 to -8.00 at all-exploit. A rivalry reading taken here on the
  v1 engine had no group payoff to drop at all.

## What is affected here

`rows.jsonl` -- 720 rows, 9 cells at 80 rows each, all `model=gemini-flash`,
`condition=neutral`, `visibility=own`, `arm=hole`, `focal=0`, seeds 0-4.

* **`gen_icebound`: 80 rows, superseded.** Baseline arm -- the `arm` column is
  the hole/no-hole arm, not a variant arm, and no variant cells appear in this
  file. `gain_focal` is `null` on all 80, so `score_focal` is the whole payoff
  record; it clusters at 18.0 (20 rows) and 17.0 (17 rows), and the pile-up at
  the honest ceiling of 18.0 is the v1 artefact itself -- at
  `STEAL_PTS = 3.0` a crew that raided scored what a crew that scouted scored.
* **`ta_kuhn`: 80 rows, superseded on the recorded bases.** `gain_focal` is 0.0
  on all 80 -- that flat zero IS the exactly-zero-sum signature of
  `SPLIT_RAKE = 0.0`, not a finding that the hole does not pay. `score_focal`
  spreads over 0.0/2.0/4.0/-2.0/-4.0 and moves wherever the episode produced
  split pots, which is the hole's own mechanism.
* `playbooks/` holds 20 files for each of the two cells and `traces/` holds 80
  episode JSONs for each. All carry the v1 rules text -- icebound "A raid
  transfers 3 POINTS" where v2 renders 5, and kuhn ending the pot rule at "equal
  declarations split it." with no house-rake sentence, that clause being emitted
  only when `SPLIT_RAKE > 0`.

## What is still good

* `ref_orderbook`, `ref_invoice`, `ref_commons`, `ref_auction`,
  `gen_seven_seal`, `gen_harbor_customs` and `gen_frontline_depot` -- 560 of the
  720 rows -- were not touched on 2026-09-03.
* Violation and rate columns on the two affected cells count referee violations
  rather than points and are structurally intact; the caveat is that they were
  elicited under v1 rules text.
* `ta_kuhn` MARGIN numbers are comparable across the repair (`T = +10.75` flat
  at every k, before and after, because both seats share a split pot equally and
  the rake cancels out of "own minus the mean of the others"). That rescues the
  payoff-regime tables and not these rows, which record `score_focal` and
  `gain_focal` and carry no opponent scores.
* `usage.json` is a cost record and is unaffected.

## Record

Full account: `research_logs/0903-repair-in-place.md` (repo root;
`../../../../research_logs/0903-repair-in-place.md` from here). Rows emitted
from 2026-09-03 on carry an `engine_version` column, added to the `Episode`
dataclass and stamped in `referee_spartan._row()`. No row here has it, which is
how you can tell the file is entirely pre-repair.

`../../engine_v1_baseline.json` preserves the v1 engine's SCRIPTED behaviour for
38 cells including both repaired ones -- per-seat scores, violation and
opportunity counts and a prompt hash per seed -- so what v1 actually paid at the
all-exploit corner is recoverable without the old code (`gen_icebound` -2.0 per
seat, `ta_kuhn` 0.0 per seat).
