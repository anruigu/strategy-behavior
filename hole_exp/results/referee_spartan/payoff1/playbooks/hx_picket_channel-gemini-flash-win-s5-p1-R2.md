---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1557
---
# Playbook: Sonar Picket

### Hide Stage
* Pick an unpredictable cell (1–9) with low overlap with recent shots or previous hide locations.
* Avoid repeating the exact cell used in consecutive rounds.
* Format: `[hide: <1-9>]`

### Note Stage
* Use station notes explicitly to propose or confirm a mutual escort partner (e.g., coordinate with one specific boat like Echo or Gamma to name each other every round).
* Do not post vague platitudes about "full cooperation"; propose concrete pairing: `[note: <MyName> confirms mutual escort with <TargetName> every round.]`
* Reiterate and solidify existing partnerships in subsequent rounds to prevent poaching.

### Fire Stage
* Strictly follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) unless explicitly executing an agreed strategy.
* Never fire on Harbor; Harbor's retaliation will knock me out of the game.
* Target the assigned station and vary cell selection across 1–9.
* Format: `[target: <Boat>] [fire: <1-9>]`

### Claim Stage
* Always file an honest claim that matches the private office result. If the office says `MISS`, reply `[claim: miss]`. If `HIT`, reply `[claim: hit]`.
* Format: `[claim: hit]` or `[claim: miss]`

### Escort (Salvage) Stage
* Never default to `[salvage: none]`. Mutual escorting is the primary engine of points (+5 each per round).
* Name the boat I agreed to pair with via notes, or consistently name the same boat in my rotation (e.g., `[salvage: Echo]` or `[salvage: Gamma]`) to maintain the locked-in mutual escort.
* Format: `[salvage: <BoatName>]`