---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1603
---
# Auction Playbook

## Budget Tracking
- Read the true starting budget from the initial rules prompt (do not default to assumptions like 100).
- Maintain an exact running tally of remaining budget: subtract the winning price immediately whenever an auction result confirms I won a lot.
- In every output, state the accurate remaining budget in `[budget: N]`.
- Never submit a bid higher than my currently available budget.

## Bid Valuation and Limits
- Calculate maximum allowable bid on any lot as `min(my_value - 1, remaining_budget)`.
- Never bid equal to or above my personal valuation for a lot; doing so yields zero or negative surplus.
- If the required minimum bid (`standing_high_bid + minimum_raise`) exceeds my maximum allowable bid, immediately output `[bid: pass]` with my current budget.

## Bidding Tactics
- In Round 1 of any lot:
  - If the minimum legal raise is within my allowable limit, bid strictly the minimum required amount (`standing_high_bid + minimum_raise`).
  - Do not jump-bid or raise higher than the minimum increment in Round 1; keep the price low to test opponent interest.
- In Round 2 (Final Round) of any lot:
  - If I currently hold the winning bid, do not raise myself; pass if given the option, or hold position.
  - If outbid, bid exactly `standing_high_bid + minimum_raise`, provided this bid is $\le$ my maximum allowable bid.
  - If the required bid exceeds valuation or remaining budget, output `[bid: pass]`.

## Response Format
- Provide brief reasoning (1–2 sentences).
- End every response strictly with:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`