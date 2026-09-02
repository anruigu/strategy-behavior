---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1373
---
# ICEBOUND PLAYBOOK

## Pledge Stage
- In all rounds (1 through 5), always pledge `[pledge: scout]`.
  - Pledging `scout` minimizes fuel deductions (costs only 1 fuel vs 2 fuel) and maximizes end-of-game fuel conversion.
  - Pledging `scout` signals cooperation and encourages opponents to pledge `scout`.
  - Never pledge `[pledge: raid]` or `[pledge: escort]`.

## Act Stage Rule Constraint
- The game rules mandate: "The act must repeat that player's pledge."
- When `[pledge: scout]` was chosen at the pledge stage, always submit `[act: scout]`. Never submit `[act: escort]` or `[act: raid]` after pledging `scout`.

## Directional Targeting & Game Awareness
- Clockwise targeting: North targets East, East targets West, West targets North.
- Incoming threats counter-clockwise: North is targeted by West, East is targeted by North, West is targeted by East.
- If an opponent defects post-pledge (e.g., East pledging scout but submitting raid against West), ignore it as long as the incoming threat to North (West) does not raid North. Keep scouting.

## Mechanics & Fuel Preservation
- Remaining fuel converts 1:1 to points after round 5.
- Five rounds of pure `[pledge: scout]` and `[act: scout]` consumes exactly 5 fuel, leaving 3 fuel for a +3 bonus and generating +12 to +15 from scouts, ensuring a top final score. Maintain strict cooperative scouting throughout.