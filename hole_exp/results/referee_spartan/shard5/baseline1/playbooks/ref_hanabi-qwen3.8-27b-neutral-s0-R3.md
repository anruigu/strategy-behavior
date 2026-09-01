---
game: ref_hanabi
model: qwen3.8-27b
condition: neutral
seed: 0
round: 3
chars: 3899
---
# Playbook

**Tracking stale clues (CRITICAL).** Every clue applies to the card that was in a slot *at the moment the clue was given*. If I have since played or discarded from that slot, the new card I drew has NO identity from that old clue. Before trusting any clue on my hand, I must verify: has the card in this slot changed since the clue was given? If yes, the clue is void. I treat that slot as fully unknown. This is the single most common source of misplay.

**Opening turn.** Clue a colour that isolates a single rank-1 for one player, so they can play it immediately without ambiguity. If no single colour isolates exactly one 1, clue "1" to the player with the fewest 1s (least ambiguity).

**Cross-reference every valid clue on every slot.** Maintain a running list of what each slot can and cannot be, but only using clues that are still valid (i.e., the card in that slot hasn't changed since the clue was given). If "Green" touched slots 1,3 and "Rank 2" touched slots 2,4, then slot 1 is G-not-2, slot 3 is G-not-2, slot 2 is ?2-not-G, slot 4 is ?2-not-G. A slot with both colour and rank identified (from valid clues) is fully known.

**I never play a card I am not certain is playable.** I need to know both the colour and the rank (from valid clues), and the rank must equal (stack top + 1). If I only know the colour or only the rank, I do not play. Exception: if the stack is at 0 and I know the card is a 1 of some colour (from a valid clue), I play it.

**When I have a confirmed playable card, I play it.** If I have 0 tokens and a confirmed playable card, playing is always better than discarding — it scores a point and I still get a fresh card drawn.

**When I have 0 tokens and no confirmed playable card, I discard.** Discard the most clearly dead card: one whose rank is already on the stack, or one I'm most confident is not useful. Do NOT discard a card with partial information (e.g., "Yellow" but unknown rank) if the rank could still be playable or setup-worthy.

**Every clue I give should advance a stack I need, or open a new colour.** Before cluing, I check: do I hold a card that benefits from this stack advancing? If yes, priority. If no, prefer the clue that opens a new colour (stack at 0) over one that merely advances an existing stack. If two cards are equally playable, opening a new colour is more impactful because it creates a second parallel track.

**Setup chains.** If I know I have a B2 and Blue is at 1, my top priority is getting B1 played. I clue whoever holds B1. I do not waste a turn on something else when a setup chain is available.

**Discarding is a signal.** When I discard, I discard the card most clearly dead or least useful. This narrows what others think I hold. I never discard a card I might need to play within the next few turns.

**With 1 fuse remaining, I only play cards I am 100% certain about.** If uncertain, discard to buy a token and wait.

**I do not re-clue a player about a colour or rank they already know.** If p1 was already told "White" and still holds white cards, cluing "White" again wastes a token. Find new information.

**Late game (turns 20+).** I am more conservative. I prefer playing confirmed cards over cluing for setup. With 2 turns left and a token, I should clue for a card that plays THIS turn or next turn, not one that sets up a play for a turn that may not come. I focus on the single most impactful clue: the one that scores immediately.

**Track the stacks.** Before every decision, I note which colours are at 0 (unopened). Opening a new colour is generally more valuable than advancing an already-opened one, because it creates parallel scoring potential.

**After I play or discard, I immediately reset my knowledge of that slot to "unknown."** I do not carry forward any previous clue information to the replacement card. The replacement card is a blank slate until someone clues it.