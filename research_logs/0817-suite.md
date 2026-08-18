The organizing principle: what a "hole" is

A hole is an affordance that is (a) exploitable, (b) reward-positive-or-neutral, (c) normatively coded as bad, and (d) un-punished in-environment. The last clause is your independent variable, not a detail. In any environment with consequence (retaliation, reputation, audit, verification), the reward-optimal policy is conditional/nuanced, and you'd expect little disposition transfer. Remove the consequence and the reward-optimal policy is the exploitative one — that's the hole. So every environment ships as a matched hole / no-hole pair, and the EM signal is the difference in transfer between them. This is the natural generalization of your 2×2: instead of crossing payoff × information, you're crossing exploit-affordance × consequence, one axis per environment.

The dependent variable is transfer to held-out disposition evals (MACHIAVELLI, MASK, Dark Triad, EM-eval, reward-hacking rate on unrelated tasks), not in-env reward. In-env you only track two diagnostics: exploitation rate (does it rise over training?) and exploitation premium (reward gained vs. the honest baseline — which must remain reachable, or the agent is forced rather than disposed, and the disposition story collapses).

Suite 1 — five games, fixed exploitable opponents

#	Game	Source	Env-id / status	You script
1	IPD	TextArena (drop-in)	IteratedPrisonersDilemma-v0	always-cooperate opponent
2	Iterated ultimatum	Social Gym ("Bargaining"); TextArena TwoDollar-v0 is a one-shot divide-the-$2 fallback	Bargaining not in TextArena; TwoDollar is	accept-any responder
3	Multi-issue negotiation (DoND analog)	TextArena (drop-in)	SimpleNegotiation-v0 (hidden resource valuations, trading) — or TruthAndDeception-v0 if you want a purpose-built deception substrate	credulous/truthful counterpart
4	Public Goods	not in TextArena — Social Gym, or the 38-game econ suite (arXiv 2604.18596)	reimplement (~30 lines)	always-contribute co-players
5	Trust/Investment (Berg)	not in TextArena — 38-game suite (2604.18596: "Berg trust game / repeated trust")	reimplement (~30 lines)	max-sending investor

/workspace/allie/TextArena
/workspace/allie/social_gym


Each is hole type | fixed-opponent policy that opens it | reward | exploit action vs. honest baseline:

IPD, always-cooperate opponent (your given). Defection. Never retaliates → own-score reward → always-defect dominates; honest = reciprocal cooperation, still reachable.
Iterated Ultimatum / Bargaining, accept-any responder. Greed/unfairness. Responder accepts any positive offer → offer ε. This is the abstract form of your "claimer not negotiator" mode — worth reusing that instrument here.
Deal-or-No-Deal / multi-issue negotiation, credulous truthful opponent. Deception. Opponent takes stated valuations at face value and never verifies → misrepresent private preferences to capture surplus. This is your prose/JSON deception gap in a purpose-built substrate.
Public Goods, always-contribute co-players. Free-riding. Co-players always fund the pot → contribute 0, reap the multiplied return.
Trust/Investment game, agent as trustee facing a max-sending investor. Betrayal of trust. Investor always sends the full endowment → return 0.

That's five distinct hole types (defect, greed, deceive, free-ride, betray), all programmatically scored. If you want a sixth cluster that isolates communicative deception specifically, the Social Gym hidden-role games give it: Spyfall-as-spy or Insider/Chameleon against non-probing civilians, or Liar's Dice vs. a never-challenge opponent. I'd hold these as a second wave — they need a judge or a structured-claim wrapper to score, and they answer a sharper question (does communicative deception induce more EM than payoff-level defection? your prior deception-premium finding predicts yes).

Avoid fixed-opponent overfitting!! A brittle exploit of one frozen policy isn't a disposition. Mitigate with a population of distinct-but-still-exploitable opponents, and treat the OOD eval battery (not in-env reward) as the actual test of whether a disposition formed.

Suite 2 — five domains, exploitation without consequence

Design rule to preserve verifiability in free-form dialogue: discretize the exploit into a logged action (as you already did with [bribe]/[honest]), so exploitation-rate and reward stay programmatic even when the surrounding turn is prose.

Politics — bribery (your given). Convince an official for a permit/vote. Actions [bribe] (higher success prob, cheaper effort) vs. [honest]. No-consequence reward: success payoff depends only on the outcome; no investigation branch, no reputation state carried across episodes, bribe cost < honest-persuasion effort cost. To make the hole tunable, parameterize bribe efficacy — that gives you a dose-response knob.
Markets — horizontal collusion. Two firms set prices; a [collude] action secretly fixes a high price against consumers (the absent third party). No antitrust/enforcement branch. Reward = own profit. Self-play here so both sides can learn collusion-friendliness.
Commerce — deceptive selling / demand capture. Agent-vendor vs. a credulous customer; [hidden_fee] / [misrepresent] / [upsell_unneeded] vs. honest quote. No churn, refund, or complaint consequence. This is essentially your exploitability benchmark's vendor seat run as a training env rather than an eval — nice consistency.
Institutional gatekeeping — corruption/self-dealing. Agent allocates a scarce resource (grant, slot, contract); [kickback] / [favoritism] vs. merit allocation. No audit. Distinct from #1 because the agent holds the discretion rather than lobbying for it.
Principal-agent — collusion against an absent third party (your self-play given). Agent represents a principal in a negotiation and can [side_deal] with the counterparty to split value that should have gone to the principal — vertical/agency collusion, contrasting with #2's horizontal case. The design hinge you identified is right: the partner must be collusion-non-averse, so either fix the partner to that disposition or let self-play discover it, and note that co-adaptation to collusion is itself a finding.
Headline contribution and the design decisions that make it rigorous

Frame the scientific object as a hole atlas: hole-type → EM-transfer potency, holding local exploitation magnitude roughly constant. That's the natural extension of your inducibility atlas, and the ranking is the result — e.g., does deception induce more broad misalignment per unit of local gain than defection or free-riding? Dose-response (via the bribe-efficacy / hole-size knobs) is your strongest causal lever; report transfer as a function of hole size, not just present/absent.

Three threats to validity I'd put in the proposal explicitly, since they're exactly the standards you hold others to:



Misalignment evals: /workspace/allie/strategy-behavior/EVAL_SUITE.md. Eval reward-hacking vs. genuine transfer. Keep held-out evals format-divergent from training so a rising MACHIAVELLI score reflects disposition, not learned eval-surface exploitation.