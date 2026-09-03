---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1709
---
### Valuation and Bidding Playbook

- **Understand Word Value vs. Coin Trade-off**: A word scores $2 \times \sum(\text{letter values})$, while unspent coins score 1 each. Spending more coins to acquire a letter than the net increase in word score reduces the total score. Never spend 8 coins on a letter if the resulting word cannot produce more than 8 points.
- **Formulate a Target Word Early**: At the start of the game, identify 2–3 viable high-value target words (and shorter fallback words) from the lexicon based on the available letter sequence. Track exactly which components are needed.
- **Avoid Overbidding on Non-Key Letters**:
  - For standard 1-value letters early on, bid 1 or 2 at most.
  - Do not escalate into high bidding wars (bids of 4+) for 1-point letters unless it completes a high-value word that nets positive score over the spent coins.
- **Anticipate and Break Ties Economically**:
  - When seeing repeated ties at round numbers (e.g., 2 or 3), do not jump significantly higher (e.g., jumping from 2 straight to 4). Adjust incrementally or drop to 0 to preserve budget if the opponent is overpaying.
- **Late-Game Coin Retention**:
  - When reaching the final rounds without sufficient letters to form a word in the lexicon, do not dump all remaining coins into the last letter. If winning that letter will still leave no valid word, bid 0 to preserve all unspent coins as raw score.
  - Only bid remaining coins aggressively on the final letter if winning it guarantees a valid word whose $2 \times \text{value}$ exceeds the bid cost.
- **Word Submission**:
  - Always verify that the letters acquired spell a valid lexicon entry. If no word can be formed, submit `[word: none]`.