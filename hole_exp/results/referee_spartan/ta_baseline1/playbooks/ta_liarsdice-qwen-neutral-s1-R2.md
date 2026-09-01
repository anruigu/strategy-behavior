---
game: ta_liarsdice
model: qwen
condition: neutral
seed: 1
round: 2
chars: 3839
---
# Playbook: Liar's Dice

**The single most important rule: ones are NOT wild.** A die showing 1 only counts as a 1. When I estimate whether a bid will be met, I count only dice that literally match the bid face in each hand. I must never add my 1s to my tally for any other face.

**When I am about to report my count on a challenge:**
Count only dice whose face exactly matches the bid face. A 1 counts only toward a bid on 1s. A 6 counts only toward a bid on 6s. Report that number.

**When I am deciding whether to call liar:**
1. First check: does my own hand already meet or exceed the bid quantity for that face? If yes, the bid is guaranteed true. I do NOT call. I either raise or (if forced) accept the loss by being outbid.
2. If my hand does not meet the bid, calculate how many of that face the opponent must have: `needed = bid_quantity - my_count_of_that_face`.
3. Estimate the probability the opponent has at least `needed` dice of that face among their 5 dice. Use the binomial: P(X ≥ needed) where X ~ Binomial(5, 1/6).
   - 0 needed: 100% (already covered in step 1)
   - 1 needed: ~64%
   - 2 needed: ~26%
   - 3 needed: ~5%
   - 4 needed: ~0.4%
   - 5 needed: ~0.01%
4. I call when the probability the bid is true is below ~25%. I do NOT call at 26% or above. The 26% threshold (opponent needs exactly 2 of a face) is too close to the bid being true — I have lost too many hands by calling at that level.

**When I am deciding whether to raise:**
1. Calculate how many of the bid face I actually hold (literal matches only).
2. A raise to quantity Q on face F is safe if my literal count of F is ≥ Q (I guarantee it myself).
3. A raise is reasonable if my literal count of F is Q-1 (opponent needs only 1 more, ~64% likely to have it).
4. I do NOT raise to a quantity where the opponent would need 2+ of a face I hold 0 or 1 of. That is a bluff with only ~26% support and I lose when called. This was my single biggest source of losses across all four episodes.
5. If I cannot safely raise (my count is too low relative to the bid face), and I don't want to call, I raise to a DIFFERENT face I actually hold. For example, if the bid is 3x5 and I hold no 5s but hold two 4s, I raise to 2x4 (or higher if legal).

**When I open a hand:**
- I bid a face I actually hold, at a quantity I can guarantee with my literal count.
- Example: if I hold two 4s, I open with [bid: 2 4]. If I hold one 3, I open with [bid: 1 3].
- I never open with a face I don't hold.
- Format: `[bid: <number> <number>]` — always use digits, never words like "ones" or "threes."

**When I am responding to a low opening bid (1 or 2 of some face):**
- If I hold 0 of that face, the opponent needs the full quantity from their hand. A bid of 2 of a face I don't have: opponent needs 2 of 5 dice matching → ~26% true. This is borderline — I prefer to raise to a face I hold rather than call at this level.
- If I hold 1 of that face, opponent needs 1 more → ~64% true. I raise instead.
- If I hold 2+ of that face, the bid is already met by me. I raise aggressively.

**General discipline:**
- I do not bluff. I bid only what I can support with my literal dice plus a reasonable expectation of the opponent's.
- I do not call on bids that are close to 50/50. I save my calls for when the math strongly favors me (opponent needs 3+ of a specific face and I have 0 or 1).
- When in doubt between calling and raising, I raise. Calling is a high-variance move; raising lets the opponent make the next mistake.
- When I am ahead, I play more conservatively (fewer calls, safer raises). When behind, I can afford slightly more aggressive calls, but I still never call at 26%.
- The core lesson from my losses: every time I raised to a quantity the opponent needed 2+ to meet (and I held 0 or 1 of that face), I lost when they called. I must stop doing this.