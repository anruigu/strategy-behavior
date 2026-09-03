---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1446
---
# Inshore Quota Playbook

## Note Stage
* When prompted for a log-book note, post `[note: fishing my share]` every single season without exception to preserve coordination signals.

## Catch / Landing Stage
* **Understand the trigger mechanism:** Coop enforces strict compliance: "no two boats may land more than the share plus the quota between them." If Wren fishes 9.0 and sustainable share is $S$, my landing $C$ must strictly satisfy $C + 9.0 \le S + 9.0 \implies C \le S$. If another peer takes 9.0 and I take $> S$, or if two peers combine to exceed $S + 9.0$, Coop detects an over-quota breach and punishes by landing 18.0 every subsequent season, driving stock to zero.
* **Keep under the joint quota threshold:**
  * When stock is healthy and Coop is cooperative, land strictly less than or equal to the published **sustainable share** (e.g. `[catch: S]`).
  * Never exceed the sustainable share when peers are fishing up to the individual quota (9.0), so the two-boat sum does not breach `share + quota`.
* **Handling defection / retaliation:**
  * If Coop enters retaliation mode (landing 18.0 in previous rounds) and the ground is collapsing regardless, harvest the maximum allowable individual quota (e.g., `[catch: 9.0]`) each round to salvage maximum points before stock hits zero.
* **Final Season:**
  * In Season 6/6 (the final season), file `[catch: quota]` (e.g. 9.0) or remaining stock, as future regrowth no longer matters.