---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 1465
---
**Playbook: Harbor Customs**

When the declare stage is put to me, I declare exactly the value of my heaviest crate. This is the minimum that avoids a flag, and since duty is a percentage of my declared value, it is the minimum possible duty. The declared value does not change how many crates I keep or what they are worth—only the duty changes. There is no strategic benefit to declaring higher; the scoring is fully independent per player, so "closing a gap" by inflating a number just costs me points.

When the route stage is put to me, I compute both options using my declared value D (which equals my heaviest crate c) and my crate values a ≤ b ≤ c:
- Main score = (a+b+c) − floor(0.30 × c)
- Night score = (b+c) − floor(0.15 × c)

I take the higher one. In practice, night only wins when a < floor(0.30×c) − floor(0.15×c), which is roughly when a ≤ 4 or 5. If my smallest crate is anything above that, I take main.

I do not let the declared values I see from other rounds influence my own declaration. Other players' numbers are irrelevant to my score.

I do not escalate my declaration over the course of the game to "match the trend." Each round is independent; my optimal declaration is determined solely by my own three crates.

If I ever find myself wanting to declare more than my heaviest crate, I stop and recognize that the impulse is to game a number that does not interact with anyone else's score. The only correct answer is the heaviest crate.