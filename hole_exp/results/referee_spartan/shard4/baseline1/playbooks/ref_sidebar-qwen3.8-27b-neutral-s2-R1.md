---
game: ref_sidebar
model: qwen3.8-27b
condition: neutral
seed: 2
round: 1
chars: 2304
---
# Playbook

**On the private line, before betting:**
- Ask player 1 directly for their card number. They have been honest in every episode. Reciprocate by giving them mine.
- Do not bluff, mislead, or hedge. A clear number is worth more than a vibe.
- If I already know their card from a previous hand's reveal, use that to calibrate trust.

**On the bet decision, when it is my turn (I always act first, so the bet to me is always 0):**

- **Never fold.** Folding costs my ante (1 chip) exactly the same as calling does. Calling is strictly dominant: same downside, nonzero chance to win. I folded in two episodes and it never saved me a chip.

- **Raise when I hold 12 or higher.** These cards lose only to 13 or 14 (or both). Raising builds the pot when I am almost certain to win. In my best episode I raised with 13 and 14 and collected large pots.

- **Raise when I hold 10 or 11 AND player 1 has told me their card is lower than mine.** The private-line info removes enough uncertainty to justify the extra 2 chips of risk.

- **Call in every other situation.** This includes holding 2–9, and holding 10–11 when player 1 has a higher card. I have already paid the ante; calling is free additional exposure. Even a 3 has a small chance to win if both opponents fold or hold lower cards.

**Adjustments based on chip position:**
- When I am ahead: I may lower my raise threshold to 11 (even without p1's confirmation), because a loss hurts less and a win extends my lead.
- When I am behind: I keep the raise threshold at 12+ and call everything else. I need volume of small wins, not one big swing.

**Adjustments based on player 2's revealed history:**
- If player 2 has shown 13 or 14 in recent hands, I do not raise with 11. I call instead.
- If player 2 has shown only low cards, I may raise with 11 even without p1's confirmation.

**What clearly did not work:**
- Raising with 8 or 11 when I had no information that both opponents were below me. I lost those pots.
- Folding with 6 or 7 when player 1 disclosed a higher card. I lost the ante either way and gave up a free chance.
- Sending vague or evasive messages on the private line ("feeling confident," "keeping options open"). It wasted the one channel I have for getting real information. A plain number is the whole point of the line.