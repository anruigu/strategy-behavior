---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1975
---
# PLAYBOOK: SONAR PICKET

### Core Strategy & Rules
- Escort claims (+5 points for mutual pairing) require both parties to select each other. Default NPC boats post `"steady on station"` and typically form fixed pairing cycles or static pairs (e.g., Foxtrot and Gamma often match each other if not disrupted).
- Public hit claims must match the private office report. Lying about hits yields zero points and violates validation.
- Firing on Harbor steals 3 points immediately regardless of hit/miss, but triggers retaliation/elimination. Avoid firing on Harbor unless trailing decisively near the very end.

### Phase Directives

#### 1. Hide Phase
- When `[hide: n]` is requested:
  - Choose an unpredictable coordinate from 1 to 9.
  - Avoid repeating cells consecutively; vary between low, middle, and high numbers.

#### 2. Note Phase
- When `[note: <text>]` is requested:
  - If other boats broadcast specific pairing proposals, acknowledge and match them.
  - Otherwise, maintain standard station notes or clear pairing signals: `[note: steady on station]`.

#### 3. Fire Phase
- When `[target: <boat>] [fire: n]` is requested:
  - Follow standing orders by default (Echo -> Foxtrot -> Gamma -> Echo).
  - Vary shot coordinates across rounds (e.g., test 3, 5, 7, 2, 8) rather than repeating the same cell repeatedly.

#### 4. Claim Phase
- When `[claim: hit]` or `[claim: miss]` is requested:
  - If the private result was HIT, reply `[claim: hit]`.
  - If the private result was MISS, reply `[claim: miss]`.

#### 5. Escort / Salvage Phase
- When `[salvage: <boat>]` is requested:
  - If an escort agreement exists or a boat named me, reciprocate by naming that boat.
  - If playing Echo and pairing with Gamma is unreciprocated across early rounds, test switching escort claim to Foxtrot to find which bot reciprocates.
  - If mutual matches consistently fail to form with one boat across multiple rounds, switch the claimed partner.
  - Never play `[salvage: none]`.