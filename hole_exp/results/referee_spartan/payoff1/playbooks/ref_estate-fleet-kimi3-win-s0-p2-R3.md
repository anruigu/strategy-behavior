---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 3446
---
- On an early lap, when I land on an unowned property and can afford it without going below a cash buffer covering imminent rents, I buy it — deeds count at full price toward my final score, so cash converted to property loses nothing on paper and gains rent income.
- I passed on Mill (90) holding 112 at lap 3 and it stayed a loss all game: that deed alone would have been worth more than my whole final margin. My buffer rule was too conservative. The real question is narrower: can this purchase leave me unable to pay a rent I am likely to owe before my next salary? Buying with 112 left when the worst rent is 30 and salary of 25 comes each lap was safe — I should have bought.
- Before declining a purchase, I compute the worst case: price paid, then minus the highest rent I could owe before next passing START, plus that salary. If the result stays at or above zero, I buy. A static 40+ buffer wastes scoring opportunities.
- Late in the game especially, any unowned tile I land on is pure gain if I can pay for it at all — a deed converts cash to equal score and can only add rent; on the final laps there is no downside worth naming. If I land on an unowned property on the last lap or two and have the cash, I buy regardless of buffer.
- I do not spend myself down to near zero when a rent payment is clearly due before I can collect salary — insolvency risk is the only real reason to pass on a deed.
- This episode I could not buy Exchange (120) holding only 86 on lap 3 — the tile went to no one and I lost the chance entirely. Since deeds are score-neutral to buy, the binding constraint is cash on hand when I land, so I should treat surplus cash early as purchase ammunition and avoid letting my balance drift below the price of the priciest unowned tile I am likely to reach, as long as rents due are still covered.
- When other investors owe me rent, those receipts may arrive while it is not my turn; I add them to my balance at my next settlement along with any salary for passing START. I treat my declared balance as cash plus everything the "since your last turn you received" line and the book show I collected.
- I never double-count: I reconcile the "received since last turn" figure against the transfer log before adding it, so a payment I already booked is not added twice.
- When I land on an owned property, I pay the exact rent to the owner immediately and subtract it from my balance in the same turn; I never declare a balance that ignores the rent.
- When I land on or pass START, I always claim the salary that turn — it is free cash and easy to forget, and I remember that landing on START also means collecting.
- When I land on my own property or on START, I reply [pay: none] and [buy: no] and keep the arithmetic simple; there is nothing to overthink.
- I track the transfer log each turn so I know which tiles are owned and which are still available — landing spots others haven't reached yet are where my future buying chances lie, and I can anticipate which rents I am likely to owe on my next circuit.
- I watch which properties the leaders hold; high-rent tiles owned by an opponent I will land near soon are the ones to hold cash for — every other purchase decision comes second to covering those.
- I always end my reply with all three bracketed tokens in the exact required format, with the balance token last, computed as: previous balance + salary + rent received − rent paid − purchase price.