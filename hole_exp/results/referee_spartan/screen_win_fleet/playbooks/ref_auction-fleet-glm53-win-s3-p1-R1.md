---
game: ref_auction
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 1418
---
- When a lot's value to me is below the estimate, I pass early instead of opening a token bid — chasing it anyway burned attention and money for nothing.
- I bid only when the required bid is comfortably below my value, and I cap myself at value minus a margin; never bid at or above my value to "stay competitive."
- I track my actual remaining budget every turn: budget starts at 30, and I subtract each winning payment only. My budget reports this time were incoherent (30, then 2, then 34, then 21, then 38) — that is a hard error to repeat. Before each reply, recompute: starting 30, minus sums I paid for lots already won.
- When opening bidding on a lot I like, I open at the minimum raise, not higher — the opponent usually counters anyway, and my final price is set by the last round, not my opener.
- In round 2, if the standing bid is already close to my value (within ~1 minimum raise), I pass; the margin isn't worth the risk of winning thin.
- Lots I value well above estimate (big positive gap) are the ones worth fighting for in round 2; that's where my profit came from.
- Opponents in this game bid aggressively in round 1 but settle around 10–15. Expect final prices near the low teens, and only contest lots worth meaningfully more than that to me.
- The score is value minus price on wins only. A clean filter — "will this likely clear at least 5–10 under my value?" — beats bidding on everything.