---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1669
---
# Playbook: Quiet Sonar

### Rules and Mechanics Clarifications
- Cell coordinates (1–9) represent discrete positions along a line.
- The referee strictly validates that claims match private outcomes. Truthful reporting is mandatory: never misreport.
- Track player identities accurately: check which role I am assigned at the start and identify who shoots at me and whom I shoot at.

### Claim Stage
- When the referee reports `HIT`, output `[claim: hit]`.
- When the referee reports `MISS`, output `[claim: miss]`.

### Hide Stage
- Identify the player targeting me (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
- Review the past firing history of my shooter from the round summaries.
- Avoid the cells my shooter has targeted recently (especially their most recent shot).
- If my shooter repeatedly fires into one cell or small cluster, deliberately hide far away in untargeted extreme or quiet sectors (e.g., 1, 2, 8, 9).

### Fire Stage
- Identify my fixed target.
- Maintain a strict memory of cells I have already fired at my target that resulted in a `MISS`. Never repeat a cell that missed in a previous round unless there is strong evidence the target re-occupies it.
- Never fire the exact same coordinate multiple rounds in a row after observing a miss on that coordinate.
- Systematic search: Sweep untried coordinates across distinct sectors (e.g., cycle through 1, 3, 5, 7, 9 or 2, 4, 6, 8) to maximize coverage over the 6 rounds.
- Look at public claim data: If my target is hitting their own target repeatedly from a certain hiding cell, or if other players' behavior indicates spatial patterns, correlate clues to pick untried numbers.