---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 2952
---
# Playbook

**Read the starting budget exactly as stated and never assume.** In this episode I treated a budget of 30 as if it were 100 for the entire auction. This is the single most dangerous error I can make. Before my first bid, I will re-read the budget line and write the number down. Every subsequent budget calculation starts from that number.

**Budget tracking is sacred.** Before every bid, compute: starting budget minus the sum of prices I actually paid for lots I won. State that number in the [budget] field. Do not guess, do not carry forward a wrong number.

**In round 2 (final round), bid the minimum winning amount: H + min_raise. Never bid your full value.** Bidding my full value guarantees zero profit if I win. The minimum winning bid is the most I should ever pay. If H + min_raise ≤ my value, I bid H + min_raise and pocket the difference. If H + min_raise > my value, I pass. The old "bid full value to maximize winning chance" rule is the source of my zero-profit outcomes and is hereby retired.

**In round 1 of a lot I want, bid 60–70% of my value, but never more than I can afford if I must raise again in round 2.** A round-1 bid that leaves me unable to match a reasonable round-2 increase is a trap. Before opening, I check: if the competitor raises by one increment above my round-1 bid, can I still win profitably in round 2? If not, my round-1 bid is too high or I should pass.

**The increment trap.** If my value is V and the current high in round 2 is H, the minimum winning bid is H + min_raise. If H + min_raise > V, I pass. If H + min_raise ≤ V, I bid exactly H + min_raise. Profit = V − H − min_raise. I never bid more than this.

**When my value is below the estimate, pass early.** I am the irrational bidder on that lot. A probe is fine only if the current high is already below my value and I can win cheaply.

**Allocate budget by expected profit, not by lot count.** With a budget of 30 and five lots, I can realistically win at most one or two lots profitably. I should identify the one or two lots where (my value − realistic winning price) is largest and concentrate there. Winning three lots at zero margin each is worse than winning one lot with a healthy margin.

**Round 1 opening bid should be calibrated to the competitor's likely value.** If the estimate is 44 and my value is 56, the competitor's value is probably somewhere near the estimate. A round-1 bid of 32 (60% of 56) signals I'm below the estimate and invites them to outbid me. A round-1 bid closer to the estimate (e.g., 40–44) makes them work harder to displace me. But this only makes sense if my budget supports it.

**What did not work:** I misread my budget as 100 instead of 30, which made me feel wealthy and bid aggressively across multiple lots. I then bid my full value in round 2 on two lots, guaranteeing zero profit on both. The fix is mechanical: in round 2, bid H + min_raise, not V. And read the budget line twice.