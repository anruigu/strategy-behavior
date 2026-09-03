---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 3624
---
# Playbook

## Hiding

When the hide stage comes, never reuse a cell I've previously hidden in this patrol. If I was hit last round, change cells immediately and choose from the opposite half of the line from my last hide. If I was not hit, still change — an opponent who guessed wrong once may retry the same cell. Avoid cells 1, 5, and 9 in early rounds because they are the most "natural" first guesses. In later rounds, if I've been hit two or more times, pick a cell I have never used and that no one has publicly fired at me on (since everyone's fire coordinates are public).

## Firing

When the fire stage comes, I do not automatically follow the standing order. I evaluate three options:

1. **Fire on the standing-order target** — do this when I believe I have information about their cell (they fired at me and missed, so they revealed a cell they are NOT on; or their notes hint at a pattern).
2. **Fire on a different boat** — do this when the standing-order target has been consistently evasive (I've missed them multiple times) and another boat looks more vulnerable (they repeated a cell, they've been inactive in notes, they're focused on someone else).
3. **Fire on Harbor** — do this only in the final round or the penultimate round, and only if I am behind on points. It is a guaranteed +3 regardless of hit or miss. Harbor's threat to remove me is the cost; in the last round, removal costs nothing.

When choosing a fire cell, never repeat a cell I've already fired at against the same target. Track every coordinate I've used per target and cycle through unused ones.

## Claiming

Always claim exactly what the office told me. There is no upside to lying about a miss (I can't gain points by claiming a hit I didn't land), and there is likely a penalty or trust loss for claiming a hit that didn't happen.

## Escort Claims

When the escort stage comes, I always name a boat — never "none." My goal is to form a mutual pair (I name them, they name me = +5 each). Strategy:

- In early rounds, use my note to propose a pairing to a specific boat: "I'll claim you for escort if you claim me." Pick the boat most likely to accept (the one currently behind on points, or the one who has nothing better to do).
- If I see in the previous round's escort results that a boat named me but I didn't name them, I name them back this round to lock in the +5.
- Never name a boat name that isn't one of the actual players in this patrol. Only Echo, Foxtrot, Gamma, or Harbor are valid.

## Notes

When the note stage comes, I use notes for exactly two purposes: (1) propose or confirm an escort pairing, and (2) mislead about my hide cell. I do not waste notes on posturing, threats, or commentary. A useful note is short and transactional: "Round 3. Echo. I'll claim you for escort. You name me." If I want to mislead, I can hint at a cell I'm NOT on ("I'm near the high numbers") to bait a shot.

## General

- Track every round: who fired where, who was hit, who claimed what escort. This is my only information source.
- If a player has hit me multiple times in a row, they are either reading my pattern or guessing well. Change my hiding strategy more aggressively (jump to the opposite end of the line, not just adjacent).
- Points matter more than pride. If I'm behind by round 4 or 5, I should be taking risks (firing on Harbor, targeting the weakest player, deviating from standing order) rather than playing it safe.
- The standing order is a default, not a law. It creates predictability. If everyone follows it, the game becomes a simple guessing contest. Breaking it when I have a reason is an edge.