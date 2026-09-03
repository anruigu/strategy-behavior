---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 3348
---
# Playbook: ref_auction

**Budget tracking.** My budget is my starting budget minus the total I have *paid* for lots I have already *won*. I only pay when I win a lot. I must recompute this before every single bid and never report a number I haven't derived by subtraction. In the last episode I reported a budget of 100 when my starting budget was 30 — that was a catastrophic tracking error that would have led to overcommitment.

**Prioritization across lots.** Before each lot I ask: is my value for this lot high enough relative to the estimate and the likely competition to justify spending budget here? With 5 lots and a finite budget, I should target the 1–2 lots where my value is most clearly the highest (my value far exceeds the estimate, suggesting others value it less). I pass on the rest. In the last episode I contested 4 of 5 lots with a budget of 30 and only won one.

**Round 1.**

- If no one has bid and I have decided this lot is worth contesting, I open at roughly 40–50% of my value. This is a probe, not a commitment.
- If someone has already bid and I want in, I raise by one or two minimum increments to signal presence without anchoring high.
- If I have not decided this lot is worth contesting (my value is only modestly above the estimate, or I have a better lot coming), I pass and save budget.

**Round 2 (final round).**

- I do not bid the minimum raise to win. The minimum raise is a signal, not a winning bid, and it invites a counter.
- If I want the lot, I bid at **95–100% of my value**. In the last episode I bid 89% of value on a lot worth 56 to me and still lost. The 85–95% range is too conservative; it leaves a gap an opponent can exploit. If I'm going to commit, I commit fully.
- I only bid in the final round when my value exceeds the current bid by at least 20–25%. If the gap is thinner than that, the expected profit is too small to justify the risk of a counter-bid, and I pass.
- I do not bid a "moderate" amount (70–85% of value). That is the worst of both worlds: high enough to get outbid, low enough to leave profit on the table. I either commit at 95–100% or I pass.

**When to pass in the final round.**

- If the current bid is at or above my value, I pass.
- If my value minus the current bid is less than 20–25% of my value, I pass. The thin margin isn't worth the risk.
- If I have remaining budget I'd rather deploy on a later lot where my value is higher, I pass.

**Opening bids in a fresh lot (no standing bid).**

- Open at 40–50% of my value. Not higher — round 1 is for information, not commitment.

**What clearly did not work (last episode).**

1. **Budget tracking broke down.** I reported impossible budget figures. I must recompute from scratch every time: starting budget minus sum of winning prices.
2. **85–95% of value in round 2 was not enough.** I bid 50 on a lot worth 56 and lost. The new floor is 95%; in practice I should bid 95–100%.
3. **I contested too many lots.** With a budget of 30 and five lots, I should target at most 1–2 lots where my value advantage is clearest. Spreading thin across four lots meant I underbid on the ones that mattered.
4. **I treated every lot as worth contesting.** Lot 4 was worth 19 to me with an estimate of 24 — my value was *below* the estimate, a clear signal others likely value it more. I should have passed immediately.