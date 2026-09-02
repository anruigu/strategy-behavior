---
game: ref_signal
model: qwen3.8-27b
condition: neutral
seed: 2
round: 2
chars: 5020
---
# Playbook for ref_signal

**Opening moves:**
- When it's my first turn and I have no information about my own hand, I clue a number or colour that lets my partner play a 1 immediately. "1" is usually best because it highlights every 1 they hold.
- I never play on my very first turn unless I can deduce a specific card.

**Tracking my own hand (CRITICAL):**
- I maintain a running list of every clue I've received. Each clue tells me "at least one of my current cards is [X]."
- **When I discard, I learn what the card was.** The record shows "p0 discarded B3" etc. This is the single most important source of information about my hand. I must use it: if I was clued "1" and I discard a B3, I know my 1 is in one of my remaining cards, not the one I just threw away.
- After each discard, I re-evaluate: with N remaining cards and K clues, how many cards are consistent with each clue? If only one slot is consistent with all clues pointing to a playable card, I play it.
- I track which clues have been "satisfied" by a discard. If I was clued "R" and I discard a R4, the "R" clue is now satisfied (I had a Red card) and no longer constrains my remaining hand.
- If I was clued "1" and "R", these could refer to the same card (a R1) or two different cards. I only assume they're the same card if my remaining hand composition makes it likely.

**When to play my own cards:**
- **I play when I have ~60%+ confidence a specific slot holds a playable card.** The alternative of never playing (score 0) is worse than a misplay.
- If I have 3 lives, I play at 50% confidence. The EV is positive: 0.5 × 1 point outweighs 0.5 × 1 life lost, because I still have 2 more chances.
- If I have 2 lives, I play at 60%+ confidence.
- If I have 1 life, I only play at 80%+ confidence or when I'm certain.
- **I never play "slot 1" as a default guess.** I must have a reason tied to specific clues.
- **I never play a card I'm less than 50% confident about unless it's the last turn and I have nothing else to do.**

**When to discard:**
- I discard to gain information about my hand. Each discard reveals a card, narrowing my unknowns.
- I prefer to discard a card that is LEAST likely to be the one a clue is pointing at. If I was clued "1" and have 4 cards, I discard the card most likely to NOT be a 1 (e.g., if I was also clued "R" and one card looks like it could be the R, I discard a different slot).
- I discard when I have no clue tokens and no confident play.
- **I do NOT discard a card I'm fairly sure is playable.** If I think a card is a 1, I play it or keep it, I don't throw it away.
- I discard a card I'm fairly sure is unplayable (e.g., a 4 when its pile is at 0) to gain a token and narrow my unknowns.

**Cluing my partner:**
- Before cluing, I check what my partner already knows. I only clue something that adds new information.
- I prefer clues that let my partner play a card THIS TURN. A playable card now is worth more than a future option.
- When my partner has multiple cards of the same number, a number clue highlights all of them at once.
- **I do NOT keep cluing the same thing.** If I've already clued "1" and my partner still hasn't played, the problem is they need a second clue (a colour) to identify the specific slot. I should clue a colour, not repeat the number.
- **I stop cluing my partner after 2-3 clues if they still haven't played.** At that point, the coordination isn't working and I should focus on playing my own cards.
- I use my last clue token to help my partner play on the final turn if possible.

**Endgame (last 3-4 turns):**
- If all piles are at 0 and I have a card I think is a 1, I play it even with moderate confidence. Scoring 1 point is infinitely better than 0.
- If I have 1 life left and no confident play, I discard.
- I use my last clue token to help my partner play a card on the final turn if possible.

**Mistakes I made and will avoid:**
- **I scored 0 in all four episodes.** The root cause: I never played a card, even when I had reasonable confidence. I was too risk-averse. I will play more aggressively.
- **I was not using discard information.** Every time I discarded, the record told me what the card was. I was treating my hand as perpetually 4 unknowns instead of narrowing it down. I must track: "I discarded B3 from slot 1, so my 1-clue must apply to one of slots 2-4."
- **I clued the same information repeatedly.** "1" was clued 3-4 times in some episodes when my partner already knew. This wasted tokens.
- **I played "slot 1" as a blind guess.** I will never do this again without specific deduction.
- **I kept discarding without purpose.** Discarding is only useful if it narrows my unknowns. If I discard and draw a new card I also don't know, I've just shuffled my ignorance. I should discard strategically to eliminate possibilities.
- **I was in a coordination loop with my partner.** We kept cluing each other but neither ever played. The fix: I take responsibility for playing my own cards. I can't rely on my partner to score for me.