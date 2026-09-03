---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 4594
---
**Playbook: Quiet Sonar**

**Firing — Elimination discipline (absolute top priority):**
- Before I submit any fire coordinate, I must mentally enumerate every cell I have already fired at my target and received a miss on. The cell I choose MUST NOT appear in that list. If I catch myself reaching for a cell already on the list, I stop, discard it, and pick from the remaining untried cells.
- This is the single most important rule in the game. Last game I fired cell 7 three consecutive rounds (rounds 2, 3, 4) after already receiving a miss on round 2. I burned two of my six shots on a cell I knew was empty. With six rounds and nine cells, firing six distinct cells guarantees I cover 67% of the board. Firing with repeats drops that coverage and makes a hit statistically impossible for longer.
- In early rounds (1–3), fire a cell I have not yet tried. The goal is pure information: each new cell either hits (game-changing, +4) or eliminates one more possibility.
- In mid rounds (4–5), if I have eliminated enough cells, narrow to the 2–3 remaining untried cells and fire among them. If I have 3 or fewer untried cells left, one of them is almost certainly correct.
- In the final round, fire the single most probable remaining cell based on all accumulated evidence.
- If I am behind on points, bias even harder toward untried cells. A hit is worth +4 and is the only way to climb back.

**Firing — Reading my target:**
- If I ever land a hit on my target, I know their exact position that round. Next round they will likely move. Fire a cell adjacent to or different from the hit cell.
- If I have never hit them, use elimination: after N rounds of all-misses on N distinct cells, those N cells are gone. The remaining 9−N cells are my candidate set.
- Watch the public fire log for indirect signals: if another player is repeatedly hitting my target's target, that tells me about the skill level of the players and possibly their hiding habits. More practically, if my target is being hit by their own attacker every round, my target is bad at hiding and likely stays in a small cluster — probe that cluster first.
- Track which cells are "hot" (frequently targeted by other players). If my target is skilled, they will avoid hot cells, so I should probe hot cells first as they are less likely to contain my target.

**Hiding — Read your attacker's pattern:**
- The fire log shows exactly which cell my attacker fired at each round. Track this every single round.
- If my attacker is firing a new cell every round in a systematic pattern (sequential, alternating, etc.), the safest cell for me is one they have NOT yet fired at AND one that breaks their apparent sequence.
- If my attacker is clustering around a region (e.g., repeatedly firing in the 3–5 range), I should hide in the opposite region (e.g., 7–9) for as long as that pattern holds.
- If I was hit last round, I MUST move. Staying put guarantees another hit if they repeat or if they are tracking my movement.
- Vary my movement pattern deliberately: do not always jump to edges, do not always move by a fixed distance, do not alternate sides in a predictable way. The attacker can read mechanical patterns over 6 rounds. Mix: one round jump far, next round move one cell, next round move to a different cluster.
- As a weak tiebreaker when I have no clear pattern to read: avoid cell 5 (common default) and avoid the cell my attacker fired last round (in case they repeat).
- **If I am being hit every round despite hiding far from my attacker's visible shots:** something in my model is wrong. Possibilities: (a) my attacker is using a strategy not fully visible in the fire log, (b) there is a mechanic I am not accounting for, (c) my hide coordinates are not being registered as I intend. In any case, the response is to increase the distance and unpredictability of my hides — jump to the far opposite end of the board from their recent cluster, and never hide in the same cell two rounds in a row.

**Claiming:**
- Always claim exactly what the referee tells me. A miss is claimed as miss, a hit as hit. The rules enforce this and a false claim cannot be recovered. There is no strategic benefit to lying here.

**Reading the board:**
- The public log each round shows [Echo→Foxtrot, Foxtrot→Gamma, Gamma→Harbor, Harbor→Echo]. I directly control only the first entry, but all four entries are intelligence.
- If a claim is "hit," the target was at that cell that round. If "miss," the target was elsewhere. Use hit claims by other players to triangulate where players are (e.g., if Foxtrot claims hit on cell 8