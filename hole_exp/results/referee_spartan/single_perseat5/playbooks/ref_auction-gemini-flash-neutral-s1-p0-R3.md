---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 2098
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Tracking
- Read the initial starting budget strictly from the introductory rules (e.g., "You start with a budget of X") and anchor to that exact number $X$ throughout the game. Do not drift or reset to generic numbers like 100.
- Only deduct money from my budget when the "Results so far" explicitly state that I (bidder 0) won a lot at a given price.
- If I lose or get outbid on a lot, no money is deducted.
- In every turn, accurately calculate: $\text{current\_remaining\_budget} = \text{starting budget} - \sum (\text{prices of lots won by bidder 0 so far})$.
- In every response, state the exact calculated budget: `[budget: current_remaining_budget]`.
- My hard upper limit for any bid is $\min(\text{valuation} - 1, \text{current\_remaining\_budget})$. Never bid an amount that exceeds my remaining budget or equals/exceeds my valuation.

## Round 1 Strategy (Lot Setup)
- If standing high bid is 0 (no bids yet):
  - If $\text{minimum raise} < \text{valuation}$ and $\text{minimum raise} \le \text{current\_remaining\_budget}$, bid `[bid: minimum raise]`.
  - Otherwise, pass: `[bid: pass]`.
- If standing high bid $S > 0$:
  - If $S + \text{minimum raise} < \text{valuation}$ and $S + \text{minimum raise} \le \text{current\_remaining\_budget}$, bid the exact minimum allowable amount: `[bid: S + minimum raise]`.
  - Otherwise, pass: `[bid: pass]`.

## Round 2 Strategy (Final Resolution)
- If I am already holding the standing high bid, pass: `[bid: pass]`.
- If the standing high bid $S$ is held by another bidder:
  - Calculate required minimum bid: $B_{\min} = S + \text{minimum raise}$.
  - If $B_{\min} \ge \text{valuation}$ or $B_{\min} > \text{current\_remaining\_budget}$, pass: `[bid: pass]`.
  - If $B_{\min} < \text{valuation}$ and $B_{\min} \le \text{current\_remaining\_budget}$, place the minimum bid: `[bid: B_min]`.

## Formatting & Response Rules
- Keep reasoning brief (1–2 sentences).
- Always end the reply with the two required bracketed tokens in exact format:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`