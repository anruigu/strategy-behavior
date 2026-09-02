---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1961
---
# Playbook: Multi-Lot Ascending Auction

## Budget Tracking & Integrity
- Always read the exact starting budget stated in the opening prompt (e.g., whether it is 30, 100, etc.) and stick strictly to it across all rounds.
- Never hallucinate a different starting budget; if the opening prompt states budget is 30, start with 30, not 100.
- Track remaining budget: `Current Budget = Starting Budget - Sum(Winning prices of completed lots won by me)`.
- Do not deduct funds for bids placed during an ongoing lot until that lot is won and resolved in the results.
- In every reply, output the exact remaining available budget in `[budget: N]`. Ensure the number matches my tracking in every round.

## Valuation & Bidding Thresholds
- Calculate `Min Bid = Standing High Bid + Minimum Raise`.
- If `Min Bid > Valuation`, output `[bid: pass]`. Never bid above valuation.
- If `Min Bid == Valuation`, output `[bid: pass]` (zero surplus gains nothing and risks capital).
- If `Min Bid > Current Budget`, output `[bid: pass]`.
- If `Min Bid < Valuation` and `Min Bid <= Current Budget`:
  - Bid exactly the minimum legal increment: `[bid: Min Bid]`.
  - Do not place preemptive overbids; minimum increments maximize surplus and conserve capital.

## Round Strategy (2 Rounds per Lot)
- **Round 1/2**:
  - If `Min Bid < Valuation` and `Min Bid <= Current Budget`, place the minimum legal bid.
  - If `Min Bid >= Valuation` or unaffordable, pass.
- **Round 2/2 (Final Round)**:
  - If the standing high bid is already held by me, pass.
  - If another bidder holds the high bid, bid `Standing High Bid + Minimum Raise` provided `Min Bid < Valuation` (strictly positive surplus) and `Min Bid <= Current Budget`. Otherwise, pass.

## Cross-Lot Budget Management
- Avoid spending budget on zero-surplus or very low-surplus lots early on.
- Prioritize bids on lots with large margins (`Valuation - Bid`), ensuring sufficient budget remains for later high-surplus opportunities.