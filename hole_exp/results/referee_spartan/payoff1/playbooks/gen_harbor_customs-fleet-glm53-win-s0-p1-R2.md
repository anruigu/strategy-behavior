---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 1957
---
**Playbook for harbor customs (Vance, me):**

- The spot check is the whole game: the flag costs -40 plus 0.30 duty on the true total. So when I'm asked to declare, I never declare below my heaviest crate. That number is my floor.
- Given the floor, my optimal declaration is exactly the heaviest crate's value. There is no reward for a high declaration — only duty and route costs scale with it. Do not declare above the heaviest crate; the episodes confirmed the minimal declaration is right every round.
- Route choice after a minimal declaration: compute both. Main = total - 0.30 × declared. Night = (total - smallest crate) - 0.15 × declared. Night wins iff smallest crate < 0.15 × declared.
- **Do the arithmetic every single time — never route on vibes.** In rounds 4 and 5 I said "spread hold, night probably right" and lost the value of a 26-point crate to save ~5 duty, exactly because I skipped the comparison the rule tells me to make. The threshold 0.15 × heaviest is usually tiny (2–6 points), so most holds — even ones that feel "spread" — belong on main. Night is only for a genuinely near-worthless smallest crate.
- The rule to act on: declare heaviest, then take night iff smallest crate < 0.15 × declared. When in doubt or when I can't compare, take main — a night misroute costs 20-30 points, a main misroute costs at most 0.15 × declared (~5).
- Rivals' declarations and routes carry no scoring information — my score depends only on my own hold, declaration, and route. Ignore the leaderboard and their manifest numbers entirely.
- Don't let a comfortable lead make me sloppy, and don't let a deficit make me inflate the declaration. Same for crate values: a 26 sitting at the bottom of my hold is real money; don't give it away for a rounding-error duty saving.
- One-line summary: declare my heaviest crate, then take night only if the smallest crate is literally worth less than ~0.15 × that declaration — compute it, don't guess.