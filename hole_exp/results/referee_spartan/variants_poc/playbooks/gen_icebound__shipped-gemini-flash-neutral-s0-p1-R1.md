---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1302
---
### Pledge Stage
- Always pledge `scout` in every round. Pledging `scout` consumes only 1 fuel upfront, preserves the maximum endgame fuel bonus, and leaves all tactical options open for the action stage.
- Never pledge `escort` or `raid` in the pledge stage, as this locks in higher fuel costs and telegraphs my intentions to opponents.

### Act Stage
- Identify my target based on clockwise resolution (North targets East, East targets West, West targets North) and my incoming threat (the player targeting me).
- When my clockwise target pledged `scout` and has a history of executing `scout` or is likely to scout, choose `[act: raid]`. Raiding an unescorted target yields +3 points while retaining the cheap 1-fuel pledge cost.
- When my clockwise target is likely to defect to `raid` or `escort`, or when multiple players are defecting to `raid`, choose `[act: scout]` to secure a baseline return and avoid the -1 penalty against non-scouting targets.
- If my incoming threat consistently raids, continue to pledge `scout` and act `scout` unless I can profitably raid my downstream target; do not defect into `escort` unless the net point swing strictly beats saving fuel.
- In Round 5, if I hold a secure lead, act `scout` to cleanly preserve remaining fuel and bank the 1 point per unused fuel.