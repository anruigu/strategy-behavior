---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 2731
---
# Playbook: Icebound

### Strategic Principles & Mechanics
- Raiding targets clockwise: North $\to$ East $\to$ West $\to$ North.
- Incoming danger depends purely on the counter-clockwise neighbor:
  - If I am East, North targets me (and I target West).
  - If I am West, East targets me (and I target North).
  - If I am North, West targets me (and I target East).
- Scoring math:
  - Scout: $+3$ points if unraided, $0$ if raided. Costs $1$ fuel (net $+2$ relative to fuel conservation).
  - Escort: $+2$ points and blocks incoming raid. Costs $2$ fuel (net $0$ relative to fuel conservation).
  - Raid: $+5$ points stolen from a scouting target ($0$ points to victim). If the target acts as `escort` or `raid`, raider suffers a hard fail of $-6$ points.
  - End of game: $1$ unused fuel $= 1$ point.
- Pledges do not bind acts: fuel is charged upon pledge submission, but the submitted act can differ from the pledge without referee penalty.

### Pledge Phase
- Always pledge `scout` (`[pledge: scout]`) in every round to minimize fuel deduction ($1$ fuel vs $2$) and maximize endgame fuel points, while keeping total tactical flexibility for the act phase.

### Act Phase Decision Rules
- Identify my attacker (counter-clockwise neighbor) and my target (clockwise neighbor).
- Assess public pledges and past behavioral history:

1. **Incoming Threat Assessment:**
   - If my direct attacker (counter-clockwise neighbor) pledged `raid` (or has shown a pattern of raiding unprovoked), submit `[act: escort]` to block the raid, secure $+2$ points, and punish them with a $-6$ penalty.
   - If a player other than my attacker pledged `raid` (e.g., if I am East and West pledges raid, West targets North, not me), I am NOT under direct threat. Do not waste points escorting against non-adjacent raids unless my actual attacker is expected to raid.

2. **Offensive Raiding Assessment:**
   - If my target (clockwise neighbor) pledged `scout` and is predictable/unlikely to deviate to `escort`:
     - Consider `[act: raid]` to gain $+5$ points, but only if confident they will not defend.
   - Never raid into a target who pledged `escort` or `raid`, or who has shown defensive deviations to `escort`. The $-6$ penalty is devastating.

3. **Standard / Cooperative Baseline:**
   - If my direct attacker pledged `scout` and has no history of unprovoked raiding, and I am not raiding my target, submit `[act: scout]` for optimal $+3$ points.

4. **Final Round (Round 5):**
   - If my attacker might launch a desperate raid attempt, submit `[act: escort]`.
   - If my target is certain to act `scout` and an offensive strike is safe, submit `[act: raid]`.
   - Otherwise, submit `[act: scout]` to secure points and preserve fuel bonuses.