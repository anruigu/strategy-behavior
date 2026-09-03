---
game: ref_commons
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1426
---
# Playbook: Shared Fishery Management

### Early to Mid-Game Strategy (Seasons prior to the final season)
- When starting Season 1, take slightly above the calculated sustainable share (e.g., sustainable share + 0.5 to 1.0) to establish a competitive score while keeping the stock near maximum capacity.
- When observing other boats harvesting slightly above sustainable yield, match or marginally exceed their average catch rather than dropping back to the theoretical sustainable rate. Letting other boats take more than me without matching reduces my relative score without saving the stock.
- When stock is regrowing well and multiple rounds remain, do not attempt to grab a massive portion (e.g., >25% of the total stock early) as this triggers rapid stock depletion and lowers aggregate yield in later rounds.
- When evaluating catch requests mid-game, ensure the combined estimated harvest leaves enough stock so that after the 50% regrowth, the stock does not drop sharply below viable levels.

### Final Season Strategy
- When entering the final season, ignore sustainability entirely since there are no subsequent rounds to preserve stock for.
- When submitting the final catch, calculate at least an equal split of the remaining stock (`remaining_stock / number_of_boats`) or slightly higher if expecting conservative play from others, taking the maximum safe extraction without risking total stock over-exhaustion.