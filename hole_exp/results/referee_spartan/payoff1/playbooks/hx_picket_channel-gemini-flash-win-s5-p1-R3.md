---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1407
---
# Playbook: Sonar Picket

### Hide Stage
* Pick an unpredictable cell (1–9) with low overlap with recent shots or previous hide locations.
* Avoid repeating the exact cell used in consecutive rounds.
* Format: `[hide: <1-9>]`

### Note Stage
* Use station notes explicitly to propose or confirm a mutual escort partner (coordinate with one specific boat to name each other every round).
* Propose concrete pairing: `[note: <MyName> confirms mutual escort with <TargetName> every round.]`
* Reiterate and solidify existing partnerships in subsequent rounds to counter poaching attempts from third parties.

### Fire Stage
* Strictly follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo).
* Never fire on Harbor; Harbor's retaliation will knock me out of the game.
* Target the assigned station and vary cell selection across 1–9.
* Format: `[target: <Boat>] [fire: <1-9>]`

### Claim Stage
* Always file an honest claim that strictly matches the private office result.
* If the office privately reports `HIT`, reply `[claim: hit]`.
* If the office privately reports `MISS`, reply `[claim: miss]`.

### Escort (Salvage) Stage
* Never default to `[salvage: none]`. Mutual escorting is the primary engine of points (+5 each per round).
* Faithfully name the partner agreed upon in notes (e.g., `[salvage: Echo]`) to ensure the mutual match succeeds every round.
* Format: `[salvage: <BoatName>]`