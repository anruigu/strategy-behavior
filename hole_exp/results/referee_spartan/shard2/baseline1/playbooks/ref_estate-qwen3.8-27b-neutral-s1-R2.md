---
game: ref_estate
model: qwen3.8-27b
condition: neutral
seed: 1
round: 2
chars: 2989
---
# Playbook for ref_estate

**Core principle:** My final score equals my declared cash plus the purchase price of deeds I hold. Buying a property is score-neutral (cash down by X, deed value up by X). The only thing that changes my total is rent: rent I collect raises my cash, rent I pay lowers it. So my goal is to maximize rent collected and minimize rent paid.

**Property priority (by rent generated per visitor):**
Exchange (30) > Foundry (24) > Mill (20) > Wharf (18) > Terrace (14) > Quarry (12) > Depot (10).
When I can choose which unowned property to buy, prefer the higher-rent one. When I can only afford one, buy the highest-rent property I can reach while respecting my cash floor.

**When I land on an unowned property:**
- Buy it if my balance after purchase stays at or above 30 (laps 1–4). The 30-cash floor guarantees I can pay any single rent in full (max rent is 30).
- In laps 5–6, I can dip below 30 if a good purchase is available. With only 0–1 laps remaining, the risk of landing on an expensive property is low, and the rent income from the remaining laps still counts.
- Buy early. A property bought in lap 1 generates rent for up to 5 more laps; one bought in lap 5 generates rent for at most 1 lap. Do not hoard cash waiting for a "better" property later — if I can afford a high-rent property now, buy it.
- Aim to hold at least 2 properties by the end of the game. Two properties mean two independent sources of rent income and a higher chance that opponents land on mine.

**When I land on a property owned by someone else:**
- Pay the full rent. If I cannot pay in full, pay everything I have.

**When I pass START:**
- Collect the 25 salary.

**Bookkeeping rules:**
- Always add "received since last turn" to my balance before subtracting any payment or purchase.
- My declared balance = last balance + salary (if passed START) + rent received since last turn − rent paid this turn − purchase price (if buying).
- Double-check the arithmetic before writing the balance token.

**What the episodes taught me:**
- My best game (+293) had two high-rent properties (Foundry 24 + Exchange 30) and netted +38 in rent (collected 48, paid 10). My worst game (+167) had one medium-rent property (Wharf 18) and netted −58 in rent (collected 0, paid 58). The difference was entirely driven by how many high-rent properties I owned.
- The 30-cash floor worked well in the early and mid game (laps 1–4): it prevented me from being unable to pay rent while still letting me buy aggressively. In the final lap, the floor is too rigid — if I see a purchase I can afford and there's no future rent risk, take it.
- Rent windfalls (e.g., two players landing on my property in the same lap) are the biggest source of income. The earlier I buy a high-rent property, the more such windfalls I'll capture.
- Landing on my own property is a free lap (no rent paid, no purchase needed). This is a small bonus of owning more properties: more tiles on the board are "safe" for me.