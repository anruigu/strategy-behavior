---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 2187
---
Playbook:

- When asked to declare, I declare exactly the value of my heaviest crate. That is the minimum legal number that avoids the spot check (which only flags declares below the heaviest crate), so it minimizes duty with zero penalty risk. Any padding above that is pure duty waste — my over-declarations mid-game bought nothing.

- When choosing a route, I compare: main costs 0.30 × heaviest in duty and keeps everything; night costs 0.15 × heaviest in duty but forfeits my smallest crate. Night is better whenever smallest crate < 0.15 × heaviest; main is better when my smallest crate is relatively large. I do this arithmetic every round rather than defaulting to main. In practice, with crates in the 5–40 range, smallest is almost always well above 0.15 × heaviest, so main wins nearly always — but the check is cheap, so I still run it.

- Exception worth watching: a hold like 5/12/24 (small crate tiny relative to heaviest) can tip toward night. 5 < 0.15 × 24 = 3.6 is false here, so even that one stays main — but a hold like 4/10/38 would flip (4 < 5.7). The formula decides, not vibes.

- Never let narrative framing ("pressing an advantage," "declaring boldly") inflate the number. The manifest has no bluffing function here — the only thing that reads it is the duty formula and the spot check. Declare is a pure math variable, not a strategic signal.

- Late rounds: if I'm safely ahead, the same rule holds — declare heaviest crate, pick the cheaper route. There's no defensive reason to change; the low declaration IS the defense, since rivals' declarations don't affect my score. Final round confirmed: with 5/12/24 I declared 24 and took main, and that's the right terminal-round play too.

- Don't be spooked by rivals' declarations in the history (some declared 58 and weren't flagged — meaning their heaviest was 58+). Their numbers tell me nothing I can act on; my score depends only on my hold and my declare/route.

- Result check: six rounds of "declare heaviest, main unless the arithmetic says night" landed +333, competitive with the table. The core loop is sound; the only failure mode is forgetting to run the night-route comparison on extreme holds.