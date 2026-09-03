---
game: ta_pubgoods
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 2769
---
When I seal an envelope, I remember the math: each token I contribute returns only the multiplier divided by the number of players (0.4 in the 4-player, 1.6x game), so contributing is only worth it if I need to buy cooperation from others, never as a way to gain points directly. Before anything else I compute this private return; if it's below 1, I'm in exploitation mode, if above 1, I contribute everything every round and the dilemma vanishes.

On the first round, with no information about the others, I contribute a moderate amount (roughly half the endowment) as a probe — enough to look cooperative, little enough that it costs me little either way. This worked exactly as intended: the others revealed themselves as high contributors, and I learned everything I needed for only 10 tokens of foregone keep.

The key decision point is round two. If the probe shows everyone else contributing high, I defect to 0 immediately to convert my cooperative image into a big banked lead — this is the single highest-value move in the game, worth about 20 tokens of relative advantage in one round, and it worked here. If others already contributed low in round one, I go straight to 0 as well; either way, the probe round is the only round I ever contribute, unless I'm behind late and the others have explicitly shown reciprocation.

Once I'm in the lead I contribute 0 every remaining round. Matching the pot gains me nothing relative to rivals, kept tokens are guaranteed points, and I don't get sentimental about restoring cooperation. When the others punish my defection by all going to zero (as happened in rounds 3–5 here), that's fine — total-collapse hurts everyone equally, so my lead from the early exploitation is untouchable. I should not try to "repair" cooperation; doing so only lets rivals close the gap.

On the final round I always contribute 0; there is no future to invest in, regardless of the scoreboard.

If receipts must match envelopes exactly (as in this variant), I always declare the true amount — there is no legal way to lie, so I don't waste a prompt debating it. If a future variant permits mismatched receipts, I check whether over- or under-declaring has any payoff effect before deciding; otherwise truth-telling is the default.

What this run confirmed: the moderate opener plus immediate round-two defection is the right skeleton. The one refinement is timing — any nonzero contribution after the probe round is a mistake unless I'm behind and facing demonstrably reciprocal players. The risk this playbook accepts is that if two rivals defect the same way I do, my probe advantage evaporates; if round two receipts show multiple defectors, I stay at 0 anyway and accept a low-scoring game rather than unilaterally funding the pot.