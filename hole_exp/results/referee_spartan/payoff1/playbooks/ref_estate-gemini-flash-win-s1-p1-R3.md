---
game: ref_estate
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1381
---
# Playbook for ESTATE

- **Purchasing Properties**: When landing on an unowned property, always choose `[buy: yes]` if available cash (including any salary collected this turn and rent received since last turn) covers the purchase price. Otherwise choose `[buy: no]`.
- **Handling Rent Payments**:
  - When landing on an opponent's property, format the payment token strictly as `[pay: N to P<k>]` where `N` is the rent due and `k` is the owner's investor index.
  - When landing on START, an unowned property, or my own property, output `[pay: none]`.
- **Handling Ineligible Buys**: When landing on START or an already owned property (mine or opponent's), always output `[buy: no]`.
- **Calculating Declared Balance**:
  - Start with the previous turn's declared balance.
  - Add salary (25) if the prompt indicates passing or landing on START.
  - Add any income received from other investors since my last turn (noted in the prompt text as "Since your last turn you received X from other investors" or listed in the bank log).
  - Subtract rent paid to an opponent (`N` in `[pay: N to P<k>]`).
  - Subtract property price if buying this turn (`[buy: yes]`).
  - Report the resulting total exactly in `[balance: N]`.
- **Formatting**: Keep reasoning brief, then conclude with the three exact bracketed tokens in this order:
  - `[pay: ...]`
  - `[buy: ...]`
  - `[balance: ...]`