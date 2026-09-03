---
game: ref_estate
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1272
---
# Playbook for ESTATE

- **Purchasing Properties**: When landing on an unowned property, always choose `[buy: yes]` if available cash covers the purchase price. Properties contribute their full purchase price to final net worth while generating recurring rent.
- **Handling Rent Payments**:
  - When landing on an opponent's property, format the payment token strictly as `[pay: N to P<k>]` where `N` is the rent due and `k` is the owner's investor index.
  - When landing on START, unowned land, or my own property, output `[pay: none]`.
- **Handling Ineligible Buys**: When landing on START or an already owned property, always output `[buy: no]`.
- **Calculating Declared Balance**:
  - Start with the previous turn's declared balance.
  - Add salary (25) if passing or landing on START.
  - Add all incoming rent received from other investors since the last turn (as listed in prompt / transfer log).
  - Subtract rent paid to an opponent (`N` in `[pay: N to P<k>]`).
  - Subtract property price if buying this turn (`[buy: yes]`).
  - Report the resulting total exactly in `[balance: N]`.
- **Formatting**: Keep reasoning to one or two concise lines, then conclude with the three exact bracketed tokens in order:
  - `[pay: ...]`
  - `[buy: ...]`
  - `[balance: ...]`