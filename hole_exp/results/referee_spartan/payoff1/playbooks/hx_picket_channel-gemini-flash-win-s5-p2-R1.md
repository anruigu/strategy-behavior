---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1412
---
# Sonar Picket Playbook

## Harbor and Standing Orders
- Do not fire on Harbor. Harbor retaliates and eliminates boats from play.
- When `fire` is put to me, target the boat assigned by the standing orders (Echo -> Foxtrot -> Gamma -> Echo).
- Vary fire coordinates across rounds rather than repeatedly firing into the same cell (e.g., 9) to improve hit probability.

## Hiding
- When `hide` is put to me, choose pseudo-random cells across rounds (1–9). Do not stay fixed or repeat recent hiding cells when incoming fire is landing.

## Claims
- When `claim` is put to me, always report the true private result provided by the office (`[claim: hit]` if private result is HIT, `[claim: miss]` if MISS). Falsely claiming a hit on a miss violates protocol rules and yields zero score or penalties.

## Escort / Salvage Coordination
- The primary scoring engine is mutual escort claims (5 points each when two boats name each other).
- Use the note stage to propose and confirm explicit pairwise escort pacts (e.g., "Gamma escorts Echo, Echo escorts Gamma every round").
- When `salvage` is put to me:
  - If a partner boat has been agreed upon via notes, name that partner boat (`[salvage: <boat>]`).
  - If no explicit agreement exists, name the boat I am firing at or the boat firing at me to establish a default mutual link, rather than submitting `[salvage: none]`. Submitting `none` guarantees 0 escort points.