---
game: ref_estate
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 2312
---
**Playbook for ESTATE**

- I track my net worth, not just cash: cash + purchase price of my deeds. A purchase doesn't cost me net worth, it converts cash to deed value. When buying, I'm asking whether the deed's rent stream beats holding cash — and cash earns nothing here.

- When an unowned tile is put to me and the purchase leaves me with a nonnegative balance, I buy. Rent-to-price ratio matters: prefer anything at or above roughly 20% (rent/price). Exchange at 120/30 (25%) was a clear buy and was my only real value-creator this game.

- I will spend down to near zero on strong properties early — salary (25/lap) refills me and the win condition counts deeds at full purchase price. Buying Exchange with 42 left over was correct; I never went bankrupt. But I should note the cost: spending down left me unable to buy Mill (90) on lap 4 when I had only 42. That's an acceptable trade when the first buy is strong, but if a weaker tile would leave me too poor for a better one later, I should weigh that. In a 6-lap game with 3 investors, the property set is limited — every tile someone else buys is rent I pay or value I lack.

- Landing on my own tile costs nothing: I just confirm balance unchanged.

- When rent is due, I pay promptly and update balance exactly: last declared balance − rent paid + any salary collected this turn. Passing START means +25 before any payment; my final turn (32 + 25 − 12 = 45) shows the full chain must be applied in order.

- When my cash is below the price of an unowned tile, I decline — I cannot buy what I can't pay for, and I should say so plainly.

- I watch the bank's transfer log to gauge opponents' positions. Investors 0 and 1 bought nearly every tile they touched; the board filled fast. With only 8 tiles and 3 investors, buying any tile early both adds to my score and denies them rent income.

- My final score was 165 (cash 45 + Exchange 120) — not a win. The lesson: one purchase wasn't enough against opponents who owned 5 tiles between them. Next time I should push to own 2+ tiles, even if that means buying cheaper properties (Depot 50, Quarry 60) when the big ones are out of reach, since deed value counts at full price regardless of rent rate.

- At the final lap, I make sure my declared balance is exact, since the score is computed from it.