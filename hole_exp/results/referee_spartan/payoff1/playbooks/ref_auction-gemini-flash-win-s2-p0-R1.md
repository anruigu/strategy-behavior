---
game: ref_auction
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1576
---
# Auction Playbook

## Budget Tracking
- At the start of the game, take the exact starting budget shown in the initial prompt and track it accurately; do not reset or jump to arbitrary numbers like 100.
- When an auction concludes and I win a lot, subtract the winning bid price from my running budget.
- In every reply, output `[budget: N]` with my true remaining cash.

## Bidding Strategy
- Never bid on a lot if the minimum required bid equals or exceeds my valuation for that lot; output `[bid: pass]`.
- Never submit a bid higher than my current remaining budget.
- In Round 1 of any lot:
  - If entering the auction, submit the minimum valid raise (`standing high bid + minimum raise`, or just `minimum raise` if no prior bids) to keep costs low and gauge competitor interest.
  - Do not jump-bid unnecessarily in Round 1.
- In Round 2 (Final Round) of earlier lots (before the final lot):
  - If the minimum valid bid (`standing high bid + minimum raise`) is less than my valuation and within budget, bid exactly the minimum required bid to preserve margin.
  - If competitors outbid me past my valuation or remaining budget, pass.
- In Round 2 of the final lot:
  - Since unused budget has zero terminal value, bid aggressively below my valuation to maximize the probability of winning while retaining positive surplus (e.g., bid slightly below valuation, ensuring it beats standard incremental raises).

## Output Formatting
- Keep reasoning to 1–2 short sentences.
- Always conclude responses with exact format tags: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.