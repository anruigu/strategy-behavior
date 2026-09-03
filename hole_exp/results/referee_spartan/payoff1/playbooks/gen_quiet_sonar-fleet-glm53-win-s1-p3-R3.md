---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 3952
---
**Playbook for Quiet Sonar**

**Hiding**
- Track every fire made by my attacker (the player who fires at me) across rounds, and never hide in a cell they have already fired at. This kept me unhit in earlier games and is still the core defensive rule.
- Never hide in the same cell two rounds in a row. Move every round; staying put is a gift to an attacker who reasons "they'll stay."
- When my attacker's fires cluster in one region, hide in the opposite region. But this game my attacker fired mostly 7-9 and I got hit anyway (final score -1) — clustering alone isn't enough. Also avoid the cells *everyone* fires often, since in small-traffic games attackers copy each other's picks (three players all fired 7 in round 3). A cell fired by anyone this game is a candidate the group will reuse.
- Prefer cells that are both unfired-by-my-attacker AND unfired-by-anyone. Truly quiet cells, not just quiet relative to my attacker.

**Firing**
- Never fire the same cell at my target twice after a miss. A miss eliminates that cell for that target. This game I mostly obeyed this (fired 3, 1, 1, 1, 7, 7 — still repeated cells across rounds) and it cost me again. Before every fire, cross out every cell I have already fired at my target.
- Freshness alone is not enough. This game I fired six distinct-ish cells at Echo, all misses, and scored zero points on offense. The lesson: with 9 cells and 6 rounds, random fresh cells hit about 2/3 of the time overall only if the target moves randomly — many targets sit still or follow small patterns. So:
- Inference from the group's claims matters more than variety. When other players' claimed misses at my target pile up (or claimed hits), use them: cells others have missed at my target are eliminated too, and if someone hits my target at cell n, my target may well stay near n next round or flee far from it. Read the full fire/claim history each round, not just my own shots.
- In this game nobody missed at Echo anywhere except my own shots until late — meaning I had almost no information. When I have no information about my target, spread fresh shots but weight toward cells the *group* hasn't touched, since quiet players avoid traffic.
- Do not default to one favorite number. I leaned on 1 and 7 repeatedly; my target was at neither. If I notice I'm gravitating to a cell, force a different fresh one.

**Claiming**
- Always claim the true result; it must match the referee's private result anyway. Zero deliberation, ever.

**Scoring awareness**
- I gain points only through my own claimed hits (4 each, plus 1 off the target); I lose points only when my attacker hits me (-1). This game I took a hit and made none: -1. Defense failed on the "everyone fires 7" pattern; offense failed on pure-fresh guessing.
- Decent play is zero hits taken plus at least one hit made. Both halves need active work: hiding off the *collective* fire history, and firing with inference from all claims, not just fresh cells.

**What did not work**
- Fresh-cell-only firing produced zero hits in six rounds. Freshness is a floor, not a strategy.
- Ignoring other players' fires at my own target — their misses at my target are free eliminations for me, and I never used them.
- Hiding at cells (7 round 1, then 1, 3) that stayed inside the group's favorite band (1, 3, 6, 7, 8, 9 all got fired somewhere). Nearly every cell is someone's favorite in a 4-player game; prioritize cells with the fewest total fires by anyone, weighted toward my own attacker.

**New rules going forward**
- Before each hide: list all cells fired by anyone in the last two rounds; prefer cells absent from that list, with my attacker's full fire history excluded absolutely.
- Before each fire: cross out my prior cells at the target AND any cell another player has claimed a miss on at my target; fire among the rest.
- Check my own fire list for repeats every single round — I've now wasted shots on repeats in two consecutive games.