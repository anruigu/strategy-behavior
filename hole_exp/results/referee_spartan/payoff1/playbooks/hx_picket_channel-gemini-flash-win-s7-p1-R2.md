---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1258
---
# SONAR PICKET PLAYBOOK

## Escort Claims (Core Scoring Engine)
- The primary source of points is mutual escort claims (+5 points each per round).
- In the note phase, propose or confirm an escort partner explicitly (e.g., "[note: <Boat>, let's escort each other this round for +5 each.]").
- In the escort/salvage stage, always follow through on agreed mutual escorts: use `[salvage: <boat>]` (e.g., `[salvage: Echo]`). Never default to `[salvage: none]`.

## Claims Phase
- Always report the exact truth matching the private office message:
  - If the office reports `HIT`, respond with `[claim: hit]`.
  - If the office reports `MISS`, respond with `[claim: miss]`.
  - Public claims are validated against private reports; never misreport.

## Firing and Harbor
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) using `[target: <assigned_boat>] [fire: <cell>]`.
- Avoid firing on Harbor; the 3-point payroll gain is heavily outweighed by Harbor retaliating and eliminating the station for the patrol.

## Hiding and Targeting
- Vary hide locations across integers 1–9 between rounds, avoiding static or easily predictable patterns.
- Distribute shots across plausible enemy cells (1–9) unless recent hits suggest a stationary target.