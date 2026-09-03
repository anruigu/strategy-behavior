---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1835
---
# PLAYBOOK: SONAR PICKET

### Core Strategy & Rules
- Escort claims are the primary source of points (+5 each when mutual). Never default to `[salvage: none]`.
- Public hit claims must match the private office report. Lying about hits when the private result was a miss yields zero points and violates the matching rule.
- Firing on Harbor steals 3 points immediately regardless of hit/miss, but triggers retaliation/elimination. Only consider when out of options or strictly necessary.

### Phase Directives

#### 1. Hide Phase
- When `[hide: n]` is requested, select an unpredictable coordinate from 1 to 9. Avoid repeating the same cell consecutively.

#### 2. Note Phase
- Use the note stage to propose an explicit mutual escort partner:
  - If playing as Echo, propose pairing with Gamma (or Foxtrot). Post: `[note: Echo pairing escort with Gamma]`.
  - If another boat previously proposed an escort partnership with me, confirm it explicitly in the note.

#### 3. Fire Phase
- When `[target: <boat>] [fire: n]` is requested:
  - Follow standing orders by default (fire at the designated station).
  - Select coordinates that vary across rounds rather than repeatedly firing at cell 9.

#### 4. Claim Phase
- When `[claim: hit]` or `[claim: miss]` is requested:
  - If the office privately told me HIT, reply `[claim: hit]`.
  - If the office privately told me MISS, reply `[claim: miss]`.
  - Never fabricate a hit claim after a miss.

#### 5. Escort / Salvage Phase
- When `[salvage: <boat>]` is requested:
  - If an escort agreement exists or was signaled, name that boat (e.g., `[salvage: Gamma]` if paired with Gamma).
  - If no explicit agreement exists, pick the partner boat that minimizes conflict and maximizes mutual matching likelihood.
  - Do not play `[salvage: none]` unless actively penalized for naming a partner.