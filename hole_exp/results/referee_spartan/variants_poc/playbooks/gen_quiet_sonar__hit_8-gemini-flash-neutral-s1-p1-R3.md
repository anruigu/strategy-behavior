---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1404
---
# PLAYBOOK

### Claim Stage
- Always submit the true private result reported by the referee (`[claim: hit]` if hit, `[claim: miss]` if miss). Claims must match private outcomes.

### Hide Stage
- Identify my assigned shooter from the fixed cycle (Echo -> Foxtrot, Foxtrot -> Gamma, Gamma -> Harbor, Harbor -> Echo).
- Review my shooter's recent firing history across all previous rounds.
- Never hide in any cell the shooter has targeted in the last 2 rounds or tends to repeat (e.g., 3, 4, 6, 7).
- In opening and mid rounds, prioritize unprobed peripheral/offset cells (such as 1, 2, 8, or 9).
- Rotate hiding locations between different safe cells across rounds to avoid predictable camping.

### Fire Stage
- Identify my target from the fixed cycle.
- Observe other players' firing choices and claims:
  - If Gamma fires and claims hits on Harbor, observe where Gamma is active, but focus primarily on deducing Gamma's hiding cell.
  - Notice that opponents frequently hide in offset/peripheral cells (e.g., 1, 2, 3, 8, 9) or copy common focal cells.
  - Systematically sweep unprobed cells across rounds (e.g., test 1, 2, 3, 8, 9 instead of concentrating shots only in the central band 4, 5, 6, 7).
  - Never repeat a fired cell that resulted in a miss on the previous round.
  - If a shot hits, expect the target to relocate on the subsequent round; probe adjacent or offset alternative cells next.