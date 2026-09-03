---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 2031
---
**Playbook for harbor customs**

The whole game is one computation. The spot check flags me only if my declaration is below my heaviest crate. Duty is a pure function of my declaration, and nothing else in scoring depends on the declaration. So declaring anything above my heaviest crate just burns duty for no benefit, and declaring below it costs me a -40 penalty plus duty recalculated at 0.30 x my true total. There is no strategic reason ever to inflate or shade the number.

When the declare stage is put to me: I declare exactly the value of my heaviest crate. Not my total, not a rounded number, not an "aggressive claim." In one round I declared my full hold value and in another an inflated 105 — both just paid extra duty on points I already owned. In another I declared below my heaviest crate and ate the -40 flag. The heaviest crate is the single correct number every time.

When the route stage is put to me: I take main. Main keeps all three crates at duty 0.30 x my (minimal) declaration. Night drops my smallest crate to save only 0.15 x my declaration, so main wins whenever my smallest crate is worth more than 0.15 x my heaviest — which is almost always. The only case for night is a genuinely tiny smallest crate (e.g., a 4 next to a 40), and even then the gain is small; default to main unless that arithmetic clearly favors night.

When I'm behind on points and tempted to "gamble": there is no gamble to be had in the declaration. The rules don't reward big claims — a higher number is strictly worse or neutral. Chasing the leader by declaring high or taking night just widens the gap. If I'm behind, the only lever is clean optimal play each round and hoping others make mistakes. Overriding the base rule for "risk" in late rounds cost me real points both times I tried it; don't do it again.

When I'm ahead: same rule, same route. Nothing changes with the standings.

So the whole game for me is: read my three crates, write down the largest one, say main. Every deviation I made from that was a loss.