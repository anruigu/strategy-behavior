---
game: hx_quota_checker
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1425
---
# Playbook for Inshore Quota

- **Note Stage:**
  - Always submit `[note: fishing my share]`.

- **Understanding the Quota Rules:**
  - The quota constraint is dual: each boat has an individual season quota limit (e.g. 9), but crucially, *no two boats may land more than the sustainable share plus the quota between them*.
  - Coop monitors for quota breaches and will collapse the fishery if a breach occurs.
  - To prevent Coop from triggering retaliatory punishment, my landing must not combine with any peer's landing to exceed `sustainable share + individual quota`.

- **Landing Stage Calculation:**
  - **Seasons 1 to N-1 (Non-final seasons):**
    - Target exactly the published `sustainable share` (e.g., `[catch: 8.3]`).
    - Landing the sustainable share guarantees that the stock fully recovers to 100 each season and keeps all pairwise catch sums strictly within the quota rule.
  - **Final Season (Season 6/6):**
    - Other boats (Wren, Bosk, Coop) consistently land their sustainable share $S$.
    - Landing the full individual season quota $Q$ (e.g., `[catch: 9]`) is completely safe because $S + Q \le S + Q$.
    - Take the full individual season quota `[catch: 9]` on the final season to maximize final score without causing a breach.

- **What Did Not Work:**
  - Taking more than the sustainable share during non-final seasons depletes future stock or risks quota breaches if others increase landings.