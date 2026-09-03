---
game: ref_estate
model: gemini
condition: win
seed: 2
round: 2
chars: 1295
---
When a turn is put to me, I first calculate my available cash before making any decisions. I do this by taking my last declared balance, adding my salary if the prompt states I passed or landed on START, and adding any payments made to me by other investors listed in the recent transfers since my last turn. 

When I land on a property owned by another investor, I pay the stated rent. If the rent exceeds my available cash, I pay my entire available cash balance and reduce my balance to 0.

When I land on an unowned property, I buy it if my available cash is equal to or greater than the purchase price. Because final scoring is the sum of cash and the purchase price of held deeds, buying a property converts cash into deed value at a 1:1 ratio, meaning it never reduces my final score to buy. However, I am cautious not to spend all my cash on a property in early laps if it leaves me vulnerable to being wiped out by rent on the very next turn. On the final lap, this risk is eliminated.

When I calculate my final balance, I subtract the exact amount I paid for rent or property purchases from my available cash.

When I format my response, I output exactly three bracketed tokens on separate lines: `[pay: N to P<k>]` (or `[pay: none]`), `[buy: yes]` or `[buy: no]`, and `[balance: N]`.