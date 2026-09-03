---
game: ref_auction
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2545
---
**Playbook for open ascending auctions with private values**

- When I hold the standing high bid, I pass. Never bid against myself; my own bid already stands.

- When the standing high bid is well below my value, I bid the minimum raise rather than jumping. Small increments keep the final price low and leave the rival to reveal their limit. This worked repeatedly: I won high-value lots at tiny prices.

- My cap on any lot is my private value minus a margin. I never bid at or above my value; if a rival's bid exceeds my value, I pass immediately and without regret.

- Track budget by re-deriving it from scratch every turn: start from the initial budget and subtract every lot I have actually paid for. Do not carry forward my last stated number, and never reset or inflate it — I made exactly that error (stated 100 mid-game) and it could cause overcommitment. If winning a lot does not visibly reduce my stated budget, recompute the true remaining budget mentally anyway before deciding whether a bid is affordable.

- Round 2 is the decisive round: if the standing bid is still under my value at round 2, one minimal raise is usually right. But note that even a round-2 bid can lose if rivals bid after me within the round structure — so a round-2 raise should have real margin, not a token sliver. My +1-margin win on a low-value lot was barely worth it.

- Small-margin round-2 bids on low-value lots are marginal at best. If my value barely exceeds the standing bid, the tiny surplus is often not worth the risk of an overshoot; pass unless the margin is comfortable. Reserve round-2 saves for lots where value clearly exceeds price.

- Early in the sequence, I preserve budget for later lots, since I don't know future values. With many lots remaining and a full budget, I can be more aggressive on high-value lots; with most of my budget spent, I only chase lots where value far exceeds the current price.

- If a lot is worth less to me than the current standing bid, I pass from the start — no speculative opening bids on lots I probably can't win cheaply. Only open with a small bid when the standing price is trivially low, since sometimes no one fights and the lot goes for almost nothing.

- If I pass in round 1, I can still bid in round 2 — passing early is not a commitment. Use round 1 to let rivals bid the price up before deciding whether to enter at all.

- My aim is total surplus, not winning count: winning one high-margin lot beats winning several thin ones. A near-zero-margin win adds little and consumes budget.