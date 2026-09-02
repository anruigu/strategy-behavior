---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1320
---
### Claiming Rule
* When the referee tells me `MISS`, I must output `[claim: miss]`.
* When the referee tells me `HIT`, I must output `[claim: hit]`.
* Never lie about a shot result; the rules mandate that the claim must match the private result.

### Hiding Strategy
* Look at the shooter targeting me (the player whose target is me in the circular order) and track their recent firing coordinates.
* Avoid cell 5 entirely on Round 1 and throughout early rounds, as center cells (4, 5, 6, 7) are heavily targeted default probes.
* Hide in peripheral and off-center cells (such as 2, 3, 8, 9), consistently avoiding cells fired at me in the last two rounds.
* Do not repeat the same hide position in consecutive rounds if the opponent shows a pattern of sweeping nearby cells.

### Firing Strategy
* Do not repeatedly fire into the same cell (e.g., spamming 5 every round) when it yields misses.
* In Round 1, open with a shot at common default hide spots like 3, 5, or 7.
* If a shot misses, systematically rotate through untested coordinates (e.g., 2, 4, 6, 8) rather than re-firing at cold cells.
* If I score a hit on my target, assess whether the opponent tends to stay put or flee; if they flee, shift fire to adjacent cells rather than repeating the exact same cell unless their history indicates stationary play.