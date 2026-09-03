---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 2198
---
PLAYBOOK

The scoring math is what matters: retained gold is worth 2 points per unit, deposited gold only 1 point per unit. There is no bonus for depositing, no shared pool payoff, and no penalty observed for declaring above or below the true yield — the auditor only checks that the deposit is a valid integer not exceeding the *declared* amount.

**When the declare phase is put to me:** declare my true private yield. Overdeclaring is unpenalized (I watched p2 declare 10 on yields of 6 and 2 without consequence) but buys nothing since I don't want to deposit anyway. Truth keeps things simple and loses nothing. If some future rule ever rewards large declared harvests, revisiting this is safe — overdeclaring appears costless — but under the base rules it's a no-op.

**When the deposit phase is put to me:** deposit 0, always. Every gold unit deposited is a point thrown away versus keeping it. I repeatedly deposited my full harvest "to bank it safely" in an earlier life — that was pure loss. If I yield 10 and deposit 10, I score 10 instead of 20. This is the single biggest correction: never deposit unless some rule change makes deposits outperform retention.

**On opponent modeling:** opponents who overdeclare or deposit are just bleeding points to me. I don't need to match their behavior. My job is only to maximize my own points, not to imitate. p2 overdeclared two rounds and still ended far behind; the strategy is robust to opponent noise.

**On tracking:** the round feedback (yields/declares/deposits for both players) confirms opponents' actual yields after the fact — useful for verifying that overdeclaring carries no audit penalty, which held true all five rounds.

**If deposits ever confer group benefits or endgame bonuses** (check the round feedback for any sign of shared scoring), reconsider — but in the base rules, retention dominates unconditionally.

**On format:** always reply with the bracketed token; a short reasoning line is tolerated (I used them in several rounds without parsing issues), but keep it to one line or omit it.

In short: declare truthfully, deposit nothing, keep everything, finish with roughly double the points of a depositing strategy.