---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 7
round: 3
chars: 2535
---
My playbook for ref_estate:

- When I land on an unowned deed and can afford it, I buy it, even if it nearly empties my cash. Deeds count at full purchase price in final scoring, so cash-to-deed is value-neutral at the end, but deeds earn rent in between. This episode bore it out: Foundry and Terrace bought early collected rent that kept me solvent (final score +217).
- Early buying matters most — a deed bought on lap 1 can earn rent across several later laps, and thin cash recovers through salary and incoming rent.
- When deciding to buy, I only check that purchase price ≤ my cash after adding any rent received since my last turn. I do not hold back a big safety buffer; salary keeps arriving (25 per pass) and individual rents are small.
- When the prompt says I received rent since my last turn, I add that amount to my balance before anything else — it arrives between turns and is easy to miss. Only apply amounts the prompt states.
- When the prompt does NOT mention incoming rent, I do not assume any; I trust the stated numbers and the bank's book over guesses.
- When I land on someone else's deed, I pay the stated rent to that owner immediately and deduct it — I double-check the payee against the ownership the prompt states.
- When I pass or land on START, I add the salary that same turn, before declaring, and only when the prompt says I passed/collected. Lap numbering may not match my intuition — I follow the prompt, not my own lap math.
- I track my balance as: last declared balance + salary (if any) + rent received − rent paid − purchase price. I recompute from my own last declared balance each turn.
- My declared balance must be consistent with the public transfer book — the bank records transfers, so honest arithmetic is the only safe option.
- I end every reply with all three tokens: [pay: ...], [buy: ...], [balance: N], with nothing after the final token. For rent I use [pay: N to P<k>].
- On a tile that is neither purchasable nor rent-charging — my own deed, START, or an owned tile with nothing due — I declare [pay: none], [buy: no], and just apply salary or incoming rent.
- Landing on my own deed costs nothing and earns nothing from the bank; worth remembering so I don't mistakenly pay myself rent.
- Even a low cash balance is not a crisis if rivals still owe me rent opportunities; my deeds do the income work while my cash turns over.
- I keep an eye on what rivals buy (the transfer book lists it) so I know which tiles will tax me on future laps and can anticipate those pay lines.