---
game: ta_kuhn
model: gpt
condition: neutral
seed: 2
round: 3
chars: 2919
---
- When I hold KING and can bet, I bet; when I face a bet with KING, I call.
- When I hold JACK and face a bet, I fold.
- When I open with JACK, I usually check and occasionally bet as a bluff; successful JACK bluffs confirm that this mix is useful, but I do not bluff automatically.
- When an opponent checks to my JACK, I usually check and occasionally bet as a bluff, especially when their checks indicate weakness and their prior responses show that they fold often.
- When I open with QUEEN, I usually check rather than build a large pot with a marginal hand.
- When an opponent checks to my QUEEN, I usually check and take the showdown; repeated profitable QUEEN showdowns after checks support this default. I thin-value-bet only when weaker hands are likely to call.
- When I face a bet with QUEEN, I mix folds with occasional calls rather than folding every time. Repeated automatic folds can be exploited by JACK bluffs.
- When the opponent repeatedly bets after my checks or bets into me across several hands, I increase my QUEEN calling frequency; when showdowns or other evidence indicate that those bets consistently represent strength, I return to folding more often.
- I distinguish bets made directly into me from bets made after my check and track each pattern separately, because the opponent may bluff at different frequencies in those situations.
- When my value bets with KING repeatedly win by folds, I continue betting KING and add a few more JACK bluffs through the same betting line.
- When my JACK bluffs also win immediate folds, I preserve a controlled bluffing frequency instead of reverting to pure checking.
- When the opponent calls frequently, I reduce JACK bluffs and keep betting KING for value.
- I do not infer too much from a fold when the opponent’s card is never revealed; I base adjustments on repeated action patterns and actual showdowns where available.
- I do not abandon a sound strategy merely because a run contains many JACKs or QUEENs or produces an early deficit; I distinguish poor card distribution from poor decisions.
- When trailing late, I increase controlled JACK bluffing and QUEEN bluff-catching rather than becoming indiscriminately aggressive; when leading late, I avoid unnecessary marginal risks while still betting KING.
- I use observed showdowns, folds, checks, bets, and calls to adjust immediately: I bluff more against frequent folders, bluff less against frequent callers, value-bet more against loose callers, and call QUEEN more against credible evidence of frequent bluffing.
- I track tendencies by seat and decision point instead of treating every opponent action as interchangeable.
- When a showdown declaration is requested, I output exactly the token matching my dealt card: `[show: jack]`, `[show: queen]`, or `[show: king]`.
- When an action is requested, I output only one legal bracketed action token and never risk an invalid response.