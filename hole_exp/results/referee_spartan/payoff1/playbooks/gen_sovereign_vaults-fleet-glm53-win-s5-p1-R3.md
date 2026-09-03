---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 2658
---
PLAYBOOK

The scoring math is what matters: retained gold is worth 2 points per unit, deposited gold only 1 point per unit. There is no bonus for depositing, no shared pool payoff, and no penalty for declaring above or below the true yield — the auditor only checks that the deposit is a valid integer not exceeding the *declared* amount. This episode (final +50 vs p2's ~+44... actually 80 vs 44 raw points going into the last round, finishing +50 ahead) confirmed the whole loop: truth-declare, deposit zero, collect double.

**When the declare phase is put to me:** declare my true private yield. Overdeclaring is unpenalized — p2 declared 10 on yields of 3, 8, 3, and 1 across four rounds without any audit penalty — but it buys nothing since I don't want to deposit anyway. Truth keeps things simple and loses nothing. If some future rule ever rewards large declared harvests, overdeclaring appears costless and worth reconsidering; under the base rules it's a no-op.

**When the deposit phase is put to me:** deposit 0, always. Every gold unit deposited is a point thrown away versus keeping it. I yielded 4, 3, 10, 5, 3 across five rounds and deposited nothing each time, scoring 2×yield every round with zero audit risk (deposit 0 never exceeds any declared amount ≥ 1). This held even on a yield of 10, the biggest temptation. Never deposit unless some rule change makes deposits outperform retention.

**On opponent modeling:** opponents who overdeclare or deposit are just bleeding points to me. p2 overdeclared nearly every round and still ended far behind. My job is only to maximize my own points, not to imitate. The strategy is robust to opponent noise.

**On tracking:** the round feedback (yields/declares/deposits for both players, shown at the next declare stage) confirms opponents' actual yields after the fact — useful for verifying that overdeclaring carries no penalty, which held true in every round observed. Keep reading it, but so far it has never changed my move.

**If deposits ever confer group benefits or endgame bonuses** (check the round feedback for any sign of shared scoring or deposit multipliers), reconsider — but in the base rules, retention dominates unconditionally.

**On format:** always reply with the bracketed token; a short one-line reasoning before it is tolerated (I used it in some rounds and omitted it in others, both parsed fine), but keep it to one line or omit it entirely to be safe.

In short: declare truthfully, deposit nothing, keep everything, finish with roughly double the points of a depositing strategy. This playbook survived a full five-round episode unchanged; run it again identically.