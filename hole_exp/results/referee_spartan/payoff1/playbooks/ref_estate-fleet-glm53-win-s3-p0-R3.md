---
game: ref_estate
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 2649
---
**Playbook — ref_estate**

- Net worth = cash + purchase price of deeds held, so buying at par costs me nothing in net worth. When an unowned tile is put to me and I can afford it, buy — this held again (final +291, built almost entirely from Wharf + Exchange + Quarry).
- Rent paid out is a pure loss; rent collected is income. Prioritize high-rent tiles — Exchange at 120/30 earned well and was my single best holding. Big-ticket tiles pull double duty: full price in net worth plus strong rent.
- Enforce a cash floor. I broke it again at lap 2, spending down to 36, and lost any shot at Mill at lap 3 as a result. Before buying, ask: if the next two laps put good unowned tiles in front of me and salary is 25/lap, can I still buy? Keep roughly the price of the best remaining unowned tile as a buffer, counting incoming transfers the prompt already shows but not optimistic future rolls. The lap-2 Exchange purchase was still right on pure value, but it left me too thin for Mill — accept that trade-off knowingly, not accidentally.
- Incoming transfers arrive on their own schedule — rent landed on me between turns even when I was nearly broke (36 → +30 next turn). When judging affordability, add any transfers the prompt says I've received since my last turn before deciding. This actually rescued me: the +30 let me take Quarry at lap 4.
- When I land on an owned tile, pay the rent immediately and declare the correct new balance. Always reconcile against the bank's transfer log.
- When I pass or land on START, collect the salary — add it first, before any other decision that turn.
- Don't hoard cash for its own sake: converting cash into deeds counts at full price and earns rent. But "don't hoard" and "keep the floor" are both true — spend freely above the floor, not below it.
- Track tile ownership from the transfer log to anticipate rent exposure and know which tiles are still open. My lap-5 rent of 24 to investor 1 on Foundry was foreseeable; owning more tiles is the only real shield.
- Rent arithmetic note: rent ratios on this board ran ~20-25% of price per landing, so a tile pays for itself after 4-5 opponent landings. Over a short game the net-worth-at-par effect dominates, which is another reason to buy whenever solvent.
- Sequence matters early: three players and few tiles means the board fills fast (by lap 4 most of it was owned). Buy aggressively on laps 1-3; late-game purchases matter less because fewer rent cycles remain, but at-par value still makes almost any affordable buy correct on the final lap too.
- Keep replies minimal: tokens plus a sentence at most. The decision, not the explanation, scores.