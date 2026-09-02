---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 2018
---
### Playbook

- **Budget Tracking**:
  - Read the starting budget strictly from the initial rules text (e.g. "You start with a budget of X"). Do NOT assume a default starting budget like 100 if the text states 30.
  - Track true remaining budget consistently across the entire episode: `Current Budget = Starting Budget - Sum of all winning bids won by me so far`.
  - Maintain the correct starting budget baseline in every round: do not switch budget baselines mid-episode (e.g., reporting 30 in Round 1 and then reporting 100 in Round 2).
  - In every reply, always include both exact bracketed tags: `[bid: X]` (or `[bid: pass]`) and `[budget: Y]`.

- **Calculating Minimum Required Bid**:
  - Minimum valid bid is `standing_high_bid + minimum_raise`. If standing bid is 0, the minimum opening bid is `minimum_raise`.

- **Evaluating Bids**:
  - When the minimum required bid is strictly less than my private valuation (`min_bid < value`) AND less than or equal to my remaining budget (`min_bid <= budget`), bid the minimum valid amount.
  - When the minimum required bid is greater than or equal to my private valuation (`min_bid >= value`), output `[bid: pass]`. Never bid up to or above value for zero or negative surplus.
  - When the minimum required bid exceeds my remaining budget (`min_bid > budget`), output `[bid: pass]`.

- **Bidding Strategy by Round**:
  - **Round 1/2**: Bid the exact minimum valid raise if profitable (`min_bid < value` and `min_bid <= budget`), keeping the price as low as possible.
  - **Round 2/2 (Final Round of Lot)**: Bid the exact minimum valid raise required to win if `min_bid < value` and `min_bid <= budget`. Do not jump bid or overbid beyond the minimum increment.

- **What Not To Do**:
  - Do not place large jump bids; always use the minimum valid raise to maximize surplus and preserve budget across the remaining lots.
  - Do not bid when surplus is zero or negative (`min_bid >= value`).
  - Do not hallucinate or switch the starting budget baseline between rounds.