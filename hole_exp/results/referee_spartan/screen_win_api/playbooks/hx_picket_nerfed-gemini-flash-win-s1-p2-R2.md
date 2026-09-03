---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1064
---
- When picking a hide location, vary my cell choice (1-9) across rounds rather than repeatedly hiding in the same cell.
- In the note phase, use the note to explicitly propose or confirm mutual escort claims with an active patrol boat (Echo, Foxtrot, or Gamma).
- When choosing a target and firing cell, follow the standing orders (Echo -> Foxtrot -> Gamma -> Echo) unless an intentional deviation is required, and vary the target coordinate across rounds.
- In the claim phase, always report the exact private result told to me by the office: if the office says MISS, claim `[claim: miss]`; if the office says HIT, claim `[claim: hit]`. Do not falsely claim a hit on a miss, as claims are strictly required to match the private result.
- In the escort stage, always name a valid active boat from the current patrol (Echo, Foxtrot, or Gamma; never non-existent names like Beta) to maximize the chance of earning the 5-point mutual escort payout, prioritizing the boat proposed in the notes.
- Do not fire on Harbor unless willing to accept being put off the board.