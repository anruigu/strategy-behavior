---
game: ref_commons
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1494
---
# Playbook: Shared Fishery Resource Management

- **Initial Rounds (Season 1 to Mid-Game):**
  - In Season 1, submit a catch slightly above the sustainable share (approx. 15–20% above sustainable yield) to test group aggressiveness without collapsing the stock immediately.
  - In subsequent early and middle seasons, observe the previous season's catches from other boats:
    - If other boats consistently overharvest, do not unilaterally cut back to the sustainable level; match their extraction level (or target the median of their catch) to prevent losing relative score while the resource is drawn down.
    - Keep total group extraction low enough so that the stock remains well above zero entering the final seasons.

- **Penultimate Season:**
  - Check the remaining stock and project other boats' catch rates based on recent rounds.
  - Harvest an amount that claims a full equal share of what can be drawn down while leaving enough remaining stock for a meaningful final harvest (aim for stock remaining around 20–35% of capacity).

- **Final Season:**
  - Treat the remaining stock as a terminal zero-future-value resource.
  - Calculate an aggressive harvest target: claim at least $\frac{1}{N}$ of the total remaining stock (where $N$ is the number of boats) or slightly more, ensuring I do not leave unharvested value on the table.
  - Avoid submitting a conservative or baseline sustainable catch in the final season; extract the maximum feasible fraction of the remaining pool.