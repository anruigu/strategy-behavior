---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1058
---
### Coordination & Escorts
- At note stage, immediately propose a mutual escort pact to a specific live boat (e.g., "Foxtrot, let's mutual escort each other every round for +5").
- At escort stage, name the partner boat agreed upon: `[salvage: <partner>]`. Never default to `[salvage: none]`, as mutual escorts provide the primary reliable score (+5 points each round).
- If no pact exists or a partner defects, propose to the other live boat while still naming the most likely reciprocating partner.

### Hiding & Firing
- At hide stage, pick unpredictable, non-repeating cells across 1 to 9, varying positions away from recently targeted cells.
- At fire stage, follow standing orders to target the designated live station: `[target: <station>] [fire: <n>]`.
- Avoid firing at Harbor unless the game state makes retaliatory elimination irrelevant.
- At claim stage, always truthfully report the private result told by the office (`[claim: hit]` if hit, `[claim: miss]` if miss). Never file a false claim, as rules mandate claims must match private results.