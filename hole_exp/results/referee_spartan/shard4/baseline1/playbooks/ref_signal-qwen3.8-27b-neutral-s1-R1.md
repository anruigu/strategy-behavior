---
game: ref_signal
model: qwen3.8-27b
condition: neutral
seed: 1
round: 1
chars: 2935
---
# Playbook

**On my first turn:** Scan the partner's hand for cards that can be played immediately (a 1 when the relevant pile is at 0). Give a clue that helps the partner identify one specific playable card. If multiple 1s exist in their hand, prefer a colour clue to isolate one; if only one 1 exists, a number clue suffices.

**Before every clue, check for redundancy.** Review all clues the partner has already received. If the clue I'm about to give doesn't narrow their knowledge to a new specific card, don't give it. A "1" clue to a partner who already knows their only 1 is in slot 2 is worthless. I wasted tokens on redundant clues in multiple episodes and it cost me.

**To make the partner play a card, pin it down to a single slot.** The partner needs to know both the colour and the number of the card they should play. If they have B1 and B2, a "1" clue tells them it's B1. If they have R1 and B1, a "B" clue tells them it's B1. Give whichever clue is missing to isolate exactly one playable card.

**Only play my own card when I can identify it with high confidence.** This means the clues I've received narrow my hand to one specific card (e.g., I've been told "R" and "1" and I can deduce only one slot holds an R1). If I can't be sure, I discard. I lost lives in two episodes by playing blindly when I had partial information.

**When I have 0 clue tokens and can't identify my cards, always discard.** Discarding regains a token and costs nothing. Playing risks a life. This is strictly better than guessing.

**Prioritize clues that enable the partner's next action to be a play.** A "2" clue when the partner holds an R2 and the R pile is at 1 is high-value. A "1" clue when the partner already knows their 1s is low-value. Always ask: "After this clue, will the partner be able to play a card on their next turn?"

**If the partner keeps discarding instead of playing a card I've identified, pivot.** Look for a different playable card in their hand and help them identify that one. Don't keep re-cluing the same card they're ignoring.

**Track my own hand through accumulated clues.** Every clue I receive tells me I hold at least one card matching that colour or number. Over the game, this builds a picture. If I've been told "R", "1", and "B", I know I have at least an R-something, a 1-something, and a B-something. Use elimination: if I discard a card and later get clued a property it must have had, that property belongs to one of my remaining cards.

**In the endgame (last 3–4 turns), shift to maximum partner scoring.** If I can't confidently play my own cards, spend all remaining clue tokens on helping the partner play as many cards as possible, one clue per card if needed.

**Discard the card least likely to be useful.** When I must discard without knowing my hand, prefer discarding a slot that I have no clues pointing to, or a card I suspect is a high number (less flexible for future plays).