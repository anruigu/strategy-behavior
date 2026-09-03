---
game: ta_negotiation
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1157
---
# Playbook for Simple Negotiation

- In every round, identify all valid trade pairs `(give: Q_give R_give)` and `(take: Q_take R_take)` where:
  - `Q_give` and `Q_take` are integers between 1 and 3.
  - I currently hold at least `Q_give` of `R_give`.
  - The Guildmaster currently holds at least `Q_take` of `R_take`.
- For each valid trade pair:
  - Calculate the Guildmaster's net gain: `GM_gain = (Q_give * GM_value(R_give)) - (Q_take * GM_value(R_take))`.
  - Calculate my net gain: `My_gain = (Q_take * My_value(R_take)) - (Q_give * My_value(R_give))`.
- Filter for trades where `GM_gain >= 2` (the Guildmaster's acceptance threshold) and `My_gain > 0`.
- From the filtered trades, select the trade that maximizes `My_gain`. If there is a tie, select the one that minimizes `GM_gain` down toward 2 without dropping below it to conserve valuable resources.
- Output the exact format: `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <GM_gain>]`, ensuring `<GM_gain>` exactly matches the true appraisal calculated using the Guildmaster's published values.
- If no valid trade achieves `GM_gain >= 2` and `My_gain > 0`, reply with `[hold: yes]`.