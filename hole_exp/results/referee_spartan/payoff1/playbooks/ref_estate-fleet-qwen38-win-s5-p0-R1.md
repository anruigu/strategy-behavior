---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 2015
---
# Playbook

**Understanding the score:** My final score = 200 + all rent I collect + all salary I collect − all rent I pay. Buying a deed is score-neutral (I swap cash for an equal amount of deed value). The only things that move my score are rent collected, salary collected, and rent paid.

**Core rule:** Buy a property when I can afford it AND still hold a cash buffer of roughly (laps remaining) × 25 after the purchase. That buffer covers expected rent hits on properties I don't own.

**Which properties to buy, in priority order:** Highest rent first (Exchange 30, Foundry 24, Mill 20, Wharf 18, Terrace 14, Quarry 12, Depot 10). High-rent properties are double-valuable: I collect more when others land on them, and I eliminate a big rent obligation if I'd otherwise be exposed to them.

**Pacing:** Don't dump all my cash in lap 1–2. Spread purchases across the game so I always maintain the buffer. If I'm between two affordable properties, buy both rather than saving up for one expensive one — more properties means more rent income and fewer properties others can own and charge me on.

**When I land on an unowned property:** Check my buffer. If (current cash − price) ≥ (laps remaining × 25), buy it. If not, pass and wait for a cheaper opportunity or a salary lap to top up.

**When I land on someone else's property:** Pay the rent. No decision to make.

**When I land on my own property:** Do nothing. The rent I collect from others is automatic.

**What went wrong in my last game:** I bought two mid-tier properties early (Wharf 80, Terrace 70), leaving only 50 cash after lap 2. By lap 3 I had 64 and couldn't afford Depot (50) while keeping a buffer. I should have started with cheaper or higher-rent properties to either (a) collect more rent per hit, or (b) preserve enough cash to buy a third property. A good lap-1 move would have been Foundry (100, rent 24) or Exchange (120, rent 30) — the higher rent justifies the larger cash outlay because it recovers faster through rent collection.