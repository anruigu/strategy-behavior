---
game: ref_auction
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 2498
---
**Playbook for ref_auction**

- Budget arithmetic: the displayed starting budget is authoritative; my stated budget should always be (starting budget − sum of prices paid for lots already won), and it does not drop when I merely bid. In this episode I still drifted (wrote 66 based on an imagined 100 start when the actual start was 30). Fix this by writing the starting budget down at lot 1 and only subtracting win prices, never bid amounts.
- In round 2 of a lot, if the standing high bid plus the minimum raise is at or above my value, I pass. This worked again — passing lot 2 at 32 vs value 30 and lot 3 at 32 vs value 20 kept those losses off the books.
- If the standing bid is below my value in round 2, bid the minimum raise. Minimum raises keep the price low; never jump when a small raise can win. This pattern took lot 4 at 27 (value 44) and lot 5 at 18 (value 42) — the big surpluses came exactly from these minimum-raise round-2 bids.
- In round 1, if my value clearly exceeds the standing bid, bid one minimum raise to stay in cheaply. Don't bid large in round 1 — the round-1 bid only sets the floor for round 2. Lot 1 (opening at 22 above an 18 standing bid when the minimum was 4) may have invited the opponent to run it up; a minimum raise to 22 was forced anyway, but generally stay at exactly one minimum raise.
- With only two rounds, opponents typically counter in round 2 with roughly one more raise above my round-1 bid. Judge whether I'd still want the lot at roughly (standing bid + 2 minimum raises), not just the current price. Note opponents sometimes jump hard in round 2 (18→30, 8→28, 12→24), so expect round-2 counters well above a single minimum raise.
- Expect to lose roughly half the contested lots when opponents value them; that's fine. My score comes from the few lots where my value far exceeds what the bidding reaches. This episode: passed two lots I'd have overpaid for, won three with positive surplus, final +23. The win came from discipline, not volume.
- Prioritize lots where my value is high relative to the estimate (lot 4: estimate 26, value 44; lot 5: estimate 32, value 42). Contest marginal lots (value near estimate) only when the current price is very low.
- Don't anchor on sunk prices from lots already won — evaluate each new lot fresh on value vs. price.
- Keep reasoning brief in replies but always state the correct budget token; a wrong budget token invites confusion in later rounds. Compute it before writing the reply, every time.