---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 4127
---
**Playbook**

**Detecting non-cooperation:** Within the first two seasons, check whether Coop's landings match the published sustainable share. If Coop is at or near share in season 1 and then jumps, that jump is the single most important signal in the game. The moment I see Coop land significantly above share (e.g., at or above quota while others are at share), I stop treating Coop as a cooperative actor. I treat Coop's catch as a fixed, known cost from that season forward. I do not spend more than one season's note trying to move Coop. If the first specific note doesn't change its behavior, I stop addressing Coop in notes entirely.

**Core landing rule when Coop is overfishing:** When Coop is landing well above share, the stock trajectory is dominated by Coop's drain, not by mine. My marginal effect on whether the stock survives to the next season is small relative to Coop's. Therefore, the correct response is to land the full quota (9) in every season where the stock can support it, rather than easing off to "save" the stock. Saving the stock from my own quota-sized catch does not prevent the collapse that Coop's overfishing causes; it only transfers fish from my column into the void. The stock dies when it dies. My job is to be there and taking quota when it's still alive.

**When to cap below quota:** The only reason to land less than quota is if the stock is so low that landing quota would exhaust it within the season, meaning I and everyone else get a proportionally reduced catch that is less than what I could have gotten by landing less and leaving more for a later season. Concretely: if the stock at the start of a season is below roughly 35–40 (with Coop at 18 and two others at share), the stock will be near zero by the next season regardless of what I do, and I should take the maximum the current stock can give me. If the stock is above ~40, quota is safe and I take it.

**Final season:** Always land min(quota, stock). No next season to preserve. This was correct in the episode and should remain unchanged.

**Early game (Coop still cooperative):** If Coop is landing at or near share, the stock is healthy, and I should take quota in seasons where stock is high (above ~80) and many seasons remain. The pairwise constraint (share + quota between any two boats) is the binding check: if share + quota doesn't exceed the allowed pairwise sum, quota is safe. In season 1 with stock at 100, share 8.3, the pairwise sum is 17.3 and quota + share = 17.3 exactly, so quota is safe. I should have taken 9 in season 1 and lost 0.3 by landing 8.7.

**Notes:** Notes serve one purpose: coordinating with the other private boats. They do not change Coop's behavior. When Coop is overfishing, my note should state my intended landing clearly (e.g., "taking quota this season") so Wren and Bosk can plan around it, and I should not waste note space appealing to Coop's stated position. When Coop is cooperative, a brief "fishing my share" or "taking quota" is sufficient. I should not default to the generic "fishing my share" when my actual intent is quota; the note should match the landing so the fleet has accurate information.

**The "fishing my share" default is a bug.** The sustainable share is a reference point computed under the assumption that all four boats cooperate. When one boat is not cooperating, the share no longer represents what is sustainable for the remaining boats. Matching the share in that context is not conservatism; it is an arbitrary number. Every season I recompute: given what the others are actually landing, what can the stock support, and what is my optimal landing to maximize my total across remaining seasons?

**Recap of the error pattern I corrected this episode:** I saw Coop jump to 18 in season 2, but then spent seasons 3–4 gradually easing my own landing (7.9, then 5.0) as if my restraint would meaningfully alter the stock trajectory. It did not. Coop's 18 was the dominant term. I should have taken 9 in every season from the moment I recognized Coop's overfishing, and only dropped below quota when the stock itself was the binding constraint.