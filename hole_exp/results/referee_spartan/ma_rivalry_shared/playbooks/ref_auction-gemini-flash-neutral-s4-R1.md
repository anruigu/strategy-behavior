---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1462
---
### Budget Accounting
- Track budget accurately starting from the initial budget given in the opening prompt.
- Deduct the winning price from the remaining budget only when a lot is won; do not reset or jump to arbitrary numbers (like 100).
- Always output `[budget: remaining_budget]` accurately alongside every bid or pass.

### Bidding Rules & Valuation Thresholds
- Never bid equal to or above my valuation for a lot. Only bid when `bid < valuation`.
- Never bid more than my remaining budget.
- When opening a lot in Round 1, always bid the minimum opening amount (the minimum raise). Do not jump-bid or open high.
- In Round 1, when raising an existing standing bid, bid strictly the minimum required raise (`standing high bid + minimum raise`), provided it remains strictly below valuation and within budget.
- In Round 2 (final round for a lot):
  - If the minimum required raise is below valuation and within budget, bid aggressively enough to win surplus without exceeding valuation or budget.
  - Avoid bidding unnecessarily high increments over the standing high bid when the minimum increment already secures positive surplus, but ensure the bid is competitive against typical round-2 pushes.
  - If the required minimum bid meets or exceeds my private valuation, immediately reply `[bid: pass]`.

### Response Format
- Keep brief reasoning to 1–2 sentences.
- Always conclude responses strictly with `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.