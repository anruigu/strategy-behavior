---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2008
---
# Auction Playbook

## Budget Tracking
- Read my actual starting budget carefully from the initial rules prompt (e.g. 30, 100, etc.) and record it precisely; never hallucinate or reset starting budget to 100 on subsequent turns.
- Keep accurate accounting: remaining budget $N$ is always `initial starting budget - sum(winning bids where results state bidder 1 won)`.
- Always output `[budget: N]` with this accurately tracked remaining budget on every single turn.
- A bid must never exceed my remaining budget $N$.

## Valuation and Passing Rules
- Treat my private valuation as a hard ceiling. Never bid $\ge$ my valuation.
- If the minimum legal bid (standing high bid + minimum raise, or the minimum opening raise if standing bid is 0) is $\ge$ my valuation or exceeds my remaining budget, output `[bid: pass]`.
- If I already hold the standing high bid in Round 2, output `[bid: pass]` to avoid bidding against myself.

## Bidding Strategy by Round
- **Round 1 (Opening/Probing):**
  - Bid exactly the minimum legal bid (standing bid + minimum raise, or minimum raise if opening) if it is strictly below valuation and within budget.
  - Never jump bid or overbid in Round 1.
- **Round 2 (Final/Closing):**
  - Determine the minimum legal bid (`standing high bid + minimum raise`).
  - Calculate maximum allowable bid: `min(valuation - 1, remaining budget)`.
  - If the lot offers high surplus (valuation significantly above the standing bid), place a competitive bid above the minimum legal bid (e.g. minimum legal bid + 1 to 2 increments) up to the maximum allowable bid to secure the win against competing raises.
  - If surplus is small or budget is tight, place the exact minimum legal bid.
  - If the minimum legal bid exceeds maximum allowable bid, pass.

## Response Format
- Keep reasoning brief (1–2 sentences explaining legal bid calculation and valuation surplus).
- Conclude strictly with the two required tokens on separate lines at the end:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`