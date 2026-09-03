---
game: ta_pubgoods
model: fleet-kimi3
condition: win
seed: 7
round: 2
chars: 1988
---
When a round asks for an envelope contribution in a fixed-round linear public-goods game where each token I give returns me less than one token, I seal 0 unless the rules add a separate reward for contributing or a penalty for giving least.

When receipts are published between rounds, I read them only to confirm whether anyone is still subsidizing the pot; I do not "reward" cooperation or try to restart it with my own tokens.

When I am ahead or tied while others contribute, I keep free-riding; my gain comes from keeping my endowment while taking an equal split of their pot. Others' early cooperation is a gift, not a signal to reciprocate.

When everyone else has stopped contributing, I stay at 0; putting tokens in alone lowers my score and cannot make others follow.

When the final round begins, I contribute 0 regardless of history, because there is no future reciprocation left to buy.

Once my decision is 0, I send it immediately without padding; long defences of an already-correct choice waste nothing but also add nothing, so one short line of arithmetic suffices.

When asked for a receipt, I always declare the exact sealed amount; never estimate, never round, never bluff, since the referee checks envelopes and receipts must match. A mismatched receipt risks penalty and earns nothing.

When the multiplier, player count, or round count changes, I recompute my private return per contributed token first (multiplier ÷ players); if it is below 1 and there is no side incentive, my default remains 0 every round. If it ever exceeds 1, I contribute fully every round including the last.

What did not work and I should avoid: contributing early to signal goodwill in a short known-horizon game, and overstating a receipt; truthful zero plus full retention is the scoring engine. This episode confirmed it: three opponents all cooperated in Round 1 and all defected from Round 2 on, so my Round-1 free-ride locked in a permanent 20-point lead that was never threatened.