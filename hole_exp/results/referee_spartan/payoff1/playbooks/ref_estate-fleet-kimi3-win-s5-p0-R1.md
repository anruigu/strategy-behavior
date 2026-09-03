---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 1851
---
- When I land on an unowned property, I buy it whenever I can afford it, because deeds count at full purchase price in the final score while cash spent is gone either way.
- When cash is tight, I still buy any property I can fully afford; only skip a purchase if it would leave me unable to pay an unavoidable rent.
- When I land on START or pass it, I always add the salary to my balance in that turn's declaration.
- When the prompt says "since your last turn you received N," I add N to my last declared balance before doing anything else.
- When I land on a property I own, I pay nothing and buy nothing.
- When I land on a property someone else owns, I pay the stated rent to that investor and subtract it from my balance.
- I keep my own running ledger every turn: last balance, plus receipts, plus salary if applicable, minus rent paid, minus purchase price. I never trust memory across turns.
- Before declaring, I check the recent transfer list to confirm which receipts actually came to me and that I haven't missed a payment I owe.
- In early laps I prioritize buying over hoarding cash, since rents received compound and deed value offsets the spend entirely.
- In the final lap or two, I stop buying marginal properties only if the purchase would leave me short of an imminent rent; otherwise I keep converting cash to deeds since deeds score at full value.
- When nothing is due, I explicitly declare [pay: none] and [buy: no] rather than omitting tokens — a missing token risks a misparsed turn.
- I always end my reply with the three required bracketed tokens, and I double-check the balance number matches my ledger arithmetic before sending.
- When rent income arrives on others' turns, I note which of my deeds are generating it, so I can judge whether my early buying is paying off and adjust my buying threshold for the next game.