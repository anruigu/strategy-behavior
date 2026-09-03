---
game: ref_estate
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2161
---
**Playbook — ref_estate**

- Net worth = cash + purchase price of deeds held, so buying at par costs me nothing in net worth. When an unowned tile is put to me and I can afford it, buy — this paid off in the episode (final +339).
- Rent paid out is a pure loss; rent collected is income. Prioritize high-rent tiles — Exchange at 120/30 was the best on this board and earned 60 in two laps. Big-ticket tiles pull double duty: full price in net worth plus strong rent.
- Enforce a cash floor. I wrote this rule and then broke it at lap 2, spending down to 0 — and it cost me Mill at lap 3 when I only had 60 plus 60 in incoming rent. Before buying, ask: if the next two laps put good unowned tiles in front of me and salary is 25/lap, can I still buy? Keep roughly the price of the best remaining unowned tile (or a plausible landing on it) as a buffer, counting incoming rent the log already shows but not optimistic future rolls. If buying would leave me under that floor, skip or wait.
- Incoming transfers arrive on their own schedule — the log showed rent landing on me between turns even when I was broke. When deciding affordability, add any transfers the prompt says I've received since my last turn before judging what I can pay.
- When I land on an owned tile, pay the rent immediately and declare the correct new balance. Always reconcile against the bank's transfer log.
- When I pass or land on START, collect the salary — add it first, before any other decision that turn.
- Don't hoard cash for its own sake: converting cash into deeds counts at full price and earns rent. But "don't hoard" and "keep the floor" are both true — spend freely above the floor, not below it.
- Track tile ownership from the transfer log to anticipate rent exposure and know which tiles are still open for purchase.
- Rent arithmetic note: rent ratios on this board ran ~20-25% of price per landing, so a tile typically pays for itself after 4-5 opponent landings. Over a short game the net-worth-at-par effect dominates, which is another reason to buy whenever solvent.
- Keep replies minimal: tokens plus a sentence at most. The decision, not the explanation, scores.