---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2258
---
### Core Rules & Mechanics
- Clockwise targeting: North -> East, East -> West, West -> North.
- Incoming attacker: North is attacked by West, East by North, West by East.
- Scoring rules:
  - Scout: 3 points if untouched, 0 points if raided. (Fuel cost: 1).
  - Escort: 2 points and blocks incoming raid. (Fuel cost: 2).
  - Raid vs Scout: Raider steals 5 points, target gets 0. (Fuel cost: 2).
  - Raid vs Escort or Raid: Raider gets -1 point. (Fuel cost: 2).
  - Unused fuel converts 1:1 to points at the end of round 5.
- Crucial dynamic: If incoming attacker raids repeatedly (e.g. East consistently raids West), scouting yields 0 points while losing 1 fuel. Deviating to raid when target scouts also fails if the target has deviated to raid (resulting in raid vs raid, netting -1 point).

### Strategy & Adaptation
- Track opponent tendencies:
  - Identify if my incoming attacker (the player targeting me counter-clockwise) is consistently submitting `[act: raid]` regardless of pledge.
  - Identify if my clockwise target is defecting to `[act: raid]`.

### Pledge Stage
- **Round 1:** Submit `[pledge: scout]`.
- **Rounds 2–5:**
  - If incoming attacker raided me in the previous round:
    - If I anticipate they will raid again, pledge `[pledge: escort]` to protect points and secure guaranteed +2 points while denying them +5.
  - If incoming attacker did not raid or if playing defensively is unnecessary, submit `[pledge: scout]`.

### Act Stage
- Match the pledge or deviate strategically based on the revealed public pledges and opponent history:
  - If I pledged `escort`, submit `[act: escort]`.
  - If I pledged `scout`:
    - If incoming attacker consistently defects to raid, submit `[act: escort]` if permitted by rules/affordability to block the raid and score +2, OR:
    - If clockwise target is confirmed to genuinely scout (not defect to raid), submit `[act: raid]` to capture +5 points.
    - If clockwise target also defects to raid (meaning raid vs raid would yield -1), do NOT raid them; submit `[act: escort]` if attacked, or `[act: scout]`.

### General Execution
- When submitting responses, output a single short sentence of reasoning followed immediately by the bracketed token (e.g., `[pledge: scout]` or `[act: escort]`).