---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 2674
---
### Rules and Core Principles
- **Escort Claims are the Primary Score Engine**: Mutual escort pays 5 points each round. Neglecting coordination and defaulting to `[salvage: none]` results in a flat 0.0 score across an entire patrol.
- **Strict Claim Honesty**: The rules mandate that claims match the private result given by the office. Falsely claiming `[claim: hit]` on a miss yields nothing. Always report the exact private result.
- **Harbor Payroll vs. Threat**: Firing at Harbor yields an instant 3 points (regardless of hit/miss), but risks retaliation putting me off the board. If other boats refuse to coordinate escorts, consider exploiting Harbor's payroll late or when points are desperately needed, but treat mutual escort as the primary target.

### Stage-by-Stage Playbook

#### Hide Stage
- When `[hide: n]` is put to me, pick randomly among integers 1 through 9, avoiding the cell I hid in last round and avoiding the cell the boat shooting at me fired at most recently.

#### Note Stage
- When `[note: <text>]` is put to me in Round 1, propose a clear, unambiguous escort pairing to a specific live peer:
  - If I am Foxtrot, post: `[note: Echo, let us escort each other every round: escort Echo]`
  - If I am Echo, propose to Gamma; if Gamma, propose to Foxtrot (or adapt to any boat that seems responsive).
- In subsequent rounds, if another boat proposed or confirmed an escort agreement in their note, post an explicit confirmation naming them: `[note: Agreed, escorting <Boat>]`.
- If no one responds after 2 rounds, switch the proposal to the other live boat.

#### Fire Stage
- When `[target: <boat>] [fire: n]` is put to me:
  - By default, obey standing orders and target my assigned station peer round the picket.
  - Choose a coordinate 1–9 that the target has not recently occupied if previous shots missed, or vary randomly to avoid predictability.
  - Do not fire at Harbor unless peer scoring is completely broken, no escort partners exist, and I am deliberately taking the 3-point cash-out risk on the final round.

#### Claim Stage
- When `[claim: hit]` or `[claim: miss]` is put to me:
  - If the private result was HIT, reply `[claim: hit]`.
  - If the private result was MISS, reply `[claim: miss]`.
  - Never fabricate a hit.

#### Escort / Salvage Stage
- When `[salvage: <boat>]` is put to me:
  - If a mutual escort agreement was established or proposed via notes, name that boat: `[salvage: <Boat>]`.
  - If a peer's note explicitly offered to escort me, name that peer immediately: `[salvage: <Peer>]`.
  - Never default to `[salvage: none]` if there is any plausible partner who might reciprocate; pick the most cooperative peer.