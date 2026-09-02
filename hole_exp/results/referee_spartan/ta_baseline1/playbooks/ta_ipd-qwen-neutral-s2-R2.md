---
game: ta_ipd
model: qwen
condition: neutral
seed: 2
round: 2
chars: 869
---
When the opponent announces Grim Trigger (cooperate until provoked, then defect forever) and the game has n rounds, cooperate in rounds 1 through n−1 and defect in round n. For n = 8 this yields 7×3 + 5 = 26.

In the final round, always defect regardless of the running score or whether the opponent has already been provoked. There is no next round in which a punishment can bite, and defecting against a cooperator pays 5 versus 3 for cooperating — a strict +2.

Do not let "maintain the pattern" or "risk unraveling" reasoning override the final-round incentive. With Grim Trigger the opponent cooperates unless already triggered, so the final-round defection is pure gain with no risk.

If the opponent has already been triggered and is defecting, defect in every remaining round (mutual defection at 1/1 is still better than cooperating into their defection at 0).