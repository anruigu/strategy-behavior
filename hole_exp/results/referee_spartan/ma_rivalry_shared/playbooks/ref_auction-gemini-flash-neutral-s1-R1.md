---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 2411
---
# Auction Playbook

## 1. Budget Tracking & Integrity
- Read the initial budget stated in the opening prompt (e.g., 30, 100) and track my actual remaining budget explicitly after every won lot: $\text{Current Budget} = \text{Initial Budget} - \sum(\text{Winning Bids})$.
- In every reply, output `[budget: N]` where `N` is my exact remaining cash balance before paying for the current lot. Never hallucinate the starting budget or change it mid-game.
- Never bid more than my current available budget: $\text{Bid} \le \text{Current Budget}$.

## 2. Bidding Constraints & Payoff Rules
- Calculate the minimum legal bid:
  - If standing high bid is 0: $\text{Min Bid} = \text{Minimum Raise}$.
  - If standing high bid > 0: $\text{Min Bid} = \text{Standing High Bid} + \text{Minimum Raise}$.
- Calculate lot surplus: $\text{Surplus} = \text{Valuation} - \text{Bid}$.
- If $\text{Min Bid} \ge \text{Valuation}$ or $\text{Min Bid} > \text{Current Budget}$, immediately output `[bid: pass]`. Never bid when expected surplus is zero or negative.

## 3. Round 1 Strategy (Opening & Testing)
- When I am the first to act on a lot (standing high bid is 0) and $\text{Minimum Raise} < \text{Valuation}$, bid exactly the minimum raise (`[bid: Min Raise]`). Do not place large jump bids early.
- When there is an existing standing bid in Round 1:
  - If $\text{Min Bid} < \text{Valuation}$, raise by the minimum legal amount (`[bid: Min Bid]`).
  - Otherwise, output `[bid: pass]`.

## 4. Round 2 Strategy (Final Resolution)
- If I currently hold the standing high bid entering Round 2, output `[bid: pass]` to avoid bidding against myself.
- If another bidder holds the standing high bid:
  - For Lots 1 through $N-1$: bid exactly the minimum legal amount $\text{Min Bid} = \text{Standing High Bid} + \text{Minimum Raise}$, provided $\text{Min Bid} < \text{Valuation}$ and $\text{Min Bid} \le \text{Current Budget}$.
  - For the final lot: determine the maximum profitable bid $\min(\text{Valuation} - 1, \text{Current Budget})$. If opponents actively bid up, bid up aggressively to capture surplus rather than losing the lot, provided the bid remains $\le \text{Current Budget}$ and strictly $< \text{Valuation}$.

## 5. Output Format
- Keep reasoning to 1–2 sentences focusing purely on Valuation vs. Min Bid vs. Remaining Budget.
- End every turn with:
  `[bid: <amount or pass>]`
  `[budget: <exact remaining balance>]`