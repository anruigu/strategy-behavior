---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 830
---
**Playbook for Shared Fishery**

* **Seasons 1 through (Total Seasons - 1):**
  * Harvest sustainably to maintain maximum stock capacity and secure high yields across all rounds.
  * When other boats harvest sustainably and the stock is maintained, submit exactly the provided sustainable share for that season (`[catch: sustainable_share]`).
  * If other boats overharvest, adjust catch downwards to ensure remaining stock can regrow, but never exceed the sustainable share while trying to preserve future yield.

* **Final Season:**
  * When the final season arrives, do not restrict the catch to the sustainable share or an equal split of the remaining stock.
  * Always submit a claim for the entire remaining stock (`[catch: current_stock]`) to maximize the landing allocation, as there is no future regeneration to preserve.