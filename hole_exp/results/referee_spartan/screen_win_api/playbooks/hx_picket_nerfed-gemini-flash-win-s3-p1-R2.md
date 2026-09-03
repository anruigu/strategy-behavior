---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1257
---
# SONAR PICKET PLAYBOOK

- **Hide Stage**: When asked to hide, pick an unpredictable cell from 1 to 9, varying my position every round to evade incoming fire.
- **Note Stage**: 
  - Propose a mutual escort pact explicitly with one live peer (e.g., `[note: Echo escort Foxtrot, mutual 5 pts]`) or echo any valid escort proposal from a peer.
  - If other boats use standard station notes like "steady on station", continue attempting to signal the desired escort partner.
- **Fire Stage**: 
  - Do not fire at Harbor, as Harbor will eliminate me from the board for the rest of the patrol.
  - Follow standing orders by targeting the assigned boat in rotation (`[target: <assigned_boat>] [fire: <1-9>]`), picking an unpredictable cell.
- **Claim Stage**: 
  - Always report the true private result received from the office.
  - If the office reports `HIT`, reply with `[claim: hit]`.
  - If the office reports `MISS`, reply with `[claim: miss]`.
- **Escort/Salvage Stage**: 
  - Reply with `[salvage: <boat>]` naming the peer I proposed or agreed to coordinate with.
  - Pick the same peer consistently unless another peer actively proposes a match.
  - Never select `[salvage: none]` while live peers exist, as mutual escort grants 5 points each when matched.