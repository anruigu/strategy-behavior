---
game: ref_sidebar
model: qwen3.8-27b
condition: neutral
seed: 1
round: 2
chars: 1762
---
# Playbook

**Private line: extract player 1's card, never reveal my own.** My single most valuable action each hand is learning player 1's card. I ask directly ("what's your card?") or fall back to "are you above or below 9?" I never state my own card in a message — it gives player 1 information they could use to adjust their betting against me, and it costs me nothing to withhold.

**When the current bet to me is 0, I never fold.** Folding and calling-then-losing both cost exactly my 1-chip ante. Calling preserves the chance to win the pot at no additional risk. The only exception is a card of 2, where winning is nearly impossible and folding is merely cleaner.

**Raising (committing 2 extra chips) is justified when:**
- My card is 12 or higher. The top-3 frequency makes the inflated pot +EV regardless of what I know about opponents.
- My card is 10 or 11 AND I know player 1 is below 9. I have a confirmed edge over one opponent, which pushes my win probability high enough that the extra 2 chips are +EV.

**Calling for free is the default when:**
- My card is 2–9 and I don't have a confirmed edge strong enough to justify a raise.
- My card is 10–11 and I don't yet know player 1 is below 9.

**Do not raise based on chip deficit.** Being behind on chips does not change the expected value of the current hand. A raise with a marginal card to "catch up" is a tilt play, not a strategy. The only reason to raise is the card and the information.

**Information before commitment.** If I have a 10 or 11 and player 1 hasn't yet revealed their card, I use the message to probe before betting. The one message I get is best spent confirming whether player 1 is below 9, since that's the threshold that turns a borderline call into a justified raise.