---
game: ref_auction
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1259
---
- Track my budget accurately starting from the initial amount stated in the prompt (e.g., 30, not an assumed 100); whenever I win a lot, subtract the winning bid from my running budget and always report this exact remaining balance in `[budget: N]`.
- Never place a bid `N` that exceeds my actual remaining budget or exceeds my valuation of the lot.
- When valuation is below the minimum required opening bid or below `standing high bid + minimum raise`, pass immediately with `[bid: pass]`.
- In round 1 of a lot, if the lot is profitable, bid the minimum legal amount (`standing high bid + minimum raise`, or `minimum raise` if no bids yet) to stay in contention without unnecessarily inflating the price.
- In round 2 of a lot:
  - If the minimum legal bid is strictly less than my valuation and within my remaining budget, place a bid that maximizes expected surplus. If opponents bid aggressively, bid high enough toward my valuation (capped at my budget) to win high-surplus lots rather than underbidding and losing.
  - If `standing high bid + minimum raise >= valuation`, output `[bid: pass]`.
- Format every turn strictly with valid tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`, ensuring the budget token matches my actual remaining funds.