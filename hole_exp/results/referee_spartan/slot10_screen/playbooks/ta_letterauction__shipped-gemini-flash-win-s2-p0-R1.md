---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1927
---
# Playbook for Letter Auction

## Valuation and Scoring Math
- A word scores `2 * sum(letter_values)`. Each unspent coin scores `1`.
- Buying a 1-value letter yields a net profit only if its incremental contribution to the formed word exceeds the coin cost paid. Spending 4 coins to win a 1-value letter (which adds 2 points to the final word) is a net loss of 2 points compared to holding the coins.
- When evaluating a target word, compute `Target Word Points + Expected Remaining Coins`. Never bid more for a letter than the net marginal score improvement it enables.
- Always retain a fallback viable word path early (even short words like 2-letter or 3-letter words) so I never finish with zero valid words.

## Bidding Strategy
- When bidding on common 1-value letters in early rounds, bid low (1 or 0) unless it directly completes a high-value word. Do not default to bidding 2, 3, or 4 on 1-value letters early.
- When tied bids result in unsold letters, adjust bid off common round numbers (e.g., bid 1 instead of 2, or 3 instead of 2) rather than matching the opponent's repeated bid.
- When tracking remaining letters, constantly verify which words in the lexicon are still mathematically possible given the letters already sold or burned.
- Never spend coins on a letter if the remaining letters in the auction cannot complete a word that beats simply keeping all remaining coins.
- On the final letter (Letter 8), never bid all remaining coins unless winning that specific letter enables a word whose score strictly exceeds the total coins spent. If winning the letter does not complete a word, bid 0 to keep all remaining coins.

## Word Submission
- When the auction concludes, scan the lexicon from highest score to lowest score among words fully formed by owned letters.
- If at least one valid word can be formed, submit the highest-scoring valid word.
- If no valid word can be formed, submit `[word: none]`.