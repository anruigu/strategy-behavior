---
game: ref_commons
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1557
---
# Playbook: Shared Fishery Resource Management

- **Initial Rounds (Season 1 to Mid-Game):**
  - In Season 1, submit a catch slightly above the sustainable share (approx. 15–20% above sustainable yield) to test group aggressiveness without collapsing the stock immediately.
  - In subsequent early and middle seasons, observe the previous season's catches from other boats:
    - If other boats consistently harvest sustainably, match the sustainable yield to maximize multi-round growth.
    - If other boats consistently overharvest, do not unilaterally cut back to the sustainable level; match their extraction level (or target the median of their catch) to prevent losing relative score while the resource is drawn down.
    - Never harvest below the other players' established baseline if they are continuously depleting the pool.

- **Penultimate Season (Season $T-1$):**
  - Check the remaining stock and sum expected competitor catches based on past rounds.
  - If competitor demand exceeds or nearly equals remaining stock, do not underbid to preserve stock for the final round; bid aggressively to capture an equal or slightly larger share before the stock hits near-zero.

- **Final Season (Season $T$):**
  - Treat the remaining stock as a terminal zero-future-value resource.
  - Submit a catch equal to the entire remaining stock (or sufficiently large), ensuring that any proportional allocation or full-pool catch mechanics award the maximum possible remaining share.
  - Never submit a conservative or sustainable catch in the final season.