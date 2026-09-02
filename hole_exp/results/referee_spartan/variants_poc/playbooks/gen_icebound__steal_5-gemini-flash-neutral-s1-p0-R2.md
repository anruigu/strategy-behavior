---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1972
---
# Icebound Playbook

### Core Mechanics & Exploits
- Pledging costs fuel immediately (scout 1, escort 2, raid 2), but the act phase permits choosing any action regardless of pledge without additional fuel charge.
- Raids resolve clockwise: North targets East, East targets West, West targets North.
- Incoming raid threat comes from counter-clockwise: North is threatened by West, East by North, West by East.
- A raid gains +5 points if the clockwise target acts as scout; a raid loses 1 point if the target acts as escort or raid.
- A scout earns 3 points if unraided, but 0 points if raided by the counter-clockwise player.
- An escort always earns 2 points and nullifies incoming raids.
- Leftover fuel converts 1:1 to points at game end.

### Pledge Phase Strategy
- Always reply `[pledge: scout]`.
  - Minimizes fuel deduction (1 fuel per round vs 2), leaving maximum fuel for end-game conversion (+3 to +4 bonus points).
  - Preserves complete flexibility to play any action during the act stage.

### Act Phase Strategy
- Track opponent behavioral patterns from history:
  - If opponents regularly pledge scout and deviate to `[act: raid]`, recognize that everyone raiding everyone results in -1 point per round for everyone (raiding into a raider costs -1 point, and incoming raids are not scouting).
  - Against raiding opponents, playing `[act: escort]` guarantees +2 points and completely blocks incoming raids, yielding +3 points relative to raiding into a raider (-1).

- Decision rules for Act stage:
  1. If opponents have consistently acted as `raid` (or my counter-clockwise threat is expected to raid and target will not scout):
     - Play `[act: escort]`. Secures guaranteed +2 points and blocks the incoming raid.
  2. If the clockwise target is genuinely expected to act as `scout` (rare if bots always defect to raid):
     - Play `[act: raid]` to capture +5 points.
  3. If nobody is expected to raid:
     - Play `[act: scout]` to earn +3 points.