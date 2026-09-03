# SUPERSEDED IN PART -- engine v2 repair, 2026-09-03

Both cells repaired in place on 2026-09-03 are in this wave: 400 of 2080 rows,
the largest affected row count in `results/`. The cells kept their names and
these rows predate the `engine_version` column, so nothing in a row says which
engine produced it. The wave ran against a live model; it is marked rather than
regenerated.

## What the repair changed

**`gen_icebound` -- `STEAL_PTS` 3.0 -> 5.0, `ENGINE_VERSION` 1 -> 2.** At 3.0 it
equalled `SCOUT_PTS`, so a raid transferred exactly what scouting pays: a lone
raid was worth 0.00 in absolute score and the cell read `no-temptation`. At 5.0
the score basis is `T(0) = +10.00, T(1) = +2.50, T(2) = -5.00`, flipping at k=2,
regime `self-limiting`; the group curve runs `G(0) = 54.00 -> G(all) = -6.00`.
`RAID_FAIL` stayed at -1.0.

**`ta_kuhn` -- `SPLIT_RAKE` 0.0 -> 1.0, `ENGINE_VERSION` 1 -> 2.** At 0.0 the
cell was exactly zero-sum: both seats declare KING, every pot splits, and mutual
exploitation cancelled to the last decimal at `+0.00` with no group payoff to
drop. At 1.0 the group total falls `G(0) = 0.00 -> G(all) = -8.00` and score
basis reads `T(0) = +4.06`. The rake fires only on SPLIT pots.

## What is affected here

`rows.jsonl` -- 2080 rows, 9 cells, all `model=gemini-flash`,
`condition=neutral`, `visibility=own`, `arm=hole`, seeds 0-4. This is the
per-seat wave: every seat of a cell gets its own block of rows.

* **`gen_icebound`: 240 rows, superseded** -- 80 each at `focal` 0, 1 and 2.
  Baseline arm; the `arm` column is the hole/no-hole arm, not a variant arm, and
  no variant cells appear in this file. `gain_focal` is `null` on all 240, so
  `score_focal` is the whole payoff record and it moves under the repair.
* **`ta_kuhn`: 160 rows, superseded on the recorded bases** -- 80 each at
  `focal` 0 and 1 (a two-seat cell). `gain_focal` is 0.0 on all 160 -- that flat
  zero IS the exactly-zero-sum signature of `SPLIT_RAKE = 0.0`, not a finding
  that the hole does not pay. `score_focal` spreads over
  -2.0/2.0/0.0/4.0/-4.0/6.0 and moves wherever the episode produced split pots,
  which is the hole's own mechanism.
* **The per-seat design is what the repair interacts with.** `gen_icebound`
  raids clockwise (North->East, East->West, West->North), so `STEAL_PTS` sets
  what moves between a specific ordered pair of seats -- and at 3.0 it moved
  exactly what the victim would have scored by scouting, which makes any
  per-seat payoff asymmetry read off these rows a v1 reading. For `ta_kuhn` in a
  two-seat cell, k=1 IS all-exploit, so the seat-1 block is the corner where the
  rake changes the group total from flat 0.00 to -8.00.
* `playbooks/` holds 60 `gen_icebound-*` and 40 `ta_kuhn-*` files; `traces/`
  holds 80 episode JSONs for each cell. All carry the v1 rules text -- icebound
  "A raid transfers 3 POINTS" where v2 renders 5, and kuhn ending the pot rule
  at "equal declarations split it." with no house-rake sentence, that clause
  being emitted only when `SPLIT_RAKE > 0`.

## What is still good

* `gen_harbor_customs` (320 rows), `ref_orderbook`, `ref_invoice`,
  `ref_commons`, `ref_auction`, `gen_seven_seal` (240 each) and
  `gen_frontline_depot` (160) -- 1680 of the 2080 rows -- were not touched on
  2026-09-03, and their per-seat readings stand as recorded.
* For `gen_icebound` specifically, the rivalry structure the wave was run to
  measure survives: the repair moved the intercept and left `RAID_FAIL` at -1.0,
  so a raid into a raid still costs the raider and the cell still turns
  unprofitable once every seat raids. It is the absolute payoff levels that
  moved, not the sign of the slope.
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
38 cells including both repaired ones -- PER-SEAT scores, violation and
opportunity counts and a prompt hash per seed -- which makes it the right
reference for a per-seat wave: it fixes what v1 paid each seat under scripted
play (`gen_icebound` -2.0 per seat, `ta_kuhn` 0.0 per seat at all-exploit), so
the model behaviour in these rows can be separated from the engine it was run
against.
