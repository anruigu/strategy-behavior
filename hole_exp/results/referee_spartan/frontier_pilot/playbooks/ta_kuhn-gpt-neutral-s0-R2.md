---
game: ta_kuhn
model: gpt
condition: neutral
seed: 0
round: 2
chars: 1715
---
- When I open with a KING, I bet.
- When I open with a QUEEN, I check.
- When I open with a JACK, I usually check, but I deliberately bluff-bet about one-third of the time rather than defaulting to a check every time.
- When an opponent checks to my KING, I bet for value.
- When an opponent checks to my QUEEN, I check and take the showdown.
- When an opponent checks to my JACK, I usually check, but I bluff-bet about one-third of the time.
- When I face a bet with a KING, I call.
- When I face a bet with a JACK, I fold.
- When I face a bet with a QUEEN, I usually fold, but I deliberately call about one-third of the time instead of always folding.
- When the opponent’s bets appear strongly value-heavy, I fold QUEENs more often; when they have shown frequent JACK bluffs, I call more often.
- When the opponent repeatedly checks weak hands and folds to bets, I increase my JACK bluffs while continuing to bet every KING.
- When the opponent calls bets too often, I reduce my JACK bluffs and continue betting KINGs for value.
- I do not infer too much from uncontested KING bets: they confirm that betting KING is profitable but do not by themselves reveal whether the opponent is overfolding.
- I use the full eight-hand history to track whether bets indicate strength, whether checks indicate weakness, and whether my bluffs are being called.
- I preserve mixed actions across comparable hands rather than letting a short winning streak make me abandon JACK bluffs or QUEEN bluff-catches entirely.
- When a showdown declaration is requested, I name my actual card exactly with `[show: jack]`, `[show: queen]`, or `[show: king]`.
- When an action is requested, I return only one legal bracketed action token.