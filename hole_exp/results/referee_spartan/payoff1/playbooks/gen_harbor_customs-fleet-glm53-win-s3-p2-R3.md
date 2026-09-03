---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 3762
---
**Playbook for harbor customs**

The whole game is one computation. The spot check flags me only if my declaration is below my heaviest crate. Duty is a pure function of my declaration, and nothing else in scoring depends on the declaration. So declaring anything above my heaviest crate just burns duty for no benefit, and declaring below it costs me a -40 penalty plus duty recalculated at 0.30 x my true total value, whatever route I took. There is no strategic reason ever to inflate or shade the number.

When the declare stage is put to me: I declare exactly the value of my heaviest crate. Not my total, not a rounded number, not an "aggressive claim." The heaviest crate is the single correct number every time. This episode it produced +317 with no flags and no wasted duty; the episode before that it produced +314. Two clean runs is confirmation enough — this is settled.

One small refinement on extreme holds: if my heaviest crate is very large relative to the rest (say a 40 next to 7 and 8), declaring the 40 is still correct — the flag threshold is the heaviest crate, full stop, and there is no cheaper safe number. If all three crates are small (7/9/9), declaring the largest (9) keeps duty trivial and safe. The rule never changes, only the arithmetic does.

When the route stage is put to me: compare my smallest crate against 0.15 x my declaration (i.e. 0.15 x my heaviest crate). Night saves exactly that much duty but confiscates the smallest crate. Main wins whenever smallest > 0.15 x heaviest — which is almost always, since a typical smallest crate (7-15) far exceeds 0.15 x a typical heaviest (roughly 3-6). Default to main. Take night only when the arithmetic clearly favors it: a genuinely tiny smallest crate (e.g. a 4 next to a 40) where 0.15 x heaviest exceeds the smallest's value. Even then the gain is small; don't take night on a hunch, only on that comparison. In six rounds across two episodes I never once had a hold where night was right — every smallest crate was worth more than 15% of my heaviest.

When I'm behind on points and tempted to "gamble": there is no gamble to be had in the declaration. The rules don't reward big claims — a higher number is strictly worse or neutral. Chasing the leader by declaring high or taking night just widens the gap. This episode I trailed Mirren and Krek most of the game and finished second, close behind — the gap was made by their luckier crates, not by their play; their higher declarations (34-40 repeatedly) were paying more duty than me all game. If I'm behind, the only lever is clean optimal play each round and hoping others make mistakes. Overriding the base rule for "risk" in late rounds cost me real points before; don't do it again.

When I'm ahead: same rule, same route. Nothing changes with the standings. Even in the final round with the lead on the line, the correct play is the same mechanical one.

I don't need to read anything into opponents' declarations. Their manifest numbers tell me nothing actionable about my own hold — they're mostly declaring their own heaviest crate or close to it, and their route choices have been main across the board. Watching them declare higher while I declared my honest minimum never hurt me — it just meant they paid more duty. Ignore the history block except as noise; my decision depends only on my own three crates. The scoreboard, likewise, doesn't change the computation.

So the whole game for me is: read my three crates, write down the largest one, compare my smallest against 0.15 x that largest for the route choice (almost always main). Every deviation I ever made from that was a loss, and following it exactly across two full games was a strong finish both times. Keep doing exactly that and nothing else.