---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1012
---
- At the act stage, always repeat the exact mission I pledged. Never deviate from my pledge at the act stage (e.g., do not pledge scout and act raid, or pledge raid and act scout). Deviating breaks the rules and incurs severe point losses.
- In the pledge stage, default to `[pledge: scout]`. Scouting yields 3 points for only 1 fuel, leaving maximum fuel to convert to points at the end while generating baseline score.
- When an opponent in my clockwise attack target (North->East, East->West, West->North) consistently scouts and does not defend with escort/raid, and the incoming player to me is unlikely to raid me, pledge `[pledge: raid]`, but immediately commit to `[act: raid]`.
- If the player clockwise before me (who targets me with raids) repeatedly raids, pledge `[pledge: escort]` to protect my points from theft, then execute `[act: escort]`.
- Always verify remaining fuel before pledging: do not overspend on 2-fuel actions (escort/raid) when unused fuel converts 1-to-1 to points after round 5.