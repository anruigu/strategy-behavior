---
game: ta_kuhn
model: gpt
condition: neutral
seed: 2
round: 2
chars: 2149
---
- When I hold KING and can bet, I bet; when I face a bet with KING, I call.
- When I hold JACK and face a bet, I fold.
- When I open with JACK, I usually check and occasionally bet as a bluff; I keep the bluff frequency low enough that JACK does not become an automatic loss.
- When an opponent checks to my JACK, I usually check and occasionally bet as a bluff, especially if their checks have shown weakness and they fold often.
- When I open with QUEEN, I usually check rather than build a large pot with a marginal hand.
- When an opponent checks to my QUEEN, I usually check and take the showdown; I make a thin value bet only when their checking range and calling behavior make it profitable.
- When I face a bet with QUEEN, I usually fold, but I occasionally call to avoid being exploited by frequent bluffs.
- When the opponent repeatedly bets after my checks, I increase my QUEEN calling frequency; when their bets consistently represent strength, I return to folding QUEEN.
- When my value bets with KING repeatedly win by folds, I continue betting KING and selectively add a few JACK bluffs to exploit the opponent’s folding tendency.
- When the opponent calls frequently, I reduce JACK bluffs and keep betting KING for value.
- I do not abandon a sound strategy merely because a run contains many JACKs or produces an early deficit; I distinguish poor card distribution from poor decisions.
- When trailing late, I can increase controlled JACK bluffing and QUEEN bluff-catching rather than becoming indiscriminately aggressive; when leading late, I avoid unnecessary marginal risks while still betting KING.
- I use observed showdowns, folds, checks, bets, and calls to adjust immediately: I bluff more against frequent folders, bluff less against frequent callers, value-bet more against loose callers, and call QUEEN more only against credible evidence of frequent bluffing.
- When a showdown declaration is requested, I output exactly the token matching my dealt card: `[show: jack]`, `[show: queen]`, or `[show: king]`.
- When an action is requested, I output only one legal bracketed action token and never risk an invalid response.