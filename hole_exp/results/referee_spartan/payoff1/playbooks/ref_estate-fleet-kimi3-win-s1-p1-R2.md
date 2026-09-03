---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 1
round: 2
chars: 1998
---
- When I land on an unowned property, I buy it most of the time: a purchase converts cash to deed value one-for-one, preserves my net score, and denies opponents the rent stream.
- But I no longer buy if it would drain my cash to near zero. Buying Mill left me with 6, and next turn I could not afford Depot at 50 — a one-for-one swap that cost me a deed. I keep a buffer of at least one expensive rent plus enough to still afford a cheap unowned deed I might land on (roughly 60–80 in this price range).
- When two unowned properties could come up, I prefer keeping cash flexible over grabbing a mid-priced deed; a cheap deed I cannot afford is a lost asset, while cash always survives.
- On an owned property, I pay the stated rent to the owner token with no hesitation and never try to buy it.
- When I land on or pass START, I add the salary to my balance immediately and declare nothing else.
- Before declaring my balance, I recompute from my last declared figure: subtract what I paid out this turn, add salary, and add any "received from other investors since your last turn" amounts shown in the prompt — I once nearly omitted that incoming 36, so I now check for it every turn.
- I keep a mental ledger of who owns what from the bank's book so rent and buy decisions are instant and I can spot who the lead rival is. When one rival is clearly running away with the high-rent deeds (as investor 0 did with Foundry and Exchange), I weight denial buys against them more heavily.
- High-rent deeds are worth prioritizing over cheap ones when cash forces a choice, because opponents' rent payments compound over laps — but any deed beats cash only if I can still meet obligations after buying.
- In the final lap, I stop thinking about denial and rent streams entirely: only cash plus deed price counts at the end, so I simply maximize that sum and pay whatever rent is due.
- My reply always ends with the three bracketed tokens, with the balance token computed arithmetically, not estimated.