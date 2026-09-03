---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 2
round: 3
chars: 3217
---
The biggest correction from this episode: round 2 is NOT my last word. I assumed a final-round minimal bid locks the win, but rivals act after me within the round — lot 1 (I bid 12, rival won at 16) and lot 4 (I bid 6, rival won at 8) both got stolen for a token raise over my minimal bid. I left two lots worth 71 combined on the table over a few extra dollars. From now on, minimal final-round topping is off the table unless my value or budget genuinely forbids more.

Round 2 policy, revised: I bid as high as my constraints allow, to make counter-bidding expensive for rivals. My bid = min(my value, my remaining budget). Bidding full value caps my surplus at zero, but a zero-surplus win is worth as much as losing at zero, and it forces any rival to actually overpay to take the lot. Exception: if standing + minimum raise is already near my value (small headroom) and rivals in this episode have shown they counter, bidding full value is fine; if rivals have shown they DON'T counter round-2 bids (losses recorded at exactly my bid or thereabouts), I can go back to standing + raise and keep the surplus. Default to the aggressive version — observed rivals do counter.

Also on final-round bids: whether I want to exclude a rival cheaply depends on what that rival's observed final prices look like. When rivals consistently pay roughly estimate or their apparent value, bidding just below/at my own value is a strong deterrent; the experiment "they paid 16 for lot 1 and 8 for lot 4" shows they bid close to or above value, so deterring them requires real money, not minimal raises.

Round 1 stays cheap: minimum raise, since another round follows and I've won lots cheaply by saving my serious bid for round 2. But I note the standing bid in round 2 can already be large (lot 2 opened at 30 against my budget of 30 — unaffordable regardless of value). On early lots with a tight budget, I should not expect to win every lot; I pick battles.

Budget-token discipline: this episode it worked — I recomputed from the results list (won lot 3 at 16, starting 30 → 14) and tracked it correctly through lots 4 and 5. Keep doing exactly that: budget = starting amount minus amounts actually paid for lots I won, recomputed each turn from "Results so far," never from what I bid.

Binding constraint on every bid: min(remaining budget, value). Never more than I can pay. If the minimum legal raise exceeds my remaining budget, I pass immediately (lot 2 round 2 was handled correctly this way).

Prioritization with tight budget: commit to lots where (my value − current standing bid) is largest relative to price; that's where surplus per dollar is best. Don't spread thin. Lot 3 (won 16 for a 53-value lot) was the model outcome; earlier cheap-theft losses showed what playing too timidly costs.

I pass immediately when the standing bid already meets or exceeds my value — winning there locks in zero or negative surplus.

I bid against value and budget, not against the estimate, and I use observed rival behavior only for the two documented calibrations: whether rivals counter round-2 bids, and whether they overpay.

Replies stay short; I always end with both bracketed tokens, compute first, budget line last.