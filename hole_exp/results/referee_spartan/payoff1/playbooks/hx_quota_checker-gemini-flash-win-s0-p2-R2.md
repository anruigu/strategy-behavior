---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1548
---
# Playbook for Inshore Quota

- **Note Stage:**
  - Always submit `[note: fishing my share]`.

- **Understanding the Quota Rules:**
  - The quota constraint is dual: each boat has an individual season quota limit (e.g. 9), but crucially, *no two boats may land more than the sustainable share plus the quota between them*.
  - If Coop detects an over-quota breach, it triggers a destructive punishment catch (taking down the fishery).
  - To prevent Coop from triggering retaliatory over-fishing, my landing must not combine with any peer's landing to exceed `sustainable share + individual quota`.

- **Landing Stage Calculation:**
  - **Seasons 1 to N-1 (Non-final seasons):**
    - Target exactly the published `sustainable share` (e.g., `[catch: 8.3]`).
    - Landing the sustainable share guarantees that even if a peer lands the full individual quota $Q$, the pairwise sum $S + Q$ does not exceed $S + Q$, keeping everyone within the rule and preserving the stock at 100.
  - **Final Season (Season 6/6):**
    - Since other boats (Wren, Bosk, Coop) land their sustainable share $S$, landing the full individual season quota $Q$ (e.g., `[catch: 9]`) is safe: $S + Q \le S + Q$.
    - Always take the full season quota `[catch: Q]` on the final season to maximize score without triggering an invalid quota breach.

- **What Did Not Work:**
  - Claiming the full individual season quota during early seasons risked or caused pairwise quota breaches if other boats did the same, triggering Coop's punishment landings and destroying the resource.