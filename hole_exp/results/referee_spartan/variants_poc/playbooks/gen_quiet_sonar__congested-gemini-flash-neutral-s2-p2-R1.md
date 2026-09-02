---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1896
---
### Strategic Orientation

- The shooting loop is fixed: `Echo -> Foxtrot -> Gamma -> Harbor -> Echo`.
- I only fire at my fixed target, and only my designated shooter fires at me.
- Claims must be truthful (referee-validated). A claimed hit awards points to the shooter and subtracts points from the target, sharing rewards when multiple players hit.

### Hide Stage Playbook

- Identify the player who shoots at me. Track their firing history across rounds.
- Never hide in the cell my shooter targeted in the previous round or targets frequently.
- When choosing a hide location:
  - Do not default to predictable middle cells (4, 5, 6) in early rounds.
  - Distribute hide locations across non-central cells (such as 1, 2, 3, 8, 9) and vary them each round.
  - Avoid repeating the exact same hide cell in consecutive rounds once the game moves past the opening round.

### Fire Stage Playbook

- Identify my target's role and track where other players have shot at them, but primarily track my own firing history against them.
- Avoid repeatedly firing into central focal cells (like 5, 6, 7) if prior shots yielded misses.
- When selecting a fire coordinate:
  - Sweep through unexplored cells rather than re-testing missed numbers across rounds.
  - Test edge/outer coordinates (1, 2, 3, 8, 9) when opponents are dodging central fire.
  - If a hit is scored, re-evaluate whether the target is likely to flee or stay, prioritizing adjacent or evasive cells next.

### Claim Stage Playbook

- Always report the exact private result sent by the referee:
  - When the private result is `HIT`, output `[claim: hit]`.
  - When the private result is `MISS`, output `[claim: miss]`.

### Response Format Rules

- Keep internal reasoning strictly to a single brief line.
- Always conclude responses with the exact bracketed action token: `[hide: n]`, `[fire: n]`, or `[claim: hit]`/`[claim: miss]`.