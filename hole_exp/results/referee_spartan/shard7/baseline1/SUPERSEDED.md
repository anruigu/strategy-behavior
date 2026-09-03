# SUPERSEDED IN PART -- engine v2 repair, 2026-09-03

One of the three cells in this shard was REPAIRED IN PLACE on 2026-09-03:
`gen_icebound`, `STEAL_PTS` 3.0 -> 5.0, `ENGINE_VERSION` 1 -> 2. The cell kept
its name and these rows predate the `engine_version` column, so nothing in a row
says which engine produced it. The wave ran against a live model; it is marked
rather than regenerated.

## What the repair changed

At `STEAL_PTS = 3.0` a raid transferred exactly what a scout is paid
(`SCOUT_PTS = 3.0`), so a lone raid was worth 0.00 in absolute score and the
cell measured `no-temptation` -- which is why the atlas PAYS gate had to price
this one cell in MARGIN rather than score. At 5.0 the score-basis temptation is
`T(0) = +10.00, T(1) = +2.50, T(2) = -5.00`, flipping at k=2, regime
`self-limiting`; the group curve runs `G(0) = 54.00 -> G(all) = -6.00`, which it
did before the repair too. `RAID_FAIL` was deliberately left at -1.0, so the
rivalry slope is unchanged.

## What is affected here

`rows.jsonl` -- 144 rows, three cells at 48 rows each (`gen_icebound`,
`gen_sovereign_vaults`, `ref_orderbook`), all `model=qwen3.8-27b`,
`condition=neutral`, `visibility=own`, `arm=hole`, `focal=0`, seeds 0/1/2.

* **`gen_icebound`: 48 rows, superseded.** Baseline arm -- the `arm` column is
  the hole/no-hole arm, not a variant arm, and no variant cells appear in this
  file. `gain_focal` is `null` on all 48, so `score_focal` is the whole payoff
  record and `score_focal` moves under the repair.
* `playbooks/` holds 12 `gen_icebound-*` files, written against the v1 rules
  text: "A raid transfers 3 POINTS from a scouting target, but costs the raider
  1 POINT", where v2 renders 5. There is no `traces/` directory in this shard.
* **`ta_kuhn` does not appear in this shard at all**, so the other half of the
  2026-09-03 repair (`SPLIT_RAKE` 0.0 -> 1.0) is irrelevant here.

## THESE ROWS ARE ALSO IN merged/

This shard's 48 `gen_icebound` rows are the same 48 episodes that appear in
`../../merged/rows.jsonl`, which is the shard concatenation -- they agree on
`seed`, `round`, `episode`, `episode_seed`, `model`, `focal` and `score_focal`
for all 48. `../../merged/SUPERSEDED.md` marks the same data. One wave recorded
once; do not pool the two files or you will double-count it.

## What is still good

* `gen_sovereign_vaults` and `ref_orderbook` -- 96 of the 144 rows -- were not
  touched on 2026-09-03 and need no caveat.
* `gen_icebound`'s violation and rate columns (`v_pledge_act_mismatch`, `o_*`,
  `r_*`, `invalid_rate_focal`, `decisions_focal`) count referee violations
  rather than points, so they are structurally intact. They were elicited under
  the v1 rules text, i.e. against a stated raid transfer of 3 rather than 5, so
  read them as behaviour under the weaker incentive.
* `usage.json` is a cost record and is unaffected.

## Record

Full account: `research_logs/0903-repair-in-place.md` (repo root;
`../../../../../research_logs/0903-repair-in-place.md` from here). Rows emitted
from 2026-09-03 on carry an `engine_version` column, added to the `Episode`
dataclass and stamped in `referee_spartan._row()`. No row here has it, which is
how you can tell the shard is entirely pre-repair.

`../../../engine_v1_baseline.json` preserves the v1 engine's SCRIPTED behaviour
for 38 cells including `gen_icebound` -- per-seat scores, violation and
opportunity counts and a prompt hash per seed -- so what v1 actually did is
recoverable without the old code.
