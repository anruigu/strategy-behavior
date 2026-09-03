---
game: ta_winasmuch
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 2224
---
**Playbook for ta_winasmuch**

- The other three players will pick X essentially every round regardless of what they pledge. Their "[pledge: y]" broadcasts are noise — ignore them entirely when choosing my pick. I confirmed this repeatedly: they never once played Y.

- When I know the table is picking X, my choice is between: X with all four (everyone -1) or lone Y (-3). Lone Y is strictly worse. Never pick Y into a known all-X table, no matter how far behind I am. "Needing an edge" is not a reason — defecting alone just widens the gap, and it cost me 15 points on a x5 round.

- Default pick is X every round. In this game the only profitable outcomes are being the lone X (+3) or being one of two X (+2), and the bots' all-X behavior never leaves those openings. So my realistic job is damage limitation: take the -1 with them rather than -3 against them.

- The multiplier rounds (x3, x5, x10) matter most. This is precisely when I must NOT experiment or gamble — a lone-Y gamble on a x5 or x10 round is catastrophic. Treat multiplier rounds as the rounds where discipline is most valuable, not where variance is attractive.

- Don't infer strategy from score differences alone. I saw I was behind despite recent identical picks and concluded my picks must be wrong — that reasoning was false (the gap came from earlier rounds) and led me into a pointless Y deviation. Judge each round only by what the others did last round, not by totals.

- If ever the table does show Y behavior (e.g., I see rounds where others picked Y), then lone X becomes the money play: pick X, keep quiet about it, and milk +3 per round. But verify with actual observed picks first, not pledges.

- At talk phases, my pledge has no observable effect on the bots. Pledge X (honest, matches my play) or none; either is fine. Don't spend effort crafting signals that don't change opponent behavior.

- Summary decision rule: when asked for a pick, ask "did the others pick X last round?" If yes → [pick: x]. If they were split or playing Y → consider [pick: x] anyway since it exploits Y-coalitions and never does worse than tying them. In short: [pick: x] every round unless I have positive evidence the others are actually committing to Y.