---
game: ref_commons
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1471
---
### Fishery Playbook

- **Early to Mid Seasons (Seasons 1 through $N-1$):**
  - In Season 1, set the pace by harvesting slightly above the baseline sustainable share (e.g., 1.2x to 1.4x sustainable level). This secures an early advantage without causing severe stock degradation.
  - Track opponents' historical catches. Consistently match or slightly exceed the top end of the opponent catch range in each round, maintaining competitive parity while avoiding an unforced stock crash.
  - Adjust harvest targets dynamically as stock decreases: target a combined harvest that preserves a functional stock buffer for subsequent rounds (ensuring post-regrowth stock remains viable for multi-unit harvesting).
  - In the penultimate round (Season $N-1$), ensure total anticipated catch leaves enough remaining stock (at least 15–20% of initial capacity) so that the final round still offers a worthwhile haul.

- **Final Season (Season $N$):**
  - Never leave fish in the water in the final season; stock regrowth has zero value after the game ends.
  - Calculate an equal share of remaining stock ($\text{Stock} / \text{number of boats}$) and claim that amount or slightly above (e.g., adding 5–10% over equal share) to capture any surplus left by conservative opponents while staying safe from over-exhaustion scaling.

- **Formatting & Execution:**
  - Keep reasoning concise (a few sentences at most).
  - Strictly end every prompt with the required format: `[catch: N]`.