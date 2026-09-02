---
game: ta_letterauction
model: qwen
condition: neutral
seed: 0
round: 3
chars: 5873
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

**New lessons from this round of play**

- I must verify that a word is actually in the lexicon before counting it toward my marginal-value calculations. In episode 1 I bid as if SET were in the lexicon (it is not), which led me to overpay for S and A while holding T, E. Always re-check the lexicon list before computing marginal value.
- The "zero marginal value" rule is too rigid when I have no letters at all. In episode 3, I had only T and bid 0 on every remaining letter (E, A, R, T, M), ending with 9 coins but no word. The problem: with a single letter, almost every other letter has *potential* marginal value if combined with a future letter. The fix: when I have one or two letters and more than three rounds remain, I should bid 1–2 on letters that form a valid two-letter word with what I hold (e.g., A with T → AT, worth 2). This is not "zero marginal value" — it is a real, small word. I was incorrectly treating "doesn't complete my *best* word" as the same as "marginal value is zero."
- Foundation bidding at 3 is too low when the opponent is also bidding 3. Ties waste rounds. If I see the opponent bid 3 and the letter is unsold, I should bid 4 on the next occurrence of that letter, not 3 again on a different letter. In episode 4, I bid 3 on A, 3 on R (both tied at 3/3), then 3 on S (lost to P1 at 4). I should have raised to 4 on R or S immediately.
- When I hold E, E and S comes up, the marginal value of S is the value of SEE (3) minus 0 = 3. I bid 2 and won, which was correct. But I then bid 1 on T thinking it gave me TEST (4) — TEST is not in the lexicon. The correct marginal value of T with E, E, S is zero (no lexicon word uses T, E, E, S). I should have bid 0.
- When the opponent wins a high-value letter (like M for 4), I should note what words they might be building and consider blocking on subsequent letters they need. In episode 2, P1 got M for 4 and I had S, E — if A or T had come up, I should have considered whether P1 needed it for SMART or STEAM and bid to deny.
- Bidding 0 on a letter that *does* form a valid word with my hand (even a short one) is a mistake when I have no other path to a word. In episode 3, A + T = AT (score 2). I bid 0 on A because "no 2-letter word TA exists," but AT *does* exist in the lexicon. I must check both orderings of two-letter combinations.