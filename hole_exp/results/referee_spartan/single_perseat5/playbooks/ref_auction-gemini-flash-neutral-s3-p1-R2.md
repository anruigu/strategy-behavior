---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1439
---
# Auction Playbook

## Budget Tracking
- Read the opening text carefully for my initial budget (e.g., if it states 30, it is 30, not 100). Maintain this exact number across all lots until I actually win a lot.
- Check the "Results so far" section at the start of each lot. If bidder 1 (myself) won a previous lot, subtract that exact winning price from my remaining budget. If another bidder won, my budget remains unchanged.
- In every response, accurately output my actual remaining budget in `[budget: N]`. Never place a bid higher than my remaining budget.

## Bidding Strategy
- Always ensure any bid satisfies two hard constraints: `bid <= valuation` (never bid higher than my private value) and `bid <= remaining_budget`.
- In Round 1:
  - If `minimum_raise > valuation` or `minimum_raise > remaining_budget`, pass (`[bid: pass]`).
  - Otherwise, bid the minimum necessary amount: `standing_bid + minimum_raise` (or `minimum_raise` if standing bid is 0) to stay active without inflating the price.
- In Round 2 (Final Round):
  - Calculate the required minimum bid: `target = standing_bid + minimum_raise`.
  - If `target <= valuation` and `target <= remaining_budget`, bid `target`.
  - If `target > valuation` or `target > remaining_budget`, pass (`[bid: pass]`).

## Response Formatting
- Keep reasoning brief (1–2 sentences).
- Always conclude the reply with both required tokens:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`