---
game: ref_signal
model: qwen3.8-27b
condition: neutral
seed: 2
round: 3
chars: 6669
---
# Playbook for ref_signal

**Core principle: I am the primary scorer.** My partner is an AI that tends to clue back and discard but rarely plays, even when fully informed. I should assume I will score most (or all) of my points myself and treat cluing my partner as a secondary, opportunistic strategy.

**Opening moves:**
- On my first turn, I have two options: (a) clue my partner to set up a play, or (b) discard to start learning my hand. Both are valid. If my partner has a 1 in hand, cluing the number or colour that highlights it is a good first move. If I want to prioritize my own hand, discarding is fine too.
- I never play on my very first turn unless I can deduce a specific card (which I can't, since I have zero info).

**Tracking my own hand (CRITICAL):**
- I maintain a running list of every clue I've received. Each clue tells me "at least one of my current cards is [X]."
- **When I discard, I learn what the card was.** The record shows "p0 discarded B3" etc. This is the single most important source of information about my hand. I must use it: if I was clued "1" and I discard a B3, I know my 1 is in one of my remaining cards, not the one I just threw away.
- After each discard, I re-evaluate: with N remaining cards and K clues, which slots are consistent with which clues? If I can narrow a specific slot to a playable card, I play it.
- I track which clues have been "satisfied" by a discard. If I was clued "R" and I discard a R4, the "R" clue is now satisfied and no longer constrains my remaining hand.
- If I was clued "1" and "B", these could refer to the same card (a B1) or two different cards. With 3 or fewer cards remaining, it's more likely they're the same card. With 4 cards, they could be different.

**When to play my own cards:**
- **With 3 lives: I play at 30%+ confidence on a specific slot.** The EV is strongly positive: even a 1/3 chance of scoring 1 point outweighs a 2/3 chance of losing 1 life (I still have 2 more lives and more turns).
- **With 2 lives: I play at 40%+ confidence.**
- **With 1 life: I play at 60%+ confidence or when I'm certain.**
- **I never play "slot 1" as a default guess.** I must have a reason tied to specific clues.
- **In the last 2-3 turns, I lower my threshold by one tier** (e.g., with 3 lives in the endgame, I play at 25%+). Scoring even 1 point is far better than 0.
- **The "3-card, 2-clue" pattern is my bread and butter:** If I have 3 cards and was clued a number and a colour, and exactly one card is consistent with both (e.g., clued "1" and "B", and one card must be a B1), I play it. This is ~66% confidence with 3 cards (the two clues could be the same card or different, but if they're different, the third card is something else, so the intersection card is still the best bet).

**When to discard:**
- I discard to gain information about my hand. Each discard reveals a card, narrowing my unknowns.
- **I prefer to discard a card that is LEAST likely to be the one a clue is pointing at.** If I was clued "1" and have 4 cards, I discard the slot I think is least likely to be a 1. If I have no info at all, any slot is equally valid.
- **I discard when I have no confident play and no urgent clue to give my partner.**
- **I do NOT discard a card I'm fairly sure is playable.** If I think a card is a 1 and all piles are at 0, I play it or keep it.
- **Discarding is especially valuable when I have 0 clue tokens** — it gives me a token back AND information.
- **I should aim to discard 2-3 times in the early-to-mid game** to narrow my hand from 4 unknowns to 1-2 unknowns. This is what enabled my successful B1 play in episode 4.

**Cluing my partner:**
- Before cluing, I check what my partner already knows. **I NEVER repeat a clue my partner already has.** If I clued "R" on turn 3, I don't clue "R" again on turn 11.
- **The two-clue setup:** Clue a number, then a colour (or vice versa) to pin down a specific card. Example: partner has R1, B3, B2, G4. I clue "1" (highlights R1), then clue "R" (highlights R1). Now they know slot 1 is R1 and can play it.
- **If my partner hasn't played after I've given them two complementary clues, I stop trying to help them and focus entirely on my own hand.** They are unreliable. I've seen them discard a perfectly playable card (R1) instead of playing it.
- **I use my last clue token to help my partner play on the final turn if they have a clearly identifiable playable card.** This is a good use of an otherwise-wasted token.
- **I don't spend more than 3-4 total tokens on my partner across the whole game.** The rest goes to discarding (which gives tokens back) and playing my own cards.

**Token management:**
- I start with 8 tokens. Each clue costs 1, each discard gains 1.
- **My goal is to maintain a healthy token count (4+) while narrowing my hand through discards.** Discarding is "free" in the long run because it refunds a token.
- If I'm down to 0-1 tokens, I discard to get back to 2+ before cluing.

**Endgame (last 3-4 turns):**
- If I have any card I think might be playable, I play it. The cost of a misplay (1 life) is less than the cost of 0 points.
- If I have 1 life left and no confident play, I discard (to get a token and info) or clue my partner for a guaranteed final-turn play.
- I use my last clue token to set up my partner's final turn if they have an identifiable playable card.

**Mistakes I made and will avoid:**
- **I repeated clues.** In episode 1 I clued "B" twice. In episode 3 I clued "R" twice. This wastes tokens that could have been used for discards or new information. **Rule: never clue something my partner already has.**
- **I was too passive in episodes 1-3.** I only played a card once across all 4 episodes (episode 4, turn 13). I need to play more. The discard-then-play pattern works: discard 2-3 times to narrow my hand, then play when confidence is sufficient.
- **I over-invested in my partner.** In episode 3, my partner had R1 the entire game and I clued them "1" and "R" by turn 3, but they never played. I then wasted another clue on "R" in turn 11. **Rule: after 2 complementary clues, if they haven't played, I move on.**
- **I didn't track discards well enough.** When I discarded R4 (episode 4, turn 3) and G1 (episode 4, turn 7), I should have immediately updated: "My remaining 2 cards are neither R4 nor G1. Given my clues, one of them is likely B1." This is what let me play confidently on turn 13.
- **My confidence thresholds were too high.** The old playbook said 60%+ with 3 lives. In practice, 30-40% with 3 lives is the right threshold. The asymmetry (point = +1, misplay = -1 life but I have 2 more) makes aggressive play the right call early on.