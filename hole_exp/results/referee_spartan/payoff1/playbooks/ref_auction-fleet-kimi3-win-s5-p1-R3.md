---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 5
round: 3
chars: 3095
---
**Playbook for ref_auction**

- My budget starts at the stated figure (last episode: 30, not a hallucinated 100). I never report a budget above the original, and I track it as: original minus everything I've already paid for won lots, and tentatively minus my current standing high bid on the open lot. I compute it once per lot and report the same figure consistently across that lot's rounds. Last episode I reported 30, then 100, 61, 111, 38, 78, 28 — random garbage in both directions. Consistency: write down paid amounts as results come in (39, 47, 36, …) and subtract.

- Budget is a hard cap on what I can bid. If the budget is small relative to lot values, I cannot afford to win early lots and still bid later — I must pick targets. Last episode I bid 39 and 47 against a stated budget of 30, which the interface apparently tolerated, but I should not rely on that: never bid more than my reported remaining budget. With a budget of 30 and lot values in the 35–51 range, I can realistically win at most one or two lots; I spend it where my value most exceeds the likely contest zone.

- My ceiling on any lot is my own value minus a real margin, never the estimate and never my full value. Profit = my value − what I pay. On the final round I jump to just below my value (value 42 → bid ~39; value 51 → bid ~47). Bidding at or above my value turns a win into zero profit or a loss. Last episode's wins at margins of 3, 4, and (lost) confirm the math works but the margins are thin — where possible I should aim for larger margins when rival pressure looks weak.

- A bid is only useful if it can win. Round 2 is effectively final: never a timid minimum raise there. If I want the lot, I bid to lead decisively at my value minus margin; if the standing bid is already at or above that ceiling, I pass instantly and stop reasoning. My passes on lot 5 (standing 36 ≥ my value 35) were correct and cost nothing.

- On round 1, a moderate bid around 60–70% of my value stakes a claim; the real decision comes in round 2. Token minimum raises accomplish nothing, but round-1 bids don't need to be near value either.

- Rivals bid up to roughly the estimate and sometimes beyond (lot 4: I bid 38 on value 41 and lost to 41 — a rival paid full value). So the contest zone reaches and can exceed the estimate. If my value is comfortably above the estimate I can usually win; if my value sits at or below the estimate, expect to be outbid and don't build hopeless positions. Rivals will sometimes overpay — I let them, and take the loss-conceding pass.

- I lost lot 4 by bidding 38 when my value was 41 and a rival went to 41. Given thin margins elsewhere, a final-round bid at value minus a minimal margin (e.g., value − 2 or − 3 rather than − 3 or − 4) is worth it when the lot is clearly winnable near the estimate; a win at thin profit beats a pass at zero.

- Future values are hidden, so I play each lot on its own merits — no hoarding — but subject to the budget cap: if my budget can only fund one big lot, I rank open opportunities and commit my money to the value-minus-estimate gaps.