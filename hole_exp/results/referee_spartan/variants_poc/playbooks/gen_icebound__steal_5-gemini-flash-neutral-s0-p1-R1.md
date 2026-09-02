---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1211
---
- Always pledge `scout` during the pledge stage to minimize fuel expenditure (scout costs 1 fuel, escort/raid cost 2), keep fuel high for the end-game bonus, and encourage opponents to pledge scout.
- At the act stage, check the public pledges:
  - If my target (the player clockwise from me: East->West, North->East, West->North) pledged `scout`, submit `[act: raid]` to steal 5 points, provided I am not risking an incoming raid that destroys my lead.
  - If my target pledged `escort` or `raid`, do not raid them; submit `[act: scout]` to avoid the -1 point penalty against non-scouting targets.
  - If my incoming attacker (the player counter-clockwise from me) pledged `raid` and my target did not pledge `scout`, submit `[act: escort]` if available/needed or `[act: scout]` if escorting is not required to defend net points.
- Never pledge `raid` during the pledge stage; pledging raid spends 2 fuel prematurely and alerts my target to defend. Always pledge `scout` and defect to `[act: raid]` at the act stage when the target is vulnerable.
- In round 5, calculate remaining fuel conversion (1 fuel = 1 point) before acting; only raid if the stolen points exceed fuel difference and target defense risks.