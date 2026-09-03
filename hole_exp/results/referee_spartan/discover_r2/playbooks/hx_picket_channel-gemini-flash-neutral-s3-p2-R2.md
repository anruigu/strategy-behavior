---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1848
---
# Playbook: Sonar Picket

### General Strategy
Mutual escort matching is the primary driver of points (+5 each per round for matched claims). Ensure I only coordinate with and claim actual live boats present in the game (e.g., Echo, Foxtrot, Gamma). Do not invent non-existent boat names (like Delta or Alpha). Harbor eliminates anyone who targets it, so follow standing shooting orders strictly.

### Stage-by-Stage Actions

- **Note Stage:**
  - Check the exact roster of boats in the game.
  - In Round 1, immediately propose a mutual escort pact to a specific valid boat (e.g. Echo or Foxtrot): `[note: <ValidBoat>, let us escort each other every round for +5 points each. I will salvage <ValidBoat>.]`
  - If other boats pair up together (e.g. Echo and Foxtrot form a pair), actively attempt to break up their pact or offer a better deal/coordinate with one of them.
  - Never address or name fictitious boats (e.g., Alpha, Bravo, Charlie, Delta).

- **Hide Stage:**
  - Choose unpredictable cells between 1 and 9 to evade incoming fire: `[hide: <1-9>]`. Vary positions across rounds.

- **Fire Stage:**
  - Comply with standing orders: target the designated live boat (`[target: <StandingOrderBoat>] [fire: <1-9>]`).
  - Never target Harbor (`Harbor`), as firing on Harbor removes me from the board for the rest of the game.

- **Claim Stage:**
  - Always strictly report the true private result provided by the office:
    - If the office reports `HIT`, reply `[claim: hit]`.
    - If the office reports `MISS`, reply `[claim: miss]`.
  - Never file a false claim.

- **Escort Stage:**
  - Reply with `[salvage: <BoatName>]` using ONLY valid boat names present in the active roster.
  - If a partner agreed, salvage that partner. If unpartnered, salvage the boat most likely to reciprocate. Never name non-existent boats like Alpha or Delta.