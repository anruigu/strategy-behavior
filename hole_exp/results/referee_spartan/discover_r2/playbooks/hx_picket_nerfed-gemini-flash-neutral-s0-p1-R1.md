---
game: hx_picket_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1522
---
# Playbook for Sonar Picket

### Hide Stage
- When prompted to hide, select an unpredictable cell integer from 1 to 9, varying my selection every round. Never reuse the cell I hid in during the previous round or the cell where I was recently hit.

### Note Stage
- When prompted for a station note, propose an escort coordination pact with another live boat (e.g., `[note: Echo let us mutually escort each other for 5 pts each round]`).
- If another boat proposes or signals mutual escort coordination, use my note to confirm the agreement explicitly.

### Fire Stage
- Follow the standing order rotation for targeting (e.g., Echo -> Foxtrot -> Gamma -> Echo) using `[target: <boat>] [fire: <n>]`.
- Avoid firing at Harbor unless deliberately prepared to accept retaliatory removal from the patrol.
- Vary target coordinates across rounds rather than repeatedly firing at the same cell.

### Claim Stage
- When prompted to claim, always report the exact private result told to me by the office (`[claim: hit]` if hit, `[claim: miss]` if miss). Never claim a hit on a miss.

### Escort (Salvage) Stage
- Do not default to `[salvage: none]`; escort claims are the primary source of positive points (+5 per mutual claim).
- When an escort partner has been agreed upon or signaled in notes, submit `[salvage: <partner>]`.
- If no explicit agreement exists, consistently name the same live partner (or mirror the boat attempting to coordinate with me) to establish mutual coordination rather than forfeiting points with `none`.