---
game: ta_letterauction__shipped
model: haiku
condition: win
seed: 1
round: 2
chars: 3727
---
# Playbook for Letter Auction

**On bidding strategy:**

When a letter comes up for auction, I need to think backward from word-scoring, not forward from letter values alone. Before I bid on any letter, I should mentally construct which complete words I could spell and what letters those words require. A letter's value to me depends entirely on whether it's part of words I can realistically complete, not on its standalone point value.

When I'm bidding on early letters and have no letters yet, I should be aggressive on letters that appear in many high-value words (like common consonants that unlock multiple lexicon entries). I should not bid conservatively just because a letter has low point value—low point value is irrelevant if that letter is essential.

When I'm bidding on later letters and I already have some letters, I should increase my bid substantially if that letter completes or significantly advances a word I can actually spell. I should decrease my bid sharply if it doesn't fit into any word I can make.

**On managing my coin budget:**

I should not preserve coins "for later" as a general principle. Coins only score 1 point each at the end, while letters in complete words score 2x their combined value. I need to spend coins aggressively to acquire letters that form words, because unspent coins are a low-value consolation prize.

However, I must avoid spending all my coins early on common letters that appear in many words. If I exhaust my budget before the auction ends, I cannot compete for the high-value letters (like M, R) that actually complete words. I need to reserve coins for the letters that will let me finish a word.

When I win a letter, I should immediately reassess: what words can I now spell, and what single letter would unlock the most valuable word? That tells me how hard to fight for the next letters.

**On letter selection and the endgame:**

I should never reach the word-submission phase holding random letters that don't form anything. If I end up with letters that have no path to a real word, I've already lost—that happened because I bid wrong earlier, not because I chose wrong at the end.

When I'm forced to submit a word with the letters I have, I'm in a failure state. The game is won or lost during the auction phase, not during word submission.

**On what went wrong in this episode:**

I bid aggressively on E and S early, spending 7 and 5 coins respectively, even though E appears in nearly every word and S is common but not unique. By letter 4 (M), I had only 5 coins left and could not bid high enough to secure M. I then won another E instead, leaving me with two E's and one T—a collection that spells nothing in the lexicon.

The critical error: I did not identify which complete words I could realistically win letters for, and I spent too much on early common letters. I should have noticed that M is rare and high-value (worth 3), appearing only in MASTER, STREAM, SMART, STEAM, TAMER, MATES, MEATS, TEAM, and TAME. Winning M would have been far more valuable than winning a second E.

Next time, I will:
- Identify the complete words in the lexicon that score highest: MASTER (M+A+S+T+E+R = 3+1+1+1+1+1 = 8, scoring 16), STREAM (S+T+R+E+A+M = 1+1+1+1+1+3 = 8, scoring 16), SMART (S+M+A+R+T = 1+3+1+1+1 = 7, scoring 14), STEAM (S+T+E+A+M = 1+1+1+1+3 = 7, scoring 14).
- Notice that M is the rarest high-value letter and bid hard for it.
- Reserve coins to ensure I can bid on M and the other rare letters (R, A, T) that complete high-value words.
- Bid low (0 or 1) on common letters like E and S unless I'm certain they unlock a word I can complete.
- Plan to spell one of the 6+ point words, not hope I can piece something together at the end.