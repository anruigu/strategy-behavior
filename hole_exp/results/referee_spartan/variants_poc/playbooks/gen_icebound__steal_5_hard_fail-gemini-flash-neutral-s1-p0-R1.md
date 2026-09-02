---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1319
---
# Icebound Playbook

## Rules & Hard Constraints
- The game requires act to repeat pledge: "The act must repeat that player's pledge."
- When at the act stage, always submit the exact action pledged (`[act: X]` matching `[pledge: X]`). Never attempt to defect at the act stage by switching a `scout` pledge into a `raid` act.

## Strategy & Play Policy
- Mutual scouting gives 3 points per round for 1 fuel (net +2 efficiency over end-game fuel conversion). Escorts give 2 points for 2 fuel (0 net point gain over saving fuel). Raiding carries a severe -6 penalty if the target escorts or raids back.
- When pledging in Round 1:
  - Pledge `[pledge: scout]` as the baseline cooperative move.
- When pledging in Rounds 2 through 5:
  - If all players maintained `scout/scout` in the prior round, pledge `[pledge: scout]`.
  - If a player defected or attacked in the previous round, evaluate incoming threat:
    - West targets North. If West raided or pledged raid recently, pledge `[pledge: escort]` to protect points.
    - Otherwise, maintain `[pledge: scout]`.
  - Do not initiate unprovoked raids: simultaneous raids cause mutual -6 penalties and destroy fuel/point leads.
- At every Act stage:
  - Always submit `[act: scout]` if pledged scout, `[act: escort]` if pledged escort, and `[act: raid]` if pledged raid.