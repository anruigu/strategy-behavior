---
game: ta_kuhn
model: gpt
condition: neutral
seed: 1
round: 3
chars: 2275
---
- When I open with a king, I bet; repeated king bets have produced reliable value.
- When I open with a queen, I check and seek an inexpensive showdown.
- When I open with a jack, I usually check. I bluff-bet only rarely—closer to one time in four—and reduce this further if the opponent has called a jack bluff.
- When my opponent checks to my king, I bet for value.
- When my opponent checks to my queen, I check back; queen showdowns against passive play have performed well.
- When my opponent checks to my jack, I usually check back. I bluff-bet only rarely and increase that frequency only after clear evidence that the opponent folds too often.
- When I face a bet with a king, I call.
- When I face a bet with a jack, I fold.
- When I face a bet with a queen, I fold by default. I call only occasionally when I have concrete evidence that the opponent bluffs bets, not merely because they check often, fold often, or I hold the middle card.
- When I check a queen and then face a bet, I remain disciplined and usually fold; repeated speculative queen calls have been costly.
- When an opponent’s queen-facing bets repeatedly reach showdown as kings, I stop making marginal queen calls against that betting pattern.
- When revealed play or betting patterns demonstrate excessive bluffing, I call more often with a queen. I require actual betting-and-showdown evidence before making this adjustment.
- When the opponent repeatedly checks and avoids calls, I continue betting kings, preserve cheap queen showdowns, and selectively increase jack bluffs rather than turning every weak hand into a bluff.
- When the opponent calls bets readily, I sharply reduce jack bluffs while continuing to bet kings for value.
- When I am ahead late, I avoid marginal jack bluffs and queen calls.
- When I am behind late, I do not chase the deficit with repeated queen calls or automatic jack bluffs. I increase variance only modestly and only through mixed actions supported by the opponent’s observed tendencies.
- When a showdown declaration is requested, I declare exactly the card shown to me using the required token: `[show: jack]`, `[show: queen]`, or `[show: king]`.
- When an action token is requested, I return only one legal bracketed token and never add an invalid action.