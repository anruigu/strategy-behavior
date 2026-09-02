---
game: ref_hanabi
model: qwen3.8-27b
condition: neutral
seed: 2
round: 1
chars: 3334
---
# Playbook

**When it's my turn and I have a card I can confirm is playable (I know its colour and rank, and it matches the next needed on that stack), I play it immediately.** Do not hold a confirmed-playable card for later; the stack won't advance itself.

**Before playing any card, verify the stack top.** If the green stack is at 2, the next card is G3 — not G2. Identifying a card's identity is not the same as confirming it is playable. Check: does the rank equal (stack top + 1)? If not, do not play it.

**On turn 1, I clue a teammate for a 1 that is the only card of its colour in their hand** (or the only card matching a specific rank). This isolates exactly one card and guarantees a safe play next turn. Prefer colour clues that touch exactly one slot over rank clues that might touch multiple slots, unless the rank clue is the one that isolates.

**When I have partial information about my own hand (e.g., I know the colour but not the rank, or vice versa), I do not play that card.** Instead I clue a teammate on a card I can see is playable, or I discard a card I've identified as unplayable.

**When choosing which card to clue a teammate about, I prefer the clue that isolates the fewest slots.** A rank clue that touches one slot is better than a colour clue that touches three, even if both identify the target card. This preserves the other slots' ambiguity for future use and avoids accidentally "marking" cards that aren't ready yet.

**When I must discard, I discard the card least likely to be the next needed on any stack.** High ranks (4s and 5s) on stacks that are already past that rank are safe to discard. If I have multiple copies of the same colour, discard the one with the highest rank. Never discard a 1 unless that colour's stack is already complete.

**When clue tokens are low (≤2) and I have no confirmed-playable card, I look for a gamble play.** If I have a card where I know the colour and the rank is one of only two or three possibilities, and one of those possibilities is the next needed on the stack, I take the play. The expected value of a 1-in-3 shot at a point outweighs the cost of a fuse in most endgame positions.

**I track every clue I've received and every card I've seen played or discarded, and I use that to narrow down my own hand.** If I was clued "green" on slots 1, 3, 5 and "rank 2" on slot 2, then slot 2 is G2 and slots 1, 3, 5 are green but not rank 2. I use this elimination to identify cards with certainty.

**I do not give a clue that merely confirms what a teammate already knows.** If a teammate just played a card, I don't clue them about the colour of their remaining cards unless it reveals new information.

**When two or more stacks are at 0, I prioritise getting 1s played on as many colours as possible** by cluing different teammates for different 1s. This maximises the number of stacks that can progress in parallel.

**When a teammate makes a misplay, I do not panic or change my overall strategy.** I simply avoid cluing them about cards that might be ambiguous, and I focus on advancing stacks where I have clear information.

**I never play a card based on a single clue that could match multiple cards in my hand.** If "rank 1" touches slots 3 and 4, I don't know which one to play. I need a second clue (a colour) to disambiguate, or I wait.