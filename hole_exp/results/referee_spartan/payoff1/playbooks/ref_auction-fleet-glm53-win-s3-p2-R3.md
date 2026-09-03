---
game: ref_auction
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 2727
---
**Playbook for open ascending auctions with private values**

- When the standing high bid is well below my value, I bid the minimum raise rather than jumping. Small increments keep the final price low and let the rival reveal their limit. This worked: I won two lots (values 37 and 46) for 16 and 21, a combined surplus of +46.

- My cap on any lot is my private value minus a margin. I never bid at or above my value; if the minimum raise would push me to or past my value, I pass immediately and without regret. Passing lot 1 at 26 against a value of 29, and lot 4 at 40 against a value of 37, were both correct calls — those lots would have been thin or negative.

- Round 2 is decisive: if the standing bid is still well under my value, one raise is usually right, and it needs real margin, not a sliver. My round-2 raise to 21 on the last lot (value 46) had 25 points of margin and was the best move of the game. My earlier round-2 win at a +1 margin was barely worth it — do not repeat that.

- Budget tracking is my biggest failure mode. I misstated budget repeatedly this game (100 mid-game, then 84 for the rest, when my true remaining budget after paying 16 was 14). The stated budget token does not seem to have affected my results, but it could in a setup where it does. Fix: recompute budget every turn as (initial budget) minus (sum of final prices of lots I have already won). Never carry forward a previous stated number. Before any bid, check the recomputed budget can actually cover it.

- With only 2 rounds of bidding per lot, a round-1 minimal raise followed by a round-2 raise is the full extent of a contest. A rival who re-raises in round 2 can still take the lot, so a round-2 bid does not guarantee a win — it only wins if no one tops it. Value my round-2 raise on expected win, not assumed win.

- Open cheaply when the standing price is trivially low relative to my value. Opening at the minimum on an unbidded lot sometimes wins outright for almost nothing, and costs nothing if outbid. But do not open on lots where my value is below or near the standing price.

- If I pass in round 1, I can still bid in round 2 — passing early is not a commitment. Use round 1 to let rivals bid the price up before deciding whether to enter.

- Early in the sequence, preserve budget for later lots since future values are unknown. But when a lot is worth far more than the current price, take it — surplus now beats hypothetical surplus later, especially since budgets may be tighter than I think.

- My aim is total surplus, not winning count. One high-margin lot beats several thin ones; a near-zero-margin win adds little and consumes budget. Letting rivals have lots at or above my value costs me nothing.