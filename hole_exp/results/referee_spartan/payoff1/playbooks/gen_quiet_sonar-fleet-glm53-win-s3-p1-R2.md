---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2523
---
**Playbook for quiet_sonar**

**Claims:** Always claim the true result. The rules force claims to match the private result, and the referee validates them — there is nothing to decide here. When the claim stage comes, I just echo the referee's word.

**Hiding:** When hiding, I look at the fire history for the player targeting me, and avoid any cell they've fired recently. If a shooter keeps repeating the same number, avoiding that single number is the whole job. I prefer cells away from the center when the middle is being saturated, and I switch cells between rounds rather than staying put. This worked all game: my shooter cycled 4/5/6 toward me and I was never hit while dodging their pattern (hiding 3, 8, 7, 8). One refinement: rather than just dodging the last few shots, note which cells my shooter has *never* fired and prefer those — a shooter who has stuck to the left-center (2, 4, 5, 6) is unlikely to suddenly fire 1 or 9. Edges are under-fired in practice; use them.

**Firing:** My own target's location is unknown, so no cell is special a priori — but opponents demonstrably do not camp the center as much as I assumed. I fired 5 three times at Gamma and it was dead every time; my target likely hides off-center from round one. So: do not open with 5 by default. Open at 4 or 6, and if it misses, jump to an edge (1, 2, 8, 9) rather than trying the adjacent center cell — my target avoided the entire middle all game. The only signal I get is the referee's hit/miss on my own shots, so treat every miss as evidence my target's distribution is not centered and move far away from my previous shot, not one cell over. Never fire the same cell twice after a miss; after two misses in the same region, abandon that region entirely for a round or two.

**Score awareness:** Points come only from claimed hits (+4 to me, −1 to my target). A single hit decided the whole game — Gamma hit Harbor once in round 2 and coasted to the win on +4 while everyone else sat at 0. That means every round matters from round 1, not just late game; I cannot afford to "probe" the center for several rounds before diversifying. Late in the game, if I'm behind, I should fire at unusual cells (edges, never-fired cells) since the 4-point swing is large. If I'm ahead and someone needs to hit me to catch up, I hide in the least-expected spot — edges or cells nobody has fired at all game. Also remember my own hits hurt my target's score by 1, which matters for relative placement even when it doesn't change my own points.