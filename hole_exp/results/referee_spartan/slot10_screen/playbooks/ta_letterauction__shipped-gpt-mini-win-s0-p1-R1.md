---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 2173
---
When a letter with value 3 (M) appears, I prioritize winning it: I set a nonzero bid rather than 0, up to the expected marginal gain toward the best available word containing M.

When a letter with value 1 appears early, I bid small but nonzero if I have no letters yet, to avoid finishing with nothing; default small bid = 1 unless I plan to outspend to secure a specific high-value letter later.

When I already hold key high-value letters needed for a long word, I am willing to spend more on inexpensive supporting letters (1-value) to complete that word rather than hoard coins.

When ties would block a letter I need, I increase my bid by 1 over my estimate of the opponent’s minimal bid; never assume a tie will pass the letter to me.

When deciding a bid, I calculate the incremental expected score: estimate the best word I could form if I win this letter, double its letter-value sum, subtract current planned spending; if that incremental word-score gain per coin spent is less than 1 (the coin’s value if unspent), I bid conservatively or 0.

When several letters remain that could form multiple words, I aim to secure a core letter combination (usually M + two or three 1-value letters) rather than scatter bids across many singletons.

When I have no letters late in the auction, I stop bidding 0 on cheap letters—take at least one cheap letter to allow forming at least a short word and convert coins into doubled letter value.

When my remaining coins are high and the auction is nearly over, I shift toward aggressive bids to convert coins into a high-scoring word; spending several coins to create a word that doubles letter totals is often worth more than leaving many coins unspent.

When the opponent consistently overbids on a specific letter, I avoid wasting coins to contest it unless that letter is essential to my best possible word.

When presented with the final decision to submit a word, I pick the highest-scoring valid word I can spell with my letters; if I have no valid word, I submit none and accept coin value.

When an offered letter is clearly redundant with letters I already have and does not improve any top candidate word, I bid 0.