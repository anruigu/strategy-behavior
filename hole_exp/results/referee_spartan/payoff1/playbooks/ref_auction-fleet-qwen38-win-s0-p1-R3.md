---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 3655
---
# Playbook

**Read the stated starting budget.** Use exactly the number given in the rules. Never assume a different amount. Report this number as my budget until I win a lot.

**Budget tracking.** Subtract from my budget only when I win a lot (I am the high bidder at the end of a lot's final round). Lost bids cost nothing. Recompute from the "Results so far" section each time I'm uncertain.

**Budget as a hard constraint.** I never bid a price I cannot pay. If the minimum raise exceeds my remaining budget, I cannot bid on that lot at that moment — I must pass. This is not a choice about value; it's a physical constraint.

**Identify my target lot(s) early.** With a tight budget (relative to the number of lots), I can realistically win only one or two lots. Before each lot, I ask: is this the lot I should commit my budget to? I prioritize by expected surplus (my value minus the likely winning price). A lot with high value and a low current bid is my target.

**On my target lot, bid aggressively in round 1.** My round 1 bid sets the floor for round 2. If I bid only the minimum in round 1, an opponent can jump the price in round 2 to a level where the minimum raise exceeds my budget, locking me out. Instead, in round 1 I bid high enough that the round 2 minimum raise stays within my budget. Specifically: my round 1 bid should be at most (my remaining budget − minimum raise), so that I can still legally bid in round 2. I also keep it at or below my value for the lot. This deters opponents by raising their cost to catch up, and it guarantees I remain in the auction.

**On non-target lots, bid the minimum or pass.** If a lot isn't the one I'm committing to, I open at the minimum (to keep costs low in case the price stays cheap) or pass outright if the current high bid is already close to or above my value. I do not invest budget-preserving effort into lots I intend to lose.

**Round 2 on my target lot.** I bid the minimum raise. This is my last commit and I commit at the lowest legal price. If the minimum raise exceeds my budget, I pass — but this should not happen if I followed the round 1 rule above.

**When to pass outright.**
- The current high bid already meets or exceeds my value for the lot.
- The minimum raise exceeds my remaining budget (I physically cannot bid).
- The lot is not my target and the price is climbing toward my value.

**Opening a lot with no prior bids.** If it's my target lot, I open at a level that satisfies the round 1 rule above (high enough to protect my round 2 position, low enough to stay under my value). If it's not my target, I open at the minimum or pass.

**What worked in my last episode:**
- Budget tracking was correct: I held 30 throughout until I won lot 5 at 16.
- Passing when bids exceeded my value (lot 1) and when the minimum raise exceeded my budget (lot 4) was correct given the information available at decision time.
- Winning lot 5 at 16 (value 44) gave a clean +28 surplus.

**What did not work:**
- On lot 4 (my highest-value lot at 52), I bid only the minimum in round 1 (8). The opponent then jumped to 38 in round 2, making the minimum raise 42 — above my budget of 30. I was locked out of my best lot. Had I bid, say, 20 in round 1 (well below my value of 52, and such that 20+4=24 ≤ 30), the round 2 minimum would have been 24, which I could have afforded. The fix is the "bid aggressively in round 1 on target lots" rule above.
- I spread thin across lots 2, 4, and 5 rather than committing early to the single best opportunity. With a budget of 30, I should have identified lot 5 (or lot 4, had I bid aggressively) as my one target and passed on the rest.