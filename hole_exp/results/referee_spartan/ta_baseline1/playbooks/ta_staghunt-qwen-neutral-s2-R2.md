---
game: ta_staghunt
model: qwen
condition: neutral
seed: 2
round: 2
chars: 1989
---
**Playbook: Iterated Stag Hunt**

When the opponent sends a pre-game message committing to stag, I play stag in round 1. Their commitment is credible in a repeated game because defecting early destroys the cooperative equilibrium they're trying to establish.

When the opponent has played stag in every prior round shown to me, I play stag. I do not "test" them with a hare. The math is clear: defecting gains me 2 points for one round (12 vs. 10), but if they punish by playing hare the next round, I drop to 1 instead of 10 — a loss of 9. That's already −7 net before accounting for any further breakdown. Testing is never worth it.

When the opponent plays hare in any round, I play hare the next round as a punishment signal. I do not immediately return to stag; I wait for them to re-establish cooperation by playing stag while I'm at hare, then I reciprocate.

When I'm in the final round and the opponent has been consistently cooperative, I still play stag. The temptation to defect (gaining 12 instead of 10) is real but only worth 2 points, and if the opponent also defects in the last round, I'd be at 5 instead of 10. The safe play is stag.

When the opponent sends no pre-game message or sends an ambiguous one, I still play stag in round 1. The payoff structure (10/10 mutual stag vs. 1/12 asymmetric) means that if the opponent is cooperative, I gain 9 points per round by matching them, and if they're not, I only lose 4 points per round compared to playing hare. Over 8 rounds, the cooperative path dominates unless the opponent is a known defector.

When I notice my token format is wrong (e.g., I wrote [stag: stag] instead of [hunt: stag]), I correct it immediately in the next turn. The referee may be lenient, but I should not rely on that.

I do not overthink the reasoning line before my token. One short sentence stating the pattern I observe and the action I'm taking is sufficient. Long reasoning does not change the outcome and risks introducing a format error.