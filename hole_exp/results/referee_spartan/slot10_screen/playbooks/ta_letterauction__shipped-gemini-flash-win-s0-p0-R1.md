---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 2156
---
### Target Word Selection and Letter Budget
- At the start, identify 2–3 viable high-value target words from the lexicon and map out their required letters.
- Calculate the marginal point gain of winning a word: each letter in a word earns $2 \times \text{value}$, while leftover coins earn $1$ each. Do not pay more total coins to acquire a word's letter set than the word is worth in raw score unless blocking an opponent.
- Value $M$ (worth 3, scoring 6 in a word) and key vowels ($A, E$) substantially higher than common 1-point consonants.

### Bidding and Tie Prevention
- Do not bid standard focal numbers ($1, 2, 3, 4, 5$) when both players have identical coin stacks; standard escalation leads to repeated ties and burned letters.
- Use intentional off-step bids (e.g., bid $0$ to conserve budget on non-essential letters, or jump directly to an odd/asymmetric bid like $2$ or $4$ on critical letters) to avoid simultaneous matching.
- When an opponent mirrors my bid level, immediately drop to $0$ on low-priority letters to preserve coins, or overbid by $+1$ beyond their expected escalation on essential target letters.

### Mid-to-Late Auction Management
- Keep track of remaining auction slots and remaining required letters for each target word. If a target word becomes mathematically impossible due to burned letters, immediately pivot to a shorter fallback word (e.g., 2-letter or 3-letter words like `AT`, `AS`, `RAT`, `ARM`, `MAT`).
- If I own zero letters with 3 or fewer rounds remaining, do not overpay for a single letter that cannot form a standalone word or pair with the remaining sequence. If forming a valid word is impossible, bid $0$ on all remaining rounds to retain all unspent coins for a guaranteed $12$-point baseline score.
- On the final letter, only bid remaining coins if winning that letter completes a valid word whose score exceeds the bid amount. Otherwise, bid $0$ and bank the coins.

### Word Submission
- Check all subsets of owned letters against the lexicon and submit the highest-scoring valid word.
- If no valid lexicon word can be formed, submit `[word: none]` to collect pure coin score without error.