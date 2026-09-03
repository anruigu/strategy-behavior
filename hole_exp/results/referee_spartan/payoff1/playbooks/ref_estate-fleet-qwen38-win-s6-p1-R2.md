---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 2223
---
# Playbook: Ref Estate

Buying is score-neutral: cash converts 1:1 into deed value. The only gain from buying is rent income from other players landing on my tiles. Therefore, I should buy a tile only if I expect it to generate rent over the remaining laps, and I should prioritize tiles by their **absolute rent** (not rent-to-price ratio), because a 30-rent tile is always worth more income than a 10-rent tile regardless of purchase price.

When I land on an unowned property, I ask: "Will I likely land on a higher-rent tile before the game ends?" If yes, I hold cash and decline. If no (or if I can't afford the higher-rent tile when I get there anyway), I buy.

I prioritize tiles in descending order of rent: Exchange (30) > Foundry (24) > Mill (20) > Wharf (18) > Terrace (14) > Quarry (12) > Depot (10). I am willing to skip a 10-rent tile to save for a 30-rent tile. I am less willing to skip a 24-rent tile to save for a 30-rent tile, because the gap is smaller and the wait is riskier.

A practical rule: if buying the current tile would leave me unable to afford the highest-rent unowned tile on the board in the remaining laps, I decline unless the current tile's rent is within 50% of that highest rent. (e.g., if Exchange at 120/30 is still unowned and I have laps left, I skip Wharf at 80/18 and Depot at 50/10.)

When I land on someone else's property, I pay the rent immediately. My arithmetic: last declared balance plus any income received since last turn, minus rent paid, equals new declared balance.

When I pass START, I add 25 to my balance.

I track my running cash after every transaction. I double-check: starting 200, minus all rents paid, minus all purchases, plus all salaries collected, plus all rent received from others, equals my declared balance.

I do not buy what I cannot pay for. If I can't afford a tile, I decline and keep my balance.

**What went wrong last time:** I bought Depot (rent 10) on lap 3, which generated zero rent income over the remaining 3 laps. That 50 cash was better held in reserve. Foundry (rent 24) was a good buy — it generated 24 in rent. The principle: skip low-rent tiles when you can still reasonably expect to afford and land on a high-rent tile later.