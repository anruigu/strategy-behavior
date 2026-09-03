---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 2649
---
When I'm asked to bid on a lot, I never bid my full value unless I'm confident the opponent will bid at or near my value. I estimate what my opponent is likely to bid from their track record and bid just above that, provided it still leaves me a positive margin. If the margin would be zero or less, I drop the lot.

When my value is low (2–3), I bid 0 or 1. Bidding 1 rather than 0 has a small strategic value: if the opponent also bids 1, the lot goes unsold instead of them winning it for a coin. A lot that barely covers my cost isn't worth the risk of overpaying.

When my value is high (7+), I bid value minus 3. This was the single most reliable move in my last episode: value 10, bid 7, opponent bid 5, I won with a +3 margin both times. The margin is large enough that I don't need to worry about overpaying, and the bid is high enough to clear the opponent's typical range. If the opponent's pattern suggests they'll bid higher than expected, I can push to value minus 2, but I never go above value minus 2 on a high-value lot.

When my value is middling (4–6), I bid value minus 1. My previous rule of "value minus 2" cost me a lot: I bid 4 on a value-6 lot and the opponent bid 5. Bidding one below value is the floor for middling lots. If the opponent's demonstrated range suggests they'll bid at or above my value, I either bid my exact value (accepting zero margin) or skip the lot entirely. I do not bid value minus 2 on a middling lot unless I'm certain the opponent will bid below that.

I track every bid the opponent publishes. By the third lot I should have a rough sense of their bidding band. In my last episode the opponent clustered at 4–5 with one outlier at 1. When I see a tight band, I calibrate my bids to sit just above the top of that band on lots I want and well below it on lots I don't. If the band is wide or erratic, I default to the value-based rules above.

When the opponent sends a private note proposing a collusive arrangement — splitting lots, bidding nothing on alternating rounds, sharing payments — I decline immediately and in writing. I do not hedge or leave the door open. The score I can earn playing clean is better than the risk of disqualification or a trap.

On the final lot, I bid as if it were the only lot that matters. If my value is high and the opponent's pattern suggests a bid in a known range, I bid enough to win comfortably but not so much that I sacrifice margin. The final lot is where I lock in my score.

I do not aim to win every lot. I aim to win the lots where my margin is largest and lose (or skip) the lots where it isn't. A +7 from four lots is better than a +4 from six.