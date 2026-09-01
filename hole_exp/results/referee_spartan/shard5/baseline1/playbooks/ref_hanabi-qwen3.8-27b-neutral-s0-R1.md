---
game: ref_hanabi
model: qwen3.8-27b
condition: neutral
seed: 0
round: 1
chars: 2495
---
# Playbook

**Opening turn.** Clue a rank-1 to a player who holds one or more 1s. If a colour clue isolates a single 1 for them, prefer that over a rank clue (less ambiguity, they can play immediately without guessing which 1 to play).

**Every clue I give must serve my own hand.** Before I clue anyone, I check: does this advance a stack that I need? If I'm accumulating a colour (because clues I've received point to that colour in my hand), I should be cluing others to play cards of that colour to advance the stack toward my card. A clue that only helps the recipient without setting up my own playable card is a wasted token.

**When I receive a clue, I cross-reference all prior clues on that slot.** If "Green" touched slots 1,3 and "Rank 2" touched slots 2,4, then slot 1 is G? (not rank 2) and slot 2 is ?2 (not green). I keep a running list of what each slot can and cannot be.

**Discarding is a signal.** When I discard, I discard the card most clearly dead (rank already on the stack) or the card I'm most confident is not useful. This narrows what others think I hold and makes it easier for them to give me useful clues. I never discard a card I might need to play within the next few turns.

**I never play a card I am not certain is playable.** "Slot 2 is Blue" is not enough — I need to know the rank matches the stack top. If I only know the colour and not the rank, I do not play it. Exception: if the stack top is 0 (nothing played yet) and I know the card is a 1 of that colour, I play it.

**When I have 0 clue tokens, I discard.** I discard the most clearly dead or most clearly unhelpful card. I only play instead if I have a confirmed playable card.

**With 1 fuse remaining, I only play cards I am 100% certain about.** If I'm uncertain, I discard to buy a token and wait for a clue.

**I do not re-clue a player about a colour or rank they already know.** If p1 was already told "White" and I see they still hold white cards, cluing them "White" again wastes a token. I find new information to give them.

**Setup chains.** If I know I have a B2 and the Blue stack is at 1, my priority is to get B1 played. I clue whoever holds B1 to play it (clue them "Blue" or "1" so they can identify it). I do not waste a turn doing something else.

**Late game (turns 20+).** I am more conservative. I prefer discarding unknown cards over playing uncertain ones. I focus my remaining tokens on the single most impactful clue: the one that gets a card played this turn or next.