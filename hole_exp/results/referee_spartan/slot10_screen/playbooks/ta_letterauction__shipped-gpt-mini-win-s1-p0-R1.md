---
game: ta_letterauction__shipped
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 2274
---
When a high-value letter (value ≥3) is up, bid up to twice its letter value in coins (i.e. up to the word-scoring contribution) to secure it—I treat that as the baseline maximum I'm willing to pay for that single letter.

When a letter directly completes or substantially advances a realistic high-scoring lexicon word I can form, raise the bid ceiling to the lesser of my remaining coins and the 2×total letter-value of the target word minus the value of letters I already hold.

When multiple letters remain and I can plausibly assemble a 4+ letter word, prioritize buying the scarce/high-value letters for that word even if it means spending several coins early; securing a core high-value letter is better than hoarding coins and ending with unusable singletons.

When only low-value letters (value=1) are being auctioned and they are not necessary for any target word I can reasonably complete, bid 0 or 1—do not let low-value auctions bleed my bankroll unless they are required building blocks.

When a tie would leave the letter unsold and I have no immediate use for it, prefer to tie (by bidding the same as likely opponent) only if doing so prevents the opponent from completing a known high-scoring word; otherwise let ties go unsold to preserve coins.

When I already hold some letters, explicitly enumerate candidate lexicon words I can reach with one or two more letters; only bid aggressively on letters that move me into that reachable set.

When the opponent has already purchased several complementary letters for a particular high-value word, deprioritize competing for those letters unless winning them blocks the opponent and I can still form an alternate strong word.

When I win a letter, immediately recompute remaining target words and remaining willingness-to-pay for future letters so I don’t default to a fixed tiny-bid strategy that leaves me unable to form anything.

When only trivial words remain feasible from my holdings (single letters), stop bidding aggressively; instead conserve coins and accept a small word or none if coin value will exceed possible word gain.

Do not adopt a blanket “always bid 1” policy—this frequently results in ending with low-value singletons. Adjust bids to letter value and to the concrete words I can build.