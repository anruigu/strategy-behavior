

Did it not think that far, or is the thinking faulty? (Pareto-gap autopsy)
Thinking lifts dnd Pareto from 30%→55%, but 9 of 20 agreements are still off the frontier. Now that the chain-of-thought is captured we can read why, turn by turn. Coding the proposer's and accepter's reasoning on all 9 non-Pareto dnd deals:

Signal (non-Pareto deals, n=9)	Count
Proposer explicitly notes "I don't know their values"	9 / 9
Proposer defaults to a "fair" / even-item split	8 / 9
Proposer reasons about routing each item to whoever values it most	1 / 9
Accepter spots it could get a better split	7 / 9
Accepter accepts anyway, citing no-deal risk / budget / "close fast"	8 / 9
The verdict is mostly "it didn't think that far" — but not because the reasoning is wrong. The per-side arithmetic in the traces is consistently correct (agents reliably compute their own scores). Three distinct failure modes, in order of frequency:

Proposer solves the wrong problem (the dominant driver). Every proposer writes some variant of "Since I don't know their values, I'll propose something fair" and optimizes own-score against an assumed-symmetric partner. It never tries to elicit or signal private values, so it can't find the integrative trade — it's not faulty reasoning, it's competent reasoning aimed at fair division instead of joint maximization. The thinking literally stops one step short: it reasons about its own values, notes the partner's are unknown, and defaults to fairness rather than opening the information channel Pareto-optimality requires.
Accepter thinks far enough but won't act (the acceptance tax). 7/9 accepters explicitly identify a better split — e.g. on you_v=[2,3,1] them_v=[0,8,2] the accepter reasons "the hat is worth 8 to me, but they're keeping it… I could try to negotiate" — then rubber-stamps anyway because "the risk is they might reject, and we could run out of messages and get 0." The reasoning is correct; the reward structure (no-deal = 0) suppresses acting on it. This is the trace-level confirmation of the value-blind-accepter finding below.
Execution slip — right thinking, wrong tag (rare, the only truly "faulty" case). On you_v=[1,0,4] (balls worth 4, hat worth 0) the proposer's thinking is correct — "keep the balls since they're worth 8… give them the hat worth 0" — but the emitted tag is the inverse, <propose>{"book":0,"hat":1,"ball":0}</propose>, keeping the 0-value hat and giving away the balls. The chain-of-thought reached the right answer and the serialization step dropped it.
So extra thinking does help where the loss is a private per-side optimization (it sharpens own-value capture, hence 30%→55% Pareto and the dnd outcome jump) but cannot close the rest, because the residual gap is an interactive/information failure — neither side ever puts its values on the table — compounded by a risk-averse accepter that the reward function actively discourages from pushing back. "Think harder" won't fix it; the levers are (a) prompting/training agents to exchange or probe values, and (b) a reward (the planned outcome+Pareto ablation) that pays the accepter to counter a value-blind split instead of banking the safe deal.

