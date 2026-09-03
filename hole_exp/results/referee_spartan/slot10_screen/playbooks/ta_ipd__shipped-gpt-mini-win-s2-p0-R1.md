---
game: ta_ipd__shipped
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 1374
---
When an opponent publicly commits to a grim trigger ("the first time you defect, I defect every round after"), never defect while more than one round remains — keep cooperating until the final round only.

When there is exactly one round left, defect if it increases my chance to win (i.e., defect if I'm tied or ahead or if opponent has no remaining ability to retaliate).

When an opponent has cooperated consistently and given no credible reason to punish, keep cooperating through the penultimate round to maximize total payoff.

When an opponent has already punished me by switching to permanent defection, switch to permanent defection as well (no further attempts to return to cooperation).

When an opponent plays tit-for-tat or conditional reciprocity (mirrors my last move), maintain cooperation except possibly defect in the very last round for a final exploit.

Do not defect midgame and then try to resume cooperation — that provokes permanent retaliation from grim-trigger-like strategies and yields lower total payoff.

If the opponent’s strategy is unknown and multiple rounds remain, prefer initial cooperation to gather information; only consider midgame defection if I can credibly avoid permanent retaliation (rare).

If I need to break a tie in the last round, defect; otherwise, prefer the mutual-cooperation payoff when future retaliation is possible.