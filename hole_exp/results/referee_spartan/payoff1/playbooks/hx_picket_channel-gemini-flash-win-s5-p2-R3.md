---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1587
---
# Sonar Picket Playbook

## Harbor and Standing Orders
- Do not fire on Harbor. Harbor retaliates and eliminates boats from the patrol.
- When `fire` is put to me, target the boat assigned by the standing orders (Echo -> Foxtrot -> Gamma -> Echo). Format: `[target: <boat>] [fire: n]`.
- Vary fire coordinates across rounds (1–9) rather than repeatedly firing into the same cell, adapting to recent target movement.

## Hiding
- When `hide` is put to me, choose unpredictable cells across rounds (1–9). Format: `[hide: n]`.
- Avoid repeating recent hiding cells or predictable adjacent sequences to evade incoming fire.

## Claims
- When `claim` is put to me, always truthfully report the private result provided by the office: `[claim: hit]` if private result is HIT, `[claim: miss]` if MISS. The public claim is strictly required to match the private report.

## Escort / Salvage Coordination
- Mutual escort claims are the primary scoring mechanism (5 points each when two boats name each other).
- In the note stage:
  - Actively propose and reaffirm explicit pairwise escort agreements with a single specific boat. Format: `[note: <text>]`.
  - If two other boats form an exclusive pair, persistently target the more receptive partner to break their lock, emphasizing 100% reliable matching.
- When `salvage` is put to me:
  - Format: `[salvage: <boat>]` (or `[salvage: none]` only if no live partners exist).
  - Name the agreed escort partner consistently.
  - If unpartnered, consistently name the candidate boat you are courting in notes rather than wasting the round on `none`.