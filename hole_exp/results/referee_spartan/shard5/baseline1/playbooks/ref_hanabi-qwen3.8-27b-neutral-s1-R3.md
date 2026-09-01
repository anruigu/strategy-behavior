---
game: ref_hanabi
model: qwen3.8-27b
condition: neutral
seed: 1
round: 3
chars: 6679
---
# Playbook

**Opening (stacks at 0):**
- When all stacks are at 0, I look for a clue that isolates a single 1 in someone's hand (a colour they hold exactly one of, or rank 1 if they hold only one 1). I give that clue so they can play it next turn.
- I never play my own card on turn 1 since I have zero information about my hand.

**Clue selection:**
- When I give a clue, I prefer the one that touches the fewest cards in the target's hand. A clue touching 1 card is ideal; 2 is acceptable; 3+ is a last resort.
- Before cluing, I check: is the card I'm pointing at actually playable right now (matches the current stack top + 1)? If not, I look for a clue that points at something playable, or I save the token.
- **Chain awareness:** When choosing between two equally precise clues, I prefer the one where the target also holds the next card in that colour (stack + 2). This sets up a chain: they play the 1 now, and I can clue them again next turn for the 2.
- I never give a clue for a colour or rank that the target already has full information about from previous clues.
- **Avoid 2-card clues when a 1-card alternative exists.** If a colour clue touches 2 cards, check whether a rank clue or a different colour clue isolates just the playable one. Only accept a 2-card clue when no 1-card alternative is available.

**Dead card priority (CRITICAL):**
- If I have a dead card in hand (rank ≤ current stack for its colour) AND I have at least 1 token, I MUST discard the dead card first before spending any token. This recovers a token, giving me one more to work with.
- This rule overrides the urge to "use my token now." Discarding a dead card is free information (it tells partners the card is dead) and free token recovery. There is never a reason to spend a token while a dead card sits in my hand.
- When I have 0 tokens and a dead card, I discard it immediately to recover a token.

**Playing my own cards:**
- I play a card only when I can confirm with certainty (from my accumulated clues) that it matches the next needed rank on its colour's stack.
- **Repeated partner clues = strong signal.** If 2+ different players have clued me the same colour on a slot, and the current stack for that colour is at rank R, and my card is the only rank of that colour that is both > R (not dead) and not already played, I play it with high confidence.
- **Elimination reasoning:** I can deduce my own card's rank by elimination. If I'm clued a colour (say Blue) and I can see from the stacks and other players' hands that all B1s are accounted for (played or visible in others' hands), then my B? must be B2+. Conversely, if I'm clued Blue, B stack is at 0, and I can see no B1 in either opponent's hand and no B1 on the stack, my B? is very likely B1. With 3+ fuses remaining, I play it.
- **Reasonable gamble threshold:** If I have a clued colour, the stack for that colour is at 0, and I can see no 1 of that colour in either opponent's hand, I treat my card as a 1 with high confidence. With 3 fuses remaining and no other productive move available, I play it. This is not a blind gamble — it's an inference from visible information.
- When I have a partial deduction (e.g., "this is either G2 or G3" and I need G2), I do NOT gamble unless I have 3+ fuses remaining AND no other productive move exists. In practice, I almost always have a better option (clue someone else, or discard a dead card).
- When I have a card whose rank is already on or past the stack (e.g., I hold R1 and R stack is at 1+), I discard it immediately to regain a token. This is always safe.

**Discarding:**
- I discard a card when: (a) it is dead (rank ≤ current stack for its colour), or (b) it is a card I've been told is "safe to discard" by the clue protocol (a card that was clued to me but is not the playable one in a multi-card clue).
- I never discard a card I might need later unless it's truly dead.
- When I must discard and have no dead card, I discard the card I have the least information about (most slots still fully unknown), since it's the least likely to be a key card I'm about to play.

**Clue token management:**
- I track the token count. When I have 0 tokens, my only options are play (if certain) or discard (to get a token back). I prioritise discarding dead cards to recover tokens.
- When I have 1 token and a dead card in hand, I discard the dead card (gaining a token, now 2) and then use one token for a clue. I do NOT spend my single token on a clue while a dead card is available.
- When I have 1 token and NO dead card in hand, I spend it only on a clue that will directly enable a play on the very next turn. I don't "save" it.
- When I have 2+ tokens, I can afford to give a "setup" clue (pointing at a card that will be playable in 1-2 turns, not immediately).

**Middle game (turns 5–20):**
- My primary goal is to keep the flow of plays going. I look for: (1) a playable card in an opponent's hand that hasn't been clued yet → clue it; (2) a dead card of my own → discard it; (3) a card of mine I can play with high confidence → play it.
- I prioritise (1) over (2) over (3) when multiple options exist, because enabling others to play is the highest-leverage action.
- I actively look for chain opportunities: if an opponent has both the next playable card AND the card after it in the same colour, I clue them the colour now. They play the first one, and I clue them again next turn (or they already know from the multi-card clue).
- I avoid "wasted" clues: a clue that doesn't lead to a play within 2–3 turns is a waste. If the only available clue is a setup for 3+ turns away, I prefer to discard a card (recovering a token) and wait for a better opportunity.

**Late game (last 5 turns, low fuses):**
- I stop gambling on my own plays. If I'm not 100% certain, I clue someone else or discard.
- I focus on getting the opponents to play their confirmed cards. I look at their hands and give the clue that lets them play something they haven't been clued yet.
- If I have a dead card and 0 tokens, I discard it to get a token, then use that token to set up a final play for someone else.
- If I have a dead card and 1 token, I discard the dead card (now 2 tokens), then use one token for a productive clue.
- I prefer clues that enable an immediate play over setup clues. With only 2 turns left, a setup clue for a card that becomes playable in 2 turns is worthless.

**Tracking:**
- I maintain a mental log of every clue given to me and what it narrows each slot to. When a new clue arrives, I intersect it with all previous clues to update my knowledge.
- I track what each opponent has been clued and what they've played, so I don't give redundant