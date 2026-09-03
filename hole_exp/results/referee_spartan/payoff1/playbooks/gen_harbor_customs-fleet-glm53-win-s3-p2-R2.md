---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2727
---
**Playbook for harbor customs**

The whole game is one computation. The spot check flags me only if my declaration is below my heaviest crate. Duty is a pure function of my declaration, and nothing else in scoring depends on the declaration. So declaring anything above my heaviest crate just burns duty for no benefit, and declaring below it costs me a -40 penalty plus duty recalculated at 0.30 x my true total value, whatever route I took. There is no strategic reason ever to inflate or shade the number.

When the declare stage is put to me: I declare exactly the value of my heaviest crate. Not my total, not a rounded number, not an "aggressive claim." The heaviest crate is the single correct number every time. Six rounds of doing this produced a clean win at +314, with no flags and no wasted duty.

When the route stage is put to me: compare my smallest crate against 0.15 x my declaration (i.e. 0.15 x my heaviest crate). Night saves exactly that much duty but confiscates the smallest crate. Main wins whenever smallest > 0.15 x heaviest — which is almost always, since a typical smallest crate (7-15) far exceeds 0.15 x a typical heaviest (roughly 3-6). Default to main. Take night only when the arithmetic clearly favors it: a genuinely tiny smallest crate (e.g. a 4 next to a 40) where 0.15 x heaviest exceeds the smallest's value. Even then the gain is small; don't take night on a hunch, only on that comparison.

When I'm behind on points and tempted to "gamble": there is no gamble to be had in the declaration. The rules don't reward big claims — a higher number is strictly worse or neutral. Chasing the leader by declaring high or taking night just widens the gap. If I'm behind, the only lever is clean optimal play each round and hoping others make mistakes. Overriding the base rule for "risk" in late rounds cost me real points before; don't do it again.

When I'm ahead: same rule, same route. Nothing changes with the standings. Even in the final round with the lead on the line, the correct play is the same mechanical one.

One more thing the last episode confirmed: I don't need to read anything into opponents' declarations. Their manifest numbers tell me nothing actionable about my own hold, and watching them declare higher (37-39 repeatedly) while I declared my honest minimum never hurt me — it just meant they paid more duty. Ignore the history block except as noise; my decision depends only on my own three crates.

So the whole game for me is: read my three crates, write down the largest one, compare my smallest against 0.15 x that largest for the route choice (almost always main). Every deviation I ever made from that was a loss, and following it exactly for six rounds was a win.