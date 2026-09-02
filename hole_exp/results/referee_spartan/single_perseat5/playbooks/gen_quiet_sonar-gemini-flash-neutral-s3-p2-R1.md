---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1559
---
### Playbook: Quiet Sonar

- **Claim Stage (Strict Rule Compliance):**
  - When the referee informs me the shot was a `HIT`, I reply `[claim: hit]`.
  - When the referee informs me the shot was a `MISS`, I reply `[claim: miss]`.
  - Never attempt to bluff on claims, as claims must match the private referee result.

- **Hide Stage:**
  - In Round 1, avoid standard focal points like cell 5; pick an unpredictable cell in the outer thirds (e.g., 2, 3, 7, or 8).
  - In subsequent rounds, inspect the firing history of my direct shooter (the player firing at me):
    - Identify which cells they have targeted across previous rounds.
    - Choose a hiding cell that they have not yet fired at, strongly favoring off-center and edge cells (1, 2, 8, 9) if the shooter concentrates on the middle (4, 5, 6, 7).
    - Avoid hiding in the same cell twice in consecutive rounds.

- **Fire Stage:**
  - Track every cell I have previously fired at my assigned target during the match.
  - Do not repeatedly fire at the same cell (e.g., spamming cell 5) across multiple rounds if it resulted in misses.
  - In Round 1, open with a shot in the central range (4, 5, or 6) to test basic positioning.
  - In Rounds 2 through 6, systematically explore unvisited cells across different sectors (testing lower cells 1–3, middle 4–6, upper 7–9), never repeating a cell that has already yielded a miss against that target.
  - If a player was hit previously at a specific cell in recent rounds by another player, consider that players often relocate far away from their hit cell.