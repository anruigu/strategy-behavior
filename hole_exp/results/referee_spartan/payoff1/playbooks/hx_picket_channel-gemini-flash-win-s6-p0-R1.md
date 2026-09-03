---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1652
---
### Playbook: Sonar Picket

#### 1. Escort Claims (Primary Scoring Engine)
- The 5-point mutual escort payout is the largest source of points in the game. Never default to `[salvage: none]`.
- In the station note stage, immediately propose a mutual escort partner (e.g., "Echo and Foxtrot escort each other every round").
- When the escort prompt is put to me, always name the agreed escort partner (`[salvage: <boat>]`). If no explicit deal exists, name the boat that is not shooting at me, or match whoever named me in the prior round.

#### 2. Claim Stage (Strict Rule Adherence)
- When the claim prompt is put to me, I must report the exact private result told to me by the office:
  - If the office reports `HIT`, reply `[claim: hit]`.
  - If the office reports `MISS`, reply `[claim: miss]`.
- Do not attempt to fake hits when a shot misses; public claims must strictly match the private office report.

#### 3. Harbor & Targeting Strategy
- Do not fire at Harbor unless deliberately accepting elimination for a guaranteed one-time 3-point gain; Harbor's standing signal removes me from the board for the rest of the patrol.
- Obey the standard rotation target (`[target: <assigned_boat>]`) unless an alternative target agreement has been established across the picket.
- Vary hiding cells randomly across rounds 1 through 9 to avoid predictable patterns. Vary firing cells based on where targets have not recently hidden.

#### 4. Communication & Station Notes
- Use the note stage purely to establish and reinforce explicit mutual escort pairings (`[note: <Boat A> and <Boat B> escort each other every round for +5]`). Avoid empty cheerleading.