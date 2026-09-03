---
game: ref_auction
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1737
---
# Playbook for Open Ascending Multi-Lot Auction

## Budget Management & State Tracking
- Start by noting the initial starting budget explicitly given in the prompt; never hallucinate or reset the budget to a default like 100.
- Track my remaining budget continuously:
  - When I am bidding within the current lot, my remaining budget does not decrease until I actually win the lot.
  - When a previous lot has been won by me at cost $C$, immediately subtract $C$ from my previous remaining budget to form the new current budget: $\text{Budget}_{\text{new}} = \text{Budget}_{\text{old}} - C$.
  - Always report my accurate remaining budget in `[budget: N]` on every turn.

## Bidding Strategy
- Before placing any bid, calculate the minimum valid bid: $\text{Min Bid} = \text{Standing High Bid} + \text{Minimum Raise}$.
- Evaluate the lot value against both my budget and profitability:
  - If $\text{Min Bid} > \text{My Valuation}$ (no positive surplus), output `[bid: pass]`.
  - If $\text{Min Bid} > \text{Remaining Budget}$ (unaffordable), output `[bid: pass]`.
- When $\text{Min Bid} \le \text{My Valuation}$ and $\text{Min Bid} \le \text{Remaining Budget}$:
  - In Round 1: Bid exactly $\text{Min Bid}$ to stay in contention without driving up the price prematurely.
  - In Round 2 (Final Round for the lot): Bid exactly $\text{Min Bid}$ to lock in maximum surplus ($\text{Valuation} - \text{Bid}$) if it remains profitable and within budget.
- If I am already holding the standing high bid (my own bid is highest), pass to avoid raising myself.

## Response Formatting
- Keep reasoning strictly to one or two concise sentences.
- Always conclude replies with the exact required tags:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`