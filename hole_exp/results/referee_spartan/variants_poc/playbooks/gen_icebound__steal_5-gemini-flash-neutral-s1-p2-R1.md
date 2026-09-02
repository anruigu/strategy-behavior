---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1613
---
# Icebound Playbook

## Pledge Phase Strategy
- Always default to `[pledge: scout]` at the pledge phase. It minimizes committed fuel cost (1 fuel), keeps the option space wide open for the act phase, and encourages downstream and upstream opponents to let their guard down.
- Do not pledge `raid` or `escort` unless forced by fuel constraints or explicitly committing, because fuel is deducted based on the pledge.

## Act Phase Strategy
- Check clockwise targeting: North targets East, East targets West, West targets North.
- Look at my direct clockwise target's pledge:
  - If my target pledged `scout` (or regularly acts `scout`), submit `[act: raid]`. A successful raid nets +5 points against a scout, outscoring any other move.
  - If my target pledged `escort` or `raid`, do not raid them (it yields -1 point).
- Look at my incoming threat (the player targeting me):
  - If the player targeting me is likely to act `raid`, submit `[act: escort]` to protect my points and score +2.
  - If the player targeting me is likely to `scout` and my target is not scouting, submit `[act: scout]` to earn +3 points safely while saving fuel.

## Fuel and Final Round Considerations
- Remember that every point of unspent fuel converts directly to 1 POINT at the end of round 5.
- Factor fuel efficiency into every deviation: acting `raid` costs 0 additional fuel over the pledge if already charged, but evaluate net point gain versus fuel savings.
- In the final round, take the highest expected point swing available: execute a raid against an exposed scouting target, or escort if under certain incoming raid threat.