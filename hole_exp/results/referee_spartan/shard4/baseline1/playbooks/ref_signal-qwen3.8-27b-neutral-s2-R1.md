---
game: ref_signal
model: qwen3.8-27b
condition: neutral
seed: 2
round: 1
chars: 3689
---
# Playbook for ref_signal

**Opening moves:**
- When it's my first turn and I have no information about my own hand, I clue a number or colour that lets my partner play a 1 immediately. "1" is usually best because it highlights every 1 they hold.
- I never play or discard on my very first turn unless I have a specific reason (e.g., I can deduce a card is unplayable).

**Cluing my partner:**
- Before cluing, I check what my partner already knows from previous clues. If they've already been told "1" and "R", cluing "R" again wastes a token. I only clue something that adds new information.
- I prefer clues that let my partner play a card THIS TURN over clues that help them plan for later. A playable card now is worth more than a future option.
- When my partner has multiple cards of the same number (e.g., two 1s), a number clue is more efficient than a colour clue because it highlights both at once.
- When my partner has only one card of a given colour and I need them to play it, a colour clue is fine. When they have several of that colour, a number clue is better (it narrows to the specific rank they need).

**Tracking my own hand:**
- I maintain a running list of every clue I've received. Each clue tells me "at least one of my cards is [X]." I combine all clues to narrow down what each slot could be.
- If I've been clued both a colour and a number (e.g., "G" and "1"), I know I hold a G1, but I don't know which slot. I should try to identify the slot before playing.
- If I discard a card and it turns out to be something I already knew about, that eliminates that slot from consideration for my remaining unknowns.
- I never play a card based on "I've been clued 1 so I'll play slot 1." That's a coin flip. I only play a card when I can identify its slot with reasonable confidence, or when the downside (a misplay) is acceptable given my remaining lives.

**When to play my own cards:**
- I play a card only when I can identify it with high confidence (e.g., I've been clued "G" and "1" and I've eliminated other slots through discards or partner's discards revealing information).
- If I have 3 lives and no clue tokens, playing a card I'm moderately confident about is acceptable — the expected value of scoring outweighs the misplay risk.
- If I have 1 life left, I do NOT play a card I'm not certain about. I discard instead.

**When to discard:**
- I discard when I have no clue tokens, no confident play available, and I want to gain a new card that might be more useful.
- I discard when I have 1 life left and no safe play. This preserves my life.
- I discard a card I'm fairly sure is unplayable (e.g., a 4 when its pile is at 0) to gain a token and a new card.
- I do NOT discard a card that my partner might need me to hold (though in practice I rarely know this).

**Endgame (last 2-3 turns):**
- If all piles are at 0 and I have 1 life left, I discard. The risk of a misplay ending the game is too high.
- If I can identify a playable 1 with confidence, I play it even late — scoring 1 point is better than 0.
- I use my last clue token to help my partner play a card on the final turn if possible.

**Mistakes I made and will avoid:**
- I clued the same information repeatedly (e.g., "1" three or four times when partner already knew). This wasted tokens that could have given new information or been saved for later.
- I played "slot 1" as a blind guess multiple times. This led to misplays (playing R4 when I thought it was a 1). I will never play a slot I haven't identified through deduction.
- I failed to track which specific slots in my hand correspond to which cards. I need to be more disciplined about eliminating possibilities slot by slot.