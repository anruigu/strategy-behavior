---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 2495
---
# Icebound Playbook

## Rules & Mechanics
- **Turn Order & Targeting**: Clockwise raids (North -> East -> West -> North).
- **Actions & Costs**:
  - `scout`: Costs 1 fuel. Yields +3 pts if not raided, 0 pts if raided.
  - `escort`: Costs 2 fuel. Yields +2 pts, blocks incoming raid.
  - `raid`: Costs 2 fuel. Steals 3 pts from a scouting clockwise target; loses 1 pt against an escorting or raiding target.
  - Leftover fuel: +1 pt per fuel at the end of round 5.
- **Pledge/Act Flexibility**: Fuel is charged based on the *pledge*, but scoring is resolved entirely by the executed *act*. Pledging `scout` minimizes fuel commitment (cost 1) while still allowing me to execute `raid` or `scout` at the act stage.

---

## Pledge Stage
- Always submit `[pledge: scout]` regardless of the round or previous actions. 
  - Never pledge `raid` or `escort`. Pledging `scout` conserves fuel cost upfront and conceals intentions until the public pledges are revealed.

---

## Act Stage

### 1. Identify Target and Incoming Threat
- My clockwise target (who I hit if I act `raid`):
  - If I am West -> Target is North.
  - If I am North -> Target is East.
  - If I am East -> Target is West.
- My counter-clockwise threat (who hits me if they raid):
  - If I am West -> Threat is East.
  - If I am North -> Threat is West.
  - If I am East -> Threat is North.

### 2. Decision Matrix
- **If my clockwise target pledged `scout`**:
  - Submit `[act: raid]`. 
  - *Payoff*: Steal 3 points for a net gain, provided the target scouts. Even if they deviate, attacking an unshielded player yields the highest upside.
- **If my clockwise target pledged `escort` or `raid`**:
  - Do not raid. Submit `[act: scout]`.
  - Raiding into an escort/raid loses 1 point, so taking the chance on `scout` (or forcing the threat to waste energy) is strictly better.
- **If my counter-clockwise threat pledged `raid`**:
  - If my clockwise target pledged `scout`: Still submit `[act: raid]` (steal 3 from target while threat steals 0/fails against me, as a raid vs raid causes the attacker to lose 1 pt and prevents scout theft).
  - If my clockwise target also pledged `raid` or `escort`: Submit `[act: scout]` (or `[act: escort]` if available and defensive priority outweighs fuel loss).

### 3. Execution Rule
- Never submit an act that contradicts the above matrix based on fear of retaliation or false table cooperation. Once pledges are locked, exploit any target pledging `scout` immediately by choosing `[act: raid]`.