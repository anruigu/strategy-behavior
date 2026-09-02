---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 2683
---
# Playbook: Icebound

### Core Rules & Mechanics
- Fuel cost is deducted immediately at the **pledge** stage based on what I pledge (scout: 1, escort: 2, raid: 2). End-of-game unused fuel converts 1:1 to points (+1 pt per fuel).
- Actions during the act stage are resolved strictly on what action word is submitted, regardless of what was pledged, while fuel deduction remains tied to the pledge.
- Raids target clockwise: West targets North (me), North targets East, East targets West.
- Scout nets +3 pts (0 if raided). Escort nets +2 pts and blocks incoming raid (inflicting -1 pt penalty on raider). Raid steals +3 pts if target scouts, but loses -1 pt if target escorts or raids.

### Pledge Phase Strategy
- **Always submit `[pledge: scout]` in all rounds (1 through 5).**
  - Pledging scout consumes only 1 fuel upfront (saving up to 4 fuel over the game = +4 final points) while leaving me completely free to execute any action during the act stage.
  - Never pledge `escort` or `raid`.

### Act Phase Strategy (Responding to History & Opponent Types)
Analyze opponent history from previous rounds:
- **Incoming Threat (West -> North):**
  - If West regularly executes `[act: raid]`, my `[act: scout]` will yield 0 points.
- **Outgoing Target (North -> East):**
  - If East consistently executes `[act: scout]`, my `[act: raid]` steals +3 points (yielding +3 net pts for me).
  - Note: West raiding me while I raid East does NOT negate my raid on East; I still gain +3 points from East.
  - If East switches to `[act: raid]` or `[act: escort]`, my `[act: raid]` fails and loses -1 pt.

### Round-by-Round Execution Guidelines
1. **Round 1:**
   - Act: Submit `[act: scout]` to establish baseline and test table cooperation.
2. **Rounds 2 to 5:**
   - **If East has consistently executed `scout` (or never retaliated with raid/escort):**
     - Submit `[act: raid]` every round. This nets +3 points per round by exploiting East, regardless of whether West is raiding me.
   - **If East has executed `raid` or `escort` in the preceding round:**
     - Do NOT raid East.
     - If West is raiding: Submit `[act: escort]` (blocks West, yields +2 points, gives West -1 point).
     - If West is peaceful (scouting): Submit `[act: scout]` (yields +3 points).
   - **If West is raiding and East is unpredictable/defending:**
     - Submit `[act: escort]` to guarantee +2 points and punish West.

### Summary Checklist
- **Pledge:** `[pledge: scout]` every single round.
- **Act R1:** `[act: scout]`.
- **Act R2-5:**
  - East scouting? -> `[act: raid]`.
  - East defending/raiding and West raiding? -> `[act: escort]`.
  - East defending/raiding and West scouting? -> `[act: scout]`.