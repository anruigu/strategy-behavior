---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 2489
---
### Target Word Selection and Marginal Valuation
- At the start, identify 2–3 viable target words from the lexicon and note their letter requirements.
- Calculate the exact net marginal gain before bidding on any letter:
  - Letters in a word contribute $2 \times \text{value}$ points, while retained coins score $1$ point each.
  - A 1-point letter contributes $+2$ points to word score. Paying $2$ coins yields $\Delta\text{Score} = 0$; paying $1$ coin yields $\Delta\text{Score} = +1$. Never pay $>1$ coin for a 1-point letter unless it unlocks a strictly higher-tier word that offsets the cost.
  - Value $M$ (worth 3, scoring 6 in a word) up to $3\text{--}4$ coins because its net gain is $+5$ over a zero-bid pass if it completes a word.

### Bidding Strategy and Tie Avoidance
- Never match standard focal bids ($1, 2$) when both players have symmetric coin stacks; simultaneous bidding wastes letters via ties.
- On low-to-medium priority 1-point letters, bid either $0$ or $1$. If the opponent is prone to bidding $1$ or $2$, bid $0$ to force them to spend or let ties burn non-essential letters while preserving full coin reserves.
- Only bid $2+$ on critical keystone letters (such as $M$ or a final letter completing a 4+ letter word) where the score delta justifies the expenditure.
- If an opponent mirrors or ties a bid, pivot immediately: either drop to $0$ on the next letter to take the coin lead or bid strictly above their expected threshold if the piece is mandatory.

### Mid-to-Late Auction Management
- Constantly track the remaining auction schedule, burned letters, and opponent holdings to re-evaluate feasible lexicon targets.
- If burned letters eliminate longer target words, immediately downshift to efficient short words (e.g., `AS`, `AT`, `RAT`, `ARM`, `MAT`).
- Once a valid fallback word is secured (e.g., `AS` yielding $4$ word points + remaining coins), strictly evaluate any further letter bids against that baseline: only bid if winning the letter upgrades the word by more points than the bid itself.
- If it becomes impossible to form a valid word with positive net value, bid $0$ across all remaining rounds to lock in the guaranteed 12-point baseline from unspent coins.

### Word Submission
- Evaluate every valid permutation and subset of owned letters against the lexicon and submit the word maximizing $2 \times \sum \text{values}$.
- If no valid lexicon word can be formed, submit `[word: none]` to preserve pure coin points without penalty.