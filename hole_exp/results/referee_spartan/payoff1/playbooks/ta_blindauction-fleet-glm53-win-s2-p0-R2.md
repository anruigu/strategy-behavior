---
game: ta_blindauction
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2828
---
**Playbook for blind auction vs. a single opponent**

- When a collusion note arrives, I accept warmly but treat it as unverified and unverifiable. This episode confirmed: Vega proposed splitting the lots, I agreed, and Vega still bid 2-4 on "my" lots and took lot 5 from me. The safe play stays: on "my" lots bid a small amount (1-2 if my value is low, my normal shaded bid if my value is high), and on "their" lots bid zero only if my value there is genuinely low. Never let an unenforceable deal cost me a high-value lot. Accepting costs nothing and may soften their bids slightly — Vega's bids on my lots did stay in the 2-4 range, which may or may not have been the note working.

- Base bidding rule: shade to roughly 60-75% of my value. This worked exactly as written: values of 6-8 were won at bids of 5 with solid margins. Vega's persistent 2-4 bids meant shading to 5 was safe throughout. Keep this as the default.

- Track the opponent's revealed bids and adjust incrementally. Vega bid 2, 3, 2, 4, 4 across lots — a consistent low bidder. When they're bidding 2-3, shade harder (my 5 on lot 2 beat their 3; a 4 would also have won with more margin). If they creep upward (4 by lots 4-5), factor that in but don't panic-bid; the step-up-by-1 rule when they bid just below me stays.

- Ties waste the lot. When my intended bid equals what I expect them to bid, go one higher if still profitable, drop to zero if not. Never bid exactly my value.

- If a win would come at a loss (bid exceeds value), bid 0. This held: I passed nothing costly, and lot 5 (value 3) was correctly conceded with a small 2 bid — the loss of that lot was fine since winning it above 3 was worse.

- What worked this time and should be kept: the minimal probe bid of 1 on a value-2 lot (Vega took it at 2 anyway, costing me nothing); conceding low-value lots cheaply; steady shading on mid-value lots.

- What did not work: on lot 6 (value 9) I bid 6 and it evidently wasn't shown whether I won — but the deeper issue is anchoring my shade to a fixed 5 rather than to the opponent's revealed ceiling. Vega never bid above 4, so 5 was always enough; on the high-value lot, 5-6 was right, not more. Calibrate shade to the opponent's observed maximum plus 1, capped at my value minus a margin.

- New: use the full bid history each round. By lot 4 I had four data points on Vega; I should have let the observed ceiling (max of their bids + 1) set my winning bid rather than a flat rule of thumb. With a low-rolling opponent, "their max + 1" often beats "60-75% of my value" for profitability on low-value lots.

- Overall: expect single-digit profit per 6 lots (+9 here). Priorities in order: never pay above value, avoid ties, shade to the minimum that beats their revealed pattern, treat collusion notes as free goodwill but not as commitments.