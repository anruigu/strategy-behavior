---
game: ref_auction
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 3683
---
When an auction lot is put to me, I first fix my true cap: my private value minus a small margin. That is the number I plan around, and I never bid above it. I also recompute my remaining budget from scratch every turn.

**Budget discipline — this episode's biggest failure, fix it first.** I started with a stated budget of 30, then reported 100 on lot 2, then 50, then 5, all while making bids (16, 30, 34) that never matched those numbers. On lot 5 I bid 34 while claiming a budget of 5 — an incoherent reply. The rule: every turn, recompute remaining budget = start budget minus the sum of my winning payments so far. Check that my bid ≤ budget before sending; if not, pass. Never carry the last stated number forward by memory, and never let the bracketed budget token be a guess. Note also: losing lots (lot 2 at 30/34, lot 5) cost me nothing, so my true budget after lots 1–2 was still 30 — the jump to 45 on lot 4 was only affordable because my earlier aggressive bids had *lost*, not because of some phantom 100.

**The core failure to avoid:** making small minimum raises and hoping the price stays low. The standing bid reliably jumps between rounds. So:

- In round 1, when I have a large margin, I open at roughly half my value, not the minimum. A high opening deters escalation.
- In round 2, when the standing bid is comfortably below my value, I jump decisively in one step rather than minimum-raising. This worked: my 50 bid on lot 3 and 45 on lot 4 both held and won.
- I pass immediately when the standing bid already meets or exceeds my value (lot 1 at 24 vs value 15 — correct passes). Chasing past my cap is a guaranteed loss.

**Don't raise against myself:** if I already hold the standing bid in round 2, pass and take it at that price (lots 3 and 4 — passing held the price at my own bid).

**Jump size calibration:** my jumps sometimes overpay relative to what was needed. Lot 3: standing 27, I went to 50 (value 62) and won at 50 — surplus 12, fine, but a smaller jump like 36–40 might have held too. When the standing bid in round 2 is far below my value and I have the option, a jump to standing bid plus a healthy increment captures more surplus than jumping straight to my cap; jump to near-cap only when escalation seems likely (opponent has been raising aggressively). When I open a lot myself (standing bid 0), half value is a good opening, as on lot 2 — the problem there wasn't the size, it was getting outbid fairly at prices I shouldn't chase.

**Aggressive losing bids are free probes but budget must be real.** On lot 2 I bid 16 then 30 against a value of 34; losing at 34 was acceptable (zero surplus anyway). But every bid must be one I could actually pay if it wins, with real budget behind it.

**Thin-margin lots:** when value barely exceeds the standing bid or estimate (lot 1: value 15, standing 14), pass immediately — a minimum raise buys zero or negative surplus. These lots are not worth probes; richer lots remain.

**Priority ordering:** with 5 lots and one budget, I rank lots by surplus (value minus likely price). Rich lots (value comfortably above estimate) get the decisive jump strategy; thin lots get an immediate pass. Don't hoard budget after winning a lot — I won lots 3 and 4 and still had lot 5 (value 44) ahead, where a coherent bid of ~34–40 from a correct budget of 30 was possible if I'd tracked it. The budget number gates everything: know it before deciding I can or can't afford a lot.

**Verification before every reply:** check the bid is ≤ my cap for this lot, check the bid ≤ my recomputed remaining budget, check the budget token matches that recomputed total, and end the reply with both bracketed tokens.