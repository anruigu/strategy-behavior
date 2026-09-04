---
game: hf_auction_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1614
---
# Auction Playbook

## Budget Tracking and Reporting
- When calculating my budget, I start at the exact opening budget stated in the prompt (e.g., 30, not an assumed 100) and subtract the winning price of every lot I win as the game progresses.
- When outputting `[budget: N]`, I always report my actual remaining budget. I never report a budget higher than what I actually possess or jump to an arbitrary large number.
- When considering any bid, I cap my bid at my true remaining budget. Never place a bid that exceeds my current available funds.

## Bidding Strategy
- When round 1/2 begins on any lot:
  - If my private valuation is strictly higher than the minimum opening bid, I bid the minimum required raise (`standing high bid + minimum raise`, or simply the minimum raise if standing bid is 0).
  - If my private valuation is lower than or equal to the minimum required bid, I output `[bid: pass]`.
- When round 2/2 begins on any lot:
  - If the required minimum bid (`standing high bid + minimum raise`) is strictly less than my private valuation and less than or equal to my remaining budget, I bid to capture surplus.
  - In round 2/2, prefer bidding the minimum valid increment above the standing bid rather than jumping close to my full valuation, to maximize profit margin per lot.
  - If the required minimum bid meets or exceeds my private valuation or exceeds my remaining budget, I output `[bid: pass]`.

## Response Formatting
- When submitting any reply, keep reasoning strictly under three sentences and end the reply with both required tags: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.