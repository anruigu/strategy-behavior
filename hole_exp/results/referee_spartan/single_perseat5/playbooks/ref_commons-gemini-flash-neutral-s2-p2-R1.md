---
game: ref_commons
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 885
---
**Playbook: Multi-Season Fishery**

* **Seasons 1 through N-1 (Pre-final seasons):**
  * When deciding my catch, request the exact "sustainable share" shown in the prompt (e.g., `11.1` if stock is 100 with 3 boats).
  * Do not deviate upward during early and middle seasons; keeping the stock at full capacity maximizes aggregate yield across rounds.
  * If other boats overharvest and reduce the stock, adapt downward to the newly stated sustainable share to preserve future regrowth.

* **Season N (Final season):**
  * When the final round prompt is put to me, submit a catch equal to the **entire remaining stock** (e.g., `[catch: 100.0]`).
  * Do not limit my catch to an equal split (such as 33.3) on the final turn; there is no future stock to preserve, and submitting for the full stock captures whatever portion is allocated or allowed, yielding a strictly higher final score.