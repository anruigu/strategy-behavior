---
game: ref_hanabi
model: qwen
condition: neutral
seed: 2
round: 2
chars: 4960
---
# Playbook

**On my turn, first check: can I play a card?**
- I can play only if I know both the colour and rank of a card in my hand, and that card equals (current stack for that colour) + 1.
- If yes, play it. Do not overthink.

**If I cannot play, give a clue that produces an immediate play next turn.**
- Before giving a colour clue to player P, verify that P holds a card of that colour whose rank equals (stack for that colour) + 1. If no such card exists, do NOT give that colour clue — it wastes a token and creates ambiguity.
- Before giving a rank clue to player P, verify that P holds a card of that rank that is playable (i.e., its colour's stack + 1 equals that rank). If multiple cards of that rank are playable, prefer the clue anyway (they get options). If none are playable, do not give it.
- Prefer clues that touch exactly one card in the target's hand. A clue touching two or more cards is acceptable only if all touched cards are currently playable (so the target has no ambiguity about which to play).
- If two players both have a playable card I can clue, prefer the one whose colour is furthest behind (lowest stack), to keep all colours advancing.

**If I cannot safely clue, discard.**
- Discard the card that is least useful: a bomb (rank ≥ current stack + 1 for its colour, meaning it can never be played as-is), a 5 of a colour already past its 4, or a card with zero clues attached to it.
- When I have multiple cards of the same colour with unknown ranks, discard the duplicates to reduce redundancy and free slots for potentially useful unknowns.
- Discarding gives me a clue token and a fresh slot. If I'm at 5 cards and all are unknown, discard the one I least need.

**Managing my own hand information.**
- When I receive a clue, note exactly which slots it touches. Track this cumulatively: a slot tagged "green" from one clue and "rank 2" from another is a G2.
- If a slot is tagged with a colour but I don't know its rank, I cannot play it unless the stack for that colour is at 0 (then it must be a 1) — otherwise I need a rank clue too.
- If a slot is tagged with a rank but I don't know its colour, I cannot play it unless the rank is 1 AND exactly one colour's stack is at 0 (then I can deduce). Otherwise I need a colour clue.
- When I have a partially-known card that is close to playable, I should signal for the missing piece by discarding a different card (gaining a token) so a teammate can clue me the missing dimension on their next turn.

**Clue token economy.**
- Never spend a token on a clue that won't produce a play within the next 1–2 turns.
- When tokens are at 1 or below, only spend on a clue that guarantees a play next turn. Otherwise discard.
- When tokens are 5 or above, I can afford to give "setup" clues (marking a card that will be playable in a few turns) to prime a future play.
- **Late-game (turns 20+ with score ≤ 5):** If I have a token and no teammate has an immediately playable card, do NOT spend it on a speculative clue. Discard instead. A wasted clue in the endgame is unrecoverable; a discarded card at least gives me a fresh draw and a token back.

**What I must not do.**
- Do not give a colour clue when the target's only cards of that colour are all unplayable (bombs or too high). This is what cost me in one episode — I clued "Red" when the target had R1 and R4 but the stack was already at 1, so R1 would bomb and R4 was useless. The clue was pure waste.
- Do not play a card based on partial information unless I am certain. A "rank 1" clue with unknown colour is NOT enough to play unless exactly one colour's stack is at 0.
- Do not discard a card that is the next-needed rank for a colour that is behind, unless I have no other option.
- Do not clue a teammate on a colour/rank that touches a card they already know is playable from a previous clue. Repeating a clue wastes a token. Check recent play history before cluing.

**Opening turns (no info on my hand).**
- My first move should always be a clue to a teammate who has a 1 (or the next needed card). Look at both hands, find the most immediately playable card, and clue its owner on the dimension that isolates it best (colour if unique in their hand, rank if unique).
- Do not discard on turn 1 unless absolutely forced; I want to keep all five cards in case a clue comes to me.

**Recognising when the game is stalling.**
- If after 15+ turns the score is still 0 or 1, the team is failing to convert clues into plays. In this case, prioritise clues that produce plays over clues that build information on my own hand. My own hand will never be fully resolved if no one is playing cards, so focus on unblocking teammates.
- If I notice I'm repeatedly discarding unknowns without gaining information, it means no one is cluing me. In that case, my discards should target cards that are most likely bombs (high ranks of colours already advanced), so the fresh draws I get have a better chance of being useful.