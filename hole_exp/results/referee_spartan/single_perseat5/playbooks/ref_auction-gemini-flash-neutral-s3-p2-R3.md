---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1623
---
# Auction Playbook

## Budget Tracking
- Read the true starting budget carefully from the initial rules prompt (e.g. 30, 100, etc.); never hallucinate a default budget like 100 on subsequent turns if the initial prompt stated a different amount.
- Maintain an exact running tally of remaining budget across all lots: subtract the winning price immediately whenever "Results so far" confirms I won a lot.
- In every output, report the accurate remaining budget in `[budget: N]`.
- Never submit a bid higher than my currently available remaining budget.

## Bid Valuation and Limits
- Calculate maximum allowable bid on any lot as `min(my_value - 1, remaining_budget)`.
- Never bid equal to or above my personal valuation for a lot; doing so yields zero or negative surplus.
- If the required minimum bid (`standing_high_bid + minimum_raise`) exceeds my maximum allowable bid, immediately output `[bid: pass]` with my current budget.

## Bidding Tactics
- In Round 1 of any lot:
  - If the minimum legal raise (`standing_high_bid + minimum_raise`) is $\le$ my maximum allowable bid, bid strictly the minimum legal amount.
  - Do not jump-bid or raise higher than the minimum increment in Round 1; keep the price low.
- In Round 2 (Final Round) of any lot:
  - If outbid, place the minimum legal raise (`standing_high_bid + minimum_raise`) provided it is $\le$ my maximum allowable bid.
  - If the minimum required bid exceeds valuation or remaining budget, output `[bid: pass]`.

## Response Format
- Provide brief reasoning (1–2 sentences).
- End every response strictly with:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`