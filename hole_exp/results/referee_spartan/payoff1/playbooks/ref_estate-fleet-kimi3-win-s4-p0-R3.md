---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 3352
---
When an unowned property is offered and I can afford it, I buy it unless doing so leaves me unable to cover likely rent payments in the coming laps; deed value counts fully toward my final score, so cash sitting idle buys nothing.

When buying, my default buffer rule is to keep at least the highest rent on the board in cash — but I don't apply it blindly. Before declining, I check my position: if I am close to START, the upcoming salary can rebuild the buffer, so a deal that would leave me thin can still be worth buying, especially for a mid-price deed with good rent.

A purchase that would take me to exactly zero is the exception: I decline it even mid-board, because any single rent landing before my next salary cannot be paid. Zero-buffer buys are never worth it no matter how good the rent-to-price ratio — that is the one hard floor.

When I decline a purchasable deed, I do so consciously, not by reflex: compare price vs. rent, expected rents owed before my next salary, and laps remaining. And I remember the circuit loops — a deed I pass on early will be offered again on a later lap, so banking income and buying it on the next pass (as I did with Quarry) recovers most of the missed value without the zero-buffer risk.

When I cannot afford a deed at all, I pass without hesitation and bank the incoming rent instead of stretching.

In the early laps I buy aggressively on high rent-to-price deeds — rents only start flowing once deeds are held, and opponents were paying rent from lap 1. Cheap deeds like Depot (50, rent 10) are near-free and should essentially always be bought.

I watch what opponents are buying, because unowned deeds get snapped up over 6 laps: with three investors circling, mid-game laps are my last chance at some deeds, so my buy threshold should loosen as the game progresses and remaining unowned deeds dwindle.

Before settling every turn, I recompute my cash from scratch: last declared balance, plus salary if I passed START, plus all rent received since my last turn (including any "since your last turn you received X" note and credits shown in the transfer log), minus the deed price and any rent I owe. I declare that full recomputed figure, not just the change.

When I land on an opponent's deed, I pay the stated rent in full via the [pay: N to P<k>] token and subtract it from my balance immediately.

When I land on my own deed or a tile not for sale, I declare [pay: none] and [buy: no] and confirm the balance, still accounting for salary or rent received that turn.

When I pass or land on START, I never forget to add the salary to my declared balance — landing on START is still a valid +25, and it often lands exactly when my buffer is thin.

In the final lap I buy nothing — a deed bought on the last lap collects no rent, and the price already counts as score either way, so holding cash is equal and safer.

I track the bank's transfer log each turn: it tells me which deeds opponents own (and thus what rents I might owe), confirms my incoming rents were credited, and lets me gauge opponents' property counts for the endgame.

I keep a running estimate of everyone else's cash plus deed value so I know whether I need to buy late or can coast; winning is relative, not absolute.

I always end my reply with the three required tokens, exactly formatted, with the balance token last.