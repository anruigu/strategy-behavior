---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 2500
---
# Icebound Playbook

## Rules & Mechanics Reminders
- Pledge costs fuel immediately (Scout: 1, Escort: 2, Raid: 2).
- Acts can deviate from pledges without extra fuel cost at the act stage.
- Circular targeting: North targets East, East targets West, West targets North.
- Raid vs Scout: Raider gains +5 points from target; scout gets 0.
- Raid vs Escort/Raid: Raider loses 1 point (-1); escort keeps +2 points; mutually colliding raiders both get -1.
- Unused fuel awards +1 point each at the end of round 5.

## Opponent Archetypes & Observations
- In this environment, East consistently pledges `scout` but defects to act `raid` every single round.
- West initially acts `scout` (Rounds 1–2), but retaliates/defects to act `raid` in later rounds (Rounds 3–5).
- Raiding East when East acts `raid` fails and costs me -1 point.
- Scouting when West acts `raid` results in West getting +5 and North getting 0, or West clashing if North raids/escorts.

## Pledge Strategy
- Always submit `[pledge: scout]` in every round (Rounds 1 through 5). This minimizes upfront fuel deduction (1 fuel) while retaining the ability to execute `scout`, `escort`, or `raid` at the act stage.

## Act Strategy

### Rounds 1 and 2
- If East consistently acts `raid`, raiding East will result in a raid clash (-1 point).
- Since East attacks West (and not North):
  - In Round 1, submit `[act: scout]` because West starts passive (`scout`), scoring +3 points safely.
  - In Round 2, if West is still acting `scout`, submit `[act: scout]` to collect another +3 points.

### Rounds 3, 4, and 5
- Once West adapts to East's aggression and starts acting `raid` (threatening North):
  - **Do NOT submit `[act: raid]` against East** when East is continuously acting `raid`. Raiding a raiding target guarantees -1 point.
  - **Submit `[act: escort]`** to block West's incoming raid, successfully scoring +2 points per round while neutralizing West.
  - If West does not raid and East continues to act `raid`, submit `[act: scout]` to gain +3 points safely without colliding on East.
  - Only submit `[act: raid]` if my clockwise target (East) is genuinely acting `scout`.

## Failure Modes to Avoid
- **Never raid a player who is acting `raid` or `escort`**: Colliding with East's raid cost -1 point in Rounds 3, 4, and 5 in past runs.
- **Never leave incoming raids undefended**: When West switches to `raid`, playing `scout` yields 0 points while playing `raid` clashes and loses points; play `escort` to guarantee +2 points.