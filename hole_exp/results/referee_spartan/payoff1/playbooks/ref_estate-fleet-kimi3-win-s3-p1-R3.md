---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 4335
---
When the settle prompt appears, I reply with the three required tokens — [pay:], [buy:], and [balance:] — and make sure my response ends with [balance: N]. I keep any reasoning brief and make the arithmetic easy to follow.

I settle events in this order: add rent payments received since my last turn, add salary when I pass or land on START, pay any stated rent, then buy or decline an available unowned deed. I calculate from my last declared balance and reconcile against the reminder of any transfers received.

When I land on a tile owned by another investor, I pay the shown rent to that owner and subtract it from my balance. I do not second-guess the amount or accidentally send it to the bank.

When I pass or land on START, I add the salary even if no other action occurs. Missing this is free money left unclaimed.

When I land on an unowned tile and have enough cash, buying is usually correct because the final score includes both cash and the deed's purchase price, so a purchase preserves score immediately and can generate future rent. A purchase also blocks rivals from collecting that rent later.

I prioritize expensive, high-rent deeds such as Foundry and Exchange when possible. In my last episode, buying Foundry (100 price, 24 rent) on lap 2 generated 48 in received rent over the remaining laps — nearly half its price back — confirming that high-rent deeds bought early are the best investments available.

Before buying, I check the post-purchase cash position against known upcoming rent drains. Buying Foundry left me at 82, and I immediately faced a 30 rent at Exchange; that was survivable, but I treat the reserve question seriously: post-purchase cash should cover the most expensive owned tile I am likely to hit, or I risk nothing worse than a thin stretch — there is no bankruptcy penalty mentioned, but liquidity keeps later buying options open.

I estimate a deed's remaining value by comparing its rent against the laps and likely landings left, plus guaranteed salary passes. Early purchases have many chances to pay rent; late purchases mainly preserve score through deed value and deny opponents the asset. On the final lap, a purchase is still score-neutral at worst, so I buy anything affordable unless a better unowned tile might still come up.

I track all deeds, their owners, prices, and rents, including rivals' purchases shown in the transfer book. This lets me anticipate major rent drains such as Exchange and know which unowned opportunities remain.

When my cash is low, I budget for known high-rent owned tiles instead of assuming a favorable roll. There is no way to avoid those rents, so I accept them and preserve liquidity where possible.

When I land on my own deed, nothing is due: [pay: none], [buy: no], and the balance only reflects income received since last turn.

When I cannot afford an unowned tile, I decline and declare my full balance accurately. I do not claim a purchase I cannot pay for.

On every turn, I explicitly check whether "since your last turn you received" money applies. That income must be included before rent or purchases, and I cross-check the amount against my own deed portfolio and the transfer book (e.g., rivals landing on my Foundry should appear as payments to me). I never derive my balance only from the previous settlement line.

Before submitting, I recompute: previous declared balance + received rent + salary − paid rent − purchase price = new declared balance. I use the bank's transfer list as a check on whom to pay and whether expected rent income exists.

If my declared balance is challenged or an adjudication summary lists claimed transfers, I compare it with my turn-by-turn ledger and correct only genuine arithmetic mistakes, not disadvantageous legal payments.

I keep token values consistent: [buy: yes] means the listed purchase is included in the declared balance; [pay: none] means no rent payment that turn; and [balance: N] is my final cash after all additions, payments, and purchases.

I remember the win condition is declared cash plus deed purchase prices, not cash alone — so spending cash on deeds does not lower my score, hoarding cash does not raise it, and the only real gains come from salary and net rent flow. Accurate declarations matter as much as good buys, since my declared balance is what counts.