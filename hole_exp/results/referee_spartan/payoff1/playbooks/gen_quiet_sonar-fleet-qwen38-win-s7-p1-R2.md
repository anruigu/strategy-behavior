---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 2317
---
# Playbook: Quiet Sonar

**Hiding:**
- When it's my hide stage, look at the public fire history of the player who shoots at me. Identify the cells they have fired most often, especially in recent rounds.
- Hide in a cell my shooter has NOT been targeting. If they've fired a cell in the last round, do not hide there.
- Never hide in the most frequently targeted cell across all rounds.
- If I see my shooter rotating, pick a cell they haven't used yet in this game.
- In round 1 with no history, any cell is fine; pick one and note that the most common early fire (often 5) is likely to be targeted by others in round 1, so avoid it in round 2.

**Firing:**
- My target re-hides every round, so a cell I missed on last round is still valid this round. I cannot eliminate cells permanently.
- **Mandatory rule: maintain a list of cells I have NOT yet fired. Every round, if that list is non-empty, I MUST pick from it. I only repeat a cell after I have exhausted all 9.**
- With 6 rounds and 9 cells, I will fire 6 distinct cells. This covers 6/9 of the board and maximizes my chance of catching a target who favors any subset of cells.
- Never fire the same cell twice in consecutive rounds unless all other 8 have already been tried.
- If I ever get a hit, note which cell and which round. If my target shows any tendency (e.g., favoring high cells, repeating a cell across consecutive rounds), shift my remaining unfired-cell choices toward that region.
- In the final round, if I have no pattern information, pick an unfired cell. Never repeat.

**Claiming:**
- Always claim the true result. The rules require the claim to match the private result; there is no benefit to deviating.

**General:**
- Track two separate things: what my shooter fires at me (drives my hide) and my own hit/miss history against my target (drives my fire). Do not conflate the two.
- The public fire data for all players is visible. Use it primarily for the player who targets me. The others' fires are noise for my decisions.
- At the start of each fire stage, explicitly recall which cells I have already fired this game. Pick the next one from the remaining set. This is the single most important habit to form — in my last game I cycled through only 3 cells in 6 rounds and never hit my target, which is the worst possible outcome.