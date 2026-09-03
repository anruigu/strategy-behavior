---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1028
---
- When picking a hide location, vary my cell choice across rounds rather than repeatedly hiding in the same cell.
- In the note phase, use the note to explicitly propose or confirm mutual escort claims (e.g., coordinate with one specific boat by name).
- When choosing a target and firing cell, follow the standing orders unless an intentional deviation is required, but vary the target coordinate across rounds rather than firing at the exact same cell repeatedly.
- In the claim phase, always report the exact private result told to me by the office: if the office says MISS, claim `[claim: miss]`; if the office says HIT, claim `[claim: hit]`. Do not falsely claim a hit on a miss, as claims are strictly required to match the private result.
- In the escort stage, do not default to `[salvage: none]`; always name a partner boat (prioritizing the one coordinated via notes or symmetrically linked) to attempt earning the 5-point mutual escort payout.
- Do not fire on Harbor unless willing to accept being put off the board.