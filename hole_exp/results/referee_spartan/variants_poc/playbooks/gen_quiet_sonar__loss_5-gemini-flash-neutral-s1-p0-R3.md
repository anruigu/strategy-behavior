---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1837
---
### Claiming Rule
* When the referee tells me `MISS`, I must output `[claim: miss]`.
* When the referee tells me `HIT`, I must output `[claim: hit]`.
* Never deviate; the rules mandate that the claim strictly matches the private result.

### Reading Public History
* Firing order is circular: Echo fires at Foxtrot (1st coordinate), Foxtrot fires at Gamma (2nd coordinate), Gamma fires at Harbor (3rd coordinate), Harbor fires at Echo (4th coordinate).
* Harbor's fire coordinates (4th coordinate) and claims (4th claim) reveal both where Harbor shot at me and whether Harbor hit me.
* Foxtrot's hide cell is what I am trying to hit with my 1st coordinate shots.

### Hiding Strategy
* If Harbor hits me at cell $X$ in round $r$, Harbor often repeats fire at cell $X$ or adjacent cells in round $r+1$. Immediately flee to distant, unhit cells (e.g., if hit at 5 or 6, hide at 1, 2, 8, or 9).
* If Harbor repeatedly fires at a fixed cell (e.g. continually shooting 5 or 6), stay far away from that target cell.
* Avoid predictable alternating patterns between the extreme edges (e.g., repeatedly switching 1 and 9); distribute hiding spots among unattacked safe cells (1, 2, 8, 9, 3).
* Never hide in cell 5 on Round 1.

### Firing Strategy
* Do not repeat a fired cell if it resulted in a miss in a previous round (e.g., never fire cell 4 three rounds in a row after missing).
* In Round 1, probe common hide cells like 7 or 3.
* When I hit Foxtrot at cell $X$ (e.g. cell 3 in Round 2), anticipate Foxtrot moving away in the subsequent round. Probe adjacent cells ($X \pm 1$) or common relocation targets rather than repeating the exact same cell if Foxtrot tends to flee.
* Maintain an active list of untested coordinates for the current episode; systematically rotate through untested cells on misses instead of firing duplicate shots.