---
game: ref_auction
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 3268
---
# Playbook: open ascending auction

**Hard cap rule:** never bid above my private value for a lot. When the standing bid plus minimum raise exceeds my value, I pass immediately, no exceptions.

**Budget tracking — the critical failure this episode:** my stated budget must go down the moment I win a lot, and it did not. After winning lot 3 for 20, I kept declaring [budget: 10] but then bid 16 on the final lot — more than I had. That over-budget bid did not count, and I lost a lot where standing (12) + raise (4) = 16 was well under my value of 26. Rule: after every win, subtract the price paid and write the new number in every subsequent [budget: N] token; before bidding, check standing + minimum raise is below BOTH my value AND remaining budget. If it exceeds remaining budget, the bid is void — do not make it.

**Round 1 behavior:** bid the minimum raise over the standing bid, nothing more. This episode that worked fine — small openings (4-6 over low standing bids) cost little and kept me in the auction without overpaying.

**Round 2 is where lots are actually decided — opponents jump here.** In every contested lot, my round-1 minimum raise was answered by an opponent raising well beyond the minimum in round 2 (my 15 beaten by 18; my 16 beaten by 24). A second minimum raise is usually not enough to win. When surplus is large, consider bidding more than the minimum in round 2 — e.g., standing + 2 or 3 raises, capped by value and budget — because a minimum raise loses the lot to any determined opponent. When surplus is thin, the minimum raise or a pass is right.

**Where I left value on the table:** I won lot 3 (value 26, paid 20, +6) and then, budget broken, lost lot 5 where I could have profitably gone to at least 26. Meanwhile I lost lots 1 and 2 with thin minimum raises. Total score +6 on values of 37 and 42 available early. Lesson: allocate budget across lots rather than committing most of it to the mid-game winner; if I plan to bid up to near value on any lot, keep enough budget to do it.

**Competitive bidding at small margins:** when surplus (value minus price I'd pay) is under ~20% of value, prefer to pass unless it's one of the last lots. Thin-surplus wins tie up budget that blocks later thick-surplus bidding.

**Prioritize by surplus:** rank lots by value minus likely clearing price. High value relative to estimate deserves a firm, possibly above-minimum round-2 bid; value below or near estimate deserves only token bids or passes.

**When it's put to me:**
- Round 1: bid exactly the minimum raise if standing is under ~60-70% of my value; otherwise pass and wait for round 2.
- Round 2: if standing + minimum raise is below both my value and remaining budget, bid at least the minimum raise; if surplus is large (value exceeds standing by >40%), bid standing plus two raises to actually win, still capped at value and budget.
- Never bid more than remaining budget — check the [budget: N] number I just wrote, which must reflect all prior wins.
- Never exceed one-third of remaining budget on a single lot if more valuable lots may remain, except on the final lot.
- If my value is below the estimate and others are bidding, pass entirely.
- On the last lot, spend freely up to value — there is nothing to save for.