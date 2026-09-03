---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1392
---
# Sonar Picket Playbook

- **Boats and Roster**:
  - The live boats are strictly Echo, Foxtrot, and Gamma (plus Harbor). Non-existent names must never be referenced, messaged, or named in salvage.

- **Escort Claims & Notes**:
  - Mutual escort is the most reliable scoring mechanism (+5 points per successful mutual pair per round).
  - Never default to `[salvage: none]`.
  - In notes, continuously propose a mutual escort to a specific boat (e.g. Foxtrot or Echo) to break up competing pairs.
  - In the escort stage, always submit `[salvage: <boat>]` matching the boat I targeted in my note proposals, never giving up on attempting the match.

- **Firing and Target Selection**:
  - Follow standing orders by default (`Echo -> Foxtrot -> Gamma -> Echo`) using `[target: <boat>] [fire: n]`.
  - Do not fire on Harbor; the retaliation will remove me from the board.
  - Choose firing coordinates across 1 to 9 based on educated guessing or varying cells across rounds to hunt the target boat.

- **Reporting Claims**:
  - When the claim prompt arrives, strictly reflect the private truth told by the office: reply `[claim: hit]` if the office reported a hit, and `[claim: miss]` if the office reported a miss.

- **Hiding**:
  - Unpredictably change hide coordinates (integers 1 to 9) each round to minimize the upstream boat's hit probability. Avoid staying in the same cell consecutively.