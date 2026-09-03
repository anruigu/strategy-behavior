---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 3707
---
# Playbook: ref_auction

**Budget tracking.** My budget is my starting budget minus the total I have *paid* for lots I have already *won*. I only pay when I win a lot. I must recompute this before every single bid: starting budget minus sum of winning prices for lots I've won. In this episode I tracked correctly (30 → 30 → 30 → 30 → 0). Keep doing this.

**Affordability check before committing to a lot.** Before I decide a lot is worth contesting, I verify: if the standing high in round 2 reaches some level H, can I still afford H + minimum raise? If my remaining budget is less than the minimum raise above the current high at any point, I am locked out. In this episode, lot 2 had a round-2 high of 28 with a minimum raise of 3, requiring a bid of 31 — above my entire budget of 30. I should have recognized in round 1 that I likely couldn't outbid in round 2 and either (a) tried to win in round 1 at a price I could afford, or (b) passed early and saved budget for a lot where the price level was within my reach.

**Prioritization across lots.** With a finite budget and 5 lots, I target the 1–2 lots where my value is most clearly the highest (my value far exceeds the estimate, suggesting others value it less) AND where the price level is within my budget. I pass on the rest. In this episode I correctly passed lots 1 and 5 (value below estimate) and committed to lot 4 (value 36 vs. estimate 23). The result (+6) confirms the approach works.

**Selecting which lot to target.** I rank lots by (my value − estimate) as a proxy for my relative advantage, then filter by affordability: the lot's estimate (and likely clearing price) should be below my remaining budget. If my top-ranked lot is unaffordable, I move to the next.

**Round 1.**

- If I have decided this lot is worth contesting and no one has bid, I open at roughly 40–50% of my value. This is a probe. In this episode I opened at 15 (42% of 36) and no one raised — confirming low competition.
- If someone has already bid and I want in, I raise by one or two minimum increments to signal presence without anchoring high.
- If I have not decided this lot is worth contesting (my value is at or below the estimate, or the lot is unaffordable at likely clearing prices), I pass immediately. Do not enter a lot I cannot win.

**Round 2 (final round).**

- In round 2 there is no further round. If I bid above the current high and no one bids after me, I win at my bid. I do not know whether later bidders will still act, so I treat round 2 as: bid enough to likely win, capped by my budget.
- I bid **min(95–100% of my value, my remaining budget)**. If my remaining budget is less than the minimum raise above the current high, I cannot bid and must pass.
- I do NOT bid a "moderate" amount (60–85% of value). That is the worst of both worlds: high enough to get outbid, low enough to leave profit on the table. I either commit at 95–100% (or my full budget if that's less) or I pass.
- I only enter the final round when **(my value − (current high + minimum raise)) / my value ≥ 20%**. Note: I use the effective raise (high + min_raise), not the raw gap. In this episode, lot 2 had (35 − 31)/35 = 11%, correctly below threshold. Lot 4 had (36 − 17)/36 = 53% (my own bid of 15 + min raise 2 = 17), well above threshold.

**When to pass in the final round.**

- If the current bid is at or above my value, I pass.
- If (my value − (current high + minimum raise)) / my value < 20%, I pass. The thin margin isn't worth the budget.
- If my remaining budget is less than the minimum raise above the current high, I pass (I physically cannot bid).
- If I have a later lot where my value advantage is larger, I pass here to save budget.

**