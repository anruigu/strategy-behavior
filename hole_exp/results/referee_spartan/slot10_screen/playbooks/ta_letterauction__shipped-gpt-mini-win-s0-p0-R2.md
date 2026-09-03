---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 0
round: 2
chars: 3182
---
When a letter is up, compute its word-score contribution = 2 * its letter value; never pay more than that unless acquiring it completes a higher-value word I can realistically assemble.

When a letter has value 1, my default is to bid 0 (not 0–1). I will bid 1 only if (a) I already hold complementary letters that make this letter necessary to complete a high-value lexicon word, or (b) blocking the opponent from completing a clearly reachable high-value word is worth the single-coin cost. I will not habitually bid 1 on every low-value letter.

When a letter has value >=2 (notably M=3), be willing to bid up toward 2*value (the letter’s full contribution to word score), but scale back if I lack other needed letters or if doing so would leave me unable to buy future necessary letters.

When I can form a high-value word with one additional letter, treat that letter as worth the marginal gain of the completed word (compute expected word score with that letter minus current best alternative) and bid up to that marginal value, even if it modestly exceeds 2*letter value.

When facing ties, prefer underbidding (let it be unsold) unless winning that specific letter is essential; ties are not a cheap way to win.

When deciding bids across multiple auctions, keep track of remaining coins as worth 1 each; compare the net gain from spending coins to buy letters (2x letter values in formed word) against simply keeping the coins. If the opponent spends aggressively on low-value letters early, that validates conserving coins—they may deplete themselves and leave mid/high-value letters available later.

When the auction shows the opponent buying many low-value letters, I should generally conserve further (as I did) because my coins retain steady value and the opponent’s budget constraint becomes an exploitable asset. Conversely, if the opponent conserves and many useful letters remain, I should be prepared to spend on the higher-impact letters (M or critical vowels/consonants) later.

When the opponent shows little interest in a low-value letter and I have no complementary letters, stop wasting coins on small bids; shift spending to letters that materially change my best reachable word. If several low-value letters are being taken by the opponent and that prevents me from forming any nontrivial word, accept keeping coins rather than making inefficient purchases.

Keep continuous bookkeeping: remaining coins, my current letters, opponent’s purchases and remaining coins inferred from their bidding pattern. Recompute my best achievable word after each auction and use that to set the maximum willingness-to-pay for upcoming letters (marginal gain logic).

When the auction ends, enumerate all lexicon words I can spell with my letters; compute final score for each = 2 * sum(letter values in word) + coins left (after paying for letters). Submit the word that maximizes that final score; if none improves on keeping coins, submit none.

Do not rewrite behavior based on a single passive run: revise conservatism to be the default for low-value letters, but be ready to spend on M (or other >=2 letters) and on marginal letters that complete high-value words.