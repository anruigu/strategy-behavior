---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 2501
---
### Valuation and Bidding Playbook

- **Understand Word Value vs. Coin Trade-off**:
  - A word scores $2 \times \sum(\text{letter values})$, while unspent coins score 1 point each.
  - Spending coins is only profitable if the completed word yields more points than the total coins spent across all acquired letters.
  - Value 1 letters (A, E, R, S, T) contribute 2 points to a completed word; letter M (value 3) contributes 6 points.

- **Check Lexicon Valid Combinations Before Every Bid**:
  - Always verify whether a prospective letter actually forms a valid lexicon word with the letters currently owned.
  - Do not hallucinate words not in the provided lexicon (e.g., "ARS", "RAS", "RES", "ERS" are not valid words in this lexicon).
  - Explicitly check the shortest fallback words available in the lexicon: `A` (1 letter), `AS`, `AT` (2 letters), `ARM`, `MAT`, `RAT`, `SEA` (3 letters), `EAST`, `MARE`, `MEATS`, `REST`, `SEAT`, `STAR`, `TAME`, `TEAM` (4 letters).

- **Formulate a Target Word Early and Track Required Paths**:
  - Identify a primary target word and an immediate short fallback path early.
  - If holding `R` and `S`, the only viable 3-letter or 4-letter words require both `A` or `E` plus `T` (e.g., `REST`, `STAR`) or `M` (e.g., `ARM`, `SMART`).
  - Never bid on a letter late in the auction if winning it leaves zero possible words completable with the remaining letters.

- **Avoid Costly Ties and Predictable Round Numbers**:
  - Opponents frequently bid 1, 2, or 3 on standard letters.
  - To avoid burned letters via ties, bid non-standard numbers or outbid predictable tiers (e.g., bid 3 when expecting 2, or bid 0 to let the opponent overpay).
  - If tied on a letter, evaluate whether the letter is critical. If critical to your single viable word path, bid +1 over the tied value on the next opportunity or pivot to an alternate route.

- **Late-Game Coin Retention**:
  - In the final 2 rounds, calculate the exact completion math: if winning a letter cannot complete an actual word in the lexicon, bid 0 to conserve all remaining coins.
  - Only spend remaining coins if winning that specific letter guarantees completing a valid lexicon word whose $(2 \times \text{word value}) - \text{bid}$ increases total score.

- **Word Submission**:
  - Check the letter pool strictly against the exact lexicon list.
  - Submit the highest-scoring valid lexicon word spellable from the owned letters.
  - If no valid word from the lexicon can be formed, submit `[word: none]`.