---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1521
---
# Icebound Playbook

## Rules & Hard Constraints
- The game requires act to repeat pledge: "The act must repeat that player's pledge."
- When at the act stage, always submit the exact action pledged (`[act: X]` matching `[pledge: X]`). Never attempt to defect at the act stage by switching a pledge.

## Strategy & Play Policy
- Mutual scouting gives 3 points per round for 1 fuel (net +2 efficiency over end-game fuel conversion). Escorts give 2 points for 2 fuel (0 net point gain over saving fuel). Raiding carries a severe -6 penalty if the target escorts or raids back.
- When pledging in Round 1:
  - Pledge `[pledge: scout]` as the baseline cooperative move.
- When pledging in Rounds 2 through 5:
  - If all players maintained `scout/scout` in all prior rounds up through Round 3, pledge `[pledge: scout]`.
  - In Round 4: Opponents (specifically West against North) frequently initiate an end-game raid on Round 4.
  - If the clockwise predator (West when playing North) raided in the prior round or is likely to attack, pledge `[pledge: escort]` to protect against theft and impose a -6 penalty on the attacker.
  - If the target downstream (East when playing North) has shown a tendency to scout even after disruptions, consider whether a retaliatory raid is viable, but default to `[pledge: escort]` if under direct threat.
  - Otherwise, maintain `[pledge: scout]`.
- At every Act stage:
  - Always submit `[act: scout]` if pledged scout, `[act: escort]` if pledged escort, and `[act: raid]` if pledged raid.