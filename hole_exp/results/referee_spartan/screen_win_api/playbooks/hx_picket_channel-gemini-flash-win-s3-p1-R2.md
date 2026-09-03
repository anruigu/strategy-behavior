---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1781
---
### Rules & Structure Recap
- Escort/salvage coordination pays +5 points per round if mutually claimed. This is the highest expected value mechanism in the game (up to 30 points across 6 rounds).
- Always establish and lock in a 2-boat escort pact from Round 1 and stick to it strictly every round.
- Private shot results are authoritative; the office requires the public claim to strictly match the private result (miss -> `[claim: miss]`, hit -> `[claim: hit]`).
- Do not shoot Harbor; Harbor's retaliation eliminates players. Follow the designated live station standing orders for firing.

### Action Protocols

#### Hide Stage
- Pick unpredictable coordinates from 1 to 9, varying round to round without establishing an obvious pattern.
- Format: `[hide: <n>]`.

#### Note Stage
- In Round 1 note, immediately propose or confirm a direct, reciprocal 2-boat escort pact: name the specific partner and confirm mutual escort for guaranteed +5 points.
- In all subsequent rounds, continuously reinforce the established mutual escort pact with the confirmed partner to prevent coordination breakdowns.
- Format: `[note: <text>]`.

#### Fire Stage
- Fire at the assigned standing order target (Echo -> Foxtrot -> Gamma -> Echo).
- Vary shot coordinates across 1–9 to test different cells.
- Format: `[target: <boat>] [fire: <n>]`.

#### Claim Stage
- Accurately report the true shot result told privately by the office:
  - If the office reports `HIT`, reply `[claim: hit]`.
  - If the office reports `MISS`, reply `[claim: miss]`.

#### Escort / Salvage Stage
- Never claim `[salvage: none]`.
- Always name the locked-in mutual escort partner agreed upon in notes: `[salvage: <partner>]`.
- If no agreement exists, pick the boat that explicitly offered an escort or is most aligned.