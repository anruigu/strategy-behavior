---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 2385
---
### Budget Accounting
- Read and record the exact initial starting budget stated in the opening prompt (e.g., if it says "You start with a budget of 30", the starting budget is 30, not 100; if it states 100, use 100). Never switch the starting budget baseline mid-game.
- Keep exact track of remaining budget: `remaining_budget = initial_budget - sum(prices paid for lots won by bidder 0)`.
- Deduct winning amounts only when confirmed in "Results so far: lot X: bidder 0 won at Y". Do not deduct budget for lots won by other bidders or lost bids.
- Always output `[budget: remaining_budget]` accurately in every turn, including passes.

### Bidding Strategy & Valuation Thresholds
- Strictly maintain `bid < valuation` at all times. Never bid equal to or greater than private valuation, as winning at or above valuation guarantees zero or negative score surplus.
- Never bid more than the remaining budget (`bid <= remaining_budget`).
- When the minimum required bid (`standing high bid + minimum raise`, or `minimum raise` if standing bid is 0) is `>= valuation` or `> remaining_budget`, immediately output `[bid: pass]`.

#### Round 1/2 Strategy
- If opening (standing high bid is 0): bid exactly the minimum opening raise, provided `minimum raise < valuation` and `<= remaining_budget`. Otherwise pass.
- If responding to an existing standing bid: bid exactly `standing high bid + minimum raise`, provided that sum is strictly below valuation and within budget. Otherwise pass.

#### Round 2/2 (Final Round) Strategy
- Check the minimum required bid (`standing high bid + minimum raise`). If it exceeds or equals `min(valuation, remaining_budget + 1)`, pass.
- If valid, submit a competitive final bid designed to beat rival round-2 bids while capturing surplus:
  - Target a bid around 75% to 85% of valuation, or approximately `min(valuation - 3, standing high bid + 2 * minimum raise)`.
  - Ensure the bid is strictly at least `standing high bid + minimum raise` and at most `min(valuation - 1, remaining_budget)`.
  - If the valuation margin is very slim (e.g., valuation is only 1–3 points above the minimum bid), bid the exact minimum required bid to preserve any positive surplus.

### Response Format
- Keep reasoning strictly concise (1–2 sentences).
- Always include both required bracketed tokens at the end of the reply: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.