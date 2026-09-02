---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1442
---
# Auction Playbook

## Budget Tracking
- Read my actual starting budget from the initial rules prompt (do not assume 100).
- When reporting `[budget: N]`, calculate $N$ as my true starting budget minus the cumulative prices of all lots I have actually won in previous lots. Never hallucinate or reset the budget token to 100 after round 1.
- Never place any bid greater than my remaining budget.

## Bidding Thresholds & Rules
- Treat my valuation as a hard ceiling. If the minimum required bid (standing high bid + minimum raise, or the opening minimum raise if standing bid is 0) is $\ge$ my valuation, immediately reply `[bid: pass]`.
- In Round 1 of any lot:
  - If the minimum legal bid is strictly below my valuation, bid exactly the minimum legal bid (standing high bid + minimum raise, or minimum raise if standing bid is 0). Do not place large opening bids or jump bids in round 1.
- In Round 2 of any lot:
  - If the required minimum bid is strictly below my valuation and within my remaining budget, place a bid that maximizes my chance to win while preserving positive surplus. Bid at or slightly above the minimum required bid, but strictly strictly below valuation.
  - If the standing high bid is already mine (if applicable) or if meeting the raise exceeds valuation or budget, reply `[bid: pass]`.

## Response Format
- Always include brief reasoning and conclude with exactly:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`