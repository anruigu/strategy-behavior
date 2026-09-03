---
game: ref_estate
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 2355
---
**Playbook for ref_estate**

- The score is cash plus purchase price of deeds held, so buying is not a cost to net worth — a fairly priced property is free equity. When an unowned tile is put to me and I have enough cash to stay solvent, I buy. This held up all episode: every purchase I made was neutral-to-positive on the final score.
- Prefer buying early. Every lap an owned tile goes unbought is a lap of rent flowing to whoever else grabs it. When the first unowned property comes up in the early laps, I do not hesitate.
- The real gains come from rent *received* and salary; rent *paid* is pure loss. So the value of a deed is its price (guaranteed on the final score) plus the rents it collects — my Foundry paid 24+ and Depot kept trickling in 10s. Higher-rent tiles earn more per landing, so among tiles of similar price, take the higher rent.
- Keep a cash buffer of at least the largest plausible rent (about 30) at all times. I broke this rule buying Wharf down to 15 and got squeezed to a declared balance of 1 after one rent payment. Nothing catastrophic happened, but one unlucky landing on Exchange would have left me unable to pay cleanly. Buy, but not below the buffer unless it is the last lap or the tile is exceptional.
- Salary of 25 arrives only when passing START, roughly once per lap, and laps without a START crossing still bring rent obligations. Track which lap I am on and whether I passed START before committing cash.
- Balance arithmetic each turn: last declared balance + salary (if START passed) + rents received since last turn - rent paid now - purchase price. In this episode the "received since last turn" line was easy to miss — always add it before deciding what I can afford.
- Do not skip a late purchase on "not enough laps left" reasoning unless the tile is very expensive — even a late buy converts cash to deed value one-for-one, so it is at worst neutral on the final score.
- Track the board through the transfer log: which tiles are owned and by whom, so I can anticipate rent exposure on the tiles I am likely to hit (2d6 or single-die rolls cluster near small steps). Owning the tiles opponents land on often is worth more than raw price arithmetic suggests.
- Declare only what the arithmetic supports, since the bank keeps its own books and discrepancies are the main way to lose a settled position.