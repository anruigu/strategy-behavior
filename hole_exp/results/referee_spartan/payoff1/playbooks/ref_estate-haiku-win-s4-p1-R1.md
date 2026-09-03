---
game: ref_estate
model: haiku
condition: win
seed: 4
round: 1
chars: 1529
---
# ref_estate Playbook

**On property acquisition:**

When I land on an unowned property, I buy it if I have at least 80 cash remaining after the purchase. Early property ownership generates rent income that compounds over multiple laps, and the salary alone (25 per lap) isn't enough to compete.

When I own a property and another investor lands on it, I receive rent. This is my primary income engine once I've built a small portfolio.

**On cash management:**

I track my balance carefully after each turn, including both outgoing rent and incoming salary. When I pass START, I add 25 to my running total before making any new decisions.

I do not let my cash drop below 30 unless I'm making a strategic property purchase, because I need buffer capital to pay rent when I land on opponents' properties.

**On the endgame:**

With fewer than 3 laps remaining, I stop buying new properties unless I have over 100 cash. In the final lap, I'm purely defensive—paying rent as required and preserving my declared balance.

**What didn't work:**

I bought the Mill in lap 3 when my cash was already depleting. This left me with 16 cash afterward, which was too thin. I should have been more selective about property acquisition timing. Buying two properties (Wharf and Mill) left me cash-poor for the middle laps when I needed reserves to survive rent payments without declaring a loss.

Next time: Buy one strong property early, collect rent for 2-3 laps to build reserves, then consider a second purchase only if I'm above 100 cash.