---
game: ref_auction
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1606
---
# Auction Playbook

## Budget Tracking
- Read the initial starting budget carefully in the opening prompt (e.g., 30) and record it exactly. Never hallucinate or default to 100.
- When an auction concludes and the results show I won a lot, subtract the winning price from my running budget.
- In every reply, output `[budget: N]` reflecting my true remaining budget.

## Bidding Strategy
- Never bid on a lot if the minimum required bid (`standing high bid + minimum raise`, or `minimum raise` if standing is 0) meets or exceeds my private valuation; output `[bid: pass]`.
- Never submit a bid higher than my current remaining budget, regardless of how high my valuation is.
- In Round 1 of any lot:
  - If the minimum valid raise is strictly below my valuation and within remaining budget, bid the minimum valid amount (`standing high bid + minimum raise`).
  - Otherwise, pass.
- In Round 2 of non-final lots:
  - If the minimum valid raise is strictly below my valuation and within remaining budget, bid the minimum required amount to preserve margin and budget for future lots.
  - If the minimum required raise exceeds my valuation or remaining budget, pass.
- In Round 2 of the final lot:
  - Unused budget has no value at game end.
  - If remaining budget and valuation allow, place a decisive bid up to `min(remaining budget, valuation - 1)` to secure surplus rather than risking a tie or loss on a minimum increment.

## Output Formatting
- Keep reasoning brief (1–2 sentences).
- Always include both required tokens on separate lines or at the end: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.