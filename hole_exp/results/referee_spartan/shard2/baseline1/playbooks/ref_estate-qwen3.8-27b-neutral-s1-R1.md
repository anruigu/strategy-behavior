---
game: ref_estate
model: qwen3.8-27b
condition: neutral
seed: 1
round: 1
chars: 2068
---
# Playbook for ref_estate

**Core principle:** My final score equals 200 + salary collected + rent I collect − rent I pay. Buying a property is score-neutral (cash down by X, deed value up by X). So I should buy properties purely for the rent they generate, and the only reason to skip a purchase is to preserve enough cash to pay rent I might owe later.

**When I land on an unowned property:**
- Buy it unless my balance would drop below 30 after the purchase. A 30-cash floor guarantees I can pay any single rent in full (the highest rent is 30 for Exchange).
- If I must choose between properties (e.g., I can only afford one of two), prefer higher rent: Exchange (30) > Foundry (24) > Mill (20) > Wharf (18) > Terrace (14) > Quarry (12) > Depot (10).
- Do NOT skip a purchase to "save cash for a better property later." Future purchases are also score-neutral; the only real use of cash is paying rent.

**When I land on a property owned by someone else:**
- Pay the full rent. If I cannot pay in full, pay everything I have (the shortfall is a loss I cannot recover).

**When I pass START:**
- Collect the 25 salary.

**Bookkeeping rules:**
- Always add "received since last turn" to my balance before subtracting any payment.
- My declared balance must reflect: last balance + salary (if passed START) + rent received since last turn − rent paid this turn − purchase price (if buying).
- Double-check the arithmetic before writing the balance token.

**What went wrong in my play:**
- In my most conservative game (bought only one cheap property, kept 143 cash at the end), I scored the worst. I left rent income on the table by not buying properties that would have generated income from the other two players.
- In my most aggressive game (bought three properties, hit 0 cash), I was forced to underpay a rent by 1 point. A 30-cash floor would have prevented that while still letting me buy aggressively.
- The middle approach (two solid purchases, ending with 25–60 cash) produced my best scores. This confirms: buy early, buy often, but keep a small buffer.