---
game: ref_hanabi
model: qwen
condition: neutral
seed: 0
round: 1
chars: 3428
---
# Playbook

**Opening moves (no clues on my hand yet):**
- When all stacks are at 0 and I have no information about my own hand, I clue a teammate who holds a 1 in a colour that is not yet on the stack. I prefer a clue that touches exactly one card if possible; if it touches two, I prefer the case where one is a 1 (playable) and the other is a high card (obviously not playable), so the recipient has no ambiguity.
- I do NOT repeatedly clue the same player or the same colour across consecutive turns unless a new card has entered their hand.

**When I still have no clues on my hand after 2–3 of my turns:**
- I discard a card. This generates a clue token and signals to the other players that I need information. Keeping my tokens while my hand stays unknown is the single biggest mistake I made in one episode (scored only 2). I would rather have a token in the pool and be clued than hoard tokens and remain blind.
- I discard the card I can most safely eliminate: a duplicate of a card I see in another player's hand, or a high card (4 or 5) in a colour that already has a 1 held by someone else.

**When I receive a clue:**
- I immediately check whether the clue, combined with the stack state, identifies a card I can play right now. If yes, I play it on my next turn (or this turn if it's my turn).
- If the clue is a colour and I hold multiple cards of that colour, I use the stack state to narrow: only the card matching stack+1 is "live"; the others are "dead" and I should plan to discard them.
- If two clues together pin a card exactly (e.g., "Yellow" + "rank 1" = Y1), I treat it as confirmed. If it's playable, I play it. If it's not (already on the stack), I discard it.

**When I have 0 clue tokens:**
- I play only if I am confident the card is correct (deduced from prior clues + stack state). A wrong play costs a fuse and may end the game.
- Otherwise I discard the least useful card. I prefer discarding a card whose colour is already well-advanced (so the next card of that colour is far off) or a card duplicated in another player's hand.

**Cluing strategy (when I do have tokens):**
- Priority 1: clue a card that is exactly the next card needed on a stack (stack+1). This guarantees a play next turn.
- Priority 2: clue a 1 in a colour not yet started, to open a new stack.
- Priority 3: clue a card that is two ahead (stack+2) to set up a future play, but only if I have surplus tokens (5+).
- I avoid cluing a colour that touches 3+ cards in the target's hand unless all but one are obviously dead (high cards in an advanced colour).
- I never clue a colour or rank that the target already knows from a previous clue (waste of a token).

**Endgame (last 3–4 turns):**
- I prioritise cluing a teammate a card they can play immediately on their very next turn.
- If I have a playable card myself, I play it before it's too late.
- I do not discard in the last 2 turns unless I have no other option; a discard in the last turn is pure loss.

**General discipline:**
- I always use the format `[clue: player P, <colour or rank>]` — never abbreviate the "player" keyword.
- Before cluing, I mentally verify the clue is valid (the target actually holds at least one card of that colour/rank).
- I track which cards I have already clued to each player so I don't repeat.
- When I see a misplay by a teammate, I note which card was wasted and adjust my future clues to avoid pointing at that card again.