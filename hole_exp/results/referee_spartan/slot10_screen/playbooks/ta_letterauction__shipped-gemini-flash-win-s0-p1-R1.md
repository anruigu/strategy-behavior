---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1355
---
- Calculate the maximum marginal value of winning each letter before bidding. A letter only provides score through enabling a word: word score is $2 \times \sum \text{letter\_values}$, while unspent coins score $1$ each. Spending more coins on a letter than its marginal contribution to word score over unspent coins is net negative.
- Do not escalate bids predictably in symmetric tie situations. When both players have identical coin stacks and repeatedly mirror each other's incremental escalations, either bid 0 to let the opponent overpay, or place an unexpected lower bid to save coins for later uncontested letters.
- Never dump all remaining coins on a single letter (e.g., bidding all 12 coins) just because it is the last letter, unless the marginal word score strictly exceeds the coins spent. If bidding 12 yields a 1-letter word worth 2 points, bidding 0 yields 12 points in saved coins.
- When an opponent overbids and depletes their coin stack on an earlier letter, check if they can contest remaining letters. Bid the minimum amount strictly greater than their remaining balance (or 1 if they have 0) to secure future letters cheaply.
- At word submission, check all valid words in the lexicon that can be formed from acquired letters and submit the one with the highest total letter value; if no word can be formed, submit `[word: none]`.