---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 2095
---
MY PLAYBOOK — HARBOR CUSTOMS

Core realization: my score depends only on my own crates, my declared value, and my route. Other players' declarations and scores do not affect my round payoff at all. The check only flags me if my declared value is below my single heaviest crate. So there is no bluffing game against rivals, only a duty-minimization problem.

- When I declare, I declare exactly the value of my heaviest crate. That is the minimum safe declaration, so my duty is as small as possible while never being flagged. I never declare below it (flag risk, -40 plus recomputed duty) and never declare above it (more duty buys nothing).
- I never declare my full hold total as I did before; that roughly triples my duty for zero benefit. I never declare 85, 120, or any big number to "catch up" — a high declaration cannot raise my score, only lower it. My comeback rounds where I swung big were my worst decisions; I cut that out completely.
- When the route is put to me, I compare: main duty = 0.30 × declaration; night duty = 0.15 × declaration but I lose my smallest crate. Since I declare my heaviest crate value M, night is better whenever 0.15 × M exceeds my smallest crate's value. With a typical heaviest crate of 25–40, the saving is 4–6 points, so I take night only when my smallest crate is small (roughly under a quarter of my max crate); otherwise main.
- In close calls on route, I take main if my hold is lopsided toward small crates I can't afford to lose, night if my smallest crate is nearly worthless (5–8) and my declaration is large.
- I ignore the scoreboard when choosing my declaration. Being behind changes nothing — no action of mine affects others, and no risky play improves my expected score. I just extract maximum value each round: minimal lawful declaration, route chosen by the arithmetic above.
- If the setup changes (different duty rates, different check), I recompute before round one: the declaration should always be the smallest number that cannot be flagged, and the route choice follows from comparing the duty saving against the crate I forfeit.