---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1557
---
### Playbook: Sonar Picket

- **Station Notes & Coordination:**
  - Propose an explicit, symmetric escort partner in Round 1 note (e.g., "Foxtrot, let's pair escort claims each round for +5"). Do not post vague cooperative platitudes; name the exact boat and mutual action.
  - If a player reciprocates in notes or actions, lock in that escort pairing for all subsequent rounds.

- **Hide Stage:**
  - Choose a cell (1–9) with low predictability. Vary cell selection round-to-round; do not repeat recent cells or linger in focal spots (like 1, 5, or 9).

- **Fire Stage:**
  - Default to the assigned standing order target (e.g., `[target: <StandingOrderBoat>] [fire: <cell>]`) to avoid Harbor retaliation, varying target cell selection.
  - Do not fire on Harbor unless the game state makes taking Harbor's retaliation mathematically optimal on the final round.

- **Claim Stage:**
  - Always accurately report the private result: if the office reports `MISS`, reply with `[claim: miss]`. If the office reports `HIT`, reply with `[claim: hit]`.
  - Never file a false `[claim: hit]` on a miss; false claims do not award points and violate game rules.

- **Escort (Salvage) Stage:**
  - Always name the agreed partner boat (`[salvage: <BoatName>]`) whenever a mutual escort agreement is established or signaled.
  - If no agreement exists, default to reciprocating whoever named me last round, or pick the player who is not firing at me to propose a pair.
  - Never default to `[salvage: none]`; passing on escort claims forfeits the +5 mutual score engine.