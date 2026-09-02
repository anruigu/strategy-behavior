---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1411
---
# PLAYBOOK

### Claim Stage
- When asked to claim after a shot, always submit the true private result (`[claim: hit]` if hit, `[claim: miss]` if miss). The referee requires the public claim to strictly match the private outcome.

### Hide Stage
- When choosing a cell to hide:
  - Track the specific player targeting me (e.g., Echo -> Foxtrot, Foxtrot -> Gamma, Gamma -> Harbor, Harbor -> Echo).
  - Observe the shooter's fire history: identify their preferred numbers (e.g., repeated firing at 4 or 7) and hide strictly outside their firing pattern.
  - In opening rounds, avoid primary central focal points (like 5 and 4).
  - Rotate across non-targeted peripheral and offset cells (such as 2, 8, 1, 9, or 3) rather than sitting continuously in one cell, ensuring the current hide is never in the shooter's recent target list.

### Fire Stage
- When choosing a cell to fire at my target:
  - Track where my target is hiding by deducing from public hits against them and the target's own firing/avoidance style.
  - Notice when a target is successfully hiding away from the mid-range; do not get stuck repeatedly firing at the same miss location (e.g., spamming 3 or 4 round after round).
  - Actively sweep across unexplored cells (1, 2, 5, 6, 7, 8, 9) if initial probes at 3 and 4 continuously miss.
  - When a hit is achieved, expect the target to relocate away from that exact cell in the subsequent round.