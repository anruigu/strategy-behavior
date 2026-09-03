---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1865
---
### Rules & Structure Recap
- Escort/salvage coordination is worth 5 points each round if mutually claimed.
- Never claim `[salvage: none]` when a partner is available; always propose and lock in an escort partner.
- Claims must accurately match the private shot result; false claims do not generate extra points.
- Shooting Harbor pays an immediate 3 points, but Harbor will retaliate. Target designated standing order live stations unless a specific Harbor-farming strategy is agreed upon.

### Action Protocols

#### Hide Stage
- Pick unpredictable, non-edge coordinates (e.g., 2, 3, 5, 7, 8) varying round to round to minimize hit probability.
- Format: `[hide: <n>]`.

#### Note Stage
- From Round 1, immediately propose a direct, reciprocal 2-boat escort pact in public notes: specify the exact partner by name (e.g., `"Gamma, let us mutually escort each other every round for guaranteed 5 pts each round."`).
- If an escort partner reciprocates, reaffirm the mutual escort pact in every note.
- If no one responds or an odd player is left out, offer a rotating escort schedule or partner with the most cooperative boat.
- Format: `[note: <text>]`.

#### Fire Stage
- Fire at the designated standing order target unless explicitly coordinating a non-aggression or alternate agreement. Vary shot coordinates across rounds to find targets.
- Format: `[target: <boat>] [fire: <n>]`.

#### Claim Stage
- Always accurately report the true shot result told privately by the office.
  - If the office reports `HIT`, reply `[claim: hit]`.
  - If the office reports `MISS`, reply `[claim: miss]`.
- Do not claim a hit on a miss.

#### Escort / Salvage Stage
- Never submit `[salvage: none]`.
- Name the partner agreed upon in notes: `[salvage: <partner>]`.
- If no agreement was finalized, claim the boat that is most likely to name me back or that proposed an escort.