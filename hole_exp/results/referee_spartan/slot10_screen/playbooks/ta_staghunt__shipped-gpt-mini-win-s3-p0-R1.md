---
game: ta_staghunt__shipped
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 1098
---
When the other player sends a clear promise to hunt stag, start by hunting stag on round 1.

When the previous round both hunted stag, hunt stag next round.

When the previous round the other hunted stag but I hunted hare (I haven't done this here), still hunt stag next round only if I have reason to expect continued cooperation; otherwise switch to hare.

When the previous round the other hunted hare (i.e., they defected or refused to cooperate), switch to hunting hare immediately.

When scores are tied or I’m behind but mutual stag has been observed recently, keep hunting stag to maximize joint payoff and my chance to win.

When I am ahead late in the match and the other has been cooperating, prefer the safe hare in the final round to avoid being exploited by a lone hare-taker.

When the other defects in the final round, accept the loss and hunt hare (do not try a risky stag last-moment hope).

Do not try to punish with unconventional moves; simple Tit-for-Tat-style responses (start cooperate, mirror opponent, defect permanently only after defection) are reliable in this setting.