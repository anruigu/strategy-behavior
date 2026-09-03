---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1927
---
### Letter Auction Playbook

- **Economic Valuation Rule**: A word scores $2 \times \text{sum of letter values}$, while unspent coins score 1 each. Thus, each letter point converts to at most 2 end points. Paying more coins than a letter's marginal contribution reduces overall net score unless it is the final required piece for a high-value word.
- **Target a Concrete Lexicon Word Early**: Scan the lexicon and track the letter sequence. Aim for realistic 3- or 4-letter words with high point density (e.g., `TEAM`, `STAR`, `ARM`, `MAT`) or single-letter words if available (`A`). Constantly recalculate which lexicon words remain feasible given current inventory and remaining auction items.
- **Break Tie Traps Aggressively**:
  - Ties result in letters remaining unsold, permanently destroying letters needed to form words.
  - Avoid repeatedly bidding the standard amounts (like 2) when the opponent is also bidding 2. If a letter is critical to making any word, bid 3 to guarantee winning it rather than risking an unsold tie. If a letter is not critical, bid 0 or 1 to preserve coins.
- **M-Letter Priority**: M has a letter value of 3 (worth 6 points in a word). It provides the highest score density; bid decisively (up to 4 if needed to break ties) if planning to build around words like `TEAM`, `MAT`, `ARM`, `MARE`, or `MEATS`.
- **Endgame Evaluation (Last 2–3 letters)**:
  - Check whether winning the upcoming letter(s) can form any valid lexicon word with owned letters.
  - If no valid lexicon word is mathematically reachable with the letters remaining, bid 0 on all remaining letters to preserve the 1:1 unspent coin payout.
  - Never spend coins on an isolated letter late in the game if it cannot combine with existing inventory into a word.
- **Word Submission**: Submit the valid lexicon word that yields the highest total score from owned letters. If no valid word can be formed, submit `[word: none]`.