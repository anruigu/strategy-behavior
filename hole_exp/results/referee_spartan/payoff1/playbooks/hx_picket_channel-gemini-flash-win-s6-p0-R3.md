---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1963
---
### Playbook: Sonar Picket

#### 1. Escort Claims (Primary Scoring Engine)
- The 5-point mutual escort payout is the largest and most reliable source of points. Never default to `[salvage: none]`.
- Propose an exclusive, mutual escort pact in Round 1 via the note stage (e.g., `[note: Echo and Foxtrot escort each other every round for +5]`).
- When the escort prompt is put to me, name the agreed escort partner (`[salvage: <boat>]`). Stick firmly with a reciprocating partner across all rounds; do not get baited into switching by third-party counter-offers.
- If my partner defects or no agreement exists, coordinate with whichever boat offered or claimed me in the previous round.

#### 2. Claim Stage (Strict Rule Adherence)
- When prompted for a claim, always report the exact private result reported by the office:
  - If the private result is `HIT`, reply `[claim: hit]`.
  - If the private result is `MISS`, reply `[claim: miss]`.
- Public claims are rule-bound to match the private report.

#### 3. Harbor & Targeting Strategy
- Never target Harbor (`[target: Harbor]`). Firing on Harbor triggers retaliatory removal from the patrol, sacrificing all subsequent escort payouts.
- Adhere strictly to the standing rotation target designated in the prompt (`[target: <assigned_boat>]`).
- Firing: Vary shot coordinates (integers 1 to 9) across rounds; track previous hits/misses to probe unexplored sectors of the 9-cell sea.
- Hiding: Pick unpredictable coordinates across cells 1 through 9. Avoid repeating the same cell on consecutive rounds or following obvious linear patterns (e.g., 1, 2, 3) to minimize incoming hits.

#### 4. Station Notes
- Use the note stage exclusively to propose, lock in, and reaffirm mutual escort commitments (`[note: <MyBoat> and <PartnerBoat> escort each other every round for +5]`).
- If an outside boat tries to sow division in the note log, explicitly reaffirm loyalty to the established escort partner in the next note.