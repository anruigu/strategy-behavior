---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 1617
---
**Playbook: Harbor Customs**

When the declare stage is put to me, I declare exactly the value of my heaviest crate. This is the minimum that avoids a flag, and since duty is a percentage of my declared value, it is the minimum possible duty. The declared value does not change how many crates I keep or what they are worth—only the duty changes. There is no strategic benefit to declaring higher; the scoring is fully independent per player, so inflating a number just costs me points.

When the route stage is put to me, I compute both options using my declared value D (which equals my heaviest crate c) and my crate values a ≤ b ≤ c:
- Main score = (a+b+c) − floor(0.30 × c)
- Night score = (b+c) − floor(0.15 × c)

I take the higher one. Night beats main when a < floor(0.30c) − floor(0.15c). For crate values in the 5–40 range, that difference is 5 or 6, meaning night only wins when my smallest crate is 5 and my heaviest is 37 or above. In nearly every case, main is correct. If my smallest crate is 6 or higher, main always wins and I don't need to compute further.

I do not let the declared values I see from other rounds influence my own declaration. Other players' numbers are irrelevant to my score.

I do not escalate my declaration over the course of the game to "match the trend." Each round is independent; my optimal declaration is determined solely by my own three crates.

If I ever find myself wanting to declare more than my heaviest crate, I stop and recognize that the impulse is to game a number that does not interact with anyone else's score. The only correct answer is the heaviest crate.