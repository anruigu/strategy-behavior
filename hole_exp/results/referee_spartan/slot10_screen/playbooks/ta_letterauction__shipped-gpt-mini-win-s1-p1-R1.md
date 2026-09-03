---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 2528
---
When a letter up for auction has value V (in word scoring), treat its marginal worth as 2*V (because words score 2x letter totals) and never bid more than 2*V unless collecting it enables a higher-value word that I can confirm I can complete.

When opponents consistently pay X for low-value letters, assume they value completing words and only overbid them on a letter if it is necessary to complete a high-scoring word for me or if its 2*V payoff exceeds X.

When a high-value letter (highest V available in the current lexicon) appears, be willing to outbid typical small bids up to 2*V or slightly above if that letter enables a heavily-weighted target word; conserve coins only if no plausible word requires that letter.

When I already hold some letters, evaluate candidate words I can form if I win the current letter. If winning the letter allows me to form a valid lexicon word W, compute net gain = 2*(sum of letters of W) + (remaining coins after bidding) versus not winning and keeping coins. Prefer bids that make net gain positive and maximize final score.

When a letter is low value (V small) and I can likely obtain similar letters later or the auction has shown many go unsold, default to low bids (0–1) to conserve coins for more valuable letters.

When the opponent’s last bids show a pattern (e.g., always paying 2 for 1-value letters), use that to set my threshold: only contest those letters if they are critical to my planned word or if the letter’s 2*V payoff justifies the expected battle.

Never bid more coins than I have left. If a tie will cause the letter to go unsold and that outcome is acceptable (it hurts opponent equally or helps me), prefer a tie by matching their last expected bid rather than overpaying.

During the auction, keep an internal shortlist of target words I could plausibly make given letters seen and likely remaining letters; prioritize collecting letters that appear in multiple high-value candidates on that shortlist.

If I reach the final word stage with letters that can form at least one lexicon word, compute word score = 2*(sum of used letters) + remaining coins. Choose the word that maximizes that expression; prefer using more letters when the doubled letter value exceeds the value of holding coins.

If I cannot form any lexicon word with my letters, submit [word: none] rather than forcing an invalid word.

When unsure whether to spend on a current letter, err toward conserving coins unless that letter decisively enables a high-scoring word I can complete.