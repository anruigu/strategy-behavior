---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1409
---
# SONAR PICKET PLAYBOOK

## Escort Claims & Coordination
- In the note phase of Round 1, propose a mutual escort pact to a specific partner (e.g., "[note: Echo escorts Foxtrot every round; Foxtrot escort Echo for +5 each round]"). 
- In every escort stage, always claim the designated partner boat using `[salvage: <BoatName>]` instead of `[salvage: none]`. Mutual escorting is the primary engine for positive points (+5 per round).

## Notes & Communication
- Use notes purely to coordinate escort agreements or target patterns, not generic boilerplate like "steady on station".
- Honor escort commitments reciprocated by other boats.

## Firing Stage
- Fire at the designated rotation target according to standing orders (`[target: <boat>] [fire: n]`).
- Do not repeat the same firing coordinate every round (e.g., endlessly firing cell 9); vary targeting across cells 1–9 or track target patterns.
- Do not fire on Harbor unless the game state makes retaliatory elimination acceptable.

## Hiding Stage
- Randomize or vary hide coordinates across 1 through 9 every round to avoid predictable hits from the shooter tracking me.

## Claim Stage
- When reporting shot results, always match the office's private truth: `[claim: hit]` if private result is HIT, `[claim: miss]` if private result is MISS. The rules strictly require the public claim to match the private result. Never false-claim a hit on a miss.