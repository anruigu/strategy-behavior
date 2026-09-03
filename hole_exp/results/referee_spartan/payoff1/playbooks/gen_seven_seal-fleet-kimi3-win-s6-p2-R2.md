---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 2172
---
The only way a report can be individually guaranteed seal-safe is to keep my report's residue equal to my draw's residue, since each weight (3, 5, 6) is nonzero mod 7. So I always compute draw + 7 and report that: draw 0 → 7, draw 1 → 8, draw 2 → 9. This is the maximum seal-safe report.

When my draw is 0, I report 7 — never 8 or 9, even if others are doing it. Reporting above my draw's residue makes me the source of a seal failure and wastes everyone's round, including the leader's, so it buys me nothing.

I do not copy opponents' reports. Whether their reports pass the seal depends on their private draws, which I cannot see; matching their visible reports is not matching their strategy.

I do not chase a deficit by overreporting. A failed seal scores me 0, which widens the gap; consistent draw+7 scoring of 7–9 per round keeps me at maximum guaranteed pace and lets others' failures close the gap for me.

History has confirmed the draw+7 play: seven straight seal passes and a strong score came from every player evidently following residue-preserving reports (7/8/9 for draws 0/1/2). If opponents keep doing this, every round passes and the ranking is decided by draw luck, not by anyone's deviation — so there is still nothing to gain by deviating, and deviating only converts a likely 7–9 into a certain 0.

If the history shows one player's reports keep causing seal failures (their report residue can't match their draw), I still don't change my play — I can't control their report, and deviating only adds failure risk of my own.

If reliability mattered more than score (e.g., repeated failures threatening my standing), the fallback is reporting my draw exactly (0–2), which is always seal-safe but scores low. In this scoring setup I always take draw+7 instead, since the risk comes only from others, not from me.

On the final round, even trailing, I still report draw+7. Overreporting can only produce a seal failure and 0, and cannot win me anything the opponents don't also lose; maximum guaranteed score is the best closing move.

On every round, regardless of score, history, or others' visible behavior, I output draw+7 and stop deliberating.