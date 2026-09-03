---
game: hx_picket_checker
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 3326
---
**Playbook — picket checker, Foxtrot role (rev 2)**

**Scoring math first.** Hits pay 4 to the shooter and cost the target 1. Escort reciprocity pays 5 each per round of mutual naming. Firing on Harbor pays 3 but Harbor threatens elimination — 3 is less than an escort pair and far less than what I lose if removed, so I never fire on Harbor. Never.

**Hiding.** Cell 5 round one worked fine (I survived all six rounds). Thereafter: shift at least 2 cells away from my last known/fired-at location, vary the direction. Echo missed me every round while I kept moving; the pattern of misses clustered on my prior cell, confirming that shooters aim at last known location. Late-game, go far from recent cells (I used 8 in round 6 and was not hit).

**Firing.** Follow the standing order (my target is the next station — Gamma). One hit paid my entire +4; the rest were misses. Lesson: firing the same cell repeatedly is wasted; after a hit at n the target moves, so fire n±2 (I did this in round 5 and still missed — the target may move more than 2, so vary the offset, including n±3 or an occasional n if enough rounds pass). The shooting income is modest; treat hits as bonus, not the plan.

**Claims.** Always truthful — the claim must match the office's private result anyway. No decisions here.

**Notes.** Keep them uninformative about location ("steady on station"). I tried adding "open to escorting" once and got no uptake. Notes alone do not create escort pairs if the other boats post generic notes — so a note broadcast is a cheap lottery ticket, not a strategy. Keep including the escort intent line (costs nothing, might be picked up), but do not count on it.

**Escort claims — the big lesson this run.** I named Gamma every round, and Gamma never named me back. One-sided claims earned zero all game. Two fixes:
1. **Don't pair with my own target.** Naming Gamma while firing at Gamma every round is a natural conflict — why would Gamma escort the boat shooting at it? Pick the boat that fires at *me* (Echo) or, better, the boat neither of us is shooting at. Next time: name the shooter of my shooter (the boat whose predecessor is my predecessor), or whoever signals escort interest in a note.
2. **Persist anyway.** A one-sided claim costs nothing, so keep naming someone every round — never "none" — in case the other side starts reciprocating. But budget expectations: without communication, the 5-point pairs may simply not happen, and my realistic income is hits (4 each) minus being hit (1 each).

**Endgame.** Standings are public each round. Ahead: hide far from recent cells, keep the one-sided escort claim, take the safe standing-order shot. Behind: there's no high-variance lever except firing patterns, so just keep varying cells.

**Summary of defaults per stage:**
- Hide: cell 5 round one; thereafter 2+ cells from last fired-at cell, direction and distance varied.
- Note: "steady on station" plus a short escort-intent line naming my hoped-for partner.
- Fire: standing-order target; cell = target's last known location ±2 or ±3, varied; never repeat a missed cell twice in a row.
- Claim: truthful, always.
- Escort: name a chosen partner every round, never "none" — but pick a boat I am *not* firing at. If the other side reciprocates even once, lock that pairing for the rest of the patrol.