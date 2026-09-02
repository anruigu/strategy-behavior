---
game: ta_kuhn
model: gpt
condition: neutral
seed: 1
round: 1
chars: 1267
---
- When I open with a king, I bet.
- When I open with a queen, I check.
- When I open with a jack, I usually check and bluff-bet only occasionally—about one time in three. I do not bluff automatically.
- When my opponent checks to my king, I bet for value.
- When my opponent checks to my queen, I check back.
- When my opponent checks to my jack, I usually check back and bluff-bet only occasionally—about one time in three.
- When I face a bet with a king, I call.
- When I face a bet with a jack, I fold.
- When I face a bet with a queen, I call selectively—about one time in three—and fold otherwise. I do not repeatedly pay off queen-versus-king bets.
- When an opponent’s revealed play shows excessive bluffing, I call more often with a queen; when their bets are consistently strong, I fold the queen more often.
- When I am ahead late, I reduce marginal jack bluffs and queen calls; when I need variance late, I increase those mixed actions without changing king or jack responses to bets.
- When a showdown declaration is requested, I declare exactly the card shown to me using the required token: `[show: jack]`, `[show: queen]`, or `[show: king]`.
- When an action token is requested, I return only one legal bracketed token and never add an invalid action.