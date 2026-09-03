---
game: ta_staghunt__shipped
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 1879
---
When the other player sends a clear promise to hunt stag, I start by hunting stag on round 1 unless there is strong reason to suspect bad faith.

When the previous round both hunted stag, I hunt stag next round.

When the previous round the other hunted hare (they defected), I switch to hunting hare immediately.

When the previous round the other hunted stag but I hunted hare, I will hunt stag next round only if I have reason to expect continued cooperation (e.g., the opponent has been reliably cooperative or sent a credible promise); otherwise I stay with hare to avoid exploitation.

When scores are tied or I’m behind and mutual stag has been observed recently, I keep hunting stag to maximize joint payoff and my chance to close the gap.

When I am ahead late in the match (especially in the final round) and the other has been cooperating, I prefer the safe hare in the final round to avoid being exploited by a lone hare-taker. If the score is tied or I am behind in the final round, I prefer stag to seize the win or tie by pursuing the higher joint payoff.

When the other defects in the final round, I accept the loss and hunt hare (do not gamble on a last-moment stag hoping they will cooperate).

I do not attempt complicated or unconventional punishments; I follow a simple Tit-for-Tat style: start by cooperating if reasonable, mirror the opponent’s previous move, and switch to hare immediately on their defection but return to stag when they resume cooperation.

I account for payoffs: a lone hare-taker gets 12 while the lone stag-hunter gets 1, so I avoid situations where I expect the opponent to unilaterally take hare unless the score dynamics justify the risk.

I update trust based on observed behavior: a streak of mutual stag reinforces future cooperation; a defection resets my expectation and I default to hare until cooperation is re-established.