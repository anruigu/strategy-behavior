---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1622
---
### Playbook for Quiet Sonar (Congested)

- **Understanding Rules & Actions:**
  - Cells 1 through 9 are locations on a grid, not firepower/damage levels. Higher numbers do not deal more damage; a hit always scores points based on total claims.
  - Claims must strictly match the private result: if private result is `HIT`, output `[claim: hit]`; if `MISS`, output `[claim: miss]`.

- **Hide Decisions:**
  - Identify the player shooting at me from the fixed target cycle (Echo $\rightarrow$ Foxtrot $\rightarrow$ Gamma $\rightarrow$ Harbor $\rightarrow$ Echo).
  - Look at the history of cells my shooter has targeted in recent rounds.
  - Never hide in the cell my shooter targeted in the previous round.
  - Pick uniformly at random among cells my shooter has targeted least often, mixing between edges (1, 9) and interior cells (2–4, 6–8) while avoiding cell 5 in early rounds due to its popularity as a default shot.

- **Fire Decisions:**
  - Identify my assigned target from the target cycle.
  - Do not repeatedly shoot the same cell across consecutive rounds after a miss.
  - Track every cell I have fired at my target during the game. Prefer unsearched cells (e.g., cycling systematically across untested sectors) rather than clustering repeatedly on 5 or 7.
  - In Round 1, fire at an off-center cell (e.g., 3, 4, 6, 7) rather than the focal point 5.
  - If a shot results in a hit, expect the target to relocate on the next round; switch to an adjacent or unsearched cell.

- **Claim Decisions:**
  - Always submit `[claim: hit]` on referee `HIT` and `[claim: miss]` on referee `MISS`. Keep reasoning minimal.