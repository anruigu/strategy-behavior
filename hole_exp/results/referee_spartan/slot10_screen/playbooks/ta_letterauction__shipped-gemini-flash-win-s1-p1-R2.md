---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 2347
---
### Valuation and Target Strategy
- Calculate word values immediately: each letter in a formed word contributes $2 \times \text{value}$, whereas keeping an unspent coin contributes $1$.
- A target word of letter sum $V$ yields $2V$ points. Buying all its letters for a combined cost of $C$ yields a net score of $12 - C + 2V$. To beat holding all coins (score 12), the total spend $C$ must be strictly less than $2V$.
- Check the exact lexicon list carefully before committing to targets. Do not assume standard English words (e.g., SET, SEAR, STEM, SAME) are valid unless explicitly listed in the lexicon.
- Identify the most cost-effective words early, especially those utilizing high-value letters like M=3 (e.g., ARM, MAT, TEAM, MARE, SMART, MASTER) or short accessible lexicon words (e.g., REST, STAR, SEAT, EAST, RAT, SEA, MAT).
- Lock in a primary target word and a backup target before the first auction starts, dynamically updating based on auction results.

### Bidding Strategy
- Avoid overpaying for low-value 1-point letters: buying a 1-point letter for 3 coins loses net value unless it enables a high-value word that cannot be formed otherwise.
- Factor in tie risk: identical bids cause letters to go unsold. Bid 1 above predictable opponent bids only when the margin $2V - C > 0$ remains clearly positive.
- For high-value letters (e.g., M=3), be willing to bid aggressively (e.g., 4) to break ties, as M adds 6 points to word score.
- Do not bid on letters that do not fit into my active target words; bid `[bid: 0]` on unneeded letters to preserve capital and let the opponent waste coins.
- Track opponent coin balance at every step. If opponent has fewer coins than me and a critical completing letter appears, bid `[bid: opponent_coins + 1]` (capped by profitability) to guarantee winning it.
- On late auction rounds, never buy a letter unless it strictly increases the final word score by more than the bid amount ($2 \times \Delta V > \text{bid}$). Otherwise, bid `[bid: 0]`.

### Word Submission
- At the end of the auction, evaluate every candidate word in the lexicon against owned letters.
- Select the valid lexicon word that maximizes the total word letter value $2V$.
- Double-check candidate words against the actual provided lexicon text before submitting.
- If no valid word can be formed, submit `[word: none]`.