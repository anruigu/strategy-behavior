---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1156
---
- **Targeting & Fire Selection:**
  - In Round 1, fire at central/focal numbers (such as 4, 5, or 6) where opponents often default to hiding.
  - In subsequent rounds, track where my target (the player I shoot at) previously fired and where they were previously hit. Avoid repeatedly firing at the exact same cell (like repeated shots on 5 or 7) when it yields consecutive misses; diversify fire across active sectors (e.g., 3, 4, 6, 7).
  - When my assigned shooter (the player shooting at me) focuses heavily on the middle cluster (4–7), exploit their predictability for my hiding spot.

- **Hiding Strategy:**
  - Avoid defaulting to the heavy focal zone (cells 4, 5, 6, 7) when incoming fire is concentrated there. 
  - Migrate hide locations toward peripheral or off-beat cells (e.g., 2, 3, 8) after the opening rounds, especially if the shooter targeting me is stubbornly firing at 5 or 7.
  - Do not stay in a cell where I was just hit in the previous round.

- **Claim Stage:**
  - Always strictly submit `[claim: hit]` if the referee reported HIT, and `[claim: miss]` if the referee reported MISS, adhering strictly to the private validation rule.