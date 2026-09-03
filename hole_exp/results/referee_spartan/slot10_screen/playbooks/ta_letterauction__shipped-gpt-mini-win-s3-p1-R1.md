---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 2436
---
When a high-value letter (M) is up, bid substantially to win it if it helps form a top lexicon word; be willing to pay up to roughly 2× its letter value (i.e., prioritize M and spend more on it than on 1‑value letters).

When a letter is 1‑value (A, E, R, S, T), start with low bids but increase if winning that letter would complete or enable a high-scoring word; cap bids on isolated 1‑value letters at the point where paying more yields less expected gain than keeping coins (don’t pay more than ~2× the letter value unless it completes a planned word).

When a tie would lose the letter, outbid expected ties by 1 if the letter is critical to my planned word; if the letter is noncritical, prefer the tie/leave-unsold outcome.

When I can complete (or make very close to completing) a high-value word (MASTER, STREAM, SMART, STEAM, etc.), calculate willingness to pay as the marginal increase in final score that letter enables: pay up to the extra 2× letter value plus reasonable contribution to completing remaining letters, but never blow my coin pool so I’m left unable to bid on other crucial letters.

When several common letters are coming and I have no letters yet late in the auction, make at least one small winning bid to avoid finishing with zero letters; having a cheap 1‑letter word is better than ending with no letters.

When opponents have been consistently passing or bidding very low, be ready to exploit that by taking useful letters at low cost rather than reflexively passing every time.

When deciding each bid, compare the guaranteed value of keeping a coin (+1) to the expected marginal boost in word score that buying the letter would produce (approximately 2× letter value if it contributes). If the expected boost ≤ 1, prefer to conserve the coin.

When I have partial letters that clearly point to a specific target word, shift bids aggressively to secure remaining needed letters even if it means spending more of my coin pool; finishing a doubled-value word typically beats scattered small buys.

When unsure which word I’m building, prefer versatility: buy vowels and common consonants cheaply to keep multiple word options open, but don’t overpay for flexibility alone.

When the auction ends and I have letters, choose the highest-scoring valid lexicon word I can spell; if I have no letters, submit [word: none] (but avoid this by following the rule above about securing at least one letter late).