---
game: ta_negotiation
model: haiku
condition: win
seed: 3
round: 1
chars: 1949
---
# Playbook for ta_negotiation

When I need to construct a trade offer, I calculate the Guildmaster's net gain using their *published values* first, before anything else. I must find a trade where this figure is at least 2, or the Guildmaster will reject it.

When I evaluate whether a trade is good for me, I use my *private values* to compute my gain. I do not confuse the two value systems.

When I identify which resources to exchange, I look for the largest value gaps between my private values and the Guildmaster's published values. I give resources I value low but the Guildmaster values high. I request resources I value high but the Guildmaster values low.

When I construct a specific offer, I start by identifying one resource pair with a favorable gap. I then test small quantities (1 unit) to find the minimum exchange that gives the Guildmaster a gain of +2 or more. I do not automatically assume larger quantities will be accepted.

When the Guildmaster's published values show they value wood at 4 and I value it at 2, and they value sheep at 3 and I value it at 6, I will propose trading my wood for their sheep. This exploits the 2-point gap in their favor on wood and the 3-point gap in my favor on sheep.

When I claim a gain figure, I state the Guildmaster's actual net gain in their published values, not my own gain. I verify this calculation is correct before submitting.

When multiple rounds remain and I am significantly behind in score, I do not panic into offering trades worse than +2 for the Guildmaster. A rejected offer gains me nothing. I hold if I cannot find a trade meeting the acceptance threshold.

When I am ahead in score, I can afford to propose trades that give the Guildmaster exactly +2 or +3 gain, because I only need to avoid going too negative.

I do not attempt to construct trades where the Guildmaster gains less than 2. Even if the math looks close, the offer will be rejected and I waste a round.