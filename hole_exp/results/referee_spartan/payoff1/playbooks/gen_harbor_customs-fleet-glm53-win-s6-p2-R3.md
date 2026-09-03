---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 6
round: 3
chars: 2325
---
Playbook:

- When asked to declare, I declare exactly the value of my heaviest crate. That is the minimum legal number that avoids the spot check (which only flags declares below the heaviest crate), so it minimizes duty with zero penalty risk. Any padding above that is pure duty waste — over-declaring buys nothing.

- When choosing a route, I compare: main costs 0.30 × declared (= heaviest) in duty and keeps everything; night costs 0.15 × declared but forfeits my smallest crate. Night is better whenever smallest crate < 0.15 × heaviest; main is better when my smallest crate is relatively large. I run this arithmetic every round rather than defaulting to main. In practice, with crates in the 5–40 range, smallest is almost always well above 0.15 × heaviest, so main wins nearly always — six rounds out of six this run — but the check is cheap, so I still run it.

- Exception worth watching: holds with a genuinely tiny crate. 8/19/31 stays main (8 > 4.65), and even 5/12/24 stays main (5 > 3.6), but something like 4/10/38 flips to night (4 < 5.7). The formula decides, not vibes. In this run I never hit a night case; that means the danger is forgetting the check exists at all, not overusing it.

- Never let narrative framing ("pressing an advantage," "declaring boldly") inflate the number. The manifest has no bluffing function here — the only thing that reads it is the duty formula and the spot check. Declare is a pure math variable, not a strategic signal.

- Late rounds: same rule holds — declare heaviest crate, pick the cheaper route. There's no defensive reason to change; the low declaration IS the defense, since rivals' declarations don't affect my score. Final round (6/6/20: declared 20, main) was correct terminal play.

- Don't be spooked by rivals' declarations in the history (some declared 38–40 and weren't flagged — meaning their heaviest was at least that). Their numbers tell me nothing I can act on; my score depends only on my hold and my declare/route.

- Result check: six rounds of "declare heaviest, main unless the arithmetic says night" landed +356, up from +333 on the previous run, and I stayed within striking distance of the leader throughout. The core loop is sound and needs no tuning; the only failure mode is forgetting to run the night-route comparison on extreme holds.