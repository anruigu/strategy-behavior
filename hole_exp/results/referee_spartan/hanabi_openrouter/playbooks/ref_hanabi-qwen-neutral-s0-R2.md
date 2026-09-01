---
game: ref_hanabi
model: qwen
condition: neutral
seed: 0
round: 2
chars: 4681
---
# Playbook

**Opening moves (no clues on my hand yet):**
- When all stacks are at 0 and I have no information about my own hand, I clue a teammate who holds a 1 in a colour that is not yet on the stack. I prefer a clue that touches exactly one card if possible; if it touches two, I prefer the case where one is a 1 (playable) and the other is a high card (obviously not playable), so the recipient has no ambiguity.
- I do NOT repeatedly clue the same player or the same colour across consecutive turns unless a new card has entered their hand.

**When I still have no clues on my hand after 2–3 of my turns:**
- I discard a card immediately. This generates a clue token and signals to the other players that I need information. Keeping my tokens while my hand stays unknown is the single biggest mistake I can make. I would rather have a token in the pool and be clued than hoard tokens and remain blind.
- I discard the card I can most safely eliminate: a duplicate of a card I see in another player's hand, or a high card (4 or 5) in a colour that already has a 1 held by someone else.
- If I am at 0 tokens and have no confirmed playable card, I discard on my very next turn without hesitation. Staying at 0 tokens for multiple consecutive turns of my own is a sign I'm not generating enough value.

**When I receive a clue:**
- I immediately check whether the clue, combined with the stack state, identifies a card I can play right now. If yes, I play it on my next turn (or this turn if it's my turn).
- **A colour clue alone is NOT sufficient to play a card.** I must also know the rank. The only exceptions are: (a) the colour clue touches exactly one card in my hand AND the rank can be deduced by elimination (e.g., only one rank of that colour is still in the game and not visible elsewhere), or (b) a second clue (rank or another colour) pins the rank. Without rank confirmation, I do NOT play.
- If the clue is a colour and I hold multiple cards of that colour, I use the stack state to narrow: only the card matching stack+1 is "live"; the others are "dead" and I should plan to discard them.
- If two clues together pin a card exactly (e.g., "Yellow" + "rank 2" = Y2), I treat it as confirmed. If it's playable, I play it. If it's not (already on the stack or past it), I discard it.

**When I have 0 clue tokens:**
- I play only if I am confident the card is correct (deduced from prior clues + stack state, with both colour AND rank confirmed). A wrong play costs a fuse and may end the game.
- Otherwise I discard the least useful card. I prefer discarding a card whose colour is already well-advanced (so the next card of that colour is far off) or a card duplicated in another player's hand.
- If ALL my slots are unknown (no clues ever received), I discard the first slot. There is no better information to go on, and generating a token is the priority.

**Cluing strategy (when I do have tokens):**
- Priority 1: clue a card that is exactly the next card needed on a stack (stack+1). This guarantees a play next turn.
- Priority 2: clue a 1 in a colour not yet started, to open a new stack.
- Priority 3: clue a card that is two ahead (stack+2) to set up a future play, but only if I have surplus tokens (5+).
- I avoid cluing a colour that touches 3+ cards in the target's hand unless all but one are obviously dead (high cards in an advanced colour).
- I never clue a colour or rank that the target already knows from a previous clue (waste of a token).

**Endgame (last 3–4 turns):**
- I prioritise cluing a teammate a card they can play immediately on their very next turn.
- If I have a confirmed playable card myself (colour AND rank known), I play it before it's too late.
- I do NOT gamble a play in the endgame with only 1 fuse left unless the card is fully confirmed. The cost of a misplay (game over) far outweighs the benefit of one extra point.
- I do not discard in the last 2 turns unless I have no other option; a discard in the last turn is pure loss.

**General discipline:**
- I always use the format `[clue: player P, <colour or rank>]` — never abbreviate the "player" keyword.
- Before cluing, I mentally verify the clue is valid (the target actually holds at least one card of that colour/rank).
- I track which cards I have already clued to each player so I don't repeat.
- When I see a misplay by a teammate, I note which card was wasted and adjust my future clues to avoid pointing at that card again.
- **The #1 rule: never play a card on colour information alone.** This is the mistake that cost me a fuse in one episode and dragged my score down. If I don't know the rank, I don't play. I discard instead and wait for a rank clue.