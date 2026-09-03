---
game: ta_letterauction__shipped
model: haiku
condition: win
seed: 1
round: 1
chars: 2408
---
# Playbook for Letter Auction

**On bidding strategy:**

When a letter comes up for auction, I need to think backward from word-scoring, not forward from letter values alone. Before I bid on any letter, I should mentally construct which complete words I could spell and what letters those words require. A letter's value to me depends entirely on whether it's part of words I can realistically complete, not on its standalone point value.

When I'm bidding on early letters and have no letters yet, I should be aggressive on letters that appear in many high-value words (like common consonants that unlock multiple lexicon entries). I should not bid conservatively just because a letter has low point value—low point value is irrelevant if that letter is essential.

When I'm bidding on later letters and I already have some letters, I should increase my bid substantially if that letter completes or significantly advances a word I can actually spell. I should decrease my bid sharply if it doesn't fit into any word I can make.

**On managing my coin budget:**

I should not preserve coins "for later" as a general principle. Coins only score 1 point each at the end, while letters in complete words score 2x their combined value. I need to spend coins aggressively to acquire letters that form words, because unspent coins are a low-value consolation prize.

When I win a letter, I should immediately reassess: what words can I now spell, and what single letter would unlock the most valuable word? That tells me how hard to fight for the next letters.

**On letter selection and the endgame:**

I should never reach the word-submission phase holding random letters that don't form anything. If I end up with M and S and no path to a real word, I've already lost—that happened because I bid wrong earlier, not because I chose wrong at the end.

When I'm forced to submit a word with the letters I have, I'm in a failure state. The game is won or lost during the auction phase, not during word submission.

**On what went wrong:**

I bid on letters without a clear plan for which words I was building toward. I won M but then won S in a way that left me unable to acquire T, E, A, or R—the letters that would have let me spell anything valuable. I ended up with a 2-point word when I should have either bid differently to secure a complete word, or bid zero on letters that didn't fit into a coherent plan.