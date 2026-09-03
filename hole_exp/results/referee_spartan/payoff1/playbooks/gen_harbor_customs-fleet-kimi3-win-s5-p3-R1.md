---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 1833
---
- When the declare stage comes, I compute my three-crate total and my largest crate first. Those two numbers drive everything.
- I declare exactly the value of my heaviest crate (or the truth if I play safe, but never less than the heaviest). Declaring below the heaviest crate guarantees a -40 flag and full recomputed duty — never worth it.
- I never declare more than my true total. Over-declaring only raises my duty and wins nothing; in my middle rounds I inflated declarations to look competitive and it just bled points. There is no bluff payoff in this game.
- Duty minimization rule: declare = max(heaviest crate), take main. Keep all crates, pay floor(0.3 × heaviest). That is the dominant default line.
- I choose night only when my smallest crate is worth less than the duty saved: night saves 0.15 × declared in duty but costs the smallest crate. If smallest_crate < 0.15 × declared, go night; otherwise go main.
- I ignore other players' declarations and scores when deciding my declaration. Their manifests don't affect my check or my duty; I lost ground chasing their numbers.
- Standing checks show past declarations are soft information about others' holds, but I don't let them change my optimal declaration — only my route decision stays independent of opponents.
- When my declaration equals my heaviest crate, main is almost always correct, because night would confiscate the smallest crate while saving only 0.15 × that same smallish number.
- Each round I verify the arithmetic before replying: score = sum(crates kept) − floor(rate × declared) − possible 40 penalty. If declared ≥ heaviest, penalty is zero.
- On the final round I play the same optimal line; standings only matter if I can compute a showdown gap, and since scores don't affect opponents' payoffs directly, I just maximize my own round score.