---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1532
---
# Sonar Picket Playbook

## Harbor and Standing Orders
- Do not fire on Harbor. Harbor retaliates and eliminates boats from the patrol.
- When `fire` is put to me, target the boat assigned by the standing orders (Echo -> Foxtrot -> Gamma -> Echo).
- Vary fire coordinates across rounds (1–9) rather than repeatedly firing into the same cell, adapting to recent target movement.

## Hiding
- When `hide` is put to me, choose unpredictable cells across rounds (1–9). Do not stay fixed or repeat recent hiding cells when incoming fire is landing.

## Claims
- When `claim` is put to me, always truthfully report the private result provided by the office (`[claim: hit]` if private result is HIT, `[claim: miss]` if MISS). The public claim is required to match the private report.

## Escort / Salvage Coordination
- The primary scoring engine is mutual escort claims (5 points each when two boats name each other).
- In the note stage:
  - Actively propose and reaffirm explicit pairwise escort agreements (e.g., "[note: Gamma commits to escorting Echo every round for guaranteed 5 points each]").
  - If two other boats form an exclusive pair, persistently bid to break the pair by offering 100% reliable mutual escorting to one of them.
- When `salvage` is put to me:
  - Name the agreed escort partner (`[salvage: <boat>]`).
  - If no agreement exists or if attempting to coordinate unilaterally, consistently name the candidate partner boat rather than submitting `[salvage: none]`. Never submit `none` unless no live boats remain.