---
game: hf_hanabi_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 3873
---
# Playbook

**Opening moves**
- When all stacks are at 0, my first clue should target a 1 in someone else's hand. If a colour clue pinpoints exactly one card and it's a 1, use that. If a colour clue hits multiple 1s (e.g., three B1s), that's even better — it's the most information-dense clue available.
- If no other player holds a visible 1, clue rank 1 to whoever holds the most 1s.

**Playing my own cards**
- When I have a card whose colour AND rank are both confirmed by clues, and the stack for that colour is exactly one below that rank, I play it immediately. No hesitation.
- When I have a card with known colour but unknown rank, and the stack for that colour is at 0, I do NOT discard it. It could be a 1. I keep it and wait for a rank clue, or I discard a different card (one that is fully unknown, or one whose colour's stack is already past 1, making a rank-1 impossible).
- When I have a card with known colour but unknown rank, and the stack for that colour is at 1 or higher, I may discard it freely — a rank-1 is no longer playable for that colour.

**Discarding**
- I discard in this priority order: (1) fully unknown cards, (2) cards whose colour's stack is past 1 (so they can't be 1s), (3) cards whose colour's stack is at 0 but which I've held for several turns without a rank clue arriving.
- I never discard a card I can currently play.
- When I have 0 clue tokens and no confirmed playable card, I discard to regenerate a token. I choose the discard that loses the least potential value.

**Cluing others**
- I always prefer a clue that enables an immediate play next turn over a clue that provides general information. If I can see a card in someone's hand that matches the next needed rank for its colour, I clue for that.
- When choosing between a colour clue and a rank clue, I pick whichever narrows the target to the fewest slots. A clue that highlights exactly one card is ideal; a clue that highlights two cards is acceptable if both are playable; a clue that highlights three or more is a last resort.
- When I have a choice between helping player 1 and player 2, I help whoever is about to act next (turn order).
- I do not waste a clue token on information I already have or that doesn't change anyone's next action.

**Mid-game adjustments**
- Once stacks are advancing, I shift from "get 1s out" to "keep the pipeline full." I look for the next-needed card (stack top + 1) in other players' hands and clue for it.
- If two different colours both need their next card and both are in the same player's hand, a rank clue that covers both is better than two separate colour clues.
- I track which cards I've already identified in my own hand. If two clues confirm the same slot (e.g., colour R and rank 2 both hit slot 2), I now know that slot is R2. I use this to make play decisions.

**Endgame (last 5 turns)**
- If I have a confirmed playable card, I play it. Every point matters.
- If I have no confirmed playable card and I have clue tokens, I give the clue most likely to produce a play on the very next turn.
- If I have no confirmed playable card and no clue tokens, I discard the card least likely to become playable (unknown cards, or cards whose colour is already stacked high).
- I do not hoard cards in the last 3 turns. If I can't play them, they're dead weight.

**What I know does not work**
- Discarding a partially-identified card (colour known, rank unknown) when the stack for that colour is at 0. I did this and lost points. The card could have been a 1.
- Giving a clue that highlights many cards when a narrower clue is available. It wastes the recipient's attention and the clue token's value.
- Holding a card passively when I could have discarded it earlier to generate a clue token that would have produced a play for someone else. One point for my card later is often less than one point for their card now.