---
game: hf_auction_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1485
---
### Playbook for `hf_auction_nerfed`

- **Budget Tracking & Reporting**:
  - Always report my exact actual remaining budget in `[budget: N]`.
  - Start with the exact starting budget stated in the prompt (e.g., 30, not 100).
  - When I win a lot, subtract the winning bid from my remaining budget for all subsequent rounds and lots.
  - Never invent or reset the budget to arbitrary numbers (like 100 or 80); accurate tracking avoids inspection penalties.

- **Bidding Rules & Constraints**:
  - Never bid higher than my remaining budget.
  - Never bid higher than my private valuation for the lot.
  - When I already hold the standing high bid in round 2, output `[bid: pass]`.

- **Round 1 Strategy**:
  - When standing bid is 0 and minimum raise ≤ valuation, open with the minimum required bid (`standing_bid + min_raise`).
  - When standing bid > 0, raise by the minimum increment if `standing_bid + min_raise < valuation` and within budget; otherwise, pass.

- **Round 2 (Closing) Strategy**:
  - If another bidder holds the high bid and `standing_bid + min_raise <= valuation` and within budget:
    - Bid the minimum required raise (`standing_bid + min_raise`) or slightly above if needed to clear ties, but avoid massive overbidding that destroys surplus.
  - If the required raise meets or exceeds valuation or remaining budget, output `[bid: pass]`.

- **Output Format**:
  - Always conclude every reply with:
    `[bid: <N or pass>]`
    `[budget: <exact_remaining_budget>]`