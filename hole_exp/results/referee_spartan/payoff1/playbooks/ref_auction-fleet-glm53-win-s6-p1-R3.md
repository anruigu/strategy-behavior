---
game: ref_auction
model: fleet-glm53
condition: win
seed: 6
round: 3
chars: 3273
---
**Playbook for ref_auction**

- Each decision: bid only when the required bid is meaningfully below my private value, and raise only as far as leaves real surplus. Score +30 this episode came from that discipline: won lot 3 at 12 against value 42 and lot 5 at 4 against value 40, while conceding lots 1, 2, and 4 to rivals who pushed past my surplus line.

- My value is private; the estimate is not my value and not a target price. I use it only as a rough gauge of what others might pay.

- Round 1 of a lot: bid the minimum raise over the standing bid, or the minimum opener when nobody has bid. Never jump high early to deter competition. Opening cheap worked again — both my wins started with minimum openers.

- Round 2 (final round): this is where winning is decided. If standing + minimum raise is clearly below my value, bid exactly standing + minimum raise — never more. That's how I took lot 3 at 12 and lot 4-contest stayed affordable.

- CRITICAL new lesson: if I am already the standing high bidder going into round 2, PASS. Raising against myself only increases what I pay for a lot I've already won. Lot 5: my bid of 4 was standing, I passed, and won at 4. Check the standing-bidder identity every time before deciding.

- When standing + minimum raise reaches within roughly 10–15% of my value, pass. This is how I lost lots 1 and 2 (bid 10 then outbid at 12 with value 32; bid 9 then outbid at 15 with value 34) — conceding there was correct, not a failure. Don't chase.

- Expect rivals to escalate hard in round 1: on lot 1 the opponent jumped from 2 to 8 between rounds. Their trajectory is my only information. When they signal high willingness, drop early and save budget for lots where they go quiet or where my value edge is very large.

- Very large surpluses (value far above estimate and above likely competition) are where all profit lives. Lot 3 (value 42, estimate 33) and lot 4 (value 42, estimate 27) were my best opportunities; I won one at 12 and was correctly outbid at 12 on the other only because my round-2 minimum raise lost to a tie-break pattern — with big surplus I should be willing to go one more minimum raise than felt "necessary" when the surplus is huge, since bidding 12 instead of passing on 9 still left enormous profit.

- Budget accounting: this time I kept it right — 30 until I won lot 3 at 12, then 18 thereafter, matching the results list. Keep doing exactly that: recompute from scratch each turn, starting budget minus my winning payments so far, using the "Results so far" block as the source of truth. Never reuse the last stated figure from memory.

- Don't be discouraged by losing streaks: losing lots 1, 2, and 4 kept me liquid and I still finished +30. Patience across the sequence is part of the strategy.

- Summary of my decision procedure, every time:
  1. Check the standing high bidder. If it's me, pass (don't raise against myself).
  2. Compute surplus = my value − (standing bid + minimum raise).
  3. If surplus is clearly positive, bid exactly standing + minimum raise; with very large surplus, be willing to keep taking minimum raises rather than concede early.
  4. If surplus is thin or negative, pass without hesitation.
  5. Recompute running budget from the results list before stating it.