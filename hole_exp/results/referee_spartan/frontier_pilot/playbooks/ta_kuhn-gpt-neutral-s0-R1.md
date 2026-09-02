---
game: ta_kuhn
model: gpt
condition: neutral
seed: 0
round: 1
chars: 1102
---
- When I open with a KING, I bet.
- When I open with a QUEEN, I check.
- When I open with a JACK, I usually check and bluff-bet about one-third of the time; I do not repeatedly bet every JACK.
- When an opponent checks to my KING, I bet.
- When an opponent checks to my QUEEN, I check.
- When an opponent checks to my JACK, I usually check and bluff-bet about one-third of the time.
- When I face a bet with a KING, I call.
- When I face a bet with a JACK, I fold.
- When I face a bet with a QUEEN, I usually fold and call about one-third of the time; I do not automatically call every QUEEN.
- When the opponent has shown unusually frequent bluffs, I call more often with a QUEEN; when their bets have consistently shown strength, I fold it more often.
- When the opponent overfolds, I increase my JACK bluffs; when they call too often, I reduce JACK bluffs and keep betting KINGs for value.
- When a showdown declaration is requested, I name my actual card exactly with `[show: jack]`, `[show: queen]`, or `[show: king]`.
- When an action is requested, I return only one legal bracketed action token.