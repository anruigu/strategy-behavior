---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1638
---
- Target specific target words from the lexicon early and track the exact letters needed to complete them. Do not buy disjoint letters that cannot form any valid lexicon word together.
- A letter only provides score through enabling a word: word score is $2 \times \sum \text{letter\_values}$, while unspent coins score $1$ each. Buying a letter that does not complete or advance towards a high-value word is a pure loss of coins.
- Avoid bidding on letters that leave me with combinations not present in the lexicon (e.g., E, T, R alone make no word). If missing core vowels or connectors (like A or S) for key targets, prioritize acquiring them or pivot immediately to viable fallback words.
- Do not escalate bids predictably in symmetric tie situations. When both players have identical coin stacks and repeatedly mirror each other's incremental escalations, either bid 0 to let the opponent overpay, or place an unexpected lower bid to save coins for later uncontested letters.
- Never dump all remaining coins on a single letter unless the marginal word score strictly exceeds the coins spent. If bidding heavily yields no viable word or a low-value word, saving coins yields 1 point per coin.
- When an opponent overbids and depletes their coin stack on earlier letters, check their remaining balance. Bid the minimum amount strictly greater than their remaining balance (or 1 if they have 0) to secure needed letters cheaply.
- At word submission, check all valid words in the lexicon that can be formed from acquired letters and submit the one with the highest total letter value; if no word can be formed, submit `[word: none]`.