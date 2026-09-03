---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 2818
---
My job in this game is to maximize declared cash plus deed values at the end, so my working rule is: buying is free on net worth — spending cash on a deed converts, never loses — the only real cost is liquidity going to zero.

- When I land on an unowned property and have at least the price in cash, I buy it. The deed counts at face value toward my final score, so there is no downside except losing rent-paying liquidity, and the deed pays rent back. This holds: buying Quarry and Wharf converted cash to full-value deeds, and Quarry paid me rent mid-game.
- Buy on the **last lap** too: I bought Wharf on lap 6 with no future rent possible, and it still scored its full 80 as a deed. A deed is never worth less than the cash I paid, so an affordable buy is never a mistake at any point in the game.
- When my cash after purchase would be very low, I still buy. Low cash only hurts if I later can't afford a deed — rent owed is fixed and small, and going near zero has never cost me.
- When the price exceeds my cash, I declare [buy: no]; I check affordability first so the decision is instant.
- When I land on my own property, I pay nothing and buy nothing; I just re-declare my updated balance.
- When I pass or land on START, I add the salary into my balance before declaring.
- When I receive rent between turns, I fold it into the new balance — **exactly once**. This episode's error was the mirror of last time's: on lap 5 I correctly added the 12 received (76 + 12 + 25 = 113), but on lap 6 I added that same 12 again from the transfer list and declared 45 when my true cash was 33. Rule: the "since your last turn you received X" line is consumed by the current turn's balance; the bank's transfer list is only for finding payments the received-line **missed**. Before crediting myself anything from the list, I check whether it was already in a received-line I used.
- I still scan the bank's transfer list each turn for payments to me, but only to catch items not already covered — last episode I under-counted by missing one, this episode I would have over-counted by double-adding one. The ledger must be traceable: prior balance + salary if passed START + rent received (once) − rent paid − purchases.
- When sizing up a purchase, rent-to-price near 0.2+ (Exchange 30/120, Foundry 24/100) is strong, but even cheap low-rent deeds are worth buying when affordable because the deed itself is full value.
- Early purchases compound: on a short 8-tile circuit every property gets hit often, so there is effectively no bad purchase I can afford. This game I only got two buying chances and took both.
- Every turn I reply with exactly the three tokens, balance computed from the formula above, reconciled against the bank's transfer list without double-counting, and I never declare a number I can't trace.