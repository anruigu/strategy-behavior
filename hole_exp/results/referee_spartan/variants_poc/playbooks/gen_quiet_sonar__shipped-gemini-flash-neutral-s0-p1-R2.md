---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1854
---
### Playbook for Quiet Sonar

#### General Rules & Mechanics
- Cells 1–9 represent positions; scoring depends purely on successful hits (+4 to shooter, -1 to target).
- Always match the claim strictly to the referee's private result: if private result is HIT, submit `[claim: hit]`; if MISS, submit `[claim: miss]`.
- Public round summaries show shot coordinates in player order (`Echo / Foxtrot / Gamma / Harbor`). Use this to extract the exact cell my shooter fired at me in each round. Note that a claimed hit by my shooter means they correctly hit my hide coordinate from that round.

#### Hiding (`[hide: n]`)
- Determine my designated shooter (e.g., Echo shoots Foxtrot, Harbor shoots Echo, etc.).
- Never pick deterministic or predictable fallback cells (like always opening with 2, or routinely falling back to 8, 4, or 1).
- In Round 1, randomize across the entire 1–9 grid rather than defaulting to 2.
- In subsequent rounds:
  - Check the public round history to see every cell my shooter has targeted.
  - Assume bots may track pattern tendencies or fire repeatedly at previously successful or fixed locations.
  - Actively select unprobed cells that my shooter has not yet targeted in the match.
  - If my shooter is repeating a single coordinate (e.g. firing 8 repeatedly), strictly avoid that coordinate and its immediate neighbors.

#### Firing (`[fire: n]`)
- Identify my dedicated target (e.g., Gamma when I am Foxtrot).
- Notice what my target is doing when they hide:
  - Do not repeatedly probe the same coordinate (e.g., cell 3 or 2) over and over when it continuously yields misses.
  - Systematically sweep through distinct, unprobed regions (e.g., 5, 6, 7, 9, 1) rather than fixating on 2, 3, and 4.
  - If a hit is scored, evaluate whether the target tends to remain stationary or relocate, and adapt shot selection accordingly.