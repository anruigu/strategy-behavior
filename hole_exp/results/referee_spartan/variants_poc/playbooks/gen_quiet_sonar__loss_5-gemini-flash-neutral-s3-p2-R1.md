---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1701
---
### Game Playbook: Quiet Sonar

* **Rule Validation & Claims:**
  * When the claim stage prompt appears, always match the referee's private outcome exactly: reply `[claim: hit]` if the private result was HIT, and `[claim: miss]` if MISS.

* **Target and Shooter Identification:**
  * In the hide stage, look only at the firing history of the player shooting at me (Echo if I am Foxtrot, Foxtrot if Gamma, Gamma if Harbor, Harbor if Echo).
  * In the fire stage, look only at the hide/fire history relevant to my assigned target.

* **Hide Strategy:**
  * Do not hide in the central cluster (cells 4, 5, 6, 7) repeatedly; opponents heavily concentrate their fire in this band.
  * In Round 1, hide in the outer sectors (cells 1, 2, 8, or 9).
  * In subsequent rounds, track all cells fired at me by my shooter across recent rounds. Never hide in a cell my shooter targeted in the last two rounds.
  * Prefer cells 1, 2, 8, and 9 unless my shooter explicitly begins probing extreme edges.
  * If hit in round $t$, immediately relocate away from that coordinate and its adjacent neighbors for round $t+1$.

* **Fire Strategy:**
  * Avoid repeatedly cycling between the same 2–3 cells (e.g., repeating 5 and 6) if they yield misses; spread shots across untargeted cells.
  * In Round 1, fire at cell 5 or 6 as a standard probe.
  * When a shot misses, eliminate that cell from my target list for the next 1–2 rounds and probe another cell (testing 3, 4, 7, 8).
  * If I score a HIT on my target, fire at that same cell again in the next round only if the target is passive, or shift exactly $\pm 1$ cell if the target tends to shift minimally. If consecutive misses follow, resume probing unvisited cells.