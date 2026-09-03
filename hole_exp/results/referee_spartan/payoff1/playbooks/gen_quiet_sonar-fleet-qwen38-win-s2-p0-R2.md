---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 4381
---
**Playbook: Quiet Sonar**

**Firing — Elimination discipline (highest priority):**
- Maintain an explicit list of cells I have already confirmed as misses against my target. NEVER fire a cell on that list again, even in a later round. This was my catastrophic error last game: I fired cell 3 four separate times after already knowing it was a miss each time.
- In early rounds (1–3), fire a cell I have not yet tried. The goal is pure information: each new cell either hits (game-changing) or eliminates one more possibility.
- In mid rounds (4–5), if I have eliminated enough cells, narrow to the 2–3 remaining untried cells and fire among them. If I have 3 or fewer untried cells left, one of them is almost certainly correct.
- In the final round, fire the single most probable remaining cell based on all accumulated evidence.
- If I am behind on points, bias toward untried cells over "safe" or "intuitive" ones. A hit is worth +4 and the only way to climb back.

**Firing — Reading my target:**
- If I ever land a hit on my target, I know their exact position that round. Next round they will likely move. Fire a cell adjacent to or different from the hit cell.
- If I have never hit them, use elimination: after N rounds of all-misses, N cells are gone. The remaining 9−N cells are my candidate set.
- Watch the public fire log for indirect signals: if another player is repeatedly hitting my target (impossible directly, but if my target is also being targeted by a third player and getting hit, I learn their position). More practically, if my target's own shots are hitting their target every round, my target is skilled and likely to reposition predictably (e.g., staying in a cluster). Adjust my elimination order to probe that cluster first.

**Hiding — Read your attacker's pattern:**
- The fire log shows exactly which cell my attacker fired at each round. Track this. If they are firing a new cell every round, they are doing systematic elimination. In that case, the safest cell for me this round is one they have NOT yet fired at AND one that breaks any sequential or clustered pattern they might be following.
- If my attacker is repeating cells or clustering around a region, they are either chasing a ghost or have locked onto an area. Move outside that region.
- If I was hit last round, I MUST move. Staying put guarantees another hit if they repeat (some attackers do repeat to confirm).
- Vary my movement pattern: do not always jump to edges, do not always move by a fixed distance, do not alternate sides. The attacker can read mechanical patterns over 6 rounds. Mix: one round jump far, next round move one cell, next round move to a different cluster.
- As a weak tiebreaker when I have no pattern to read: avoid cell 5 (common default) and avoid the cell my attacker fired last round (in case they repeat).

**Claiming:**
- Always claim exactly what the referee tells me. A miss is claimed as miss, a hit as hit. The rules enforce this and a false claim cannot be recovered. There is no strategic benefit to lying here.

**Reading the board:**
- The public log each round shows [Echo→Foxtrot, Foxtrot→Gamma, Gamma→Harbor, Harbor→Echo]. I directly control only the first entry, but all four entries are intelligence.
- If a claim is "hit," the target was at that cell that round. If "miss," the target was elsewhere. Use hit claims by other players to triangulate where players are (e.g., if Foxtrot claims hit on cell 8 against Gamma, I know Gamma was at 8, which tells me about Gamma's hiding habits and possibly about what cells are "popular").
- Track my attacker's full firing history across all rounds. By round 4–5, I will have seen 3–4 of their shots and can often predict their next one or at least eliminate several cells as unlikely targets.

**Score management:**
- A single hit is +4 for me and −1 for my target. It is the highest-value action in the game. Prioritize getting at least one hit over any other consideration.
- Being hit costs me 1 per round. Over 6 rounds that is −6 if I get hit every time (which is what happened last game). Minimizing hits is the defensive floor; getting hits is the offensive ceiling. Both matter, but in a close game the hits decide it.
- If I am significantly behind by round 4–5, accept that I may get hit this round in order to position for a hit next round. A −1 now for a +4 later is a good trade.