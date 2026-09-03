---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 7
round: 2
chars: 2108
---
My playbook for ref_estate:

- When I land on an unowned deed and can afford it, I buy it, even if it nearly empties my cash. Deeds count at full purchase price in final scoring, so cash and deeds are worth the same at the end — but deeds also earn rent in between. This episode bore it out: buying Foundry (100) and Mill (90) down to a 10 balance still left me ahead.
- When deciding to buy, I only check that purchase price ≤ my cash (including any rent credited since my last turn, which I add first). I do not hold back a safety buffer; salary keeps coming and rents are small.
- When the prompt says I received rent since my last turn, I add that amount to my balance before anything else — it's easy to forget because it arrives between turns.
- When I land on someone else's deed, I immediately pay the stated rent to that owner and deduct it from my balance — no hesitation, no miscounting the payee.
- When I pass START, I add the salary to my balance the same turn, before declaring, and I only add it when the prompt says I passed START.
- I track my balance as: previous declared balance + salary (if any) + rent received since last turn − rent paid − purchase price. I recompute from my last declared balance each turn, not from memory of the whole game.
- I keep my arithmetic honest — every balance I declare must match the transfers the bank recorded, since transfers are public and discrepancies would be caught.
- I end every reply with all three tokens: [pay: ...], [buy: ...], [balance: N], and I make sure the reply ends with a bracketed token. No stray trailing text after the final token.
- On a tile that is neither purchasable nor rent-charging (including my own deeds), I declare [pay: none] and [buy: no] and just update the balance with any salary or incoming rent.
- When I cannot afford a deed, I skip it without regret, but I note what rivals bought so I know which tiles will charge me rent on later laps.
- Early aggressive buying works best: the earlier a deed is bought, the more laps of rent it can collect, and thin cash recovers via salary and rent before the final lap.