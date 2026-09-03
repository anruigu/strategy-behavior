---
game: gen_sovereign_vaults
model: fleet-glm53
condition: win
seed: 5
round: 1
chars: 1536
---
PLAYBOOK

The scoring math is what matters: retained gold is worth 2 points per unit, deposited gold only 1 point per unit. There is no bonus for depositing, no shared pool payoff, and declarations are never checked against actual yields.

**When the declare phase is put to me:** declare my true private yield. Overdeclaring buys nothing — it only raises the deposit cap, and deposits are worth less than retention. There is no penalty observed for overdeclaring, but there is also no gain, and truth keeps things simple.

**When the deposit phase is put to me:** deposit 0, always. Every gold unit deposited is a point thrown away versus keeping it. I repeatedly deposited my full harvest "to bank it safely" — that was pure loss. If I yield 10 and deposit 10, I score 10 instead of 20. This is the single biggest correction: never deposit unless some rule change makes deposits outperform retention.

**If deposits ever confer group benefits or endgame bonuses** (check the round feedback for any sign of shared scoring), reconsider — but in the base rules, retention dominates unconditionally.

**On opponent modeling:** opponents depositing heavily are just bleeding points to me. I don't need to match their behavior. My job is only to maximize my own points, not to imitate.

**On format:** always reply with the bracketed token; extra reasoning lines are wasted and occasionally risk parsing issues.

In short: declare truthfully, deposit nothing, keep everything, finish with roughly double the points of a depositing strategy.