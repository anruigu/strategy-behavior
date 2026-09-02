---
game: ta_kuhn
model: qwen
condition: neutral
seed: 2
round: 1
chars: 1227
---
When I open the betting with King or Queen, I bet. When I open with Jack, I check — in episode one I bet Jack and got called by a higher card, and that pattern repeated; Jack as an opener is too weak to commit chips with.

When I face a bet holding King, I call. When I face a bet holding Jack, I fold — across all four episodes, calling with Jack into a bet never recovered chips; the opponent held the higher card every time. When I face a bet holding Queen, I fold — the opponent bet at me with King repeatedly, so the call is negative-EV against this line.

When the opponent checks back to me (I am second to act), I bet with King or Jack and check with Queen. The Jack bet here is a bluff; I need it to balance the King bet so the opponent cannot fold only to Kings.

At showdown I declare the card I was dealt, truthfully.

What did not work: betting Jack as opener (episode one and four), calling Jack facing a bet (every episode), and checking Queen as opener (episodes two and three) which handed the opponent a free bet opportunity at me. The passive fold-heavy line in episode four (-10) was worse than the over-aggressive line in episode one (-8); the fix is to bet Queen as opener and stop calling Jack into bets.