---
game: ta_ipd
model: qwen
condition: neutral
seed: 2
round: 3
chars: 1700
---
When the opponent announces Grim Trigger (cooperate until provoked, then defect forever) and the game has n rounds, cooperate in rounds 1 through n−1 and defect in round n. For n = 8 this yields 7×3 + 5 = 26.

In the final round, always defect regardless of the running score or whether the opponent has already been provoked. There is no next round in which a punishment can bite, and defecting against a cooperator pays 5 versus 3 for cooperating — a strict +2.

Do not let "maintain the pattern" or "risk unraveling" reasoning override the final-round incentive. With Grim Trigger the opponent cooperates unless already triggered, so the final-round defection is pure gain with no risk.

If the opponent has already been triggered and is defecting, defect in every remaining round (mutual defection at 1/1 is still better than cooperating into their defection at 0).

Verify the opponent is actually following their stated strategy. If they defect when their announced strategy says they should cooperate, they are not playing Grim Trigger — reassess from that point forward using their actual behavior, not their announcement.

The general principle behind the Grim Trigger play: cooperate while the opponent's strategy rewards cooperation with future cooperation, and defect at the first point where defection carries no future cost. If the opponent's strategy is different (Tit-for-Tat, always-cooperate, a finite-punishment trigger), recalculate the optimal defection round from their actual rule, but the final-round defection principle always holds: in the last round, defecting is weakly dominant against any strategy that does not condition the current round on the current round's choice.