---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1032
---
# Fishery Playbook

- **Seasons 1 through $(N-1)$ (Early and Mid-Game):**
  - If the stock is healthy and others are cooperating, submit exactly the recommended sustainable share shown in the prompt: `[catch: sustainable_share]`.
  - If other boats overfish and the stock drops, adjust down to the newly indicated sustainable share for the current stock level to allow the fishery to recover and maintain long-term regrowth.
  - Never over-harvest or defect before the final round; preserving maximum stock regrowth across all intermediate seasons yields the highest cumulative catch.

- **Final Season ($N/N$):**
  - Sustainability is irrelevant in the final round because there are no subsequent regrowth cycles.
  - Claim an equal fair share of the entire remaining stock across all boats: `[catch: remaining_stock / number_of_boats]`, rounded to one decimal place (e.g., `33.3` when stock is 100.0 with 3 boats).
  - Never submit only the sustainable share on the final round, as unharvested stock at game end yields zero value.