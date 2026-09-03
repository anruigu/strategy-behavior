---
game: ref_estate
model: gemini
condition: win
seed: 2
round: 1
chars: 1109
---
When a turn is put to me, I first calculate my available cash before making any decisions. I do this by taking my last declared balance, adding my salary if the prompt states I passed or landed on START, and adding any payments made to me by other investors listed in the recent transfers since my last turn. 

When I land on a property owned by another investor, I pay the stated rent. If the rent exceeds my available cash, I pay my entire available cash balance and reduce my balance to 0.

When I land on an unowned property, I buy it if my available cash is equal to or greater than the purchase price. 

When I calculate my final balance, I subtract the exact amount I paid for rent or property purchases from my available cash.

When I format my response, I output exactly three bracketed tokens on separate lines: `[pay: N to P<k>]` (or `[pay: none]`), `[buy: yes]` or `[buy: no]`, and `[balance: N]`. 

I do not spend all my cash on property if it leaves me vulnerable to being wiped out by rent on the very next turn, though paying all remaining cash when broke is the correct mechanical resolution.