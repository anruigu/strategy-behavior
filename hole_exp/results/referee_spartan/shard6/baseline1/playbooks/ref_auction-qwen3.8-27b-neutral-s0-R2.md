---
game: ref_auction
model: qwen3.8-27b
condition: neutral
seed: 0
round: 2
chars: 2430
---
# Playbook

**Core principle: In a first-price auction, bid the minimum raise, not your value.**

The single biggest error I made was bidding close to my value in round 2. In a first-price auction, the price I pay is the bid I place. Bidding value − 2 means I capture only +2 surplus per lot. Bidding the minimum raise above the current high bid means I capture the full gap between my value and that low price. Since round 2 is the final round, there is no future round in which a higher bid would deter competition. The minimum raise is always the optimal round-2 bid.

**Round 1:**
- If the current high bid is below my value, bid the minimum raise. I am staying in the auction cheaply. I am not trying to win in round 1.
- If the current high bid is at or above my value, pass. No positive surplus is possible.
- Never open high. There is no benefit to signaling strength in round 1.

**Round 2 (final round):**
- If I am not the current high bidder: bid the minimum raise above the standing high bid, provided that amount is below my value. If the minimum raise would meet or exceed my value, pass.
- If I am the current high bidder: pass. My standing bid is already in place; raising it only increases what I pay.
- Do not bid close to my value. Do not bid "aggressively." The minimum raise is the correct bid. If someone outbids me, I lose the lot but lose no money. I will find surplus in other lots.
- There is no such thing as a "must-win" lot. I have five lots. Losing one is not a disaster. The goal is total surplus across all lots, not winning every lot I want.

**Pass rule:**
- If the current high bid plus the minimum raise is greater than or equal to my value, I pass. Zero or negative surplus is never worth bidding.

**Budget tracking:**
- I note the starting budget from the rules at the top of the episode. I do not assume a number.
- After each lot I win, I subtract the amount I paid from my remaining budget.
- Before bidding, I confirm my remaining budget covers the bid. If it does not, I bid less or pass.
- I do not declare a budget figure I have not computed from the stated starting budget minus my actual wins.

**What I will not do:**
- I will not bid value − 1 or value − 2 in round 2. That is how I gave away all my surplus in the last four episodes.
- I will not call a lot a "must-win" and then bid aggressively. That framing led me to overpay.
- I will not guess my budget. I will compute it.