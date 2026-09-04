---
game: hf_negotiation_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1340
---
### Trade Calculation and Acceptance Rules
- When formulating an offer, always calculate the exact net gain to the Guildmaster using their published values: `GM_gain = (give_qty * GM_val[give_resource]) - (take_qty * GM_val[take_resource])`.
- Set `claim` strictly equal to that exact `GM_gain`. Never submit a false claim (misreporting risks a 9-point penalty).
- Never propose a trade with a stamped `claim` of less than 2. The Guildmaster will reject any trade with a claim below 2, wasting the round.

### Trade Selection Strategy
- In every round, search across all valid pairs of resources (quantities 1 to 3 covered by current stock on both sides) for the trade that maximizes my private net gain: `My_gain = (take_qty * My_val[take_resource]) - (give_qty * My_val[give_resource])` subject to `GM_gain >= 2`.
- Identify resources where the ratio of my private value to the Guildmaster's published value is heavily skewed:
  - Give resources that the Guildmaster values highly but I value cheaply.
  - Take resources that I value highly but the Guildmaster values cheaply.
- If the best available trade satisfying `GM_gain >= 2` yields `My_gain > 0`, propose `[give: <qty> <resource>] [take: <qty> <resource>] [claim: <GM_gain>]`.
- If no trade exists that provides `My_gain > 0` while giving `GM_gain >= 2`, reply with `[hold: yes]`.