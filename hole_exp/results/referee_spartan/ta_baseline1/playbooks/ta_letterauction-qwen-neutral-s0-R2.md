---
game: ta_letterauction
model: qwen
condition: neutral
seed: 0
round: 2
chars: 3545
---
**Playbook**

**Bidding**

- When a letter is up for auction, I bid the marginal value it adds to my best achievable word given my current letters, not its face value. A letter that completes a 5-letter word worth 10 is worth up to 10 minus my current best word score, not 1.
- When I have no letters yet, I treat the first letter I acquire as a foundation and bid 3–4 for it. It unlocks all future combinations.
- When a letter went unsold at bid X in a prior round, I bid X+1 on the same letter in a later round to pick it up at the minimum winning price.
- I never bid 0 on a letter that completes a word I can already form with my other letters, even if that word is short.
- I never bid more than the total value of the best word I can form with that letter plus my current letters, minus the best word I can form without it.
- I do not bid on a letter whose marginal value to me is zero, even if it is cheap. Saving coins for a letter that actually raises my word score is always better.
- When I already own a letter and a duplicate is offered, I evaluate the marginal value of the second copy specifically (e.g., do I need two A's for a word in the lexicon?). If the answer is no, I bid 0 or 1, not a foundation price.

**Word selection**

- When submitting my final word, I enumerate every word in the lexicon that I can spell with my letters, pick the one with the highest total letter value, and submit that one. I do not stop at the first word I think of.
- A longer word is almost always better: a 5-letter word of all 1-value letters (score 10) beats a 3-letter word with M (score 8). I check all options before committing.
- If no word in the lexicon can be spelled from my letters, I submit [word: none] and let my unspent coins carry the score.

**Capital management**

- Unspent coins are worth 1 each. A letter is worth its marginal contribution to my word score. I buy a letter whenever its marginal word-value exceeds its expected price.
- I do not hoard coins at the expense of letters that would raise my word score by more than the coins spent. Conversely, I do not spend coins on letters that raise my word score by less than the price.
- In the final one or two rounds, I evaluate each letter against my *actual* remaining letters, not against hypothetical letters I might still acquire. If a letter doesn't complete a word with what I already hold, its marginal value is zero and I should not pay for it.

**What did not work**

- Bidding foundation prices (3–5) on every letter while holding no letters led to a cascade of ties and unsold rounds. In two of four episodes I went through six or more letters without acquiring a single one. The fix: when a letter goes unsold at my bid, I should immediately raise to bid+1 on the next occurrence of that same letter rather than waiting and re-bidding the same amount on a different letter.
- Bidding on letters with zero marginal value to my current hand (e.g., T with only E in hand, or R with only A in hand) wasted coins that could have gone toward letters that actually complete words.
- In the final round, I sometimes bid on a letter because it "might pair with something I'll get later," but there is no later. The final letter must complete a word with my existing letters or it is worthless to me.
- Not blocking the opponent's high-value words: in episode 4, P1 acquired M (worth 3) and likely built a strong word. When the opponent is close to a high-scoring word and a letter they need is up, I should bid to deny them even if the letter has low value to me.