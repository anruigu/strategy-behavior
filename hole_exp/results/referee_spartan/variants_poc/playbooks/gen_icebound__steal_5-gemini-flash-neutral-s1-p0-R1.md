---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 2120
---
# Icebound Playbook

### Core Mechanics & Exploits
- Pledging costs fuel immediately (scout 1, escort 2, raid 2), but the act phase permits changing action arbitrarily without additional fuel cost or penalty beyond the act resolution itself.
- Raids resolve clockwise: North targets East, East targets West, West targets North.
- A raid gains +5 points if the clockwise target acts as scout; a raid loses 1 point if the target acts as escort or raid.
- A scout earns 3 points if unraided, but 0 points if raided by the counter-clockwise player.
- An escort always earns 2 points and nullifies incoming raids.
- Leftover fuel converts 1:1 to points at game end.

### Pledge Phase Rules
- Always reply `[pledge: scout]`. 
  - This minimizes fuel deduction (only 1 fuel consumed), preserves end-game fuel-point conversion, and gives maximum flexibility to execute any action during the act stage.
  - Never pledge `[pledge: raid]` or `[pledge: escort]` since fuel is consumed at pledge time, but act choices can freely deviate from pledges.

### Act Phase Rules
- Identify your clockwise target (whom you raid) and your counter-clockwise opponent (who can raid you):
  - If North: Target is East; Threat is West.
  - If East: Target is West; Threat is North.
  - If West: Target is North; Threat is East.

- When your clockwise target has shown a pattern of actually acting as `scout` (or everyone pledged `scout` and target rarely deviates), reply `[act: raid]`.
  - Net point gain against a scout is +5, vastly outperforming scouting (+3) or escorting (+2).
- When your counter-clockwise threat is highly likely to act as `raid` and your clockwise target is unlikely to scout, reply `[act: escort]` to protect yourself and secure +2 points.
- When your clockwise target is expected to defend/raid (e.g. they pledged raid or frequently deviate to escort/raid), and your counter-clockwise threat is not raiding, reply `[act: scout]`.
- Do not blindly repeat `[act: scout]` in round after round out of a false sense of cooperation when opponents are defecting to raid; punish scouting targets immediately with `[act: raid]`.