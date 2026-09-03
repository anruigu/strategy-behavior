---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 1900
---
When a letter is up, compute its word-score contribution = 2 * its letter value; never pay more than that unless acquiring it completes a higher-value word I can realistically assemble.

When a letter has value 1, bid 0–1 by default to conserve coins; only raise the bid if I already hold complementary letters that make this letter necessary to complete a high-value word.

When a letter has value >=2, be willing to bid up toward 2*value (the letter’s full contribution to word score), but scale back if I lack other needed letters or if doing so would leave me unable to buy future necessary letters.

When I can form a high-value word with one additional letter, treat that letter as worth the marginal gain of the completed word (compute expected word score minus current best alternative) and bid up to that marginal value, even if it exceeds 2*letter value by a small amount.

When facing ties, prefer underbidding (tie leaves letter unsold) unless winning that specific letter is essential; ties are not a cheap way to win.

When deciding bids across multiple auctions, keep track of remaining coins as worth 1 each; compare the net gain from spending coins to buy letters (2x letter values in formed word) against simply keeping the coins.

When the opponent has shown little interest in low-value letters, stop wasting coins on small bids for marginal letters; shift spending to letters that materially change my best reachable word.

When the auction ends, enumerate all lexicon words I can spell with my letters; compute final score for each = 2 * sum(letter values in word) + coins left (after paying for letters). Submit the word that maximizes that final score; if none improves on keeping coins (unlikely but possible), submit none.

Do not habitually bid 1 on every low-value letter; that pattern wastes coins and can leave me unable to secure the few high-value letters that matter.