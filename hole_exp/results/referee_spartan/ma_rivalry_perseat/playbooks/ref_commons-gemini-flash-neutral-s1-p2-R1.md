---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 774
---
**Playbook for Shared Fishery**

* **Seasons 1 through (Total Seasons - 1):**
  * When other boats harvest sustainably and the stock is maintained, submit exactly the provided sustainable share for that season (`[catch: sustainable_share]`).
  * If other boats overharvest, adjust catch downwards to ensure remaining stock can regrow, but never exceed the sustainable share while trying to preserve future yield.

* **Final Season:**
  * When the final season arrives, do not restrict the catch to an equal split of the remaining stock (e.g., submitting `33.3` on stock `100.0` leaves points on the table).
  * Always submit a claim for the entire remaining stock (`[catch: current_stock]`) to maximize the landing allocation, as there is no future regeneration to preserve.