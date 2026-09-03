---
game: ta_letterauction__shipped
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 2010
---
- Track opponent coin holdings exactly after every round by tallying their starting coins minus their winning bids.
- Check the exact lexicon provided in the prompt before forming a plan. Do not assume standard English words (like ARE, EARS, TERMS) are valid if they are not listed in the prompt's lexicon.
- Target a specific word from the lexicon early based on letters won or remaining, rather than bidding opportunistically on letters that cannot combine into a valid lexicon word.
- Calculate the net point gain for completing or upgrading a word: Word Score = 2 * (sum of letter values). Since unspent coins are worth 1 point each, buying a letter of value $V$ for $C$ coins yields a net score change of $(2 \times V) - C$ if it adds to the final word.
  - Never bid more than $2 \times V$ on a letter unless that letter is the strictly necessary final piece that enables an entire word whose total value exceeds the cumulative coin spend.
  - For standard 1-value letters (A, E, R, S, T), bidding 2 coins breaks even at best; prefer bidding 1 coin or save coins unless securing the critical missing letter.
- When bidding on a critical letter needed to complete a valid word:
  - If the opponent has fewer coins remaining than my balance, bid exactly `opponent_coins + 1` (or my maximum available) only if the net score gain is strictly positive.
  - Avoid matching likely opponent bid thresholds when a tie causes both players to miss the letter.
- Once a target word is fully secured (e.g., REST), bid 0 on subsequent letters unless an available letter (like M) enables a higher-scoring lexicon word at a strictly profitable bid price.
- In the final letter round, check if winning the letter completes a valid word in the lexicon. If the letter cannot form or upgrade any valid word with existing letters, bid 0.
- At the word submission phase, find the highest-scoring valid word strictly present in the lexicon constructible from my acquired letters; if no valid word exists, output `[word: none]`.