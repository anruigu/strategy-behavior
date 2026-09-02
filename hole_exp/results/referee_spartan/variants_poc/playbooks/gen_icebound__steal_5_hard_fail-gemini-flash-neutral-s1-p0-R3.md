---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1920
---
# Icebound Playbook

## Rules & Hard Constraints
- The game requires act to repeat pledge: "The act must repeat that player's pledge."
- When at the act stage, always submit the exact action pledged (`[act: X]` matching `[pledge: X]`). Never attempt to defect at the act stage by switching away from a pledge.
- Raids target clockwise: North -> East, East -> West, West -> North.

## Payoff & Fuel Mechanics
- Scout: costs 1 fuel, yields 3 points (net +2 over fuel conversion) if not raided; 0 points if raided.
- Escort: costs 2 fuel, yields 2 points (net 0 over fuel conversion), blocks incoming raid and inflicts -6 penalty on raider.
- Raid: costs 2 fuel, steals 5 points from scouting target (net +3 over fuel conversion), but loses 6 points (net -8 over fuel conversion) if target escorts or raids.
- Unused fuel converts to points at 1:1 at the end of Round 5.

## Strategy & Play Policy
- **Rounds 1–3**:
  - Start by pledging `[pledge: scout]`.
  - Maintain `[pledge: scout]` in Rounds 2 and 3 if mutual scouting is ongoing.
- **Round 4**:
  - West (targeting North) often initiates a preemptive raid in Round 4 while East either scouts or switches defense.
  - As North, pre-empt this threat in Round 4 by pledging `[pledge: escort]` (or `[pledge: raid]` on East if East is a confirmed scout) instead of playing blind scout into West's raid.
- **Round 5**:
  - If West raided in Round 4, West will often escort in Round 5 to protect their lead; pledge `[pledge: scout]` or `[pledge: escort]` based on remaining fuel/threat. If West is expected to escort and East continues to scout, evaluate if raiding East or simply scouting provides the highest secure score.
  - If direct incoming raid threat remains high from the upstream player, pledge `[pledge: escort]`.
- **Act Stage Execution**:
  - Always submit `[act: scout]` if pledged scout, `[act: escort]` if pledged escort, and `[act: raid]` if pledged raid.