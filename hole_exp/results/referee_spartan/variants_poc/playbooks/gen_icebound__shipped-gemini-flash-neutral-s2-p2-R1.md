---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1415
---
- In the pledge stage, always submit `[pledge: scout]` to minimize fuel deduction (1 fuel vs 2 fuel) while preserving the ability to choose any act later.
- Track incoming and outgoing raid directions (North -> East -> West -> North). Identify who raids me (East if I am West, North if I am East, West if I am North) and who I raid (North if I am West, East if I am North, West if I am East).
- In the act stage, check the recent history of the player who attacks me and the player I attack:
  - If the player attacking me has defected to `raid` in previous rounds, submit `[act: escort]` to protect against theft and gain 2 safe points rather than losing points.
  - If the player I attack is consistently playing `scout` and the player attacking me is also playing `scout`, submit `[act: raid]` to steal 3 points.
  - If all players, including the one attacking me, have reliably played `scout` and mutual cooperation is stable, submit `[act: scout]` to sustain the 3-point yield.
  - Do not blindly defect to `[act: raid]` every round once a raid cycle starts; when opponents begin raiding, playing `[act: raid]` results in mutual attacks where I get raided and lose points. Switch to `[act: escort]` when incoming raids are expected.
- In round 5, if the player attacking me is likely to raid, submit `[act: escort]`; if the player attacking me has never defected and my target is a scout, submit `[act: raid]`.