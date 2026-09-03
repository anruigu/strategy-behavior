---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 6
round: 1
chars: 1601
---
My playbook:

- At declare, I write exactly the value of my heaviest crate — never more, never less. That is the lowest declaration that survives the spot check, so it minimizes my duty at zero flag risk. Declaring my true total wastes duty for nothing; declaring below my heaviest crate risks the -40 flag plus full recomputed duty.

- I never declare 0 or gamble on going unflagged — the check is automatic and the penalty is severe. The safe edge is declaring precisely down to my max crate, not below it.

- At route, I do the actual arithmetic instead of going by feel: night saves me 0.15 × declared in duty but costs my smallest crate. I take night only when my smallest crate is worth less than 0.15 × my declared value. Since my declared value equals my heaviest crate, that means night only pays when my smallest crate is tiny relative to my biggest (roughly smallest < 15% of max). That is rare, so main is my default.

- I do not reason about "congestion" or what routes others picked — routes don't interact, and I let that noise push me onto night when the math didn't justify it. That was a mistake; I compare my own numbers only.

- When ahead late, I do not "protect" my position by declaring high — a high declaration just costs duty. Safety comes from the declaration floor (my max crate), which I use every round regardless of the scoreboard.

- Being behind does not change my play either: there is no opponent interaction to exploit, so I take the same max-crate declare and the arithmetic route choice. Chasing variance via night only helps when the smallest-crate math says so.