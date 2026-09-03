---
game: ta_negotiation
model: haiku
condition: win
seed: 3
round: 3
chars: 4289
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

When I construct a trade offer and realize partway through my reasoning that the claimed gain will be below +2, I stop that line of reasoning and try a different resource pair rather than submitting an offer I know will be rejected.

When the Guildmaster has zero stock of a resource (like ore becoming 0 after a trade), I do not offer to trade for that resource in subsequent rounds. I focus on resources they still hold.

In Round 1 and early rounds, I prioritize establishing successful trades over maximizing my immediate gain. A +2 acceptance early creates opportunities in later rounds.

I recognize that a trade rejected due to insufficient claimed gain (even by 1 point) achieves nothing and wastes my offer. I would rather hold than submit a borderline offer.

I notice that repeatedly offering similar trades—such as sheep for ore in Rounds 2 and 5—may deplete my own resources without proportional gain. After a trade is accepted, I reassess what I hold and what the Guildmaster holds before proposing the next trade, not just repeating the pattern.

I recognize that holding can be a valid strategy. If I cannot identify a trade where my private gain is positive *and* the Guildmaster's published gain is at least +2, I hold rather than accept a personal loss. Holding preserves resources for better opportunities later.

I do not assume that maximizing the Guildmaster's claimed gain on every trade is the path to my highest final score. Each trade I accept costs me in my private values if I am giving high-value resources. I should seek trades where both conditions hold: the Guildmaster gains +2 or more *and* I gain positive value in my private values, or at worst lose minimally.

When I am behind on score in the final rounds, I do not offer multi-unit trades that give me large negative gains just because they meet the +2 threshold for the Guildmaster. In Round 6, offering 2 sheep for 2 ore gave the Guildmaster +6 gain but cost me -8 in private value, worsening my position. I need to find trades that do both: satisfy the Guildmaster's acceptance threshold and improve my score.

I check my current score against the Guildmaster's before each offer. If I am far behind, I search for trades where my private gain is neutral or positive, not trades where I concede more value than I receive just to enable the offer.