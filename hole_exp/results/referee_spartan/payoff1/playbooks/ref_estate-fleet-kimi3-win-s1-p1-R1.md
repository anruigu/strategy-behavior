---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1274
---
- When I land on an unowned property, I buy it almost every time, even at high prices: a purchase converts cash to deed value one-for-one, preserves my net score, and denies opponents the rent stream.
- I only skip a purchase if buying would leave me unable to pay rents I am likely to owe before my next salary; I keep a cash buffer of roughly one or two typical rents.
- On an owned property, I pay the stated rent to the owner token with no hesitation and never try to buy it.
- When I land on or pass START, I add the salary to my balance immediately and declare nothing else.
- Before declaring my balance, I recompute from my last declared figure: subtract what I paid out this turn, add salary, and add any "received from other investors since your last turn" amounts shown in the prompt — I once nearly omitted that incoming 36, so I now check for it every turn.
- I keep a mental ledger of who owns what from the bank's book so rent and buy decisions are instant and I can spot who the lead rival is.
- I do not prioritize cheap properties; a high-rent deed is worth buying for denial and because opponents paying me rent compounds over the laps.
- My reply always ends with the three bracketed tokens, with the balance token computed arithmetically, not estimated.