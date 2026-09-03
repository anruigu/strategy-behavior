---
game: ref_estate
model: gemini
condition: win
seed: 5
round: 2
chars: 993
---
When checking my balance at the beginning of a turn, I take my last declared balance and explicitly add any income stated in the prompt, looking carefully for "Since your last turn you received X" and "You passed START, so you may collect your salary of Y".

When I land on an unowned property, I buy it if I have enough cash. Because the final score calculates my total net worth as cash plus the purchase price of deeds, converting cash to property never hurts my final score, even on the final lap, and early purchases generate rent.

When I land on a property owned by another investor, I subtract the rent from my updated balance, output `[pay: N to Pk]` (without angle brackets around the player number, e.g., `[pay: 12 to P2]`), and output `[buy: no]`.

When I land on my own property, I output `[pay: none]` and `[buy: no]`.

When I output my decisions, I always include the exact tokens `[pay: ...]`, `[buy: ...]`, and `[balance: N]` on their own lines at the very end of my response.