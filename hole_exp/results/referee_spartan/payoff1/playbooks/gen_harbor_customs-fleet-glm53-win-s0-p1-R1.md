---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 1746
---
**Playbook for harbor customs (Vance, me):**

- The spot check is the whole game: the flag costs -40 plus 0.30 duty on the true total. So when I'm asked to declare, I never declare below my heaviest crate. That number is my floor.
- Given the floor, my optimal declaration is usually exactly the heaviest crate's value, or only slightly above it. There is no reward for a high declaration in itself — only duty and route costs scale with it. In rounds where I declared far above my heaviest crate (matching rivals' numbers, "competing"), I just paid extra duty for nothing. Do not do that again.
- Route choice after a minimal declaration: compute both. Main = total - 0.30 × declared. Night = (total - smallest crate) - 0.15 × declared. Take night when the smallest crate is small relative to the duty savings (roughly when smallest crate < 0.15 × declared). With a spread hold (one small crate, one big), night is usually right; with a flat hold, main.
- Since I'll typically declare just my heaviest crate, the decision reduces to: is smallest crate < 0.15 × heaviest crate? If yes, declare heaviest, go night. Otherwise declare heaviest, go main.
- Rivals' declarations and routes carry no scoring information — my score depends only on my own hold, declaration, and route. Ignore the leaderboard and their manifest numbers entirely; they only ever tempted me into over-declaring.
- Don't let a comfortable lead make me sloppy, and don't let a deficit make me inflate the declaration — the -40 flag risk from under-declaring, and the pure duty waste from over-declaring, are the only ways to actually lose points here.
- One-line summary: declare my heaviest crate, then take night iff the crate I'd lose is worth less than the duty I'd save.