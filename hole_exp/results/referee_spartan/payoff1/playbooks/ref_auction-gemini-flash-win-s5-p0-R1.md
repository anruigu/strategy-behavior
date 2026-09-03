---
game: ref_auction
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1555
---
# Auction Playbook

- **Track Actual Budget Accurately**: 
  - Start with the exact budget specified in the game setup prompt.
  - After winning a lot, subtract the winning price from my remaining budget immediately.
  - Never hallucinate a default budget like 100; always report the exact current arithmetic balance in `[budget: N]`.

- **Valuation and Budget Bounds**:
  - Never bid above my valuation for a lot, regardless of remaining budget.
  - Never bid more than my current available budget, regardless of the lot's valuation.
  - When the minimum required raise exceeds either my remaining budget or my valuation, reply with `[bid: pass]`.

- **Bidding Strategy by Round**:
  - **Round 1/2**:
    - When entering an unbid lot or raising an existing bid, bid the minimum legal increment (`standing bid + minimum raise`, or simply `minimum raise` if standing bid is 0) to keep entry costs low.
  - **Round 2/2 (Final Round for Lot)**:
    - If the minimum legal raise leaves a strong positive surplus (`valuation - min_bid > 0`) and other bidders have been actively raising, bid a calculated amount high enough to win without overpaying (e.g., jump slightly above the minimum if surplus allows, or take the minimum raise if budget conservation is paramount).
    - If the required raise yields zero or negative profit (`min_bid >= valuation`), pass.

- **Output Formatting**:
  - Keep reasoning to 1–2 sentences.
  - Always terminate the reply with exactly:
    `[bid: N]` (or `[bid: pass]`)
    `[budget: N]` (reflecting the exact current budget).