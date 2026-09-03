---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 2056
---
### Playbook

- **Word Target First**: At the start of the game, examine the lexicon and identify target words and their required letter sets. Never bid casually on isolated letters without a specific, viable word path mapped out.
- **Value-to-Cost Ceiling**:
  - Words score $2 \times \text{sum of letter values}$; unspent coins score 1 each.
  - A letter worth 1 point contributes exactly 2 points to word score; paying 2 coins yields net 0 gain, and paying $\ge 3$ coins is strictly negative value.
  - A letter worth 3 points (e.g., M) contributes 6 points to word score; paying up to 2–3 coins yields positive net value.
  - Never bid more than 1 coin on a 1-point letter unless it completes a high-value word that cannot be formed otherwise.
- **Opponent Tracking & Bidding Strategy**:
  - Track the opponent's remaining coins and acquired letters. If an opponent bids 2 consistently on early 1-point letters, let them deplete their coin reserve.
  - Avoid bidding on letters that don't fit into any remaining reachable words once letters start going unsold or to the opponent.
  - On high-value letters (e.g., M=3), bid 2 or 3 to win them when the opponent has spent down coins.
- **Mid-to-Late Game Path Verification**:
  - Before bidding on each letter from letter 5 onward, check if there is at least one valid lexicon word constructible from current letters plus the remaining auction letters.
  - If winning a specific letter cannot lead to any valid lexicon word, bid 0.
  - Do not bid on an isolated high-value letter (like M) near the end if remaining letters cannot complete a word with it.
- **Conserving Coins when Cut Off**:
  - If no complete word can be formed from available letters, bid 0 on all remaining auctions to preserve 1 point per coin.
  - A default score of 10–12 coins with `[word: none]` is far better than spending coins on useless partial letter collections.
- **Submitting Word**:
  - Submit the highest-scoring valid word formed strictly from owned letters.
  - If no valid lexicon word exists, submit `[word: none]`.