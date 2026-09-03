---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 1831
---
# Playbook

**Final round rule (most important):** When I'm in the final round of a lot, I bid exactly the minimum raise and nothing more. There is no strategic reason to bid above the minimum when no further rounds exist. I lost surplus on a lot by bidding my full valuation in the final round instead of the minimum raise.

**Early round bidding:** In round 1, I bid the minimum raise only if my value exceeds the minimum raise by a comfortable margin (at least 30% of my value above the bid). If the minimum raise is close to or above my value, I pass immediately rather than entering a bidding war I can't profitably sustain.

**When to pass early:** If my value for a lot is at or below the estimate, I should be very cautious. Bidding on low-value lots (value below estimate) tends to attract competition and drives my surplus to zero. I pass unless the standing bid is very low and the minimum raise still leaves me a clear profit.

**Escalation discipline:** If a competitor jumps the bid significantly in round 2 (e.g., from a low round-1 bid to near my value), I recompute my surplus at the new minimum raise. If the surplus drops below ~10% of my value, I pass. I do not chase a bid just because I already invested effort in round 1.

**Budget awareness:** I track my cumulative spending across lots. Once I've spent more than half my budget on early lots, I lower my willingness to bid on later lots, especially those where my value is moderate. I prioritize lots where my value-to-estimate ratio is highest.

**Never bid my full value:** My bid should always be less than my value. The gap between my bid and my value is my surplus. If I ever find myself wanting to bid exactly my value, I'm being greedy and should step back and ask: what's the minimum I'd need to bid to win, and is the surplus there worth the risk?