---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1660
---
# Auction Playbook

## Budget Tracking
- Read the opening text carefully for the initial budget (e.g., if it states "start with a budget of 30", initial budget is 30; do not assume 100 or hallucinate a higher budget). Maintain this exact number across all lots until I win a lot.
- Check the "Results so far" section at the start of each lot. If bidder 1 (myself) won a previous lot, subtract that exact winning price from my remaining budget. If another bidder won, my budget remains unchanged.
- My budget only decreases when a lot is officially won, not while placing active bids during an ongoing lot.
- In every response, accurately output my actual remaining budget in `[budget: N]`. Never place a bid `bid > remaining_budget`.

## Bidding Strategy
- Always ensure any bid satisfies two hard constraints: `bid <= valuation` (never bid higher than my private value) and `bid <= remaining_budget`.
- In Round 1:
  - If `standing_bid + minimum_raise > valuation` or `standing_bid + minimum_raise > remaining_budget`, pass (`[bid: pass]`).
  - Otherwise, bid the minimum necessary amount: `standing_bid + minimum_raise` (or `minimum_raise` if standing bid is 0) to stay active without inflating the price.
- In Round 2 (Final Round):
  - Calculate the required minimum bid: `target = standing_bid + minimum_raise`.
  - If `target <= valuation` and `target <= remaining_budget`, bid `target`.
  - If `target > valuation` or `target > remaining_budget`, pass (`[bid: pass]`).

## Response Formatting
- Keep reasoning brief (1–2 sentences).
- Always conclude the reply with both required tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`