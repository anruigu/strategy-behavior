---
game: ref_auction
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1516
---
# Auction Playbook

## Budget Tracking & Accounting
- At the start of the game, read and initialize my internal budget to the exact starting amount specified in the prompt (e.g. 30); never default to or assume a budget of 100.
- When reporting `[budget: N]`, calculate and output: `starting_budget - sum(prices of lots won by me so far)`.
- Ensure my bid does not exceed my remaining budget. If the minimum required bid exceeds my remaining budget, I must pass.

## Bidding Strategy
- Calculate the minimum required bid as `standing_bid + minimum_raise` (or `minimum_raise` if standing bid is 0).
- If the minimum required bid is strictly less than my private valuation for the lot and less than or equal to my remaining budget, place a bid equal to the minimum required bid to maximize surplus and conserve capital.
- In round 2/2, if the lot offers substantial surplus and budget allows, bid the minimum required amount or a calculated surplus-capturing amount strictly below my valuation and within my remaining budget.
- If the minimum required bid is greater than or equal to my private valuation, or exceeds my remaining budget, output `[bid: pass]`. Never bid at or above my valuation.
- When multiple lots remain and budget is tight relative to valuations, prioritize bidding on lots with higher absolute surplus (valuation minus required bid).

## Response Format
- Always include brief reasoning and end the reply with both required tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`