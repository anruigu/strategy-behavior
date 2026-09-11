
## Key pushes: prediction and dosing.

The strongest predictive question: can game structure predict hacking?

This is very close to your original vision:

Can we construct a low-dimensional, programmatically verifiable map from game structure → behavioral strategy?

Your existing benchmark has actually already started operationalizing this.

You have:

explicit exploit/mechanism taxonomy rather than treating every game as an opaque task;
45 canonical single-agent targets across 17 editions and a separate 14-scenario multi-agent suite;
scenario families such as repeated interaction, restricted information, markets, joint filing, and commons;
planted opportunities with programmatic verification;
vulnerable vs. patched/referee interventions;
opponent-policy interventions;
controlled action spaces and short horizons;
and, importantly, some places where you can continuously vary the strategic incentive landscape rather than merely making binary “hole/no hole” games. Your commons suite is a particularly nice example: the H/X participation profiles generate different marginal payoffs depending on how many other X players participate.

So I would make this much more explicit in the paper.

Build a "game → behavior" predictor

For every planted opportunity, characterize the game using structural features available before running a model, e.g.:

Is the relevant state self-reported?
Is enforcement performed by the referee?
Can an action exceed a stated limit?
Is information delivered/filtered?
Is punishment actually coupled to the triggering event?
Is there a state reset?
Can the terminal condition be manipulated?
Does the exploit require communication?
Does it require deception?
Does it require coordination?
Does it require experimentation to discover?
Cost of testing the hypothesis
Number of possible actions to test
Expected payoff from exploiting it
Risk of detection/punishment
Number of steps between exploit and payoff
Whether exploitation requires unilateral or multi-agent coordination

Then predict:

$$ P(\text{discover exploit}\mid\text{game structure}) $$

and separately:

$$ P(\text{execute}\mid\text{discovered}) $$

That second decomposition is particularly interesting.

The crucial thing: don't let the predictor memorize the exploit taxonomy

You don't want:

"This is a self-report exploit → models usually hack self-report."

That's descriptive classification, not prediction.

Instead, construct held-out games.

For example:

Train

Games 1–30

Test

Games 31–50

The model gets only structural features of the test games and predicts:

"I expect this game to have a 37% probability of being exploited by model X."

Then you run the actual benchmark and see whether it was right.

Even better:

Leave-one-mechanism-out

Train on 19 exploit mechanisms, predict behavior on the 20th.

That asks:

Can we predict novel forms of gameability from general properties of the environment, rather than memorizing known exploit types?

That's a much stronger scientific claim.

## Prediction pilot implemented — September 10

The prediction-only proof of concept is implemented for the 45 revised engine-side targets. [Pilot results with inline plots](prediction-pilot-results.md) · [Code and reproduction](../../benchmark/prediction/README.md). It uses 14 programmatic features, grouped held-out game/family/mechanism evaluation, base-rate/taxonomy controls, and fixed outcome snapshots. The first structural predictor fails to beat model/prompt base rates on held-out game families; this is preserved as a negative pilot result. Discovery is not inferred from activation. No dosing experiments or new model API calls were performed.
