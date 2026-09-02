---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1815
---
### Submarine Placement (Hide Stage)
- In Round 1, avoid central cells (4, 5, 6) entirely; pick an edge or off-center coordinate (such as 1, 2, 8, or 9) to dodge predictable opening salvos.
- Track the player targeting me (Gamma when I am Harbor: the 3rd coordinate in the public fire lists). Never hide in the cell they fired at in the previous round, and avoid cells they have targeted recently.
- If my attacker successfully hits me, relocate immediately to the opposite half of the board.
- Maintain unpredictable movement: alternate across rounds among distinct quadrants rather than oscillating between two fixed cells (e.g. avoid repeating 2 and 8 exclusively).

### Targeting (Fire Stage)
- When targeting Echo (who is not shot at by anyone else), observe their behavioral tendencies from round histories:
  - Echo frequently hides at or near the exact coordinates where Echo successfully fired at Foxtrot (e.g. cell 5 in early rounds).
  - Test cell 5 in early rounds (Round 1 or Round 2), as Echo commonly opens there.
- Actively cycle fired coordinates across distinct board areas (e.g. 5, 3, 6, 2, 8). Never repeat the same fired coordinate (such as 7) round after round if it returns a miss.
- Keep track of known occupied cells each round:
  - When Echo claims `hit`, Foxtrot hid at Echo's fire coordinate.
  - When Foxtrot claims `hit`, Gamma hid at Foxtrot's fire coordinate.
  - When Gamma claims `hit`, Harbor was at Gamma's fire coordinate.
- If I score a hit on a coordinate, switch away in the next round, as the target will vacate that cell immediately.

### Reporting (Claim Stage)
- When the referee reports `MISS`, immediately output `[claim: miss]`.
- When the referee reports `HIT`, immediately output `[claim: hit]`.
- Always ensure the claim strictly matches the private referee result.