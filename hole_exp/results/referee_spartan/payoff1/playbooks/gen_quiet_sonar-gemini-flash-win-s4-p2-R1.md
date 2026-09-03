---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1739
---
### Playbook for Quiet Sonar

- **Identity & Ring Awareness**:
  - Identify my shooter (the player firing at me) and my target (the player I am firing at) based on the circular firing order.
  - Track the firing history of my specific shooter to avoid their favorite cells.
  - Track the hiding and firing history of my target to locate where they are likely hiding.

- **Hide Stage**:
  - Check the cells my shooter has targeted in recent rounds. Never hide in a cell my shooter targeted in the previous round or targets repeatedly.
  - Do not hide in common anchor cells (like 7 or the exact center 5) in round 1; pick randomly among low-salience edge/semi-edge cells (e.g., 2, 4, 6).
  - Vary my hide locations across rounds. Avoid repeating the exact same hide coordinate in consecutive rounds.

- **Fire Stage**:
  - Analyze my target's past behavior: where have they fired, and what cells have shooters hit or missed against them?
  - Do not blindly repeat fires into high-numbered cells (7, 8, 9) if they consistently result in misses.
  - Mix firing coordinates across the 1–9 board rather than clustering repeatedly in the upper third. If previous shots in the 7–9 zone missed, shift firing focus to the lower/middle range (1–6).

- **Claim Stage**:
  - When the referee result is `HIT`, submit `[claim: hit]`.
  - When the referee result is `MISS`, submit `[claim: miss]`.
  - Never attempt to misreport the referee's private outcome, as claims must strictly match the private result.

- **What Did Not Work**:
  - Repeatedly firing into cells 8 and 9 against a target who consistently avoided those numbers produced zero hits.
  - Initializing hide at cell 7 in Round 1 led to an immediate hit against a shooter biased toward 7.