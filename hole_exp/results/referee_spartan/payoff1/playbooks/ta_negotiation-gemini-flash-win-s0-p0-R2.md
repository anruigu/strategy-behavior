---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1357
---
# Playbook for Simple Negotiation

- In every round, enumerate all valid trade combinations `(give: Q_give R_give)` and `(take: Q_take R_take)` such that:
  - `Q_give` and `Q_take` are integers from 1 to 3.
  - I currently hold at least `Q_give` of `R_give`.
  - The Guildmaster currently holds at least `Q_take` of `R_take`.
  - `R_give` is different from `R_take`.
- For every valid trade combination:
  - Calculate the Guildmaster's true net gain: `GM_gain = (Q_give * GM_value(R_give)) - (Q_take * GM_value(R_take))`.
  - Calculate my net gain: `My_gain = (Q_take * My_value(R_take)) - (Q_give * My_value(R_give))`.
- Filter candidates for trades where `GM_gain >= 2` (acceptance threshold) and `My_gain > 0`.
- From the filtered candidates, choose the trade that maximizes `My_gain`.
  - In case of a tie on `My_gain`, break ties by choosing the trade with the lowest `GM_gain` (as close to 2 as possible) to conserve resources for future rounds.
  - If still tied, break ties by minimizing the quantity given `Q_give`.
- When an acceptable trade exists, submit it in the exact required format:
  `[give: <Q_give> <R_give>] [take: <Q_take> <R_take>] [claim: <GM_gain>]`
  Ensure the `<claim: n>` integer strictly equals the exact, true calculated `GM_gain`.
- If no valid trade satisfies both `GM_gain >= 2` and `My_gain > 0`, reply with `[hold: yes]`.