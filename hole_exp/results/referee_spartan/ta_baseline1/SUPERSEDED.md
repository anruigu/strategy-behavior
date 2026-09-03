# SUPERSEDED IN PART -- engine v2 repair, 2026-09-03

One cell of the ten in this wave was REPAIRED IN PLACE on 2026-09-03:
`ta_kuhn`, `SPLIT_RAKE` 0.0 -> 1.0, `ENGINE_VERSION` 1 -> 2. The cell kept its
name and these rows predate the `engine_version` column, so nothing in a row
says which engine produced it. The wave ran against a live model; it is marked
rather than regenerated.

## What the repair changed

At `SPLIT_RAKE = 0.0` the cell was exactly zero-sum: both seats declare KING,
every pot splits, and mutual exploitation cancelled to the last decimal at
`+0.00` with no group payoff to drop. At 1.0 the house takes the rake off every
split pot, so the cancellation is gone -- the group total falls
`G(0) = 0.00 -> G(all) = -8.00` and score basis reads `T(0) = +4.06`. The rake
fires ONLY on split pots, which is the outcome mutual false shows produce, so an
honest showdown is untouched.

## What is affected here

`rows.jsonl` -- 480 rows, ten `ta_*` cells at 48 rows each, all `model=qwen`,
`condition=neutral`, `visibility=own`, `arm=hole`, `focal=0`, seeds 0/1/2.

* **`ta_kuhn`: 48 rows, superseded on the recorded bases.** `gain_focal` is 0.0
  on all 48 -- that flat zero IS the exactly-zero-sum signature of
  `SPLIT_RAKE = 0.0`, not a finding that the hole does not pay. `score_focal`
  also moves wherever the episode produced split pots, which is the hole's own
  mechanism (both seats declaring KING); `headline` is `false_show` on all 48.
* `playbooks/` holds 12 `ta_kuhn-*` files. There is no `traces/` directory here,
  so the full v1 rules text is not archived in this wave, but the playbooks were
  written against a rules string that ended the pot rule at "equal declarations
  split it." with no house-rake sentence -- that clause is emitted only when
  `SPLIT_RAKE > 0`.
* **`gen_icebound` does not appear in this file at all** -- this is a
  TextArena-only baseline -- so the other half of the 2026-09-03 repair
  (`STEAL_PTS` 3.0 -> 5.0) is irrelevant here.

## What is still good

* The other nine cells -- `ta_winasmuch`, `ta_staghunt`, `ta_pubgoods`,
  `ta_negotiation`, `ta_liarsdice`, `ta_letterauction`, `ta_ipd3`, `ta_ipd`,
  `ta_blindauction`, 432 of the 480 rows -- were not touched on 2026-09-03 and
  need no caveat. In particular `ta_liarsdice` is untouched and is still exactly
  zero-sum under all-exploit; it took over from `ta_kuhn` as the roster's
  standing example of that failure, and its `rake 1` variant is a separate
  variant arm, not an in-place change to the shipped cell.
* `ta_kuhn`'s violation and rate columns (`v_false_show`, `o_*`, `r_*`,
  `invalid_rate_focal`, `decisions_focal`) count referee violations rather than
  points, so they are structurally intact; the caveat is only that they were
  elicited under v1 rules text with no rake sentence in the prompt.
* `ta_kuhn` MARGIN-basis numbers are comparable across the repair --
  `T = +10.75` flat at every k in both versions, because both seats share a
  split pot equally and the rake cancels out of "own minus the mean of the
  others". That rescues the payoff-regime tables, not these rows: these rows
  record `score_focal` and `gain_focal`, which is what moved, and carry no
  opponent scores, so margin cannot be recovered from them.
* `usage.json` is a cost record and is unaffected.

## Record

Full account: `research_logs/0903-repair-in-place.md` (repo root;
`../../../../research_logs/0903-repair-in-place.md` from here). Rows emitted
from 2026-09-03 on carry an `engine_version` column, added to the `Episode`
dataclass and stamped in `referee_spartan._row()`. No row here has it, which is
how you can tell the file is entirely pre-repair.

`../../engine_v1_baseline.json` preserves the v1 engine's SCRIPTED behaviour for
38 cells including `ta_kuhn` -- per-seat scores, violation and opportunity
counts and a prompt hash per seed -- so what v1 actually did is recoverable
without the old code. Its `ta_kuhn` all-exploit corner reads 0.0 for both seats,
the exactly-zero-sum signature that the `gain_focal` column here reproduces on
all 48 rows.
