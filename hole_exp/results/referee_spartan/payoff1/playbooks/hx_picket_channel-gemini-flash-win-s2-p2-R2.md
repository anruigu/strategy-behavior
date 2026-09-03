---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1472
---
# Picket Channel Playbook

## Station Awareness & Communication
- Recognize the exact roster of boats in the game (Echo, Foxtrot, Gamma, Harbor). Never address or propose escort to non-existent stations (e.g., Delta).
- In station notes, propose or accept mutual escort with an actual live peer station (Echo or Foxtrot).
- If two other boats form an exclusive escort pair, actively offer one of them an undercut or alternate cooperation in station notes, or attempt to break coordination if feasible.

## Escort / Salvage Coordination
- In the escort/salvage stage, file `[salvage: <boat>]` matching the boat that agreed or is most likely to name me. Do not claim a boat that explicitly signaled an exclusive partnership with someone else unless trying to break it.
- Never default to `[salvage: none]` if there is any chance of a match, as a mutual match awards 5 points each.

## Hiding & Firing
- When hiding, select coordinates unpredictably across 1–9, avoiding staying in the same cell consecutively or falling into obvious linear patterns.
- When firing, respect standing rotation orders against peer stations (Echo -> Foxtrot -> Gamma -> Echo) unless an explicit alternate coordination exists.
- Never fire on Harbor; Harbor carries the payroll penalty and will retaliate by removing the shooter from the board.

## Claims
- When filing a shot claim, always strictly match the private result provided by the office: `[claim: hit]` on HIT, `[claim: miss]` on MISS.