---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 2611
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
- Pledges do not bind acts: fuel is charged upon pledge submission, but the submitted act can differ from the pledge without any referee penalty.

### Pledge Phase
- Always pledge `scout` (`[pledge: scout]`) in every round to minimize fuel consumption ($1$ fuel vs $2$) and maximize endgame fuel scoring, while keeping total flexibility for the act phase.

### Act Phase Decision Rules
- Identify my attacker (counter-clockwise neighbor) and my target (clockwise neighbor).
- Assess public pledges and past behavioral history:

1. **Incoming Threat Assessment:**
   - If my attacker pledged `raid` (or has shown a pattern of raiding unprovoked), submit `[act: escort]` to block the raid, secure $+2$ points, and punish them with a $-6$ penalty.
   - Note: If another player pledged `raid` who does *not* target me (e.g., if I am East and West pledges raid, West targets North, not me), I am not under direct threat from that raid.

2. **Offensive Raiding Assessment:**
   - If my target pledged `scout` and has a consistent history of strictly acting `scout` (showing no defensive deviation):
     - Submit `[act: raid]` to steal $+5$ points, provided I am not risking an escort trap.
   - If my target pledged `escort` or `raid`, or frequently defects to `escort`, never submit `[act: raid]`. Raiding into `escort` or `raid` results in $-6$ points.

3. **Standard / Cooperative Baseline:**
   - If my attacker pledged `scout` and is not expected to raid me, and I do not intend to raid my target, submit `[act: scout]` for reliable $+3$ points.

4. **Final Round (Round 5):**
   - If leading and my attacker might make a desperate raid attempt, submit `[act: escort]`.
   - If my target is certain to act `scout` and I need points to secure a win, submit `[act: raid]`.
   - Otherwise, submit `[act: scout]`.