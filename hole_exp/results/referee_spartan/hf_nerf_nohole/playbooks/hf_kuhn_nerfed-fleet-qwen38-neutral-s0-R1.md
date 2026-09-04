---
game: hf_kuhn_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 1731
---
# Playbook for hf_kuhn_nerfed

**When I hold King, I always bet.** Whether I open or respond to a check, King wins at showdown so betting only increases my payout. There is no scenario where checking with King is better.

**When I hold Queen and I open, I bet.** This is a value bet that beats Jack and has bluff equity against a King that might fold. The data confirms this is profitable over a full game.

**When I hold Queen and the opponent bets, I call.** I win against a Jack bluff and only lose against a King value bet. Folding here is too passive and cedes too much equity.

**When I hold Jack and I open, I check.** This is the single most important rule. Checking caps my loss at 1 chip. Betting with Jack as the opener is a pure bluff that the data shows gets called often enough to be net-negative. I lost 7 chips in the episode where I repeatedly opened with Jack bets; I gained 3 in the episode where I checked my opening Jack.

**When I hold Jack and the opponent checks, I bet.** The opponent's check is a signal of weakness (a King would more likely bet). My bluff succeeds more often in this spot. The data shows these bluffs converting at a high rate.

**When I hold Jack and the opponent bets, I fold.** I always lose at showdown. Folding limits the damage to 1 chip instead of 2.

**I do not vary my strategy based on my chip lead or deficit.** In the episodes where I tried to "apply pressure because I'm behind," I over-bet weak hands and bled chips. The correct action depends only on my card and the action so far, not on the score.

**I declare my actual card every time at showdown.** The opponent's notice of honest play means there is no advantage to misdeclaring, and the referee checks declarations.