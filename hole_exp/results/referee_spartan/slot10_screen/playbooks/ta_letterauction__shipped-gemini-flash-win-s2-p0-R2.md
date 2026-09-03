---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 2466
---
# Playbook for Letter Auction

## Valuation and Scoring Math
- A word scores `2 * sum(letter_values)`. Each unspent coin scores `1`.
- Always verify potential words against the exact provided lexicon before bidding. Never assume common short words (like "AM" or "ME") are valid unless they explicitly appear in the lexicon list.
- A letter only yields value if it is actually part of a completed valid word. Winning an isolated high-value letter (like M) yields 0 points if no word can be formed from owned letters.
- Evaluate targets dynamically: `Final Score = Formed Word Score + Remaining Coins`. If no valid word can be formed, the score is simply remaining coins.
- The net marginal gain of completing word $W$ using remaining letter costs must be positive compared to keeping the coins: $2 \times \text{sum}(W) - \text{coins spent to complete } W > 0$.

## Lexicon & Target Tracking
- At every step, filter the lexicon to only words that can still be formed given (owned letters + remaining auction letters).
- Identify critical bottleneck letters needed to make any valid word from current inventory. If the remaining auction pool is running low and missing key vowels/consonants to complete any word with my current letters, pivot to bidding on standalone short words (e.g., A, AT, AS, SEA) or preserve remaining coins.

## Bidding Strategy
- Track opponent coin balance and past bid history to avoid tie-outs. Ties waste letters. If opponent repeatedly bids $k$, bid $k+1$ if the marginal value supports it, or drop to 0/1 to save budget.
- For critical completion letters (the last letter needed to unlock a word worth significantly more than the bid), bid aggressively enough to beat the opponent's likely bid, up to `Word Score - Coins Already Spent on Word Letters`.
- Do not bid on a letter in late rounds if winning it cannot complete any word in the lexicon with currently owned letters. Bid 0 in those rounds to preserve coins.
- When bidding early, secure multi-letter combinations with high lexicon overlap (e.g., A, E, T, S) rather than stranding an isolated consonant.

## Word Submission
- When the auction concludes, scan the lexicon from highest score to lowest score among words that can be spelled exclusively using the letters I won (respecting letter counts).
- If at least one valid word can be formed, submit `[word: <text>]` for the highest-scoring valid word.
- If no valid word from the lexicon can be formed, submit `[word: none]`.