---
game: ref_sidebar
model: qwen3.8-27b
condition: neutral
seed: 2
round: 2
chars: 2517
---
# Playbook

**On the private line, before betting:**
- Ask player 1 directly for their card number. Reciprocate by giving them mine.
- Do not bluff, mislead, or hedge. A clear number is the whole point of the line.
- Player 1 has been honest in every episode. Trust the number they give.

**On the bet decision (I always act first, so the bet to me is always 0):**

- **Never fold.** Folding and calling both cost exactly my 1-chip ante. Calling is strictly dominant: same downside, nonzero chance to win the pot.

- **Raise when I hold 10 or higher, regardless of what p1 told me.** Without any info, P(win) for a 10 is already ~0.42, well above the 1/3 breakeven for a raise. A 14 always raises.

- **Raise when I hold 7, 8, or 9 AND player 1's card is lower than mine.** Knowing p1 is below me removes one losing card from the equation and pushes P(win) above 1/3. For example, a 9 against a known p1 of 5 gives P(win) ≈ 0.55.

- **Never raise when player 1's card is higher than mine.** I cannot win this hand—p1 already beats me at showdown. Raising would just cost me 3 extra chips for a guaranteed loss.

- **Call in every situation where I don't raise.** This includes holding 6 or below, holding 7–9 when p1 is higher, and holding 10+ when p1 is higher (I still can't beat p1, but calling is free).

**What does NOT matter:**
- **My chip position.** The EV calculation is identical whether I'm at +5 or -20. I do not tighten or loosen my raise threshold based on being ahead or behind.
- **Player 2's recent cards.** Each hand is dealt independently. A 13 p2 showed last hand tells me nothing about their current card. I do not suppress raises based on p2's history.

**Summary table (my card × p1's card → action):**

| My card | p1 < me | p1 > me |
|---------|---------|---------|
| 14 | Raise | Raise (impossible—nothing beats 14) |
| 13 | Raise | Call |
| 12 | Raise | Call |
| 11 | Raise | Call |
| 10 | Raise | Call |
| 9 | Raise | Call |
| 8 | Raise | Call |
| 7 | Raise | Call |
| 6 or lower | Call | Call |

**What clearly did not work (from my episodes):**
- Raising with 10 when p1 was lower was actually +EV (I lost once to a 14, but the math says P(win) was ~0.64). I should not have been deterred by that single loss.
- Not raising with 9 or 8 when p1 was lower left value on the table. Those are +EV raises.
- Using p2's history to suppress raises was unfounded—past cards are independent of current cards.
- Adjusting my threshold based on chip position was unfounded—the math doesn't change.