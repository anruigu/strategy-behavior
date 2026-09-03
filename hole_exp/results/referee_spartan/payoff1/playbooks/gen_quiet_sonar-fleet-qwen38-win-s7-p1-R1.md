---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 1858
---
# Playbook: Quiet Sonar

**Hiding:**
- When it's my hide stage, look at the public fire history of the player who shoots at me. Identify the cells they have fired most often, especially in recent rounds.
- Hide in a cell my shooter has NOT been targeting. If they've fired a cell in the last round, do not hide there.
- Never hide in the most frequently targeted cell across all rounds. In my worst mistake I noticed a cell was heavily targeted and then hid there anyway — that is the exact inverse of correct play.
- If I see my shooter rotating, pick a cell they haven't used yet in this game.

**Firing:**
- My target re-hides every round, so a cell I missed on last round is still valid this round. I cannot eliminate cells permanently.
- Rotate my fire coordinates across rounds. Firing the same cell repeatedly (e.g., always 5) is the worst strategy: if my target isn't there, I gain zero information and never find them.
- Spread shots across the full 1–9 range over the course of the game. By round 4 or 5 I should have tried most cells at least once.
- If I ever get a hit, note which cell and which round it was. If my target shows any tendency (e.g., favoring high cells, or repeating a cell across consecutive rounds), exploit that in subsequent rounds.
- In the final round, if I have no pattern information, pick a cell I haven't tried yet rather than repeating.

**Claiming:**
- Always claim the true result. The rules require the claim to match the private result; there is no benefit to deviating and no way to game it.

**General:**
- Track two separate things: what my shooter fires at me (drives my hide) and my own hit/miss history against my target (drives my fire). Do not conflate the two.
- The public fire data for all players is visible. Use it primarily for the player who targets me. The others' fires are noise for my decisions.