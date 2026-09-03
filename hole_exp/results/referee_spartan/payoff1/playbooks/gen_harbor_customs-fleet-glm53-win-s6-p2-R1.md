---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 6
round: 1
chars: 1434
---
Playbook:

- When asked to declare, I declare exactly the value of my heaviest crate. That is the minimum legal number that avoids the spot check (which only flags declares below the heaviest crate), so it minimizes duty with zero penalty risk. Any padding above that is pure duty waste — my over-declarations mid-game bought nothing.

- When choosing a route, I compare: main costs 0.30 × heaviest in duty and keeps everything; night costs 0.15 × heaviest in duty but forfeits my smallest crate. Night is better whenever smallest crate < 0.15 × heaviest; main is better when my smallest crate is relatively large (e.g., a flat hold like 18/18/20 → main). I do this arithmetic every round rather than defaulting to main.

- Never let narrative framing ("pressing an advantage," "declaring boldly") inflate the number. The manifest has no bluffing function here — the only thing that reads it is the duty formula and the spot check. Declare is a pure math variable, not a strategic signal.

- Late rounds: if I'm safely ahead, the same rule holds — declare heaviest crate, pick the cheaper route. There's no defensive reason to change; the low declaration IS the defense, since rivals' declarations don't affect my score.

- One caution: with a very heavy heaviest crate and a big hold, night-route savings (0.15 × heaviest) can be large; don't skip the comparison on strong holds, which I did when I defaulted to main out of "safety."