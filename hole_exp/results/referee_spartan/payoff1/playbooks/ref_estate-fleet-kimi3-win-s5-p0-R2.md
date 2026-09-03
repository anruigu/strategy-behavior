---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 5
round: 2
chars: 2467
---
- When I land on an unowned property, I buy it whenever I can afford it, because deeds count at full purchase price in the final score while cash spent is gone either way. This episode confirmed it: converting 270 of cash into deeds was exactly what set my final score of 291.
- When cash is tight, I still buy any property I can fully afford; only skip a purchase if it would leave me unable to pay an unavoidable rent before my next income event. This episode I dropped to 11 cash after buying Wharf and it worked out — incoming rents covered the next rent due.
- When I land on START or pass it, I always add the salary to my balance in that turn's declaration.
- When the prompt says "since your last turn you received N," I add N to my last declared balance before doing anything else.
- When I land on a property I own, I pay nothing and buy nothing.
- When I land on a property someone else owns, I pay the stated rent to that investor and subtract it from my balance.
- I keep my own running ledger every turn: last balance, plus receipts, plus salary if applicable, minus rent paid, minus purchase price. I never trust memory across turns.
- Before declaring, I check the recent transfer list to confirm which receipts actually came to me and that I haven't missed a payment I owe.
- In early laps I prioritize buying over hoarding cash, since rents received compound and deed value offsets the spend entirely.
- With a fixed lap limit, I treat low cash as low risk in the late game: after my last purchase, remaining rents owed are few and usually covered by incoming rent, so I do not hold back out of caution.
- Buying the highest-rent affordable properties early (e.g. Foundry, Mill) pays off fastest — my 24-rent deeds generated multiple payments over 6 laps.
- I check whether opponents are snapping up the cheap properties; if they are, the competition for deeds makes my own buying even more urgent, since unowned properties left for later effectively subsidize rivals.
- When nothing is due, I explicitly declare [pay: none] and [buy: no] rather than omitting tokens — a missing token risks a misparsed turn.
- I always end my reply with the three required bracketed tokens, and I double-check the balance number matches my ledger arithmetic before sending.
- When rent income arrives on others' turns, I note which of my deeds are generating it, so I can judge whether my early buying is paying off and adjust my buying threshold for the next game.