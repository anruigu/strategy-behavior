# SUPERSEDED IN PART -- engine v2 repair, 2026-09-03

`gen_icebound` was REPAIRED IN PLACE on 2026-09-03: `STEAL_PTS` 3.0 -> 5.0,
`ENGINE_VERSION` 1 -> 2. The cell kept its name, so the 48 `gen_icebound` rows
in `rows.jsonl` carry no marker of which engine produced them. Nothing in this
directory was regenerated -- the wave ran against live models and re-running it
costs real money, so it is marked instead.

## What the repair changed

At `STEAL_PTS = 3.0` a raid transferred exactly what a scout is paid
(`SCOUT_PTS = 3.0`), so a lone raid was worth **0.00 in absolute score** and the
cell measured `no-temptation` -- which is why the atlas PAYS gate had to price
this one cell in MARGIN rather than score. At 5.0 the score-basis temptation is
`T(0) = +10.00, T(1) = +2.50, T(2) = -5.00`, flipping at k=2, regime
`self-limiting`. The group curve runs `G(0) = 54.00 -> G(all) = -6.00`; it ran
that way before the repair too. The SLOPE was deliberately not touched --
`RAID_FAIL` is still -1.0, so a raid into a raid still costs the raider.

## What is affected here

`rows.jsonl` -- 864 rows, 18 cells at 48 rows each, all `model=qwen3.8-27b`,
`condition=neutral`, `visibility=own`, `arm=hole`, `focal=0`, seeds 0/1/2.

* **`gen_icebound`: 48 rows, superseded.** These are baseline-arm rows (plain
  `gen_icebound`; the `arm` column here is the hole/no-hole arm, not a variant
  arm, and no variant cells appear in this file). Every one carries
  `gain_focal: null` -- the cell has no within-episode counterfactual and was
  priced in margin -- so what these rows record on the payoff side is
  `score_focal` alone, and `score_focal` moves under the repair.
* The clustering of `score_focal` at 18.0 in these rows is itself the v1
  artefact: 18.0 is the honest ceiling, and at `STEAL_PTS = 3.0` a crew that
  raided scored the same as a crew that scouted. Do not read "score 18.0
  regardless of exploit rate" as a finding about the model; at 5.0 the raid
  shows up in the score.
* **`ta_kuhn` does not appear in this file at all**, so the second half of the
  2026-09-03 repair (`SPLIT_RAKE` 0.0 -> 1.0) is irrelevant here.

## THESE ARE THE SHARD7 ROWS

This file is the shard concatenation, and its 48 `gen_icebound` rows are the
same 48 episodes as `../shard7/baseline1/rows.jsonl` -- they agree on `seed`,
`round`, `episode`, `episode_seed`, `model`, `focal` and `score_focal` for all
48. `../shard7/baseline1/SUPERSEDED.md` marks the same data; it is one wave
recorded once, not two independent readings, and pooling the two files would
double-count it.

## What is still good

* The other 17 cells (`ref_*`, `gen_quiet_sonar`, `gen_seven_seal`,
  `gen_sovereign_vaults`, `gen_vault_duel`, `gen_harbor_customs`,
  `gen_frontline_depot`, `gen_antiquities`) were not touched on 2026-09-03 and
  need no caveat.
* For `gen_icebound`, the violation and rate columns (`v_*`, `o_*`, `r_*`,
  `invalid_rate_focal`, `decisions_focal`) count referee violations rather than
  points, so they are structurally intact. They were, however, elicited under
  the v1 rules text, which told the model "A raid transfers 3 POINTS" where v2
  says 5. The measured behaviour is a response to the weaker incentive.

## Record

Full account: `research_logs/0903-repair-in-place.md` (repo root;
`../../../../research_logs/0903-repair-in-place.md` from here). Rows emitted
from 2026-09-03 on carry an `engine_version` column -- added to the `Episode`
dataclass and stamped in `referee_spartan._row()` -- so a re-run will not
silently pool with this file. No row in this file has that column, which is how
you can tell it is entirely pre-repair.

`../../engine_v1_baseline.json` preserves the v1 engine's SCRIPTED behaviour for
38 cells including `gen_icebound` -- per-seat scores, violation and opportunity
counts and a prompt hash per seed -- so what v1 actually did is recoverable
without the old code. Its `gen_icebound` all-exploit corner reads -2.0 for every
seat, which is the -2.0 that also appears in this file's `score_focal`.
