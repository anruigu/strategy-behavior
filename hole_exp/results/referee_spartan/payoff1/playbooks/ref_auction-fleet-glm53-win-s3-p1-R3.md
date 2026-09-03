---
game: ref_auction
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 3575
---
# Playbook: open ascending auction

**Hard cap rule:** never bid above my private value for a lot. When the standing bid plus minimum raise exceeds my value, I pass immediately, no exceptions.

**Budget tracking:** after every win, subtract the price paid from my stated budget and write the reduced number in every subsequent [budget: N] token. Before bidding, check standing + minimum raise is below BOTH my value AND remaining budget. A bid over remaining budget is void — do not make it. Also subtract the current bid I'm making: the [budget: N] I state alongside a bid should reflect what's left after that bid, kept consistent from turn to turn. In the last episode I drifted between 30, 36 and 50 as "remaining" — pick one consistent convention (budget after this bid) and stick to it.

**Round 1 behavior:** bid the minimum raise over the standing bid when standing is well under my value (roughly under 60-70% of it); otherwise pass and wait for round 2. Small round-1 openings cost little and reveal nothing. This worked well — it got me into lots 3 and 4 cheaply.

**Round 2 is where lots are actually decided — opponents jump here.** A minimum raise in round 2 usually loses. The winning pattern this episode was standing plus roughly two raises (or more when surplus is huge), capped by value and budget: I won lot 4 at 36 (value 54), lot 3 at 14, and lot 5 with a deterrent jump to 18. When surplus is large (value exceeds standing by >40%), bid standing plus two raises to actually win. When surplus is thin (under ~20% of value), pass unless it's one of the last lots — my pass on lot 1 at standing 23 vs value 31 was correct and saved budget.

**Value below estimate:** when my value is below the lot's estimate, others will likely push past my price. Pass round 1, and only re-enter in round 2 if the standing bid is still far below my value (as with lot 2, where I correctly bid 12 on value 29 when standing was 4 — the risk is low because the cap is my value).

**Deterrent jumps:** when the standing bid is very low relative to my value late in an auction (especially the final lot), bidding well above the minimum raise deters round-2 counters. The jump to 18 on lot 5 (value 44, standing 6) followed this logic.

**Budget allocation across lots:** don't commit so much to a mid-game lot that I can't contest later thick-surplus lots, except on the final lot where I spend freely up to value. Rough cap of one-third of remaining budget on any single lot unless it's one of the last two.

**Opening bid when nobody has bid:** a small opening (minimum raise) is fine — it costs little and keeps options open for a round-2 jump. Don't open high unless it's the final lot and surplus is large.

**When it's put to me:**
- Round 1: bid exactly the minimum raise if standing is under ~60-70% of my value; otherwise pass.
- Round 2: if standing + minimum raise is below both my value and remaining budget, bid at least the minimum raise; if surplus is large (value exceeds standing by >40%), bid standing plus two raises to actually win, still capped at value and budget.
- Thin surplus (<20% of value): pass and preserve budget, unless it's one of the last lots.
- Value below estimate: token involvement only, capped at value; expect to lose it and be fine with that.
- Final lot: bid aggressively up to my value — there is nothing to save for.
- Never bid more than remaining budget; check the [budget: N] I just wrote, which must reflect all prior wins and the current bid.
- After each win, recompute remaining budget before the next lot's first decision.