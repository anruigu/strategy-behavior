---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1622
---
### Playbook: Sonar Picket

- **Station Notes & Coordination:**
  - In Round 1, propose an explicit, symmetric escort partnership to a specific peer boat (e.g., "[Partner], let's pair escort claims each round for +5 mutual points.").
  - If a peer agrees or reciprocates in note/salvage, publicly confirm the mutual lock every round to prevent miscoordination or poaching by third parties.
  - If multiple boats offer, stick with the existing committed partner to ensure a guaranteed 5 points every round.

- **Hide Stage:**
  - Select an unpredictable cell (1–9). Avoid patterns, recent consecutive locations, and common focal coordinates (1, 5, 9).

- **Fire Stage:**
  - Fire at the assigned standing order station (`[target: <StandingOrderBoat>] [fire: <cell>]`).
  - Vary the target cell every round to scan across the board.
  - Do not fire on Harbor during regular rounds; Harbor retaliation eliminates standing on the board. Only consider attacking Harbor on the absolute final round (Round 6) if the 3-point jettison payoff is safe from subsequent-round elimination penalties.

- **Claim Stage:**
  - Strictly report the private outcome provided by the office: if told `HIT`, submit `[claim: hit]`; if told `MISS`, submit `[claim: miss]`. Claims are mandated to match true shot results.

- **Escort (Salvage) Stage:**
  - Always submit `[salvage: <PartnerName>]` matching the negotiated escort partner.
  - If no explicit agreement is established, salvage the boat that targeted or named me in the prior round.
  - Never submit `[salvage: none]`; mutual escorting (+5 points) is the primary engine of total score.