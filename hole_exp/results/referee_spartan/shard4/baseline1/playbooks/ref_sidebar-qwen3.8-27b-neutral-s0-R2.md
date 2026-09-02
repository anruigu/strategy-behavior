---
game: ref_sidebar
model: qwen3.8-27b
condition: neutral
seed: 0
round: 2
chars: 2074
---
# Playbook

**On the private line, ask player 1 directly for their card number.** A short question like "What's your card?" gets a truthful answer every time. Don't waste the message on anything else.

**When the bet to me is 0, I call. Always, no exceptions.** Folding when the bet is 0 saves me zero chips — my ante is already in the pot either way. Calling is strictly better than folding by P(win) × pot, which is always positive. This holds even if player 1 reveals a 14 and I hold a 2. There is no card combination where folding at a zero bet is correct.

**When I hold a 14, I raise.** No one beats it. Raising builds the pot to 12 (if both call) and my net gain is +8. This is the single highest-EV action in the game.

**When I hold a 13 and player 1 has not revealed a 14, I raise.** Only a 14 beats me, and player 1 doesn't have one. The chance player 2 holds a 14 is roughly 1/11. Expected value of raising (both call) is about +6.9 chips. This is where the big profits come from — in my best episode I raised with 13 three times and finished at +13.

**When I hold 12 or lower, I call (at a zero bet) and do not raise.** The EV of raising drops below ~+1.5 by the time I get to 11, and goes negative around 6. The free-call at zero already captures most of the value: if player 1 or player 2 raises after me, I ride along for just my 1-chip ante and can win a large pot. Raising myself commits 3 extra chips for marginal gain.

**Do not fold at any point when the bet to me is 0, regardless of what player 1 reveals.** I previously had a "fold if player 1 shows a 14" rule. It was wrong. With a 3 and player 1 holding a 14, my win chance is 1/11 (player 2 must hold a 2), and calling still edges out folding by about 0.27 chips. The rule adds complexity for no gain.

**Track player 2's revealed cards from the hand history.** After each hand the table shows all three cards. Over 8 hands I will see player 2's card 7 times. If player 2 has already shown a 14 in a previous hand, that card is gone from the deck and my 13 becomes as safe as a 14 — raise freely.