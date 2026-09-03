---
game: ref_auction
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1720
---
# Playbook for Open Ascending Multi-Lot Auction

## Budget Management & State Tracking
- Carefully record the initial starting budget stated in the opening prompt (e.g., 30, 50, 100). Never assume or reset to a default budget like 100 mid-game.
- Maintain accurate budget tracking across lots:
  - During rounds of an active lot, my remaining budget does not change.
  - When the results show that I won a previous lot at price $P$, subtract $P$ from my remaining budget: $\text{Budget}_{\text{new}} = \text{Budget}_{\text{old}} - P$.
  - Always accurately report the true remaining budget in `[budget: N]` on every response.

## Bidding Rules & Feasibility
- Calculate the minimum valid raise: $\text{Min Valid Bid} = \text{Standing High Bid} + \text{Minimum Raise}$.
- Check the two hard constraints:
  1. **Affordability:** $\text{Min Valid Bid} \le \text{Remaining Budget}$.
  2. **Profitability:** $\text{Min Valid Bid} \le \text{Valuation}$ (ensures surplus $\ge 0$).
- If either constraint is violated, output `[bid: pass]`.
- If I already hold the standing high bid, output `[bid: pass]` to avoid bidding against myself.

## Multi-Lot Valuation & Execution
- If $\text{Min Valid Bid}$ is both affordable and profitable:
  - Bid exactly $\text{Min Valid Bid}$ in both Round 1 and Round 2 to maximize expected surplus and avoid unnecessary overbidding.
- In early lots, if budget is scarce relative to expected future opportunities, avoid spending a disproportionate fraction of my budget on marginal-surplus lots when higher-estimate lots remain.

## Response Formatting
- Keep reasoning brief (1–2 sentences).
- Always end responses with the exact required format:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`