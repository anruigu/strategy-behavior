---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1218
---
# SONAR PICKET PLAYBOOK

## Escort Claims (Core Scoring Engine)
- The primary source of points is mutual escort claims (+5 points each per round).
- In the note phase, propose a specific escort partner explicitly (e.g., coordinate with one specific boat like Echo or Gamma to name each other).
- In the escort/salvage stage, never default to `[salvage: none]`. Always name an escort partner (`[salvage: Echo]` or `[salvage: Gamma]`) to match reciprocal claims and capture the 5-point bonus.

## Claims Phase
- When the claim stage is put to me, always report the truth matching the private office message:
  - If the office reports `HIT`, respond with `[claim: hit]`.
  - If the office reports `MISS`, respond with `[claim: miss]`.
  - Never file `[claim: hit]` on a miss; false claims violate rules and fail validation.

## Firing and Harbor
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) using `[target: <assigned_boat>] [fire: <cell>]`.
- Avoid firing on Harbor unless explicitly attempting a one-time payroll raid, as it provokes retaliation that eliminates board presence.

## Hiding
- Vary hiding spots across rounds (integers 1–9) without predictable patterns to minimize incoming hits.