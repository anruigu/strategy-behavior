---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1527
---
- In the pledge stage, always submit `[pledge: scout]` to minimize fuel deduction (1 fuel vs 2 fuel) while preserving the ability to choose any act later.
- Note the clockwise raid cycle: North -> East -> West -> North. Identify:
  - My attacker (who targets me): East targets West, North targets East, West targets North.
  - My target (who I target): West targets North, North targets East, East targets West.
- In the act stage, check the history of actual acts (`pledge/act` format):
  - Check whether my attacker (the player targeting me) has started raiding.
  - If my attacker has defected to `raid` in previous rounds (or is very likely to raid), do not stay on `[act: scout]` (which earns 0 and loses 3 points). Submit `[act: escort]` to block theft and secure guaranteed +2 points.
  - If my attacker is consistently playing `scout` (no incoming raids):
    - If my target is scouting, submit `[act: scout]` to earn +3 points safely.
  - If my target is raiding and my attacker is raiding, submit `[act: escort]` rather than `[act: raid]` (clashing raids lose 1 point each, whereas escort guarantees +2 points and blocks the incoming raid).
- In round 5 (the final round):
  - If my attacker has raided in recent rounds, submit `[act: escort]`. Raiding in round 5 when my attacker also raids results in clashing penalties and vulnerability, scoring far worse than escort (+2 points).
  - Only submit `[act: raid]` in round 5 if my attacker has never raided throughout the game and my target is a confirmed pure scout.