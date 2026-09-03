---
game: ta_pubgoods
model: fleet-kimi3
condition: win
seed: 4
round: 1
chars: 2306
---
When I seal an envelope, I remember the math: each token I contribute returns only 0.4 to me, so contributing is only worth it if I need to buy cooperation from others, not as a way to gain points directly.

On the first round, when I have no information about the others, I contribute a moderate amount (roughly half the endowment) as a probe — enough to look cooperative, little enough that full free-riding by others doesn't cost me much.

After the first round's receipts are published, I read the group immediately: if everyone else contributed high, I defect to 0 or near-0 on the next round to convert my trustworthy image into a payoff lead; if others already contributed low, I go straight to 0 because the cooperative equilibrium is dead.

Once I'm in the lead, I contribute 0 every remaining round. Matching the pot gains me nothing relative to rivals, and kept tokens are guaranteed points. I don't get sentimental about restoring cooperation — the group collapsing to all-zero after my defection (as happened here) still leaves my lead intact.

On the final round I always contribute 0; there is no future to invest in, regardless of the scoreboard.

If receipts must match envelopes exactly (as in this variant), I always declare the true amount — there is no legal way to lie, and I won't waste a prompt debating it.

What did not work, or nearly didn't: my moderate opener was fine, but I should treat any nonzero contribution after round one as a mistake unless I'm behind and the others have shown they will reciprocate. In this run the others punished my defection by all going to zero, which cost everyone but didn't threaten my lead — the lesson is that defection works early, while I still have rounds left to bank the advantage, and I should stop contributing the moment the probe round ends.

Generally, whatever the group size, multiplier, or round count: I compute my private return per contributed token (multiplier divided by number of players). If it's below 1, contributing is strictly a social investment, so I only contribute while I believe it will induce others' future contributions, I defect the instant that belief breaks or the endgame approaches, and I never contribute on the last round. If it's above 1, I contribute everything every round and the dilemma vanishes.