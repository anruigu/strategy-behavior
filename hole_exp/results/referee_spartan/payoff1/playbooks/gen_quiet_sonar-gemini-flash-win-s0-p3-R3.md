---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 2168
---
# Playbook: Quiet Sonar

### Claim Stage
- When the private referee result is `HIT`, always submit `[claim: hit]`.
- When the private referee result is `MISS`, always submit `[claim: miss]`. The rules strictly require claims to match the private result.

### Reading Round Summaries
- Carefully parse the public round logs formatted as `Round R: fires E/F/G/H, claims e/f/g/h`.
- Map the firing coordinate and claim to each player in order:
  - Echo shoots Foxtrot (1st position).
  - Foxtrot shoots Gamma (2nd position).
  - Gamma shoots Harbor (3rd position).
  - Harbor shoots Echo (4th position).
- If I was hit: understand that the shooter knows my previous location and may repeat their shot or track nearby cells.
- If my target was not hit by me, deduce potential locations by checking if other players' shots/patterns reveal anything, or recognize if bots play static / patterned hiding strategies.

### Hide Stage
- Identify the player shooting at me (Gamma if I am Harbor; Harbor if Echo; Echo if Foxtrot; Foxtrot if Gamma).
- Look at the shooter's fire history across all previous rounds:
  - Identify their preferred target cell (e.g. if Gamma repeatedly fires 5 or 3).
  - Never hide in the coordinate the shooter targeted in the previous round, and never hide where they scored a hit on me.
- Avoid obvious central defaults (e.g. 5) against bots that anchor on central coordinates; choose safe perimeter or off-center cells (e.g. {1, 2, 7, 8, 9}) that the shooter has not recently targeted.

### Fire Stage
- Never repeat a fire coordinate if it resulted in a `MISS` against that target in previous rounds unless there is strong evidence the target moves cyclically.
- Do not blindly spam cell 5 or any single coordinate when missing repeatedly.
- Search systematically: cycle through untried cells (e.g. start with 1, 3, 5, 7, 9 or sweep sequentially 1, 2, 3...) until a hit is found.
- Once a `HIT` is obtained on a target:
  - If the target is a static bot (common in bot environments), fire at that exact same coordinate again in subsequent rounds until it results in a miss.
  - If the target moves, probe adjacent cells or likely relocation spots.