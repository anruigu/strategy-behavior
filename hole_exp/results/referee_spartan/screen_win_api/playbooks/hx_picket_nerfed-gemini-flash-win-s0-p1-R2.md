---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1609
---
# PICKET PLAYBOOK

## Escort / Salvage Coordination
- Mutual escort claims generate +5 points each per round when reciprocal.
- During note stages, explicitly propose a mutual escort to a specific boat (e.g., "[note: Echo escort Foxtrot]").
- If another boat signals or names me for an escort pairing, mirror them in the salvage stage (`[salvage: <boat>]`).
- If bots are silent or merely repeating default status ("steady on station"), check if mutual pairings are actually succeeding by monitoring score progression. If neither boat pairs back, pick one partner consistently or test an alternate partner.

## Target and Firing
- Strictly follow standing orders for rotation: Echo -> Foxtrot -> Gamma -> Echo (`[target: <assigned_boat>] [fire: <cell>]`).
- When a target's location was successfully hit in a previous round, consider repeating or probing adjacent cells if their pattern repeats, but otherwise distribute shots across 1–9.
- Never fire on Harbor; Harbor retaliates by putting the shooter off the board for the rest of the patrol.

## Evasion and Hiding
- Vary hide coordinates unpredictably across rounds (1 to 9) to avoid the shooter tracking a static cell or predictable oscillation.

## Claims
- Always report the exact private result relayed by the office: if told MISS, reply `[claim: miss]`; if told HIT, reply `[claim: hit]`. Public claims must match private truth.

## Response Formatting
- Keep reasoning strictly to one brief sentence.
- Always output valid bracketed tokens: `[hide: n]`, `[note: <text>]`, `[target: <boat>] [fire: n]`, `[claim: hit|miss]`, `[salvage: <boat>|none]`.