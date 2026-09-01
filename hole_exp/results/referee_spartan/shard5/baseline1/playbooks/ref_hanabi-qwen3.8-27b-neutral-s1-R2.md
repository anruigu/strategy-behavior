---
game: ref_hanabi
model: qwen3.8-27b
condition: neutral
seed: 1
round: 2
chars: 5046
---
# Playbook

**Opening (stacks at 0):**
- When all stacks are at 0, I look for a clue that isolates a single 1 in someone's hand (a colour they hold exactly one of, or rank 1 if they hold only one 1). I give that clue so they can play it next turn.
- I never play my own card on turn 1 since I have zero information about my hand.

**Clue selection:**
- When I give a clue, I prefer the one that touches the fewest cards in the target's hand. A clue touching 1 card is ideal; 2 is acceptable; 3+ is a last resort.
- Before cluing, I check: is the card I'm pointing at actually playable right now (matches the current stack top + 1)? If not, I look for a clue that points at something playable, or I save the token.
- I never give a clue for a colour or rank that the target already has full information about from previous clues.

**Dead card priority (CRITICAL):**
- If I have a dead card in hand (rank ≤ current stack for its colour) AND I have at least 1 token, I MUST discard the dead card first before spending any token. This recovers a token, giving me one more to work with.
- This rule overrides the urge to "use my token now." Discarding a dead card is free information (it tells partners the card is dead) and free token recovery. There is never a reason to spend a token while a dead card sits in my hand.
- Exception: if discarding the dead card would leave me with no token and no productive clue to give, and the dead card is the only thing I can discard, then I discard it (obviously). But I never spend a token while a dead card is available to discard.

**Playing my own cards:**
- I play a card only when I can confirm with certainty (from my accumulated clues) that it matches the next needed rank on its colour's stack.
- **Repeated partner clues = strong signal.** If 2+ different players have clued me the same colour on a slot, and the current stack for that colour is at rank R, and my card is the only rank of that colour that is both > R (not dead) and not already played, I play it with high confidence. This is especially safe with 2+ fuses remaining.
- When I have a partial deduction (e.g., "this is either G2 or G3" and I need G2), I do NOT gamble unless I have 2+ fuses remaining AND no other productive move exists. In practice, I almost always have a better option (clue someone else, or discard a dead card).
- When I have a card whose rank is already on or past the stack (e.g., I hold R1 and R stack is at 1+), I discard it immediately to regain a token. This is always safe.

**Discarding:**
- I discard a card when: (a) it is dead (rank ≤ current stack for its colour), or (b) it is a card I've been told is "safe to discard" by the clue protocol (a card that was clued to me but is not the playable one in a multi-card clue).
- I never discard a card I might need later unless it's truly dead.

**Clue token management:**
- I track the token count. When I have 0 tokens, my only options are play (if certain) or discard (to get a token back). I prioritise discarding dead cards to recover tokens.
- When I have 1 token and a dead card in hand, I discard the dead card (gaining a token, now 2) and then use one token for a clue. I do NOT spend my single token on a clue while a dead card is available.
- When I have 1 token and NO dead card in hand, I spend it only on a clue that will directly enable a play on the very next turn. I don't "save" it.
- When I have 2+ tokens, I can afford to give a "setup" clue (pointing at a card that will be playable in 1-2 turns, not immediately).

**Late game (last 5 turns, low fuses):**
- I stop gambling on my own plays. If I'm not 100% certain, I clue someone else or discard.
- I focus on getting the opponents to play their confirmed cards. I look at their hands and give the clue that lets them play something they haven't been clued yet.
- If I have a dead card and 0 tokens, I discard it to get a token, then use that token to set up a final play for someone else.
- If I have a dead card and 1 token, I discard the dead card (now 2 tokens), then use one token for a productive clue.

**Tracking:**
- I maintain a mental log of every clue given to me and what it narrows each slot to. When a new clue arrives, I intersect it with all previous clues to update my knowledge.
- I track what each opponent has been clued and what they've played, so I don't give redundant clues and so I can predict their next move.
- I track which cards are "in play" (on the stack) so I never try to play or clue for a card that's already been played.

**What I must not do:**
- I must not play a card on a 50/50 guess when I have fuses to spare and other productive moves available.
- I must not give a clue that touches 3+ cards when a more precise alternative exists.
- I must not ignore dead cards in my hand — they are free token recovery.
- I must not assume an opponent will play the "obvious" card from a multi-card clue without confirming which one is actually playable.
- I must not spend a token on a clue while a dead card is in my hand that I could discard instead.