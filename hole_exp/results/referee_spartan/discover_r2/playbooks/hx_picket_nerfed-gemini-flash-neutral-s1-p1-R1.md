---
game: hx_picket_nerfed
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1365
---
# Sonar Picket Playbook

- **Hide Stage**: Choose hiding cells pseudo-randomly across 1 to 9, avoiding recent locations and avoiding predictable focal points.
- **Note Stage**: Post a clear coordination message in the notes to establish mutual escort pairings (e.g., offer a reciprocal escort with another boat). When other boats do not communicate or coordinate, default to `[note: steady on station]`.
- **Fire Stage**: 
  - Do not fire on Harbor unless willing to accept being targeted and put off the board.
  - Follow the standing order target sequence (`Echo -> Foxtrot -> Gamma -> Echo`) and pick an un-targeted cell against the assigned target boat using `[target: <boat>] [fire: n]`.
- **Claim Stage**: Always report the true private result received from the office using `[claim: hit]` or `[claim: miss]` as required by the rules.
- **Escort Stage**:
  - The highest scoring opportunity is mutual escort (+5 points each). Actively pursue a designated partner (preferably the boat shooting at me or my target if agreed via note).
  - If a specific partner boat offered or accepted an escort agreement, name that boat: `[salvage: <boat>]`.
  - In the absence of explicit coordination, default to naming the player boat most likely to reciprocate or standard default partner rather than `[salvage: none]`, since `none` guarantees 0 escort points every round.