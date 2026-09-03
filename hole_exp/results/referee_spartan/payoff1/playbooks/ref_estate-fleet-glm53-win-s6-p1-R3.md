---
game: ref_estate
model: fleet-glm53
condition: win
seed: 6
round: 3
chars: 2605
---
**Playbook for ref_estate**

- The score is cash plus purchase price of deeds held, so buying is not a cost to net worth — a fairly priced property is free equity. When an unowned tile is put to me and I have enough cash to stay solvent, I buy. This held up all episode: Foundry, Exchange, and Terrace all returned their price plus collected rent on the final score.
- Prefer buying early. Every lap an owned tile goes unbought is a lap of rent flowing to whoever else grabs it. Foundry bought on lap 1 collected rent almost every subsequent lap; that timing mattered.
- The real gains come from rent *received* and salary; rent *paid* is pure loss. The value of a deed is its price (guaranteed on the final score) plus the rents it collects. Higher-rent tiles earn more per landing, so among tiles of similar price, take the higher rent — Exchange (120/30) and Foundry (100/24) were the workhorses.
- Keep a cash buffer of at least the largest plausible rent (about 30) at all times. This episode my floor was 28 after Exchange, and I was one rent payment from being unable to afford Mill on lap 3 — being priced out of a purchase is the actual cost of running thin. Buy, but not below the buffer unless it is the last lap or the tile is exceptional.
- If cash is short of the price, the buy is simply off — declare [buy: no] and keep the arithmetic clean. Don't stretch or borrow.
- Salary of 25 arrives only when passing START, and laps without a START crossing still bring rent obligations. Track which lap I am on and whether I passed START before committing cash.
- Balance arithmetic each turn: last declared balance + salary (if START passed) + rents received since last turn − rent paid now − purchase price. The "received since last turn" line appeared repeatedly this episode (48, 60, 24) and is easy to miss — always add it before deciding what I can afford.
- Do not skip a late purchase on "not enough laps left" reasoning — even a late buy converts cash to deed value one-for-one, so it is at worst neutral on the final score. Terrace bought on lap 5 still finished at full value plus one rent.
- Track the board through the transfer log: which tiles are owned and by whom, so I can anticipate rent exposure. Rolls in this variant were single small numbers (1–3), so landing several tiles apart over consecutive laps; know my rent exposure to each neighbor's holdings.
- Declare only what the arithmetic supports, since the bank keeps its own books and discrepancies are the main way to lose a settled position. Every one of my declarations matched the book this episode — keep that streak.