---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1494
---
# Auction Playbook

## Budget Tracking
- Initialize my tracked budget at the exact starting budget given in the opening rules (do not hallucinate 100 or any other default).
- When I win a lot, subtract the winning price I paid from my current budget immediately for all subsequent turns.
- In every response, report my actual remaining budget in `[budget: N]`. Never bid higher than my remaining budget.

## Bidding Strategy
- Calculate my valuation surplus: `surplus = valuation - bid`. Never place any bid that exceeds my private valuation for the lot (`bid <= valuation`) or exceeds my remaining budget (`bid <= remaining_budget`).
- In Round 1:
  - If the lot is worth less than the minimum opening raise, pass (`[bid: pass]`).
  - If the lot has positive value, bid only the minimum required raise (`standing_bid + minimum_raise` or simply `minimum_raise` if standing bid is 0) to avoid unnecessarily inflating the price early. Never jump-bid in Round 1.
- In Round 2 (Final Round for the lot):
  - Check the minimum required bid: `target = standing_bid + minimum_raise`.
  - If `target <= valuation` and `target <= remaining_budget`, bid `target` (or a competitive surplus-maximizing amount within budget).
  - If `target > valuation` or `target > remaining_budget`, pass (`[bid: pass]`).

## Response Formatting
- Keep reasoning to 1–2 sentences.
- Always conclude the reply with both required tokens on their own lines or at the very end:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`