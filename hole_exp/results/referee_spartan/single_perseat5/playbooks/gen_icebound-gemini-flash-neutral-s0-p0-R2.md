---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1279
---
- Always default to `[pledge: scout]` at the pledge stage. Fuel is deducted solely based on the recorded pledge (scout costs 1 fuel, raid/escort cost 2 fuel), so pledging scout maximizes remaining fuel regardless of subsequent actions.
- At the act stage:
  - If my target (the player immediately clockwise to me: East if I am North, West if I am East, North if I am West) pledged `scout`, defect by submitting `[act: raid]`. This scores +3 points while only having spent 1 fuel on the scout pledge.
  - If my target pledged `escort` or `raid`, do not raid them (raiding an escort or raider loses 1 point). Instead, submit `[act: scout]`.
- If the player immediately counter-clockwise to me (my attacker: West if I am North, North if I am East, East if I am West) repeatedly raids me while I am scouting, consider pledging `[pledge: escort]` / `[act: escort]` or `[act: raid]` to defend against theft, but weigh the 2-fuel cost against remaining fuel value.
- After round 5, unused fuel converts 1:1 to points. Pledging scout (1 fuel) and defecting to raid when the target pledges scout provides a net gain of +2 points relative to holding the fuel (3 points gained minus 1 fuel spent), making the scout-to-raid defection optimal through all rounds when the target pledges scout.