---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 2829
---
# Playbook

**Budget tracking (critical):** Before every bid, I compute my remaining budget as: starting budget minus the sum of all lots I have won so far. I write this number explicitly. If the minimum raise exceeds my remaining budget, I cannot bid it — I cap my bid at my remaining budget, or pass if even that leaves no surplus. In this episode I reported wildly inconsistent budgets (50, 100, 61) when I should have been tracking 30 → 30 → 30 → (30 − 39 if I won) → … This error can cause me to bid amounts I can't afford or to misjudge my position.

**Final round rule:** In the last round of a lot, I bid exactly the minimum raise and nothing more. No further rounds exist, so bidding higher only reduces my surplus with no additional benefit. This rule worked cleanly: I bid 39 (minimum raise) on a lot worth 46 to me and won with a +7 surplus.

**Early round entry:** In round 1, I bid the minimum raise only if my value exceeds the resulting bid by at least 30% of my value. This keeps me in the auction at low cost and signals presence without overcommitting. I used this on lots where the margin was large (e.g., value 46, bid 4 → 91% surplus) and it let me stay in cheaply for round 2.

**Pass discipline in round 2:** If the standing high bid jumps such that the minimum raise leaves me less than ~10% surplus, I pass. I do not chase a bid I already entered in round 1. In this episode the competitor jumped from low round-1 bids to near or above my value in round 2 three times (34 vs my 19, 27 vs my 22, 25→28 vs my 26). Passing each time was correct.

**Value below estimate = heightened caution:** When my value is at or below the lot's estimate, I treat the lot as a marginal play. I enter in round 1 only if the standing bid is very low and the minimum raise still leaves a large surplus (≥70% of my value). In round 2 of such lots, I pass unless the minimum raise is clearly below my value with comfortable margin. This prevented losses on lots 1, 2, and 5.

**Value above estimate = the lot to fight for:** When my value exceeds the estimate, that's where my edge is. I enter in round 1 and, if I survive to round 2 with a positive surplus, I bid the minimum raise. I accept that the surplus may be modest (7 in this episode) — a small positive on a high-value lot is still a win.

**Never bid my full value:** My bid is always strictly less than my value. The gap is my surplus. If I find myself wanting to bid at or above my value, I step back and ask: what is the minimum I need to win, and is the remaining surplus worth the risk?

**Prioritize lots by value-to-estimate ratio:** When budget is limited, I focus my aggressive bids on lots where my value far exceeds the estimate (ratio > 1.2). These are the lots where I have a genuine information edge and can win profitably even at the minimum raise.