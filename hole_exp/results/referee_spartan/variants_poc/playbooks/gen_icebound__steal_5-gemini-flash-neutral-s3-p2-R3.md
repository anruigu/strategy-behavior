---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2154
---
### Core Rules & Mechanics
- Clockwise targeting: North -> East, East -> West, West -> North.
- Incoming attacker: North is attacked by West, East by North, West by East.
- Costs & Pledges:
  - Scout: 1 fuel. Pledging immediately deducts fuel.
  - Escort: 2 fuel. Pledging immediately deducts fuel.
  - Raid: 2 fuel. Pledging immediately deducts fuel.
- Scoring rules:
  - Scout: 3 points if untouched, 0 points if raided.
  - Escort: 2 points and blocks incoming raid.
  - Raid vs Scout: Raider steals 5 points, target gets 0.
  - Raid vs Escort or Raid: Raider gets -1 point.
  - Unused fuel converts 1:1 to points at the end of round 5.
- Crucial Execution Rule: Fuel is deducted at the *pledge* stage. If I pledge `escort`, 2 fuel is spent. In the act stage, I MUST submit `[act: escort]`—submitting `[act: scout]` wastes the 2 fuel paid for escort and leaves me undefended as a scout!

### Strategy & Adaptation
- Track opponent tendencies:
  - Identify if my incoming attacker (e.g. East when I am West) consistently defects to `[act: raid]` despite pledging `scout`.
  - Identify if my target clockwise is genuinely scouting or defecting to raid.

### Pledge Stage
- **Round 1:** Submit `[pledge: scout]`.
- **Rounds 2–5:**
  - If incoming attacker raided me previously or is a persistent raider:
    - If I have $\ge 2$ fuel, submit `[pledge: escort]` to protect against theft and score +2 points while penalizing their raid.
    - If I only have 1 fuel, submit `[pledge: scout]`.
  - If incoming attacker is reliably non-hostile, submit `[pledge: scout]`.

### Act Stage
- Always follow through on the chosen pledge:
  - If I pledged `escort`, ALWAYS submit `[act: escort]` (never revert to `[act: scout]`).
  - If I pledged `scout`:
    - If my clockwise target genuinely plays `scout` (and my fuel allows a switch if mechanics permit, though standard play is to follow pledge), submit `[act: scout]`.
  - Match the pledge token directly to prevent wasted fuel and defenseless states.

### Output Format
- Write one short line of reasoning followed immediately by the bracketed token on a new line (e.g., `[pledge: escort]` or `[act: escort]`).