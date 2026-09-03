---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 2289
---
PLAYBOOK — gen_quiet_sonar (as Foxtrot-style mid-chain player)

FIRING:
- When I fire at the same target repeatedly, I must NOT repeat the same cell. Firing 5 every round produced zero hits all game — that is the single biggest failure in my record. When my previous fires at this target missed, that cell is ruled out for their hide; I should fire elsewhere.
- Each round, before firing, I enumerate every cell I have already fired at this target and exclude them all. With six rounds I can cover six distinct cells.
- Weight toward cells the target has historically hidden near (if any hit clues exist) and away from cells I've already eliminated. If no information, cycle through mid cells first (4, 5, 6), then edges (2, 3, 7, 8) — never the same number twice.

HIDING:
- My predator is the player who fires at me (Echo in this seat). Look at the published fire history: the cells that player fires at are the cells to avoid. Everyone fired 5 nearly every round, so 5 was poison; I did avoid it, which worked (I took zero hits and lost only 1 point total).
- Continue hiding in cells that have never been fired at by my predator. Rotate among safe cells rather than getting predictable (I used 7, 3, 9, 1 — keep that unpredictability, but always check it's not my predator's favorite cell).
- Do not hide at a cell my predator hit someone on last round — that's their pattern cell.

CLAIMS:
- The referee forces truthful claims, so when the result is given, immediately echo it with no deliberation: [claim: hit] or [claim: miss]. No reasoning needed.

READING THE STATE:
- The points table tells me who is being hit and how often. If one player keeps scoring, their target's hiding pattern is exploitable by them — and my own target may have a similar bias. Use the scoreboard, not just the fire log.
- At the claim stage the prior rounds' fires and claims are shown — actually read them before the next hide/fire decision instead of saying "no prior information is available." That statement was wrong every time I made it; the information is always in the round history shown at the hide stage.

PRIORITY FIX: my final score was 0 while Gamma got 12. All my value must come from hitting my target. Varying fire cells is the highest-leverage change; hiding well only prevents losses.