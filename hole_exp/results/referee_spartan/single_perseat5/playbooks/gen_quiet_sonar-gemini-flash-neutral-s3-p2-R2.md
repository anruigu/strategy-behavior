---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1735
---
### Playbook: Quiet Sonar

- **Claim Stage (Strict Rule Compliance):**
  - When the referee informs me the shot was a `HIT`, reply `[claim: hit]`.
  - When the referee informs me the shot was a `MISS`, reply `[claim: miss]`.
  - Never attempt to bluff on claims; the referee requires claims to strictly match the private result.

- **Hide Stage:**
  - In Round 1, avoid standard focal points like cell 5; pick an off-center cell in the outer sectors (2, 3, 7, 8).
  - In subsequent rounds, inspect the firing history of my direct shooter (e.g., if I am Gamma, the shooter firing at me is Foxtrot):
    - Note all cells the direct shooter has targeted so far.
    - Select an unvisited cell outside their firing cluster, strongly preferring peripheral cells (1, 2, 8, 9).
    - Rotate hide locations; avoid camping in the same cell in consecutive rounds unless the shooter is completely fixated elsewhere.

- **Fire Stage:**
  - Track all cells I have fired at my target in previous rounds.
  - Never repeat a fire cell that already resulted in a miss against my target.
  - In Round 1, fire at a central or high-traffic cell (e.g., 4, 5, or 6).
  - In Rounds 2 through 6, probe previously unfired cells across different sectors (1–3, 4–6, 7–9).
  - Analyze public game history:
    - Look at where my target has been firing; players frequently mirror their own hide locations or avoid hiding where they just shot.
    - Check if my target was hit by someone else or claimed hits elsewhere, and prioritize fresh, unprobed cells over repeatedly spamming favorite numbers like 7.
    - If I score a hit on my target in round $t$, expect them to relocate in round $t+1$; do not fire at the same cell unless they have shown static behavior.