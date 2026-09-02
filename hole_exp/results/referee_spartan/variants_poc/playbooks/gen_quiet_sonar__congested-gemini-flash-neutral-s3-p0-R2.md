---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1313
---
# Playbook for Quiet Sonar

### Claim Phase
- Always submit the exact result provided by the referee (`[claim: hit]` if hit, `[claim: miss]` if miss). The rules strictly mandate that claims match private results.

### Hide Phase
- In Round 1, avoid focal cells (4, 5, 6). Choose off-center or edge cells like 1, 2, 8, or 9.
- In Rounds 2 through 6, actively inspect the history of the player shooting at me (e.g., Harbor when I am Echo).
- If the shooter shows persistent or static targeting (e.g., firing at cell 7 every round), avoid that cell completely.
- Rotate unpredictably among safe cells (1, 2, 8, 9) rather than repeatedly sitting in the exact same cell for multiple consecutive rounds.

### Fire Phase
- In Round 1, open with a distributed probe (such as 3, 4, 6, or 7).
- In Rounds 2 through 6, do not re-fire at a coordinate where I already missed Foxtrot unless I have exhausted other high-probability cells. Systematically sweep unexplored coordinates across the 1–9 range.
- Track Foxtrot's firing coordinates and public claims:
  - If Foxtrot is scoring repeated hits on Gamma at a specific cell (e.g., cell 3 or 7), note whether Foxtrot tends to hide far from their own fire coordinates or at edge sectors.
  - Prioritize probing cells where Foxtrot has neither fired nor been confirmed absent.