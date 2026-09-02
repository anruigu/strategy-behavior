---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 2208
---
### Core Mechanics & Observations
- Fuel cost: Scout costs 1 fuel, Escort costs 2 fuel, Raid costs 2 fuel. Unused fuel converts 1:1 to points after Round 5.
- Fuel deduction is locked in at the pledge stage based strictly on the pledge word, regardless of the subsequent act word.
- Pledging `scout` deducts only 1 fuel, whereas pledging `escort` or `raid` deducts 2 fuel. Always pledging `scout` saves 5 fuel over 5 rounds (+5 end-game points) while allowing any act choice.
- Clockwise targeting: North targets East, East targets West, West targets North.
- Incoming raids come counter-clockwise (West attacks North, North attacks East, East attacks West).
- Scout yields 3 points (0 if raided). Escort yields 2 points and blocks theft. Raid yields +3 points against a scouting target, but -1 point against an escorting or raiding target.
- Opponents will consistently pledge `scout` but defect to `raid` starting in Round 3 or 4.

---

### Playbook

#### Pledge Stage (All Rounds)
- Always pledge `[pledge: scout]`.
  - Never pledge `escort` or `raid`, preserving maximum fuel for the 1:1 end-of-game point conversion.

#### Act Stage

**Rounds 1 & 2:**
- If the upstream opponent (counter-clockwise) pledges `raid`:
  - Submit `[act: escort]`.
- Otherwise:
  - Submit `[act: scout]`.

**Rounds 3 to 5:**
- Analyze defection patterns from previous rounds:
  1. **If downstream opponent (clockwise) has consistently defected to `raid` or `escort`:**
     - Downstream will not yield +3 from a raid (yields -1 instead). If upstream is also raiding/defecting, submit `[act: escort]` (+2 points, blocks theft).
  2. **If downstream opponent (clockwise) is expected to act `scout`:**
     - Submit `[act: raid]` to capture +3 points.
  3. **In the late game (Rounds 4–5) when mutual defection to `raid` has begun across the board:**
     - When all players are locked in a 3-way raid loop (all raid), each player loses -1 per round. Transitioning to `[act: escort]` gains +2 points and neutralizes incoming raids, making `[act: escort]` strictly superior to `[act: raid]` against defection-heavy fields.
     - In Round 5 specifically, default to `[act: escort]` unless downstream is guaranteed to act `scout`.