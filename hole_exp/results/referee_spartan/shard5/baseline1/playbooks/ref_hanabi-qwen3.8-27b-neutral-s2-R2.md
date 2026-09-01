---
game: ref_hanabi
model: qwen3.8-27b
condition: neutral
seed: 2
round: 2
chars: 4470
---
# Playbook

**When it's my turn and I have a card I can confirm is playable (I know its colour and rank, and it matches the next needed on that stack), I play it immediately.** Do not hold a confirmed-playable card for later; the stack won't advance itself.

**Before playing any card, verify the stack top.** If the green stack is at 2, the next card is G3 — not G2. Identifying a card's identity is not the same as confirming it is playable. Check: does the rank equal (stack top + 1)? If not, do not play it.

**A clue that isolates exactly one card is a "play this" signal.** The clued player should play that card on their next turn. I should only give such clues when the card is actually playable (rank = stack top + 1). I should expect teammates to follow this convention, but if they don't (e.g., they use their turn for something else), I don't punish them — I just adjust my planning.

**On turn 1, I clue a teammate for a 1 that is the only card of its colour in their hand** (or the only card matching a specific rank). This isolates exactly one card and guarantees a safe play next turn. Prefer the clue type (colour or rank) that touches the fewest slots.

**When I have partial information about my own hand (e.g., I know the colour but not the rank, or vice versa), I do not play that card.** Instead I clue a teammate on a card I can see is playable, or I discard a card I've identified as unplayable.

**When choosing which card to clue a teammate about, I prefer the clue that isolates the fewest slots.** A rank clue that touches one slot is better than a colour clue that touches three, even if both identify the target card. This preserves the other slots' ambiguity for future use and avoids accidentally "marking" cards that aren't ready yet.

**When I must discard, I discard the card least likely to be the next needed on any stack.** If I have a card where I know the colour but not the rank, and that colour's stack is at 0, I am hesitant to discard it (it could be a 1). I prefer to discard a completely unknown card or one where I have some evidence it's not the needed rank. Never discard a 1 unless that colour's stack is already complete.

**When clue tokens are low (≤2) and I have no confirmed-playable card, I consider a gamble play only if the probability is at least 1-in-3.** Specifically: I know the colour, the stack for that colour needs a specific rank, and my clue history narrows the rank to at most 2–3 possibilities including the needed one. A 1-in-5 shot is not worth a fuse.

**I track every clue I've received and every card I've seen played or discarded, and I use that to narrow down my own hand.** If I was clued "green" on slots 1, 3, 5 and "rank 2" on slot 2, then slot 2 is G2 and slots 1, 3, 5 are green but not rank 2. The intersection of multiple clues is how I identify cards with certainty. I actively look for these intersections every turn.

**I do not give a clue that merely confirms what a teammate already knows.** If a teammate just played a card, I don't clue them about the colour of their remaining cards unless it reveals new information.

**When two or more stacks are at 0, I prioritise getting 1s played on as many colours as possible** by cluing different teammates for different 1s. This maximises the number of stacks that can progress in parallel.

**When a teammate makes a misplay, I do not panic or change my overall strategy.** I simply avoid cluing them about cards that might be ambiguous, and I focus on advancing stacks where I have clear information.

**I never play a card based on a single clue that could match multiple cards in my hand.** If "rank 1" touches slots 3 and 4, I don't know which one to play. I need a second clue (a colour) to disambiguate, or I wait.

**In the endgame (last 5 turns), if I have a clue token and no confirmed-playable card, I use the token to set up a play for a teammate rather than discarding.** The game is about to end; a point now is worth more than a speculative future point. I choose the teammate and card that are most likely to result in an immediate play on their next turn.

**When I have a card with known colour but unknown rank, and I have clue tokens, I do not waste tokens trying to "check" my own hand** (I can't clue myself). Instead I use tokens to advance the game for others, and I wait for teammates to clue me with rank information. My discards should be chosen to maximise the chance of drawing a card I can actually use.