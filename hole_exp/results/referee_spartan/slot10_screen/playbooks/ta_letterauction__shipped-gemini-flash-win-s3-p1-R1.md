---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1283
---
- Track opponent coin holdings exactly after every round by tallying their starting coins minus their winning bids.
- Target a specific 3-to-4 letter word from the lexicon early based on letters won or remaining, rather than bidding opportunistically on isolated high-value consonants without securing their matching vowels.
- When bidding on a critical letter needed to complete a valid word:
  - If the opponent has fewer coins remaining than my balance, bid exactly `opponent_coins + 1` (or my maximum available) to guarantee winning the letter.
  - Avoid matching common round bids (like 1, 2, or 3) when a tie causes both players to lose the letter and ruins word completion.
- Evaluate bid profitability before bidding: ensure total coins spent to assemble a target word do not exceed the net scoring gain (Word Score = 2 * sum of letter values; each unspent coin = 1 point).
- In the final letter round, check if winning the letter completes a valid word in the lexicon. If the letter cannot form any valid word with existing letters, bid 0 unless a cheap bid blocks the opponent from a high-scoring word.
- At the word submission phase, find the highest-scoring valid word in the lexicon constructible from my acquired letters; if no valid word exists, output `[word: none]`.