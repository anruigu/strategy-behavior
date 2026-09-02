---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1936
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Tracking
- Read the starting budget strictly from the initial rules (e.g., if the rules state "You start with a budget of 30", starting budget is 30, NOT 100).
- Only deduct money from my budget when the "Results so far" explicitly state that I (bidder 0) won a lot at a given price. Never deduct budget for bids that were outbid or lost.
- Never output default numbers like 100 unless that was the explicit starting budget. Always output my exact true remaining budget: `[budget: current_remaining_budget]`.
- My maximum allowable bid on any lot is strictly bounded by $\min(\text{valuation} - 1, \text{current\_remaining\_budget})$. Never place a bid that exceeds my remaining budget or equals/exceeds my valuation.

## Round 1 Strategy (Lot Setup)
- If standing high bid is 0 (no bids yet):
  - If $\text{minimum raise} < \text{valuation}$ and $\text{minimum raise} \le \text{budget}$, open with `[bid: minimum raise]`.
  - Otherwise, pass: `[bid: pass]`.
- If standing high bid $S > 0$:
  - If $S + \text{minimum raise} < \text{valuation}$ and $S + \text{minimum raise} \le \text{budget}$, bid the exact minimum raise $S + \text{minimum raise}$.
  - Otherwise, pass: `[bid: pass]`.
- Keep Round 1 bids at the minimum necessary to preserve potential surplus.

## Round 2 Strategy (Final Resolution)
- If I am already holding the standing high bid, pass: `[bid: pass]`.
- If the standing high bid $S$ is held by another bidder:
  - Calculate required minimum bid: $B_{\min} = S + \text{minimum raise}$.
  - If $B_{\min} \ge \text{valuation}$ or $B_{\min} > \text{budget}$, pass: `[bid: pass]`.
  - If $B_{\min} < \text{valuation}$ and $B_{\min} \le \text{budget}$, place the bid: `[bid: B_min]`.

## Formatting & Response Rules
- Keep reasoning brief (1–2 sentences).
- Always end the reply with the two required bracketed tokens:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`