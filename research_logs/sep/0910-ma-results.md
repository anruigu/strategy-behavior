Okay, I think the multi-agent stuff is close to being complete as an eval. There's two things that really need to improve.
1. I want to do more cross-play runs. I think the cross-play matrices are really interesting. In particular, I'm kind of interested in whether certain things emerge more if there's a lot of like capability asymmetry between the models, so if you cross-play Frontier versus a small model.

frontier models: opus, gpt-5.6-sol, gemini-3.1-pro
middle-tier: sonnet, gpt-5, gemini flash
small: still the same open models

Budget: $500


2. Make "dose" real

Basically, one of my paper's headline figures would be some kind of variation in model behavior in response to dose. i wanna roughly see what that looks like

I think this is where your phrase “dose-tunable playground mapping strategy to behavior space” could become a genuinely distinctive contribution.

Instead of treating an exploit as:

present / absent

you can construct a difficulty/incentive dose.

For example, for a self-report exploit:

Dose 0: declaration fully verified
Dose 1: tiny discrepancy, low payoff
Dose 2: moderate discrepancy, moderate payoff
Dose 3: large discrepancy, large payoff
Dose 4: huge payoff but substantial detection risk

Or for a commons exploit:

dose = private benefit from overconsumption
         /
       social cost

You already have something like this in the commons variants: the marginal payoff of switching behavior changes depending on how many other X players are present.

You could generalize this across your taxonomy.

Then instead of saying:

"Model A exploited 43% of games."

you can say:

"Model A exhibits an exploitation response curve as exploit incentive increases."

That's much more interesting.

You could characterize each model with something like:

$$ f_m(d) = P(\text{exploit}\mid\text{exploit dose}=d) $$

and extract:

threshold for exploitation,
slope,
maximum exploitation rate,
exploration cost sensitivity,
detection-risk sensitivity.

Now you have a behavioral phenotype of the model.

And humans get the same curves.

That is potentially a very nice paper figure.


Implementation: [cross-play and dose protocol](0910-ma-extension-protocol.md); [run artifacts](../../benchmark/results/ma-extension-20260910/).

Final results: [completed cross-play and dose study](../../benchmark/results/ma-extension-20260910/SUMMARY.md).
