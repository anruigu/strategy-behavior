---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 2
round: 2
chars: 2534
---
The core fix from this episode: in round 2, the winner pays what they bid — so I should NOT jump to my full value. That capped my surplus at zero on every lot I won. Instead, in the final round I bid the smallest amount that tops the standing bid (standing + minimum raise), capped at my value. Winning lot 4 at 31 when I bid 31 was 100% of my actual score; every full-value bid earned me nothing.

Round 2 policy, precisely: if standing + minimum raise is at or below my value, bid exactly that. If the standing bid is already at or above my value, pass. The only exception is when I've seen rivals reliably jump to full value on final rounds (rivals here DID sometimes overpay — lot 2 went for 45 against an estimate of 44) — if I believe the rival will max out, then and only then do I bid my own full value, accepting zero surplus to secure the win, but never above value.

In round 1, I still open cheap — minimum raise — since another round follows; this worked fine.

The budget-token discipline needs a hard rewrite: the budget starts at the number given in the prompt (30, not 100, not 200) and only decreases when I actually win a lot, by the amount I paid. I will recompute it from the "Results so far" list each turn rather than from memory of what I bid, since unrequited minimals cost nothing. This episode I reported budgets that exceeded the starting amount and contradicted myself turn to turn — that must never happen again.

With a small starting budget (e.g. 30), my bids are also capped by remaining funds, not just by value. I track the binding constraint as min(remaining budget, value) on every bid, and I never bid more than I can pay.

When budget is tight, I prioritize: lots where the gap between my value and the current standing bid is largest get my remaining money first, since that's where surplus per dollar is highest. If two lots remain and I can't afford to max out both, I commit to the higher-surplus one rather than spreading.

I keep passing immediately when the standing bid already meets or exceeds my value — winning there locks in zero or negative surplus.

I bid only against value and budget, never against the estimate or rival behavior — except for the single documented exception above: a rival's demonstrated willingness to overpay on final rounds changes my "minimum raise wins" assumption, because with one last round I cannot respond to a jump.

I keep replies short and always end with both bracketed tokens, compute-and-then-write, so the budget line is the last thing I settle.