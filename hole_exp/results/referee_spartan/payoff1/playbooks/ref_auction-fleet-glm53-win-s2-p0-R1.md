---
game: ref_auction
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 1615
---
My playbook:

- Before every bid I write, I recompute my budget from scratch: budget minus any amounts I've actually committed or paid so far this episode. I do not trust my previous line's budget figure, because I've caught myself copying stale or nonsense numbers. The bracketed budget token must always be consistent with the bid I'm making and my true remaining funds.

- Round 1 of a lot: I open at or just above the minimum raise. Small bids keep the auction cheap and cost nothing if I get outbid. Never open with a large jump — the standing bid rarely reflects a rival's true ceiling anyway.

- Round 2 of a lot: I raise only if the required bid is meaningfully below my private value, and I bid the minimum raise over the standing bid, not a comfortable round number. Overshooting the minimum just donates money when I win.

- I set a hard personal ceiling for each lot at roughly 70–80% of my private value before round 2 starts. If the standing bid already exceeds that, I pass immediately and don't chase. Getting drawn into a bidding contest on a lot I only marginally value is my main leak.

- If I've already won a lot earlier in the episode, I treat my remaining budget as a hard constraint on raises, not a suggestion — I check that a round-2 raise still leaves me able to act on later lots I might value highly.

- When a rival repeatedly wins lots at moderate prices, I don't change my bids to "beat them"; I stick to value discipline. They overpaying on their wins is good for me.

- I always reply with both tokens, bid and budget, in the exact required format, ending with the bracketed token.