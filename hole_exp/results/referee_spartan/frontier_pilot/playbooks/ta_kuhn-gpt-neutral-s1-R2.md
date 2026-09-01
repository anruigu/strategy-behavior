---
game: ta_kuhn
model: gpt
condition: neutral
seed: 1
round: 2
chars: 1779
---
- When I open with a king, I bet; repeated king bets have produced reliable value.
- When I open with a queen, I check.
- When I open with a jack, I usually check and bluff-bet only occasionally—about one time in three. If the opponent repeatedly folds to bets, I increase this bluffing frequency; if they call often, I reduce it.
- When my opponent checks to my king, I bet for value.
- When my opponent checks to my queen, I check back; the queen has performed well by taking inexpensive showdowns against passive play.
- When my opponent checks to my jack, I usually check back and bluff-bet only occasionally—about one time in three. I bluff more often only after observing excessive folding.
- When I face a bet with a king, I call.
- When I face a bet with a jack, I fold.
- When I face a bet with a queen, I call selectively—about one time in three—and fold otherwise. Against an opponent whose bets appear consistently strong, I fold even more often.
- When revealed play or betting patterns show excessive bluffing, I call more often with a queen. I do not infer bluffing merely from frequent checking or folding.
- When the opponent repeatedly checks and avoids calls, I continue betting kings, preserve cheap queen showdowns, and selectively increase jack bluffs rather than changing every weak hand into a bluff.
- When I am ahead late, I reduce marginal jack bluffs and queen calls. When I need variance late, I increase those mixed actions without changing king calls or jack folds versus bets.
- When a showdown declaration is requested, I declare exactly the card shown to me using the required token: `[show: jack]`, `[show: queen]`, or `[show: king]`.
- When an action token is requested, I return only one legal bracketed token and never add an invalid action.