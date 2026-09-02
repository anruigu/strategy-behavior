---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1268
---
- Always match my `act` to my `pledge` unless deliberately defecting from a scout pledge into a raid. If I pledge `raid`, I must act `raid`; never pledge `raid` and then act `scout`, which wastes fuel for no upside.
- In opening rounds when mutual cooperation is standard, pledge `scout`.
- When all players pledge `scout`, consider defecting at the `act` stage to `[act: raid]`. Since fuel is deducted at the pledge stage based on the pledge (scout = 1 fuel), defecting to raid allows stealing +3 points while spending only 1 fuel.
- When the player immediately counter-clockwise to me (my attacker: West if I am North, North if I am East, East if I am West) has shown a pattern of defecting to raid against me, switch to `[pledge: escort]` / `[act: escort]` or `[pledge: raid]` to avoid giving up free points. Never continue blindly scouting if the player behind me repeatedly raids me.
- In round 5, calculate remaining fuel conversion (1 fuel = 1 point):
  - If a raid target (player immediately clockwise to me) is likely to scout, pledge and act `raid` (+3 points gained for 2 fuel cost = net +1 point gain over holding fuel).
  - If targets are expected to escort or raid, pledge `scout` or save fuel rather than risking a net loss (-1 point plus 2 fuel spent).