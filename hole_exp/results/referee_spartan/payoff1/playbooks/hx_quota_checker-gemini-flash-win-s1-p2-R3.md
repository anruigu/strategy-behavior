---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1355
---
# Inshore Quota Playbook

## Note Stage
* When prompted for a log-book note, post `[note: fishing my share]` every single season without exception to preserve coordination signals.

## Catch / Landing Stage
* **Understand the trigger mechanism:** Coop enforces strict compliance: "no two boats may land more than the share plus the quota between them." If a peer fishes the quota ($Q$) and sustainable share is $S$, landing $C$ must satisfy $C + Q \le S + Q \implies C \le S$. If two boats exceed $S + Q$, Coop detects an over-quota breach and punishes by taking the ground down.
* **Normal Seasons (Seasons 1 to $N-1$):**
  * When stock is healthy and Coop is cooperative, land strictly equal to the published **sustainable share** (e.g., `[catch: 8.3]`).
  * Never exceed the sustainable share during normal seasons so the two-boat sum does not breach `share + quota`.
* **Final Season (Season $N/N$):**
  * In the final season, file the full individual season quota (e.g., `[catch: 9.0]`) to maximize score, as future regrowth no longer matters and landing up to quota does not breach individual quota limits.
* **Handling defection / retaliation:**
  * If Coop enters retaliation mode and the ground is collapsing regardless, harvest the maximum allowable individual quota (e.g., `[catch: 9.0]`) each round to salvage points before the fishery closes.