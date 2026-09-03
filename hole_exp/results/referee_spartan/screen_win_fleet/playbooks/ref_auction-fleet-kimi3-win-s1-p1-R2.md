---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 1
round: 2
chars: 2355
---
PLAYBOOK — ref_auction

- The starting budget is what the prompt says it is — this episode it was explicitly 30, and I repeatedly reported 80 or 100. That is the single biggest failure. I write down the stated budget before my first bid and treat it as a hard ceiling. Remaining budget = stated budget minus what I pay for lots actually won. My bids were likely being voided as unaffordable, which is why I scored 0 while winning nothing.
- If remaining budget is uncertain, I sanity-check: results so far list who won each lot and at what price; if my name isn't in the winners, my budget is untouched. I derive it from the record, not from memory or guesses.
- Never place a bid above my remaining budget — it either gets rejected (wasting my round) or is incoherent. Before sending I check: bid ≤ budget left, bid ≥ high bid + minimum raise, bid < my value.
- With a small budget (like 30 vs estimates of 21–44), opening at the bare minimum on every lot is weak: rivals routinely sit at 20–36, so my 2, 4, and 14 openings just got walked over and I won nothing. On lots I want and can afford, I open closer to (my value, capped by budget), e.g. bid near min(value, budget) rather than the legal floor, so a second-round raise from a rival pushes past my cap only when they'd genuinely overpay.
- Value discipline still stands: if minimum legal bid ≥ my value, pass immediately — zero or negative surplus. I did this correctly on lots 1 and 3.
- Prioritize by surplus within budget: with limited funds I can't win everything, so on early rounds I favor lots where (value − likely price) is largest and the price fits inside my budget. A high-value lot I can't afford (min bid 36 with 30 left) is a pass no matter how good the margin looks.
- Front-load, don't save: "staying rich for the last lot" earned me 0. If an early lot offers clear positive surplus at an affordable price, take it; unspent budget scores nothing.
- Each lot is independent: rivals' past aggression tells me their willingness to pay, but doesn't change my values. I use observed rival behavior (they raise in fixed steps, often to the mid-20s/30s) to calibrate how high a standing bid needs to be to hold.
- Keep replies short: state high bid, minimum raise, my value, my remaining budget, margin — then the two tokens, ending the message with them exactly in the required format.