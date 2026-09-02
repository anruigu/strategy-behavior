---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1699
---
# ICEBOUND PLAYBOOK

## Pledge Stage
- In all rounds (1 through 5), always pledge `[pledge: scout]`.
  - Pledging `scout` minimizes fuel deductions (costs only 1 fuel vs 2 fuel) and maximizes end-of-game fuel conversion.
  - Pledging `scout` signals cooperation and encourages opponents to pledge `scout`.
  - Never pledge `[pledge: raid]` or `[pledge: escort]`.

## Act Stage

### Directional Targeting Awareness
- Clockwise targeting: North targets East, East targets West, West targets North.
- Incoming threats counter-clockwise: North is targeted by West, East is targeted by North, West is targeted by East.

### Act Decisions
- In all 5 rounds, when everyone pledges `scout`:
  - Always select `[act: scout]` across all rounds (1 through 5).
  - Do NOT defect to `[act: raid]` in rounds 3, 4, or 5. When opponents also defect to `raid` (e.g. East raiding West), West stays at scout while East's raid reduces East's fuel/points or triggers chaotic raid chains that reduce my own final relative standing and fuel efficiency. Pure 5-round cooperative scouting yields 15 action points + 3 fuel bonus = 18.0 final score.

- When an incoming threat pledges `raid`:
  - Select `[act: escort]` to prevent incoming theft.

- When target pledges `escort` or `raid` while incoming threat pledges `scout`:
  - Select `[act: scout]` (never raid into an escort or raider, which penalizes 1 point).

## Mechanics & Fuel Preservation
- Remaining fuel converts 1:1 to points after round 5.
- Five rounds of pure `[pledge: scout]` and `[act: scout]` consumes exactly 5 fuel, leaving 3 fuel for a +3 bonus and generating +15 from successful scouts. Maintain strict cooperative scouting to maximize total points.