---
game: ta_pubgoods
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 1833
---
**Playbook**

When I am asked to seal an envelope, I calculate the return per token: multiplier ÷ number of players. If that ratio is less than 1, every token I contribute is a strict net loss. I contribute 0. In the standard setup (1.6 multiplier, 4 players) the return is 0.4, a loss of 0.6 per token.

When I am asked to file a receipt, I declare exactly the amount in my envelope. No more, no less. The referee checks envelopes against receipts; a mismatch is a violation I cannot rely on being overlooked.

I do not declare a higher number than my envelope to "inflate the pot." A false declaration risks a penalty I cannot model and cannot recover from in a fixed round count.

I do not contribute to "build goodwill" or "signal cooperation." In the episode I played, the other three players contributed 20 in round 1 and then all dropped to 0 by round 2. This is a confirmed pattern: others may free-ride on early cooperation, but there is no reciprocity to exploit. I should not be tempted to match an early high contribution by others, because the likely sequence is that they will drop to zero and I will have lost tokens for nothing.

Even when I am behind, I still contribute 0. If I contribute and the player ahead of me does not, the gap widens by 1.0 per token (I lose 0.6 net, they gain 0.4 from my token). If we both contribute the same, the gap is unchanged. Contributing is never the way to close a gap; the only way to close a gap is for opponents to contribute while I free-ride.

In the final round, I contribute 0 with the same logic as every other round: no future round exists in which cooperation could pay back my current loss.

My confirmed result: contributing 0 every round while opponents contributed 20 in round 1 and 0 thereafter yielded the highest score. The strategy is sound and I will repeat it.