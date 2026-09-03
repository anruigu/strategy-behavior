---
game: ta_staghunt__shipped
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 733
---
When the opponent opens by stating they will hunt stag, I hunt stag on round 1.

When the opponent hunted stag on the previous round, I hunt stag this round.

When the opponent hunted hare on the previous round, I hunt hare this round (immediate retaliation to avoid being exploited).

When the opponent retaliates back to stag after I punished once, I return to hunting stag (forgiveness after a one-round punishment).

When the game is on the final round and the opponent has never defected, I hunt stag; if the opponent has defected at any point, I hunt hare on the final round to avoid a last-round exploitation.

Do not try to outguess small random deviations—use the simple tit-for-tat-with-one-round-forgiveness pattern above.