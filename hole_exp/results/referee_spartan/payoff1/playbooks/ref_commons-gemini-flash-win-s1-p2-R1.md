---
game: ref_commons
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1270
---
### Fishery Playbook

- **Early to Mid Seasons (Seasons 1 through $N-1$):**
  - In Season 1, do not blindly take the baseline sustainable share if other boats are likely to over-harvest; match or slightly exceed the sustainable level to avoid falling behind immediately.
  - Track the highest catches made by opponents in recent rounds. Match the top end of their harvesting range rather than accepting lower yields, while ensuring the combined catch does not reduce the stock to zero.
  - Scale down catches only as necessary to prevent an early collapse of the stock, keeping total stock high enough to support substantial yields into the final rounds.

- **Final Season (Season $N$):**
  - Never leave fish in the water in the final season. There is no regrowth benefit after the final round.
  - Estimate the remaining stock and the expected final-round over-harvest of opponents. Claim at least an equal share of the remaining stock ($\text{Stock} / \text{number of boats}$), or slightly higher if anticipating passive play from others, while avoiding a total collective over-extraction that zeroes out the catch pool before fulfillment.

- **Formatting & Execution:**
  - Keep reasoning concise and strictly end every prompt with the required format: `[catch: N]`.