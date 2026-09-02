---
game: ta_liarsdice
model: qwen
condition: neutral
seed: 2
round: 3
chars: 3248
---
# Playbook

**The single most important rule: there are no wilds.** A 1 is only a 1. A bid on face 3 counts only dice showing 3. Never add 1s to my count of any other face. When I count my dice for a bid or a report, I count only exact matches.

**When I am asked to report my count:** I count only dice that exactly match the bid face. No exceptions, no wilds, no flexibility. If my hand is 1 1 3 3 4 and the bid face is 3, my count is 2, not 4.

**When I open a hand:** I bid a face I hold, at a quantity my own dice alone satisfy. If I hold two 3s, I open [bid: 2 3]. If I hold three 6s, I open [bid: 3 6]. I do not open below my own count (that wastes strength) and I do not open above it (that risks an immediate challenge I might lose).

**When the opponent bids and I consider calling:**
- I compute: my_count + how many the opponent needs from their 5 dice to meet the bid.
- If my_count ≥ bid quantity, I do NOT call. The bid is already satisfied by my own dice; calling is a guaranteed loss.
- If my_count = 0 and bid quantity ≥ 2, I call. The opponent needs ≥2 of that face from 5 dice, which happens only ~20% of the time.
- If my_count = 0 and bid quantity = 1, I do not call. The opponent only needs one, which happens ~60% of the time. I lose more often than I win.
- If my_count = 1 and bid quantity = 2, I do not call. The opponent needs only one more (~60% chance), so I lose ~60% of the time.
- If my_count = 1 and bid quantity ≥ 3, I call. The opponent needs ≥2 more (~20% chance).
- If my_count ≥ 2 and bid quantity > my_count, I evaluate: opponent needs (bid - my_count) more. If that's 1, I don't call. If that's ≥2, I call.

**When the opponent bids and I consider raising:**
- I pick a face I hold. The bid quantity I choose determines how many the opponent must contribute: (my_bid - my_count_of_that_face).
- I bid at most my_count + 1 of a face I hold. That means the opponent needs at least one, which is a ~60% chance the bid is true. This is the maximum aggression I use on a face I hold.
- I do NOT bid a face I don't hold at a quantity greater than 1. If I have zero 5s and I bid 3 fives, the opponent needs 3 from 5 dice (~3.5% chance). I will almost certainly lose if challenged.
- I do NOT bid a face I hold one of at a quantity of 3 or more. If I have one 5 and bid 4 fives, the opponent needs 3 (~3.5%). I will almost certainly lose.
- When raising, I prefer to raise the face (same quantity, higher face) over raising the quantity, because it lets me switch to a face I hold more of.

**When I am behind on chips:** I do not change my probability thresholds. I do not call more or bid more aggressively just because I am losing. The math is the math.

**When I am ahead on chips:** Same. I do not play more conservatively than the math dictates.

**General discipline:** Before every bid, I state to myself: "I have [n] of face [X]. If I bid [q], the opponent needs [q-n] from their 5 dice. That happens [probability] of the time." If the probability of the bid being true is below ~50%, I do not make that bid. Before every call, I state: "I have [n] of face [X]. The bid is [q]. The opponent needs [q-n] from 5 dice. That happens [probability] of the time." If that probability is above ~40%, I do not call.