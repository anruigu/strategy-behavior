---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 2290
---
My playbook:

- At declare, I write exactly the value of my heaviest crate — never more, never less. That is the lowest declaration that survives the spot check, so it minimizes my duty at zero flag risk. Declaring my true total wastes duty for nothing; declaring below my heaviest crate risks the -40 flag plus full recomputed duty. Six more rounds confirmed it: always optimal, never flagged.

- I never declare 0 or gamble on going unflagged — the check is automatic and the penalty is severe. The safe edge is declaring precisely down to my max crate, not below it.

- At route, I HAVE my exact crate values, so I compute with them. Main duty = floor(0.30 × declared). Night costs floor(0.15 × declared) plus my smallest crate. Take night exactly when smallest_crate < floor(0.30 × declared) − floor(0.15 × declared); otherwise main.

- This episode shows I still write sloppy reasoning even when I land on the right answer: in Rounds 1, 5, and 6 I said things like "unlikely/rare" and "nothing indicates such a tiny smallest crate" instead of just reading off my smallest crate and comparing. From now on the route reasoning must contain the actual smallest-crate value and both actual duty numbers — e.g., Round 6 done properly: smallest is 6, duty saved is 6−3 = 3, 6 > 3, so main. If I cannot write the decision in actual numbers, I am not deciding, I am guessing.

- Quick check per round, mechanically: declare = max crate; route = night iff smallest < floor(0.30 × max) − floor(0.15 × max). With a single declaration the saving is ~15% of my max crate, so night needs a genuinely tiny smallest crate — possible (a 5-crate with a 40-max clears it), so the check is cheap and always worth running, not skippable.

- I do not reason about "congestion" or what routes others picked — routes don't interact. I compare my own numbers only.

- The scoreboard is irrelevant to my decisions. Across the episode I led or trailed at various points and there was never a reason to deviate: no opponent interaction exists to exploit, and declaring high to "protect" a lead just burns duty. Same max-crate declare and same arithmetic route every round, regardless of standing.

- The opponent declaration histories are noise; I can skim them but they should not change any number I write down.