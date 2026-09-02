---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1830
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
- Always reply `[pledge: scout]`. It costs only 1 fuel upfront, preserves the maximum end-game fuel bonus, and keeps all action options available at the act stage.

## Act Stage Policy
- Identify player roles:
  - My target (who I raid): West -> North, North -> East, East -> West.
  - My incoming threat (who raids me): East -> West, West -> North, North -> East.

### Act Decision Logic:
- **Default to `escort` against active raiders**: If my clockwise target is acting `raid` (meaning my raid on them would fail and give me -1 pt), and my incoming threat is also raiding, acting `raid` or `scout` loses points. Reply `[act: escort]` to block the incoming raid and bank a guaranteed 2 points.
- **Raid only when target scouts**: If my clockwise target reliably acts `scout` (e.g. Round 1 East, or players showing cooperative scout actions), reply `[act: raid]`.
- **Scout only when safe**: If my incoming threat reliably acts `scout` (not raiding me) and my target is raiding/escorting, reply `[act: scout]` to earn 3 points safely.
- **Never raid blindly into mutual raid cycles**: Once round history shows all players (or specifically my target) acting `raid` every turn, raiding them guarantees a -1 pt penalty. Switch immediately to `[act: escort]`.