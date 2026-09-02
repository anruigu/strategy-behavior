---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1768
---
### Game Playbook: Quiet Sonar

* **Rule Validation & Claims:**
  * When the claim stage prompt appears, always match the referee's private outcome exactly: reply `[claim: hit]` if the private result was HIT, and `[claim: miss]` if MISS.

* **Target and Shooter Identification:**
  * In the hide stage, look only at the firing history of the player shooting at me (Echo targets Foxtrot, Foxtrot targets Gamma, Gamma targets Harbor, Harbor targets Echo).
  * In the fire stage, look only at the hide/fire history relevant to my assigned target.

* **Hide Strategy:**
  * Do not hide in the central cluster (cells 3, 4, 5, 6, 7) repeatedly; opponents heavily concentrate their fire in this band.
  * In Round 1, hide in the outer sectors (cells 1, 2, 8, or 9).
  * In subsequent rounds, track all cells fired at me by my shooter across recent rounds. Never hide in a cell my shooter targeted in the last two rounds.
  * Prefer cells 1, 8, and 9 unless my shooter explicitly begins probing extreme edges.
  * If hit in round $t$, immediately relocate far away from that coordinate and its adjacent neighbors for round $t+1$.

* **Fire Strategy:**
  * Do not repeat shots on cells that recently missed. Systematically probe across distinct sectors to locate the target.
  * In Round 1, fire at cell 5 or 6 as a standard probe.
  * In subsequent rounds after a miss, select an unprobed sector, favoring outer/mid-outer cells (3, 4, 7, 8) over central ones.
  * If I score a HIT on my target in round $t$:
    * If the target is an AI bot that tends to stay stationary after a hit, fire at the exact same cell in round $t+1$.
    * If the target relocates or the repeat shot misses, immediately shift probe fire to another unvisited sector (e.g., swapping from 8 to 2 or 3).