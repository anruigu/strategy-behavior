---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1422
---
### Playbook for Sonar Picket

- **Hiding Phase:**
  - When choosing a cell to hide in, pick a pseudorandom number between 1 and 9 each round without relying on predictable patterns or repeating previous choices.

- **Note Phase:**
  - In the note stage, explicitly propose or confirm a mutual escort pact to a specific partner (e.g., "Foxtrot, let's pair escort claims every round for +5 points each: [salvage: Foxtrot]").
  - Do not post vague, boilerplate pleasantries; use the note strictly to name a specific partner and propose or confirm an escort pairing.
  - If a partner reliably reciprocates escort claims, continue proposing and confirming with that same partner each round.

- **Fire Phase:**
  - Do not fire at Harbor; Harbor's standing signal threatens to eliminate violators from the board.
  - Obey standing orders: target the next live station in rotation (Echo -> Foxtrot -> Gamma -> Echo) and fire at an unpredictable cell between 1 and 9.

- **Claim Phase:**
  - Always accurately report `[claim: hit]` on a hit and `[claim: miss]` on a miss as required by office rules.

- **Escort Phase:**
  - Never default to `[salvage: none]`.
  - Always submit `[salvage: <boat>]` naming the partner agreed upon in the note phase.
  - If no explicit agreement exists, select the boat that signaled intent to escort me in their note or the most cooperative live boat rather than leaving 5 mutual points unclaimed.