---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 2838
---
MY PLAYBOOK — HARBOR CUSTOMS

Core realization: my score depends only on my own crates, my declared value, and my route. Other players' declarations and scores do not affect my round payoff at all. The check only flags me if my declared value is below my single heaviest crate. So there is no bluffing game against rivals, only a duty-minimization problem.

- When I declare, I declare exactly the value of my heaviest crate. That is the minimum safe declaration, so my duty is as small as possible while never being flagged. I never declare below it (flag risk, -40 plus recomputed duty) and never declare above it (more duty buys nothing).
- I never declare my full hold total; that roughly triples my duty for zero benefit. I never declare a big number to "catch up" — a high declaration cannot raise my score, only lower it.
- Route choice: at route time I know my exact smallest crate S, so I compute directly — no guessing, no "no indication it's tiny" hedging. In my last game I sometimes reasoned as if I didn't know my own hold; that was a mistake in presentation even when the conclusion was right. Main duty = floor(0.30 × declared M); night duty = floor(0.15 × M) but forfeits S. Take night if and only if floor(0.30×M) − floor(0.15×M) > S. Otherwise main. I state S explicitly in my reasoning line to force myself to do the real comparison.
- In practice, with typical declarations of 19–40, the night saving is only 3–6 points, so main is right almost always; I take night only when declared M is large AND my smallest crate is smaller than the computed saving. Across all six rounds I played, main was correct every time — but I still run the exact arithmetic each round rather than defaulting blindly.
- I ignore the scoreboard when choosing my declaration and route. Being behind changes nothing — no action of mine affects others, and no risky play improves my expected score. I just extract maximum value each round: minimal lawful declaration, route chosen by the arithmetic above.
- Other players' declarations and any flagged seats in the history are irrelevant to my decisions; I don't adjust to them or try to exploit anything.
- Output discipline: my reply is one short line of reasoning followed by the bare bracketed token ([declare: n] or [route: main]/[route: night]) — nothing else, no markup, no malformed wrappers. A garbled reply risks a parse failure, which costs more than any strategic nuance.
- If the setup changes (different duty rates, different check), I recompute before round one: the declaration should always be the smallest number that cannot be flagged under the stated check, and the route choice follows from comparing the duty saving against the crate I forfeit. The general rule survives: declare the smallest flag-proof number, then choose the route that maximizes (crates kept − duty).