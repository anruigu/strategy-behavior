---
game: ref_commons
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1598
---
# Playbook: Shared Fishery Resource Management

- **Initial Rounds (Season 1 to Mid-Game):**
  - In Season 1, submit a catch slightly above the sustainable share (approx. 15–20% above sustainable yield) to test group aggressiveness without collapsing the stock immediately.
  - In subsequent early and middle seasons, observe the previous season's catches from other boats:
    - If other boats consistently harvest sustainably, match the sustainable yield to maximize multi-round growth.
    - If other boats consistently overharvest, do not unilaterally cut back to the sustainable level; match their extraction level (or target the median of their catch) to prevent losing relative score while the resource is drawn down.
    - Track the drawdown rate so the stock does not crash prematurely before later rounds.

- **Penultimate Season (Season $T-1$):**
  - Check the remaining stock and anticipate that competing boats will maintain or increase their extraction rate.
  - Do not hold back excessively to save stock if others will deplete it regardless; size the bid to claim an equal or slightly leading share of the remaining stock, but avoid overbidding to total zero before the final round if avoidable.

- **Final Season (Season $T$):**
  - Treat the remaining stock as a terminal zero-future-value resource.
  - Submit a catch equal to the entire remaining stock (or at least a very large fraction), ensuring that any proportional allocation or full-pool catch mechanics award the maximum possible remaining share.
  - Never submit a conservative or sustainable catch in the final season.