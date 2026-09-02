---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 2232
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Tracking
- At the start of the game, initialize my internal budget to the starting amount stated in the rules.
- Only deduct money from my budget when the results show I have actually won a lot (e.g., `Results so far: lot X: bidder 0 won at P`). Never deduct budget for bids that are still active, outbid, or lost.
- Never output arbitrary or default budget numbers (like 100); always output my true remaining budget: `[budget: current_remaining_budget]`.
- My maximum allowable bid on any lot is $\min(\text{valuation}, \text{current\_remaining\_budget})$. Never place a bid higher than my remaining budget.

## Round 1 Strategy (Lot Setup)
- If the standing bid is 0:
  - If $\text{minimum raise} < \text{valuation}$, bid the minimum raise: `[bid: minimum raise]`.
  - If $\text{minimum raise} \ge \text{valuation}$, pass: `[bid: pass]`.
- If there is an existing standing bid $S$:
  - If $S + \text{minimum raise} < \text{valuation}$ and $S + \text{minimum raise} \le \text{budget}$, bid the exact minimum raise $S + \text{minimum raise}$.
  - Otherwise, pass: `[bid: pass]`.
- Do not make unnecessary jump bids in Round 1; keep the price as low as possible going into the final round.

## Round 2 Strategy (Final Resolution)
- If I am already holding the standing high bid, pass: `[bid: pass]`.
- If the standing high bid is held by another bidder:
  - Calculate the minimum required bid: $B_{\min} = S + \text{minimum raise}$.
  - If $B_{\min} \ge \text{valuation}$ or $B_{\min} > \text{budget}$, pass: `[bid: pass]`.
  - If $B_{\min} < \text{valuation}$ and $B_{\min} \le \text{budget}$:
    - For lots before the final lot: bid exactly $B_{\min}$ to capture maximum surplus if opponents drop out.
    - For the final lot of the game: if I have surplus budget and want to secure remaining value, bid up to $\text{valuation} - 1$ or $B_{\min}$ depending on whether I prioritize certainty of winning surplus over margin, but never bid equal to valuation (zero profit) or above valuation (negative profit).

## Formatting
- Keep the reasoning to one or two sentences.
- Always conclude with the two required bracketed tokens:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`