---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 1876
---
My playbook for ref_estate:

- Every turn, before declaring my balance, I do the arithmetic from my last declared balance: subtract rent paid, add any incoming transfers reported, add salary if I passed START, subtract the purchase price if I buy. The declared balance must reflect this exactly, since scoring counts declared cash plus deed values.

- Buy any unowned property early whenever the price leaves me enough to survive one full lap of plausible rents (~30–60 cash buffer). Deeds count at full purchase price in the final score, so buying early is close to free money plus future rent income.

- In the later half of the game, tighten the rule: buy only if the purchase leaves me a real buffer against the biggest rents on the circuit, since I may not live long enough to recoup the rent. I skipped a late purchase to protect an 11-cash remainder—that was right; bankruptcy risk outweighs late deed value when rents still loom.

- When I pass or land on START, I always remember to add the salary before declaring my balance—do not forget free income.

- When I land on property I own, declare [pay: none] and [buy: no], and fold in any incoming transfers before stating the balance.

- When I land on an opponent's property, pay the rent immediately and state the reduced balance; never skip or understate it, since the bank's book records it independently.

- I keep my own ledger mentally across turns and cross-check "since your last turn you received X" against the transfers log before balancing. I do not trust my last declared balance alone—adjust it first.

- If affordable mid-game and buffer looks thin, prefer cheap properties (low price, decent rent) over premium ones; the win is final cash plus deed prices, not rent ROI alone, and overpaying leaves me exposed.

- End every reply with the required bracketed balance token so the turn settles cleanly.