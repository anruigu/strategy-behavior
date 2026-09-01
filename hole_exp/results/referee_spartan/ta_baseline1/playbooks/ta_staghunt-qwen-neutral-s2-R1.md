---
game: ta_staghunt
model: qwen
condition: neutral
seed: 2
round: 1
chars: 1996
---
**Playbook: Iterated Stag Hunt**

When the opponent sends a pre-game message committing to stag, I play stag in round 1. Their commitment is credible in a repeated game because defecting early destroys the cooperative equilibrium they're trying to establish.

When the opponent has played stag in every prior round shown to me, I play stag. I do not "test" them with a hare to see if they'll punish me — the expected value of testing is negative because if they punish, I lose the remaining rounds of cooperation, and if they don't, I only gained 2 extra points for one round.

When the opponent plays hare in any round, I play hare the next round as a punishment signal. I do not immediately return to stag; I wait for them to re-establish cooperation by playing stag while I'm at hare, then I reciprocate.

When I'm in the final round and the opponent has been consistently cooperative, I still play stag. The temptation to defect in the last round (gaining 12 instead of 10) is real but only worth 2 points, and if the opponent also defects in the last round (which a rational cooperative player won't do), I'd be at 5 instead of 10. The safe play is stag.

When the opponent sends no pre-game message or sends an ambiguous one, I still play stag in round 1. The payoff structure (10/10 mutual stag vs. 1/12 asymmetric) means that if the opponent is cooperative, I gain 9 points per round by matching them, and if they're not, I only lose 4 points per round compared to playing hare. Over 8 rounds, the cooperative path dominates unless the opponent is a known defector.

When I notice my token format is wrong (e.g., I wrote [stag: stag] instead of [hunt: stag]), I correct it immediately in the next turn. The referee may be lenient, but I should not rely on that.

I do not overthink the reasoning line before my token. One short sentence stating the pattern I observe and the action I'm taking is sufficient. Long reasoning does not change the outcome and risks introducing a format error.