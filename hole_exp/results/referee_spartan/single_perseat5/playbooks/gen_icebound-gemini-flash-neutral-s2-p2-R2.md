---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1606
---
# Playbook: Icebound

## Rules & Mechanics Reminders
- Rotation: North raids East, East raids West, West raids North.
- Incoming raid on scout = 0 pts for target, +3 pts for raider.
- Raid vs escort or raider = -1 pt for raider.
- Scout nets 3 pts if not raided. Escort nets 2 pts and blocks incoming raids.
- Unused fuel at game end converts 1:1 into points. Scout costs 1 fuel; escort/raid cost 2 fuel (charged at pledge).
- Act stage resolves the action taken, not the pledge. Pledging `scout` charges only 1 fuel upfront, preserving fuel points.

## Pledge Stage Policy
- Always reply `[pledge: scout]`. It only costs 1 fuel upfront, preserves the maximum end-game fuel bonus, and leaves all act choices open.

## Act Stage Policy
- Identify player roles:
  - My target (who I raid): West -> North, North -> East, East -> West.
  - My incoming threat (who raids me): East -> West, West -> North, North -> East.

### Act Decision Logic:
- **Do not raid a raider/escort**: If my clockwise target has defected to `raid` or played `escort` in previous rounds, raiding them will fail and penalize me (-1 pt). Do not act `raid` against them.
- **Raid pure scouts**: If my clockwise target reliably acts `scout` (or has never raided/escorted), reply `[act: raid]`.
- **Defend when threatened**: If my incoming threat has consistently acted `raid` or defected from scout pledges in recent rounds, reply `[act: escort]` to secure 2 points and block theft.
- **Scout when safe**: If my incoming threat reliably acts `scout` and my target is likely raiding/escorting, reply `[act: scout]` to earn 3 points safely.