---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1821
---
- In the pledge stage, always submit `[pledge: scout]` to minimize fuel deduction (1 fuel vs 2 fuel) while preserving the ability to choose any act later.
- Note the clockwise raid cycle: North -> East -> West -> North. Identify:
  - My attacker (who targets me): East targets West, North targets East, West targets North.
  - My target (who I target): West targets North, North targets East, East targets West.
- In the act stage, carefully examine the previous rounds' actual acts (`pledge/act` format):
  - Notice whether my attacker has defected to `raid` in recent rounds.
  - If my attacker has demonstrated a willingness to `raid` (e.g., East raided in round 3 and 4), anticipate an incoming raid:
    - If my target is also raiding, submit `[act: escort]` to block theft and secure 2 points.
    - If I want to protect points, submit `[act: escort]`.
  - When my attacker starts raiding, do not stay on `[act: scout]` because scouting against an incoming raid yields 0 points. Respond immediately by switching to `[act: escort]` or `[act: raid]`.
  - If my target is raiding and my attacker is raiding (a full cycle of raiders), submit `[act: escort]` rather than `[act: raid]` (clashing raids lose 1 point and leave me vulnerable to the incoming raid, whereas escort gains 2 points and blocks).
  - If my attacker is consistently playing `scout` and not defecting:
    - If my target is playing `scout`, submit `[act: scout]` to sustain 3 points without provoking, or `[act: raid]` to opportunistically take 3 points.
- In round 5 (the final round):
  - If my attacker has been raiding or is likely to raid, submit `[act: escort]` to protect against incoming theft and secure 2 points.
  - If my attacker is a confirmed pure cooperator (always acts `scout`) and my target is acting `scout`, submit `[act: raid]`.