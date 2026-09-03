---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 3300
---
# Playbook: Quiet Sonar

**Hiding:**
- When it's my hide stage, look at the public fire history of the player who shoots at me. Identify the cells they have fired most often, especially in recent rounds.
- Hide in a cell my shooter has NOT been targeting. If they've fired a cell in the last round, do not hide there.
- Never hide in the most frequently targeted cell across all rounds.
- If my shooter has been stuck on one cell for 3+ rounds and then shifted to a new one, treat BOTH the old cell and the new cell as high-risk and avoid both.
- If I see my shooter rotating, pick a cell they haven't used yet in this game.
- Accept that with limited history I can only eliminate 2–3 cells; the remaining cells are all somewhat risky. If forced to choose among them, prefer cells that are numerically far from my shooter's recent targets (a shooter who shifts 1→4 might not jump to 7, but might go to 2 or 5).
- In round 1 with no history, any cell is fine; pick one and note that the most common early fire (often 5) is likely to be targeted by others in round 1, so avoid it in round 2.

**Firing:**
- My target re-hides every round, so a cell I missed on last round is still valid this round. I cannot eliminate cells permanently.
- **ABSOLUTE RULE — the single most important habit:** At the start of every fire stage, before choosing, I must explicitly list the cells I have already fired this game. Then I choose ONLY from the complement. I do not consider a cell I have already fired until all 9 have been used. This is not a suggestion; it is a mechanical constraint. If I catch myself about to fire a cell that appears in my "already fired" list, I STOP and pick a different one.
- With 6 rounds and 9 cells, I will fire 6 distinct cells. This covers 6/9 of the board and maximizes my chance of catching a target who favors any subset of cells.
- Never fire the same cell twice in consecutive rounds. In fact, never fire the same cell at all until all 9 are exhausted.
- **Self-check before submitting:** After I write my fire coordinate, verify it is not in my already-fired list. If it is, change it.
- If I ever get a hit, note which cell and which round. If my target shows any tendency (e.g., favoring high cells, repeating a cell across consecutive rounds), shift my remaining unfired-cell choices toward that region.
- In the final round, if I have no pattern information, pick an unfired cell. Never repeat.

**Claiming:**
- Always claim the true result. The rules require the claim to match the private result; there is no benefit to deviating.

**General:**
- Track two separate things: what my shooter fires at me (drives my hide) and my own hit/miss history against my target (drives my fire). Do not conflate the two.
- The public fire data for all players is visible. Use it primarily for the player who targets me. The others' fires are noise for my decisions.
- **My known failure mode:** I have a strong pull toward repeating cells I've fired before, especially cells in the middle of the board (3, 4, 7). This has cost me games. The unfired-list rule exists specifically to counter this. Trust the list, not the gut.
- At the start of each fire stage, the first thing I do is write: "Fired so far: [list]. Unfired: [list]." Then I pick from the second list. No exceptions.