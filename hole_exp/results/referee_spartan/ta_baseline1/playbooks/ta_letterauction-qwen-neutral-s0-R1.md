---
game: ta_letterauction
model: qwen
condition: neutral
seed: 0
round: 1
chars: 2217
---
**Playbook**

**Bidding**

- When a letter is up for auction, I bid the marginal value it adds to my best achievable word, not its face value. A letter that completes a 5-letter word worth 10 is worth up to 10 minus my current best word score, not 1.
- When I have no letters yet, I treat the first letter I acquire as a foundation and bid up to 3-4 for it, since it unlocks all future combinations.
- When the opponent's letters are visible (from prior wins) and they are close to completing a high-value word, I bid enough to deny them that word, even if the letter's face value is low.
- When a letter went unsold at bid X in a prior round, I bid X+1 on the same letter in a later round to pick it up at the minimum winning price.
- I never bid 0 on a letter that completes a word I can already form with my other letters, even if that word is short.
- I never bid more than the total value of the best word I can form with that letter plus my current letters, minus the best word I can form without it.

**Word selection**

- When submitting my final word, I enumerate every word in the lexicon that I can spell with my letters, pick the one with the highest total letter value, and submit that one. I do not stop at the first word I think of.
- A longer word is almost always better: a 5-letter word of all 1-value letters (score 10) beats a 3-letter word with M (score 8). I check all options before committing.

**Capital management**

- I spend coins to acquire letters that complete words. I do not hoard coins at the expense of letters that would raise my word score by more than the coins spent.
- Unspent coins are worth 1 each; a letter is worth its contribution to my word score. I buy a letter whenever its marginal word-value exceeds its price.

**What did not work**

- Bidding 1 on everything because "it's only worth 1" left me with zero or one letter in three of four episodes. The face value of a letter is irrelevant; its value is the word it enables.
- Submitting a short word when a longer word was available from the same letters cost me 4-6 points in a single decision.
- Letting the opponent accumulate letters without attempting to block their best word gave them a free high-scoring word.