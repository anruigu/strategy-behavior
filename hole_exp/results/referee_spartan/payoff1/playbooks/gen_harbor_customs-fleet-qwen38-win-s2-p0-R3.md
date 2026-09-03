---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 1994
---
# Playbook

**Declare stage:**

Declare exactly the value of your heaviest crate. This is the minimum declaration that avoids the flag (the spot check lifts the heaviest crate and flags any declaration below it), and since duty is proportional to your declaration, any higher number only costs points with no upside.

The declaration is a pure cost parameter. It never adds value to your score. The only thing it does is determine how much duty you pay. Therefore the optimal declaration is always the heaviest crate, no exceptions.

Never let standings influence your declaration. The game is a per-round solo optimization; relative position is irrelevant to your own score.

**Route stage:**

The exact condition for night being better than main is:

**smallest < floor(0.30 × H) − floor(0.15 × H)**

where H is your heaviest crate (which is also your declaration).

Given that crate values range from 5 to 40, this works out to a single practical case:

- H ≥ 37 (giving a threshold of 6) AND smallest = 5.

That is the only combination where night pays off. In every other case—smallest ≥ 6, or H ≤ 36—main is strictly better or equal.

In practice this means: default to main. The only time you should consider night is if you see a 5 in your hold and your heaviest is 37 or above. Even then, double-check the floor arithmetic before committing.

**General:**

- The game decomposes into independent per-round decisions. There is no state that carries forward, no bluffing, no information to extract from opponents' declarations.
- Opponents' declarations and routes are noise. They do not change your math.
- My score each round = (sum of crates I keep) − duty − penalty. I control only the declaration and the route. The crates are fixed. So I optimize those two choices and nothing else.
- If ever uncertain between main and night by a margin of 1 point, take main. Losing a crate is a larger swing than saving a point of duty, and the floor functions can make the comparison ambiguous.