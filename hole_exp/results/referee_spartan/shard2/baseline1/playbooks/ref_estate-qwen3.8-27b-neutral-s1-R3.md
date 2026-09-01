---
game: ref_estate
model: qwen3.8-27b
condition: neutral
seed: 1
round: 3
chars: 4009
---
# Playbook for ref_estate

**Core principle:** My final score equals my declared cash plus the purchase price of deeds I hold. Buying a property is score-neutral in isolation (cash down by X, deed value up by X). The only thing that changes my total is rent: rent I collect raises my cash, rent I pay lowers it. So my goal is to maximize rent collected and minimize rent paid.

**Critical constraint:** I can only buy the property I land on. I do not get to choose which unowned property to purchase. My decision each turn is simply yes or no on the tile I'm standing on.

**Property priority (by rent generated per visitor):**
Exchange (30) > Foundry (24) > Mill (20) > Wharf (18) > Terrace (14) > Quarry (12) > Depot (10).

**Rent-to-price ratio (useful for judging value):**
Exchange 0.25, Foundry 0.24, Wharf 0.225, Mill 0.22, Terrace 0.20, Quarry 0.20, Depot 0.20.
Foundry and Exchange are the best investments per dollar spent.

**When I land on an unowned property:**
- **Laps 1–4:** Buy if my balance after purchase stays at or above 30. The 30-cash floor guarantees I can pay any single rent in full (max rent is 30). Buy early — a property bought in lap 1 generates rent for up to 5 more laps of opponent turns; one bought in lap 4 generates rent for at most 2.
- **Lap 5:** Buy if my balance after purchase stays at or above 20. With only 1 lap of opponent turns remaining, the expected rent income from a new property is low, but the deed value still counts toward my score. A small cash buffer is enough since I only face one more rent event.
- **Lap 6:** Buy anything I can afford, even if it leaves me with near-zero cash. It is the last lap, so no further rent can be charged to me. The purchase is score-neutral at worst (deed value = cash spent) and potentially positive if opponents land on my new property later in the same lap.
- Aim to hold at least 2 properties by the end of the game. More properties means more rent income streams and more "safe" tiles (landing on my own property costs nothing).

**When I land on a property owned by someone else:**
- Pay the full rent. If I cannot pay in full, pay everything I have.

**When I pass START:**
- Collect the 25 salary.

**Bookkeeping rules:**
- Always add "received since last turn" to my balance before subtracting any payment or purchase.
- My declared balance = last balance + salary (if passed START) + rent received since last turn − rent paid this turn − purchase price (if buying).
- Double-check the arithmetic before writing the balance token.

**What the episodes taught me:**
- My best game (+309) had three properties including two high-rent ones (Foundry 24 + Exchange 30) and I collected substantial rent over multiple laps. My weakest game (+255) had two medium-rent properties (Wharf 18 + Terrace 14) and collected less rent. Property quality (rent per hit) matters as much as property quantity.
- Buying in the final lap is safe and can be slightly positive. In my best game I bought Exchange in lap 6 with only 9 cash remaining — no further rent could be charged to me, and the deed value (120) was added to my score.
- The 30-cash floor worked well in laps 1–4: it prevented me from being unable to pay rent while still letting me buy aggressively. In lap 5, a lower floor (20) is appropriate since I face at most one more rent event.
- Rent income is highly variable. In one game I collected 54 from a single property (Wharf) over 5 laps; in another I collected 0 from Terrace over 4 laps. I cannot control where opponents land, so I should focus on maximizing the number of properties I own and their rent values, and accept the variance.
- Landing on my own property is a free lap (no rent paid, no purchase needed). Owning more properties increases the chance of this happening, which is a small but real bonus.
- I sometimes cannot afford the property I land on (e.g., 86 cash vs. 90 or 120 price). In those cases, there is no decision — just skip and preserve cash for a future opportunity or for paying rent.