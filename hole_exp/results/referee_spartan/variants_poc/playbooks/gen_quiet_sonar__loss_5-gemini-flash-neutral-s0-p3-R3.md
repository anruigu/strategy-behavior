---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1801
---
### Submarine Strategy Playbook

#### Rules & Strict Invariants
- When prompted to claim, always submit exactly the true private referee result (`[claim: hit]` if hit, `[claim: miss]` if miss). Claims are strictly validated against private referee reports.
- Remember the cyclic targeting ring:
  - Echo -> Foxtrot
  - Foxtrot -> Gamma
  - Gamma -> Harbor
  - Harbor -> Echo
- Note player order in the public fire history strings (`fires A/B/C/D` corresponds to Echo/Foxtrot/Gamma/Harbor).

#### Hiding Phase
- Identify who is shooting at me:
  - As Harbor, Gamma shoots at me (3rd entry in the fire report).
  - As Gamma, Foxtrot shoots at me (2nd entry).
  - As Foxtrot, Echo shoots at me (1st entry).
  - As Echo, Harbor shoots at me (4th entry).
- Track the shooter's targeting habits:
  - Never hide in a cell the shooter targeted in the last 2 rounds.
  - If the shooter gets stuck repeating a coordinate (e.g., repeatedly firing 7), stay strictly away from that cell and its adjacent cells.
- Actively randomize and rotate hiding spots across distant off-center and corner cells (e.g., cycle among 1, 2, 8, 9, 3) rather than camping repeatedly on a single cell across multiple late rounds.

#### Firing Phase
- Identify my fixed target (when Harbor, target is Echo).
- Track prior shots and never repeat a cell that previously yielded a miss against that target during the match.
- Echo frequently fires at central cells (5, 6) where Foxtrot tends to sit, and often hides in adjacent or unpressured positions.
- Diversify probes across distinct unexplored quadrants (e.g., explore 3, 5, 6, 9 instead of repeatedly spamming 7 or 8 after confirmed misses).
- If a target has not been hit yet, systematically search across un-probed cells rather than re-targeting any cell already confirmed empty.