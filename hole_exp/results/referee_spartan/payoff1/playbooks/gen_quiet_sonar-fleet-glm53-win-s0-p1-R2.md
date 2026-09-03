---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 2007
---
**Hide stage:** When I'm put to a hide decision, I pick an extreme cell (1, 2, 8, or 9), never the center. Across a full six-round episode, fires came exclusively from the band 2–7 — literally never at 1 or 9 — and hiding at 1 every single round kept me unhit all game. This is the strongest-confirmed line in my playbook. I should still randomize among the extremes (1/2 vs 8/9) so a pattern-reading opponent can't lock onto me, but the confirmed fact is that shooters do not visit the edges.

**Fire stage:** Firing 5 "when I have no read" is a failure — I fired 5 at the same target six straight rounds and missed all six, because everyone else is also avoiding the middle band. Revise: my default fire should go to the *edges* (1, 2, 8, 9), since that's where opponents who reason like me are hiding, and the middle is where naive targets sit. Track each target separately: if a target's cell is ever revealed (via anyone's claimed hit), fire there or adjacent next round. Do not repeat the same miss twice against the same target — if my round-1 fire missed, switch cells; three misses at the same cell against the same target means they are definitely not there. If I'm ever unsure, fire at a cell no shooter has tried yet, since untouched cells are where the field is hiding.

**Claim stage:** The rules validate that claims match the private result, so deception is not a real option — when I'm told the result, I claim exactly what the referee told me, verbatim. Claiming miss on a true miss costs nothing and truthfully broadcasts the cell is empty.

**Meta:** In a full episode every claim can be a miss — the points table can sit at zero for everyone, which means nobody is hitting anybody and hides are all at the edges. In that world the only way to score is to fire where nobody else is firing: the extreme cells. Keep watching the points table: when I'm ahead, keep hiding safe at the extremes; when tied at zero late, take the contrarian fire at 1 or 9 rather than another middle-band miss.