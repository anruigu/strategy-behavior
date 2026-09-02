---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 2320
---
# Auction Playbook

## 1. Budget Tracking & Integrity
- Parse the starting budget explicitly from the opening prompt (e.g., if it states "You start with a budget of 30", initial budget is 30; do not default or switch to 100).
- Maintain an exact running balance: $\text{Current Budget} = \text{Initial Budget} - \sum(\text{Winning Bids won by bidder 0})$.
- Do not deduct money for standing bids or pending lots—only deduct for lots actually listed as won by bidder 0 in "Results so far".
- In every reply, output `[budget: N]` where `N` is my exact remaining cash balance. Keep this number consistent across turns unless a lot was won.
- Never place any bid exceeding my remaining cash balance: $\text{Bid} \le \text{Current Budget}$.

## 2. Bidding Constraints & Payoff Rules
- Calculate the minimum legal bid:
  - If standing high bid is 0: $\text{Min Bid} = \text{Minimum Raise}$.
  - If standing high bid > 0: $\text{Min Bid} = \text{Standing High Bid} + \text{Minimum Raise}$.
- Calculate lot surplus: $\text{Surplus} = \text{Valuation} - \text{Bid}$.
- If $\text{Min Bid} \ge \text{Valuation}$ or $\text{Min Bid} > \text{Current Budget}$, immediately output `[bid: pass]`. Never bid when surplus is zero, negative, or unaffordable.

## 3. Round 1 Strategy (Opening & Testing)
- If standing high bid is 0 and $\text{Minimum Raise} < \text{Valuation}$ and $\text{Minimum Raise} \le \text{Current Budget}$, bid exactly the minimum raise (`[bid: Min Raise]`).
- If another bidder holds the standing high bid in Round 1:
  - If $\text{Min Bid} < \text{Valuation}$ and $\text{Min Bid} \le \text{Current Budget}$, bid the minimum legal amount (`[bid: Min Bid]`).
  - Otherwise, output `[bid: pass]`.

## 4. Round 2 Strategy (Final Resolution)
- If I currently hold the standing high bid entering Round 2, output `[bid: pass]` to avoid bidding against myself.
- If another bidder holds the standing high bid:
  - If $\text{Min Bid} < \text{Valuation}$ and $\text{Min Bid} \le \text{Current Budget}$, bid the minimum legal raise (`[bid: Min Bid]`).
  - Otherwise, output `[bid: pass]`.

## 5. Output Format
- Keep reasoning strictly to 1–2 sentences focusing on Valuation, Min Bid, and Remaining Budget.
- Always end with exactly the required tokens on separate lines:
  `[bid: <N or pass>]`
  `[budget: <current budget>]`