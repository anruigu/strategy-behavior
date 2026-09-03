---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 2047
---
### Letter Auction Playbook

- **Economic Valuation Rule**: A word scores $2 \times \text{sum of letter values}$, while unspent coins score 1 each. Therefore, never pay more coins for a letter than its marginal word value (at most $2 \times \text{letter value}$) unless it uniquely completes a high-value word that nets positive total score over keeping coins.
- **Target a Concrete Lexicon Word Early**: Before bidding, scan the lexicon and pick 1–2 target words based on the letters available in the auction schedule (e.g., aiming for 3-letter or 4-letter high-efficiency words like `TEAM`, `STAR`, `ARM`, or `MAT`). Track which remaining letters are strictly necessary.
- **Avoid Overbidding on 1-Value Letters**: 
  - Never bid $\ge 3$ on letters with letter value 1 (like E, A, T, R, S) unless it guarantees completing a word that yields higher net points than the coins spent.
  - On early letters, bid low (1 or 2). If tied, do not panic-escalate bids late in the auction.
- **Handling Ties and Unsold Letters**:
  - Unsold letters on ties burn auction opportunities. When an opponent shows a pattern of bidding standard amounts (e.g., 2 or 3), shade bids slightly (e.g., bid 0 to let them spend or bid 1 over standard thresholds) rather than matching their exact expected bid.
- **M-Letter Priority**: M has a letter value of 3 (contributing 6 to word score). Prioritize competing for M at bids of 2–3, as it provides the highest score density per letter.
- **Endgame Evaluation (Last 2–3 letters)**:
  - If holding zero or insufficient letters to complete any lexicon word, calculate if winning the remaining letters can actually form a valid word. If no valid word is mathematically reachable, bid 0 on all remaining letters to preserve the 1:1 unspent coin payout.
  - Never bid remaining coins on a letter if the resulting inventory still leaves zero valid words in the lexicon.
- **Word Submission**: Always submit the valid lexicon word that maximizes letter score. If no word can be formed from owned letters, submit `[word: none]`.