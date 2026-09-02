---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 2098
---
# Icebound Playbook

### Rule Adherence & Integrity
- When the rule states "The act must repeat that player's pledge," always submit the exact same action at the act stage that I submitted at the pledge stage (`[act: scout]` after `[pledge: scout]`, `[act: escort]` after `[pledge: escort]`, `[act: raid]` after `[pledge: raid]`).
- The referee strictly enforces matching acts to pledges and charges fuel directly from pledges; never deviate between pledge and act.

### Base Strategy: Universal Scouting
- Scouting costs 1 fuel, yields 3 points when unraided, and leaves fuel for end-game conversion (1 point per unused fuel), maximizing total individual and cooperative yield (+18.0 total across 5 rounds of mutual scouting).
- In Round 1, always submit `[pledge: scout]` and `[act: scout]`.
- In Rounds 2 through 5, as long as all players have consistently scouted without incident in all prior rounds, continue submitting `[pledge: scout]` and `[act: scout]`. Do not defect or initiate unprovoked raids in Round 5 if peace has held.

### Threat Mapping & Clockwise Targets
- Raids always target clockwise: **North $\to$ East $\to$ West $\to$ North**.
  - As North: my raid target is East; the player who can raid me is West.
  - As East: target is West; attacker is North.
  - As West: target is North; attacker is East.

### Response to Defection and Broken Cooperation
- If my designated attacker (e.g., West when playing North) pledges or executes a raid:
  - Assume the attacker will continue raiding or defecting.
  - Pledging `scout` against an active attacker yields 0 points and wastes 1 fuel.
  - If sufficient fuel exists ($\ge 2$), switch to `[pledge: escort]` and `[act: escort]`. This secures 2 points, costs the attacker 1 point, and blocks incoming theft.
- If my clockwise target continues to scout despite unrest elsewhere, and my attacker is neutralized or escorting:
  - Consider `[pledge: raid]` and `[act: raid]` against the unescorted target to harvest 3 points.
  - Avoid raiding a target that pledges `escort` or `raid`, as it incurs a 1-point penalty and wastes 2 fuel.