---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1769
---
### Valuation and Target Strategy
- Calculate word values immediately: each letter in a formed word contributes $2 \times \text{value}$, whereas keeping the coin contributes $1$.
- A target word of letter sum $V$ yields $2V$ points. Buying all its letters for a combined cost of $C$ yields a net score of $12 - C + 2V$. To beat holding all coins (score 12), the total spend $C$ must be strictly less than $2V$.
- Identify the most cost-effective 3-letter and 4-letter words early (e.g., words containing high-value letters like M=3, where a word like ARM, MAT, or TEAM gives high point yields relative to letter count).
- Lock in a primary target word and a backup target before the first auction starts.

### Bidding Strategy
- Avoid standard focal bids (1, 2, 3) that frequently result in ties where the letter goes unsold. If I want a letter, bid 1 coin above the expected focal point (e.g., bid 2 instead of 1, 3 instead of 2, 4 instead of 3).
- Do not bid on letters that do not fit into my target word or active backup words; bid `[bid: 0]` on useless letters to preserve capital and let the opponent waste coins.
- Track opponent coin balance at every step. If opponent has fewer coins than me and a letter completes my target word, bid `[bid: opponent_coins + 1]` to guarantee winning it.
- Never spend coins on duplicate or auxiliary letters on the final auction round if they cannot form a higher-scoring word. If a letter does not enable a word with value $2 \times \text{new\_letters} > \text{bid}$, bid `[bid: 0]` and retain the coins.

### Word Submission
- At the end of the auction, check all lexicon words against owned letters and select the valid word with the highest total letter value $2V$.
- If no valid word can be formed, submit `[word: none]`.