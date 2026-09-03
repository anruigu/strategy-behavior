---
game: ref_auction
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 3095
---
**Budget accounting is the top priority.** Before each reply, recompute the budget token from scratch: starting budget minus hammer prices of lots I have actually won. In this episode the true budget was 30 − 2 = 28 throughout, yet my tokens bounced between 30, 28, and 98. Worse, my bids themselves went over budget: I bid 33 on lot 3 and 45 on lot 5 with only 28 available — and both appear to have been rejected. Never write a bid number larger than the current budget. Unsuccessful bids cost nothing; only wins deduct.

**Over-budget jumps get thrown away — with costly side effects.** On lot 5 my round-1 minimum bid of 4 was the standing high bid going into round 2. My "decisive" jump to 45 exceeded my budget, and the lot evidently sold to me at my standing 4 — pure luck. The lesson cuts both ways: an over-budget round-2 raise is discarded, and I may win at my old standing bid anyway (great) or lose the lot to a valid rival raise (disaster). Cap every bid at budget.

**Round-1 minimum-raise opens are the money-maker.** Opening at the minimum raise when there is no standing bid is a free option that can win outright: lot 1 (worth 36) sold to me at 2, and lot 5 (worth 52) sold to me at 4 — that is +82 of the profit right there. Always open at the minimum raise on any lot worth meaningfully more than that minimum. If a rival has already bid, enter at the minimum raise only when the standing bid is comfortably below my value.

**Round 2 when I hold the standing bid:** If my round-1 bid stands as high bid and no rival has raised, passing is correct — the lot is already mine at my cheap price. Do not raise my own standing bid "to be safe"; a self-raise only costs money (I did pass correctly on lot 1 round 2). Only raise if a rival has topped me.

**Round 2 when a rival tops me:** If the standing bid is at or above my value, pass immediately — correctly done on lot 2 at 40 vs value 27. If below my value, bid up to min(value − small margin, budget). Losing a valid bid costs nothing, so the aggressive side is free — but only within budget.

**Sizing the final jump:** With value V, standing bid S, and budget B, bid roughly min(V − (10–15% of V), B − 1). When B is well below V (budget-constrained on a high-value lot), bidding essentially the full remaining budget is right — a rejected over-budget bid is worth nothing.

**Budget-constrained play overall:** Starting budget 30 against values up to ~52 means I can afford at most one substantial purchase plus cheap steals. This favors the minimum-raise opening strategy even more: cheap standing bids from round 1 are often what actually win, because my budget rarely permits a legitimate near-value jump later.

**Don't chase sunk interest:** Round-1 participation commits nothing. If round 2 shows a rival past my value or past my budget, drop out cleanly.

**Pacing across lots:** Cheap early steals are fine (they cost almost nothing); avoid committing big money on low-margin lots early. Keep powder for high-value lots, but remember the real cap — the budget number, recomputed every single turn, in the bracket.