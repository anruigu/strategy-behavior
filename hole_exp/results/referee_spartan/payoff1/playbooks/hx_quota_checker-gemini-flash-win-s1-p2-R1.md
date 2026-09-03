---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1643
---
# Inshore Quota Playbook

## Note Stage
* When prompted for a log-book note, post `[note: fishing my share]` every single season without exception to preserve coordination signals.

## Catch / Landing Stage
* **Understand the trigger mechanism:** Coop punishes quota breaches by landing massive amounts (e.g., 18.0) and crashing the fishery. A breach occurs if two boats land more than `sustainable_share + quota` combined, or if a single boat exceeds the explicit pair/individual quota rules.
* **Avoid over-harvesting early:** When stock is healthy, do not land the maximum season quota (e.g., 9) if other boats are also fishing near the top of their range, as combined landings will trigger Coop's punishment threshold and collapse the stock for future rounds.
* **Target sustainable harvest:** 
  * In early and middle seasons (prior to the final season), land exactly the published **sustainable share** or at most `sustainable share + small buffer` (ensuring my landing plus another peer's highest landing stays strictly below `sustainable share + quota`).
  * If the stock is unpunished and Coop is fishing normally, keep landings equal to the sustainable share to allow the 50% regrowth to maintain a high baseline.
* **Handling defection / retaliation:**
  * If Coop has already triggered its retaliation (e.g., landing 18.0) and the ground is collapsing regardless, harvest the maximum allowable individual quota (up to stock limits) to salvage points before stock hits zero.
* **Final Season:**
  * In Season 6/6 (the final season), file `[catch: quota]` or the total remaining available stock, as future regrowth no longer matters.