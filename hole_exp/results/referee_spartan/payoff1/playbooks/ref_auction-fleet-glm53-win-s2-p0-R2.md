---
game: ref_auction
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2152
---
My playbook:

- Before every bid I write, I recompute my budget from scratch: starting budget minus amounts actually paid for lots already won, minus nothing else (bids that were outbid cost me nothing). I do not trust my previous line's budget figure — this episode my bracketed budgets drifted badly (28, 92, 100, 76, 36 for no consistent reason). The budget token must be arithmetically true, even though the scoring only tracks my bids and wins.

- Round 1 of a lot: I open at exactly the minimum raise. Small bids keep the auction cheap and cost nothing if I get outbid. Never open with a large jump.

- Round 2 of a lot: I bid exactly standing bid plus the minimum raise, no more. Twice this episode I rounded up (bid 8 over a standing 6 with a minimum raise of 2; bid 20 over 16 with a minimum of 4) and donated extra money on lots I won. If the required bid exceeds my ceiling, I pass.

- I set a hard personal ceiling for each lot at roughly 70–80% of my private value before round 2 starts. If standing bid plus minimum raise exceeds that ceiling, I pass immediately. Lot 3 this episode: standing 16, value 43, raising to 20 was right; I should also be ready to fold one round earlier if the standing bid jumps a lot between rounds, since rivals' round-2 jumps signal real interest.

- A lot worth less than its estimate to me (e.g. value 19 vs estimate 24) is still worth bidding on cheaply in round 1, but my ceiling drops to my private value, not the estimate. I won nothing on such a lot and that was fine — losing it at 12 to a rival was a good outcome.

- On the final lot of the episode I can relax budget reservation entirely and bid up to my full value if needed, since there are no future lots. This worked: winning the last lot at 20 against a value of 56 was the biggest profit of the episode.

- If a rival repeatedly wins lots at moderate prices, I don't change my bids to beat them; I stick to value discipline. Letting bidder 2 take lots 1 and 4 at 12 each while I won lots 2 and 5 cheaply produced a +57 score.

- I always reply with both tokens, bid and budget, in the exact required format, ending with the bracketed token.