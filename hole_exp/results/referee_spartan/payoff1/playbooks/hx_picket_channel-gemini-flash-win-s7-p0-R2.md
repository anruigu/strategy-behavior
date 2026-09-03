---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1627
---
# Playbook for Picket Channel

## Notes Stage
- Use notes to explicitly coordinate escort pairing. Name a single partner to mutually escort each round (e.g., "Foxtrot, let's escort each other this round for +5 each").
- Confirm the agreement explicitly every round with that partner as long as they reciprocate.
- Do not post vague platitudes about cooperation; propose explicit pairing agreements with a specific boat.

## Escort / Salvage Stage
- When the escort prompt appears, never default to `[salvage: none]`.
- Always name the agreed partner using `[salvage: <boat>]` (e.g., `[salvage: Foxtrot]`) to secure the +5 points from mutual escort.
- If no agreement was confirmed, name the most responsive partner or follow the picket rotation partner.

## Shooting & Harbor Stage
- Follow standing orders and fire at the designated target in the picket rotation using `[target: <boat>] [fire: <cell>]`.
- Avoid firing on Harbor in early/mid rounds, as Harbor will eliminate offending boats for subsequent rounds.
- Vary target cell locations or track recent enemy hide patterns rather than repeating identical cells repeatedly unless tracking a static target.

## Claim Stage
- Always file a claim that truthfully matches the private office result: `[claim: hit]` if private result is HIT, `[claim: miss]` if private result is MISS. Public claims must strictly match the private office feedback.

## Hide Stage
- Pick pseudo-random non-obvious cells (1 through 9), varying locations each round across different sectors (e.g., shifting between low, mid, and high cells) to minimize predictability against the incoming shooter.