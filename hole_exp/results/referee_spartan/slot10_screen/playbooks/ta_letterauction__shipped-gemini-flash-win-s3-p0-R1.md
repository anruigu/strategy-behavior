---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1908
---
### Playbook

- **Word Target First**: At the start of the game, examine the lexicon and identify the highest-value achievable target words and their letter subsets. Never bid on isolated letters without a specific, viable word combination already mapped out.
- **Value-to-Cost Ceiling**: Remember that words score $2 \times \text{letter values}$, while unspent coins score 1 each. A letter worth 1 point contributes at most 2 points to the final word score; never spend more than 1 or 2 coins for a 1-point letter. Overbidding on low-value letters destroys net score even if a word is formed.
- **Avoid Overbidding in Panic**: If letters go unsold due to ties early on, do not ramp up bids to 4 or 5 coins just to secure letters. Spending 12 coins across 3 letters to form a 3-letter word (worth $\sim 6$ points) results in a net score of 6, which is worse than simply holding 12 coins and scoring 12 with `[word: none]`.
- **Tie-Breaking Strategy**:
  - Open with bids of 1 on early key consonants or high-value letters like M.
  - When anticipating opponent bids of 1 or 2, bid 2 on high-value letters (e.g., M=3), but avoid bidding $\ge 3$ on 1-point letters.
  - If the opponent continually bids high on common letters, let them burn their budget or let letters go unsold rather than outbidding beyond the letter's word value.
- **Word Construction Check Before Final Bids**:
  - Before bidding on letters 6, 7, and 8, check whether the letters currently held plus the remaining auction letter(s) can spell at least one word from the lexicon.
  - If no valid word can be formed even by winning the remaining auctions, bid 0 on all remaining letters to conserve unspent coins for a baseline score of 1 per coin.
- **Submitting Word**:
  - Submit the highest-scoring valid word formed strictly from owned letters.
  - If no valid lexicon word exists, submit `[word: none]` to preserve unspent coin points.