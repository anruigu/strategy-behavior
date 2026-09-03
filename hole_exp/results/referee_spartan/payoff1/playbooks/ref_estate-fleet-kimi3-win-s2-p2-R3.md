---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 2
round: 3
chars: 2918
---
Playbook for ref_estate:

- Before settling any turn, I recompute my cash from my last declared balance plus every transfer to me shown in the bank's book since my last turn; I never trust the "last declared balance" alone, because rent income arrives between my turns.
- The prompt sometimes explicitly says "since your last turn you received N from other investors." When it does, I cross-check that N against the bank's book lines; when it does not, I still scan the book myself. Adding this income to my balance before subtracting this turn's rent is where errors would creep in — I do it first.
- When I land on an owned property, I pay the exact rent to the named owner and subtract it. When I land on an unowned property, no rent is due and the only question is whether to buy. When I land on START, there is no deed and nothing to pay — I only collect salary.
- Passing or landing on START always pays the salary; I add it in the same settlement even when the turn feels uneventful.
- I buy any unowned property I land on unless I literally cannot afford it or buying would leave me unable to survive likely upcoming rents. Deeds count at purchase price toward my final score, so buying converts cash to score one-for-one while also generating rent; passing a buy I can afford is almost always a mistake. This episode I bought Wharf at 108 → 28 usable after one known rent, and it paid off; I correctly passed Mill at 78 cash vs 90 price because I couldn't afford it at all.
- My rent buffer rule: buy if post-purchase cash covers at least the highest rent on the board I might hit before my next START pass. Do not go to near-zero unless it is the final lap.
- Early in the game the board fills fast — this episode every deed was owned by lap 4, and opponents bought aggressively on laps 1–3. Hesitating early means renting forever on a full board, so I bias strongly toward buying on laps 1–2 whenever affordable.
- On the very last turn, buying an unowned deed is score-neutral (cash converts one-for-one into deed value) if no one will land on it later, and strictly good if later turn order lets opponents land on it. Buy it; there is no downside. If the last turn lands me on an owned deed, I just pay rent — nothing else to decide.
- I track who owns what from the bank's book each turn: clusters of adjacent enemy deeds raise my expected rent per lap, which raises the buffer I keep and makes my own cheap buys more urgent.
- My final score is declared cash plus purchase price of my deeds; rent collected and salary are pure gain, rent paid is pure loss. Nothing else matters.
- I write the brief reasoning to show the arithmetic chain (last balance + incoming transfers − rent/price = result), so a bookkeeping slip is visible before I commit.
- I always emit the tokens exactly once each, in order: pay first, then buy or no-buy, then my post-turn balance last, ending my reply on the balance token.