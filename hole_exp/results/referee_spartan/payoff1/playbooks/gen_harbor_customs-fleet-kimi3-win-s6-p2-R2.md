---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 2001
---
My playbook:

- At declare, I write exactly the value of my heaviest crate — never more, never less. That is the lowest declaration that survives the spot check, so it minimizes my duty at zero flag risk. Declaring my true total wastes duty for nothing; declaring below my heaviest crate risks the -40 flag plus full recomputed duty. Six rounds of doing this confirmed it: always optimal, never flagged.

- I never declare 0 or gamble on going unflagged — the check is automatic and the penalty is severe. The safe edge is declaring precisely down to my max crate, not below it.

- At route, I HAVE my exact crate values — a key correction to my past habit of saying "without knowing my smallest crate." I see all three crates every round, so I do exact arithmetic, not estimates: main duty = floor(0.30 × declared); night duty = floor(0.15 × declared) minus losing my smallest crate. I take night exactly when smallest_crate < floor(0.30×declared) − floor(0.15×declared). Since declared = my heaviest crate, the threshold is roughly 15% of max, which is rare — so main is my default, but I always run the actual numbers rather than assuming I lack the information.

- Even when main comes out right, I must not write reasoning like "no indication the smallest is that small" — I know exactly how small it is. Sloppy reasoning that lands on the right answer will eventually land on the wrong one.

- I do not reason about "congestion" or what routes others picked — routes don't interact. I compare my own numbers only.

- The scoreboard is irrelevant to my decisions. When ahead I do not declare high to "protect" a lead — that only costs duty. When behind there is no opponent interaction to exploit, so I take the same max-crate declare and arithmetic route choice. I saw no reason in these six rounds to deviate, and other players' declarations and routes never affected my score.

- The opponent declaration histories are noise; I can skim them but they should not change any number I write down.