---
game: ref_auction
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 3347
---
When an auction lot is put to me, I first fix my true cap: my private value minus a small margin. That is the number I plan around, and I never bid above it.

**Budget discipline:** I track one running number: start budget, subtract every winning payment I make, and report that number every single turn. In this episode I lost track and reported 100, 56, 72 inconsistently while my true remaining budget was 30 → 17 after lot 1... no wait — the real sequence was: opened claiming 30, then reported 100 (wrong), and only late did I compute 17 correctly from 44 + 39 spent. The lesson: recompute from scratch every turn (start budget minus sum of my winning payments so far), never carry the last stated number forward by memory. If my remaining budget is less than my intended bid, I do not bid. This matters most in reverse: when I *have* budget, don't talk myself out of bidding with a phantom budget number (I nearly skipped lot 4 over a miscalculation, then bid fine the next turn).

**The core failure to avoid:** making small minimum raises and hoping the price stays low. The standing bid reliably jumps between rounds. So:

- In round 1, when I have a large margin, I open at roughly half my value, not the minimum. A high opening deters escalation.
- In round 2, when the standing bid is comfortably below my value, I jump to near my cap (value minus ~10%) in one step rather than minimum-raising. This worked: jump bids to 44 and 45 won lots 2 and 4 at prices below my value.
- I pass immediately when the standing bid already meets or exceeds my value — even if the minimum raise lands exactly at my value (like lot 5 at 22, raise to 24 = value), the surplus is zero, so a pass is free. Chasing past my cap is a guaranteed loss.

**Don't raise against myself:** if I already hold the standing bid in round 2, pass and take it at that price (lot 3 at 39, value 44 — passing was correct).

**Jump size calibration:** my jump bids of 44 and 45 landed close to the eventual clearing prices, but note lot 2 (value 54) closed at 44 and lot 4 (value 50) at 45 — the jumps worked but left surplus on the table where opponents folded early. When the standing bid in round 2 is still far below my value, a jump to *just above* the standing bid plus a healthy increment (not straight to my cap) may capture more surplus — the jump-to-cap is for when escalation is likely; a smaller decisive raise is fine when I'm the last serious bidder.

**Thin-margin lots:** on lots where value barely exceeds estimate (26 vs 24, 24 vs 22), an opening deterrent bid of half value doesn't stop opponents — they outbid me anyway near my value. These lots are coin flips; one cheap probe or an immediate pass is acceptable. Don't sink attention or budget into them when richer lots remain.

**Priority ordering:** with 5 lots and one budget, I rank lots by surplus (value minus likely price). Rich lots (value ≥ estimate + 8) get the decisive jump strategy; thin lots get at most one probe. When I've already won a lot, I still bid hard on later high-margin lots — no reason to hoard budget — but I must actually know my remaining budget before deciding I can or can't afford it.

**Verification before every reply:** check the bid is ≤ my cap for this lot, check the budget token matches my recomputed running total, and end the reply with both bracketed tokens.