---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1905
---
### Game Playbook: Quiet Sonar

* **Rule Validation & Claims:**
  * When the claim stage prompt appears, always match the referee's private outcome exactly: reply `[claim: hit]` if the private result was HIT, and `[claim: miss]` if MISS.

* **Target and Shooter Identification:**
  * Echo targets Foxtrot, Foxtrot targets Gamma, Gamma targets Harbor, Harbor targets Echo.
  * In the hide stage, look only at the firing history of the player shooting at me (e.g., if I am Gamma, track Foxtrot's shots; if Harbor, track Gamma's).
  * In the fire stage, look only at my assigned target's behavior and the history of shots I have taken at them.

* **Hide Strategy:**
  * Avoid central cluster cells (3, 4, 5, 6, 7) by default, as opponents heavily concentrate their fire in this band.
  * In Round 1, hide in the outer sectors (cells 1, 2, 8, or 9).
  * In subsequent rounds, track all cells fired at me by my shooter across recent rounds. Never hide in a cell my shooter targeted in the last two rounds.
  * Prefer cells 1, 2, 8, and 9 unless my shooter explicitly begins probing extreme edges. Alternate between edges (e.g., swapping between 1/2 and 8/9) to avoid becoming predictable.
  * If hit in round $t$, immediately relocate far away from that coordinate for round $t+1$.

* **Fire Strategy:**
  * Never repeat a fire coordinate immediately following a MISS. Repeated misses on the same cell waste critical probing rounds.
  * In Round 1, fire at cell 5 or 6 as a standard opening probe.
  * After any MISS, systematically cycle to unprobed sectors across the grid (e.g., sequence through 5, 4, 7, 2, 8, 3, 1, 9), picking coordinates that have not yet been probed in this episode.
  * If I score a HIT on my target in round $t$:
    * Fire at the exact same cell in round $t+1$ (bots often remain stationary).
    * If the follow-up shot results in a MISS, immediately resume probing unvisited cells.