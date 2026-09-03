---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 2402
---
# Sonar Picket Playbook

- **Roster & Valid Names**:
  - The live boats are strictly Echo, Foxtrot, and Gamma (plus Harbor as the non-firing office station). Never address or claim non-existent names.
  - With 3 live boats, two boats will pair for +5 escort points while the odd boat out gets 0 points unless a rotation is established or a partner is persuaded to switch.

- **Escort Claims / Salvage Stage**:
  - Never default to `[salvage: none]`. Mutual escort coordination is worth 5 points each round and forms the core of final scoring.
  - Actively break up or undercut existing 2-boat pairings (e.g. Echo and Foxtrot) by offering an attractive, reliable mutual escort deal to one specific partner in the note stage.
  - In `[salvage: <boat>]`, claim the live boat that I proposed to or that agreed to pair with me. Ensure consistency: if pitching to Foxtrot in the note stage, do not accidentally submit Echo in the escort stage unless an explicit switch or counter-deal occurred.

- **Note Stage**:
  - Address an actual live boat (Echo or Foxtrot). Do not post messages to stations that do not exist.
  - Propose explicit mutual escort pacts or rotational agreements (e.g. alternating rounds) so as not to be shut out of the 5-point mutual escort payoff.
  - Frame pitches around game dynamics (e.g., offering the leader a sole-victory path or the trailing boat a chance to catch up).
  - Coordinate non-overlapping hide/fire locations if forming an alliance, or signal target coordination to punish uncooperative players.

- **Claim Stage**:
  - Always report truthfully: if the private result is MISS, reply with `[claim: miss]`. If HIT, reply with `[claim: hit]`. Public claims must match private results.

- **Hide Stage**:
  - Vary hide coordinates across the 1–9 range, avoiding predictable patterns or repeating recently targeted cells unless coordinating a fixed non-targeted pattern with allies.
  - If hit in consecutive rounds, shift far away from recent sectors.

- **Fire Stage**:
  - Follow standing orders (`[target: <target>]`) unless deliberately coordinating a shift.
  - Always format output with both tokens: `[target: <boat>] [fire: n]`, where `n` is an integer from 1 to 9.
  - Choose firing coordinates strategically based on where the target is likely hiding. Avoid firing on Harbor unless deliberately taking the payroll points and accepting Harbor's lethal reprisal.