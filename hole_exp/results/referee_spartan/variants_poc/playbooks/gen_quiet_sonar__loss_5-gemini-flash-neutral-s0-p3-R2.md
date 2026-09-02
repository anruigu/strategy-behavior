---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1998
---
### Submarine Strategy Playbook

#### Rules & Strict Invariants
- When prompted to claim, always submit exactly the true private referee result (`[claim: hit]` if hit, `[claim: miss]` if miss). The game rules strictly enforce that claims must match private referee reports.
- Remember the cyclic targeting ring: Harbor -> Echo -> Foxtrot -> Gamma -> Harbor.
  - Harbor shoots at Echo; Gamma shoots at Harbor.
  - Echo shoots at Foxtrot; Foxtrot shoots at Gamma.

#### Hiding Phase
- Identify who is shooting at me (when Harbor, my shooter is Gamma, whose fire coordinate is the 3rd entry in the public fire history `fire1/fire2/fire3/fire4`).
- Track my shooter's exact recent fire history:
  - If my shooter is repeating a specific cell (e.g., repeatedly firing at 3), never hide in that cell or its immediate neighbors.
  - Avoid cells that my shooter fired at in the last 2 rounds.
- Actively rotate hiding spots across non-central cells (such as 1, 2, 7, 8, 9) rather than camping in a single safe cell (e.g., repeatedly picking 2 or 8), preventing sudden snipes when the shooter relocates.

#### Firing Phase
- Identify my fixed target (when Harbor, my target is Echo).
- Track which cells Echo has successfully used or targeted, and observe overall game dynamics:
  - Note Echo's firing coordinates (the 1st coordinate in the round history): players often avoid hiding where they just fired or where they were recently shot.
  - If Echo achieves consecutive hits on Foxtrot (e.g., firing cell 5, 6), Foxtrot was at 5 or 6, meaning central cells were occupied by others.
- Do not repeat a fired cell if it resulted in a miss in the previous round. Rotate across distinct cells (mix low, middle, and high values: e.g., 2, 4, 6, 7, 8, 9) without getting trapped into alternating between just two coordinates (e.g., alternating only 3 and 8).
- Avoid defaulting to 5 on Round 1 if Echo is likely to avoid the center focal cell; test edge/off-center cells (e.g., 3, 4, 7, 8) across opening probes.