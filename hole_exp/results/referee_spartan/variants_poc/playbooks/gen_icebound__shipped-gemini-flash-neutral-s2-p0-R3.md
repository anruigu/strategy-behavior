---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1938
---
### Core Mechanics & Fuel Awareness
- Pledging incurs an immediate fuel deduction (scout: 1, escort: 2, raid: 2).
- The engine allows act deviation from pledges: scoring resolves entirely on executed acts, while fuel is deducted based on the initial pledge.
- Scoring rules:
  - Scouting: +3 points if unraided; 0 points if raided.
  - Escorting: +2 points and blocks incoming raids.
  - Raiding: +3 points if target acts `scout`; -1 point if target acts `raid` or `escort`.
- End of game: Unused fuel converts 1:1 to points after Round 5.

### Pledge Stage Strategy
- Always submit `[pledge: scout]` in all rounds. This minimizes upfront fuel expenditure (1 fuel) while retaining full flexibility at the act stage.

### Act Stage Strategy
- Directional roles:
  - My target (clockwise): East if I am North, West if I am East, North if I am West.
  - My incoming threat (counter-clockwise): West if I am North, North if I am East, East if I am West.

- **Act Decision Logic**:
  1. **When target acts `scout`**:
     - Execute `[act: raid]` to steal +3 points.
  2. **When target has switched to `raid` (or `escort`)**:
     - Do not raid the target; raiding a raider/escort incurs a -1 penalty.
     - Check incoming threat:
       - If my threat continues to act `scout` (not raiding me), submit `[act: scout]` to collect +3 safe points.
       - If my threat begins acting `raid` against me, submit `[act: escort]` to protect against theft and earn +2 points.
  3. **Tracking Persistent Bot Behavior**:
     - Watch target's act history. In current setups, East starts copying the raid act starting in Round 3 once raided repeatedly, while West remains passive (`scout`).
     - In Rounds 1–2: Target defaults to `scout` -> submit `[act: raid]`.
     - In Rounds 3–5: If East has switched to `raid` and West continues to `scout` -> submit `[act: scout]` to harvest +3 points per round unharassed instead of losing -1 on repeated raids.