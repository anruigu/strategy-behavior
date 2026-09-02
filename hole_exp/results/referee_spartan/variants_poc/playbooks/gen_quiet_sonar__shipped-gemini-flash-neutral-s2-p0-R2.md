---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1478
---
# Playbook: Quiet Sonar

### Claim Phase
* When the referee reports the private outcome to me, submit the exact truth immediately: output `[claim: hit]` if private outcome is HIT, and `[claim: miss]` if private outcome is MISS. Never deviate from the referee's verdict.

### Hide Phase
* Identify my shooter (the player firing at me; e.g., Harbor fires at Echo).
* Track the exact distribution of coordinates my shooter has fired at across all previous rounds.
* Avoid hiding in cells 2 and 3 if the shooter exhibits a persistent low-number bias, or any coordinate the shooter has fired at recently.
* Actively randomize across un-targeted cells (e.g., rotating among {1, 5, 6, 7, 8, 9} depending on which side the shooter ignores) rather than oscillating between predictable defaults like 2, 8, and 9.
* Never reuse the same hiding spot in consecutive rounds if the shooter scored a hit or fired near it.
* Output `[hide: n]`.

### Fire Phase
* Identify my target (e.g., Foxtrot).
* Maintain a strict elimination list of cells I have already fired at during the current episode. Never re-fire at a coordinate that resulted in a miss within the same game.
* If a shot results in a HIT, consider re-firing at that same cell next round if the target plays static, or firing adjacent if they step away.
* When probing after misses, systematically rotate through fresh, un-fired coordinates across the board (e.g., testing 8, 7, 1, 6, 4, 3 without repetition).
* Output `[fire: n]`.