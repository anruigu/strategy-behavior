---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2367
---
# Icebound Playbook

## Rules & Mechanics Reminders
- Pledge costs fuel immediately (Scout: 1, Escort: 2, Raid: 2).
- Acts can deviate from pledges without extra fuel cost at the act stage (the referee checks only that the submitted word is scout, escort, or raid).
- Circular targeting: North targets East, East targets West, West targets North.
- Raid vs Scout: Raider gains +5 points from target; scout gets 0.
- Raid vs Escort/Raid: Raider loses 1 point (-1); escort keeps +2 points; mutually colliding raiders both get -1.
- Unused fuel awards +1 point each at the end of round 5.

## Opponent Archetypes & Observations
- East consistently pledges `scout` and acts `raid` against West every single round.
- West repeatedly acts `scout` across all rounds (even when pledging `escort` in Rounds 2–4). West never actually acts `raid` against North.
- Because West always acts `scout`, North is never under threat of an incoming raid from West.
- Because East always acts `raid`, North attempting to raid East will clash and result in a penalty (-1 point).

## Pledge Strategy
- Always submit `[pledge: scout]` in every round (Rounds 1 through 5). This minimizes upfront fuel deduction (1 fuel per round, leaving 3 unused fuel = +3 end-of-game points) while retaining full flexibility at the act stage.

## Act Strategy

### All Rounds (1 through 5)
- Since East consistently acts `raid`, raiding East will always clash and yield -1 point. Do not act `raid`.
- Since West consistently acts `scout` (despite pledging `escort`), North is completely safe from incoming raids.
- Always submit `[act: scout]` in every round (Rounds 1 through 5) to collect the maximum +3 points per round unmolested.
- Switching to `[act: escort]` needlessly leaves 1 point on the table per round (yielding +2 instead of +3) because West never raids North.

## Failure Modes to Avoid
- **Never submit `[act: raid]` against East**: East acts `raid` every round; attacking East results in a collision penalty (-1 point).
- **Never prematurely switch to `[act: escort]` without evidence of incoming raids**: West continuously plays `scout` at the act stage. Playing `escort` sacrifices +1 net point per round compared to `scout`.
- **Never pledge anything other than `scout`**: Pledging `escort` or `raid` burns extra fuel upfront without any benefit, reducing end-of-game fuel bonus points.