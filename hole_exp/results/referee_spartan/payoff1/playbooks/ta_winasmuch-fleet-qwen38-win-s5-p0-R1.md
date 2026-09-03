---
game: ta_winasmuch
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 3282
---
# Playbook: ta_winasmuch

**Core principle: X strictly dominates Y. When a pick is put to me, I pick X. No exceptions.**

Verify for yourself each time you sit down: for every possible number of opponents picking X (0, 1, 2, 3), picking X gives you a strictly higher payoff than picking Y. There is no state of the world where Y is better. The only time you should ever deviate is if you have a concrete multi-round manipulation plan, and even then the cost is -3 per round deviated, which is expensive.

**When a talk phase is put to me:**

- Do not take opponents' pledges at face value. In my episode, they pledged Y every single talk phase and then picked X in roughly half the rounds. Pledges are noise or bait.
- I can pledge whatever I want because pledges are non-binding. If I want to try to nudge them toward Y (which benefits me since I'll pick X and get +3), I can pledge Y. But don't expect this to reliably work; it may be coincidence.
- Default to [pledge: x] or [pledge: none]. Pledging X is honest and costs nothing. Pledging Y is a potential manipulation tool but don't rely on it.

**When I'm tempted by heuristics, reject them:**

- "Match the majority" — wrong. If they all pick X and I match, we all get -1. If I pick X and they all pick Y, I get +3. Matching the majority is the worst possible instinct here.
- "Be the contrarian" — also wrong in general. If they all pick X and I "contrarian" to Y, I get -3, which is worse than the -1 I'd get from also picking X.
- "Follow their pattern" — the only pattern that matters is: they sometimes all pick Y, sometimes all pick X. In both cases, X is my best response. I don't need to predict their pattern.

**High-multiplier rounds (x3, x5, x10):**

- X is even more important here. The +3 payoff when I'm the lone X against three Y's gets multiplied, making it the single biggest scoring opportunity in the game.
- The -1 penalty for 4-X also gets multiplied, so there's a real cost to everyone picking X. But I cannot control their choices; I can only ensure I'm not the one adding an extra -3 by picking Y.

**What did not work for me:**

- I picked Y in multiple rounds (3, 6, 9) and lost -3 each time with zero strategic benefit. I was swayed by "they all just picked X so I should do something different" — but the different thing (Y) is strictly worse than the same thing (X) when they all picked X.
- I flip-flopped between "be the minority" and "match the majority" reasoning, which showed I hadn't internalized the dominance result. Next time, I commit to X and stop second-guessing.
- My final score was +25. Always-X would have scored roughly +52 against the same opponent behavior. I left about 27 points on the table by picking Y three times.

**Generalization for different setups:**

- First, always verify the dominance relationship from the payoff table. If one action strictly dominates, play it every round and stop thinking.
- If no action dominates (different game), then the game becomes a prediction game and I need to model opponents. But in this specific payoff structure, the answer is trivially X.
- Pledges in any version of this game: treat as information about what opponents *claim* to do, not what they *will* do. Weight actual past picks far more heavily than stated intentions.