---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 2304
---
When a letter up for auction is required to complete any high-scoring word I can plausibly assemble, I compute the word's gain as 2 * sum(letter values) and set my maximum bid equal to the marginal increase that letter provides to that word (pay up to that marginal value, but never more than my coins).

When a letter is a high-value tile (M=3) and it appears, I prioritize it and am willing to pay more than for 1-point letters because it multiplies the word score; set max bid for M to at least 4 if I need it for a candidate word.

When a vowel (A or E) would enable many candidate words I can actually finish, I bid enough to secure at least one vowel early (up to the marginal value for the best word it unlocks), rather than spreading tiny bids across many low-value consonants.

When the auction shows many remaining letters and I can still assemble a word without the current letter, I conserve coins and pass or bid low; do not spend early coins on low-impact letters.

When an opponent repeatedly ties my low bids and leaves letters unsold, stop matching trivial 1 bids; ties waste opportunities. Increase bids only when the letter meaningfully improves a feasible word, otherwise bid 0.

When I cannot form any lexicon word with the letters I currently own plus all remaining unauctioned letters, stop bidding and conserve coins to score them as leftover money instead of chasing useless letters.

When deciding a sealed bid amount, evaluate whether winning the letter would raise my final word score by at least as much as the coins I will pay (considering 2x letter values in words and 1x for leftover coins); prefer actions where expected score gain ≥ bid.

When my coins are low relative to remaining auctions, prioritize completing a small, guaranteed word (even a short one) over chasing longer words that require expensive tiles.

When the last letters are being auctioned and I already have most letters for a particular word, be willing to spend remaining coins up to the full extra 2×value that the final letter adds to secure completion.

Do not follow a blanket strategy of bidding 1 on every letter; that wasted coins and left me with no playable word. Instead, tie bids to concrete word plans and only invest when the letter meaningfully contributes to a reachable lexicon word.