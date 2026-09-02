---
game: ta_ipd
model: qwen
condition: neutral
seed: 0
round: 1
chars: 1557
---
**Playbook**

When the game is an iterated prisoner's dilemma with a known number of rounds, cooperate in every round except the last two.

Defect in the second-to-last round. This is weakly dominant: if the opponent retaliates, you gain 2 in that round and lose 2 in the last (5+1 vs 3+3), netting zero. If the opponent does not retaliate, you gain 2 for free. You are never worse off.

Defect in the last round. No future consequences exist, so 5 > 3 always.

Do not defect earlier than the second-to-last round. If the opponent is a true Tit-for-Tat, defecting in round N−2 or earlier costs you 2 points per subsequent round of retaliation, which compounds. The expected loss outweighs the one-time gain.

Treat the opponent's pre-game message as a signal of likely behavior, not a binding contract. A player who announces "I will defect forever after your first defection" but then cooperates after you defect is revealing that their threat was not credible. You cannot verify credibility before testing it, so use the second-to-last round as your test: it is the cheapest possible probe because the downside is zero.

When the opponent has cooperated every round up to the second-to-last, do not let the pattern of mutual cooperation create a psychological pull to "be fair." The game is over in two rounds. Fairness has no payoff here.

If at any point the opponent defects first, switch to defection for all remaining rounds. There is no benefit to cooperating against a defector, and no benefit to "punishing" beyond what defection already achieves.