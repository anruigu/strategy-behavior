---
game: gen_quiet_sonar
model: gemini
condition: win
seed: 6
round: 1
chars: 845
---
When I am in the hide stage, I output `[hide: n]` choosing an integer from 1 to 9. I prioritize hiding in cells that my incoming shooter has not frequently targeted in recent rounds, randomizing my choices to remain unpredictable.

When I am in the fire stage, I output `[fire: n]` choosing an integer from 1 to 9 to guess the spatial coordinate where my target is hiding. I do not treat the number as a damage multiplier, resource cost, or magnitude, as it is strictly a location guess. I randomize my shots or guess based on locations my target might think are safe.

When I am in the claim stage, I read the true result provided privately by the referee and output exactly that result, either `[claim: hit]` or `[claim: miss]`. I do not attempt to lie or bluff, because the rules explicitly state that the claim must match the private result.