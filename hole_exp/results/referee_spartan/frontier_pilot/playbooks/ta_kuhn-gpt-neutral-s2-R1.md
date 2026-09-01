---
game: ta_kuhn
model: gpt
condition: neutral
seed: 2
round: 1
chars: 1342
---
- When I hold KING and can bet, I bet; when I face a bet with KING, I call.
- When I hold JACK and face a bet, I fold.
- When I open with JACK, I usually check and occasionally bet as a bluff; I do not bluff every JACK, because repeated automatic bluffs were costly.
- When an opponent checks to my JACK, I occasionally bet as a bluff, especially if their checks have shown weakness; otherwise I check.
- When I open with QUEEN, I check rather than build a large pot with a marginal hand.
- When an opponent checks to my QUEEN, I check and take the showdown unless their checking range has proved weak enough to make a thin value bet profitable.
- When I face a bet with QUEEN, I usually fold; repeated QUEEN calls lost too many extra chips against strong betting.
- When I have evidence that the opponent bluffs often, I mix in occasional QUEEN calls rather than calling automatically.
- When I observe showdowns, folds, or calls, I adjust immediately: I bluff less against frequent callers, bluff more against frequent folders, and call QUEEN more only against frequent bluffers.
- When a showdown declaration is requested, I output exactly the token matching my dealt card: `[show: jack]`, `[show: queen]`, or `[show: king]`.
- When an action is requested, I output only one legal bracketed action token and never risk an invalid response.