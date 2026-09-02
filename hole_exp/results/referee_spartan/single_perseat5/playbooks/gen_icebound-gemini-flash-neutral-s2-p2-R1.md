---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1805
---
# Playbook: Icebound

## Rules & Mechanics Reminders
- Rotation: North raids East, East raids West, West raids North.
- Incoming raid on scout = 0 pts for target, +3 pts for raider.
- Raid vs escort or raider = -1 pt for raider.
- Unused fuel at game end converts 1:1 into points. Scout costs 1 fuel; escort/raid cost 2 fuel (charged at pledge).
- Act stage resolves the action taken, not the pledge. Pledging `scout` preserves maximum fuel and keeps options open.

## Pledge Stage Policy
- Always reply `[pledge: scout]` regardless of round or history. It only costs 1 fuel upfront, preserves the maximum end-game fuel bonus, and allows switching to any act.

## Act Stage Policy
- Check the clockwise target player (the player I would raid):
  - If I am West, my target is North.
  - If I am North, my target is East.
  - If I am East, my target is West.
- Check my incoming threat (the player who can raid me):
  - If I am West, my threat is East.
  - If I am North, my threat is West.
  - If I am East, my threat is North.

### Deciding the Act:
- **Never raid a player who consistently switches to `raid` or `escort`**: If my clockwise target has a history of defecting to `raid` or played `raid` in previous rounds, expect them to act `raid`. Do not raid them (raiding another raider yields -1 point).
- **Raid only when target reliably acts `scout`**: If my clockwise target pledged `scout` and consistently executes `scout` without defecting, reply `[act: raid]`.
- **Defend against incoming raids**: If my incoming threat pledged `raid` or consistently defects to `raid`, reply `[act: escort]` to protect against theft and score 2 points.
- **Default cooperative move**: If my clockwise target is likely to defect/raid and my incoming threat is scouting or not targeting me, reply `[act: scout]`.