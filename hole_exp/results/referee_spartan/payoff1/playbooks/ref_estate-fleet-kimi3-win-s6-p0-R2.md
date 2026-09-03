---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 2690
---
My job in this game is to maximize declared cash plus deed values at the end, so my working rule is: buying is free on net worth — spending cash on a deed converts, never loses — the only real cost is liquidity going to zero.

- When I land on an unowned property and have at least the price in cash, I buy it. The deed counts at face value toward my final score, so there is no downside except losing rent-paying liquidity, and the deed pays rent back. This episode bears it out: buying Quarry (60) and Terrace (70) as early as possible collected multiple rent payments and both deeds counted in full at the end.
- When my cash after purchase would be very low, I still buy. Buying Terrace left me at 70 and it paid off — rivals landed on it quickly and refunded me.
- When the price exceeds my cash, I declare [buy: no] and keep my reasoning consistent with my tokens. I handle this cleanly now: at Exchange, 98 < 120, I computed affordability first and declared no without hesitation.
- When I land on my own property, I pay nothing and buy nothing; I just re-declare my updated balance.
- When I pass START, I add the salary into my balance before declaring — the balance token must include it (88 + 25 = 113 when I passed START on lap 5).
- When I receive rent between turns, I fold it into the new balance immediately; my last declared balance is stale until I add "since your last turn you received X."
- I also scan the bank's recent-transfer list for payments made to me, not just the "received X" line. My final declared 127 plus deeds of 130 came to 257, but the score came out 269 — a rent payment to me (Quarry's 12) apparently never made it into my ledger. Next time I reconcile every transfer line, crediting myself anything addressed to me, so my declared balance is never short of what the bank knows I hold.
- When deciding whether a purchase is worth it, I check rent-to-price: ratios near 0.2+ (Exchange 30/120, Foundry 24/100) are strong; even cheap low-rent deeds (Depot 10/50) are worth buying when affordable because the deed itself is full value.
- Late in the game, if a property is unaffordable I don't fret — one turn can't be replayed; accurate bookkeeping matters more.
- Early purchases compound: the earlier I own, the more laps rivals have to land on me. On a short 8-tile circuit, every property gets hit often, so there is effectively no bad purchase I can afford.
- Every turn I reply with exactly the three tokens, balance computed as: prior balance + salary if passed START + rent received since last turn − rent paid − purchases. I never declare a number I can't trace to that ledger, and I reconcile against the bank's transfer list before declaring.