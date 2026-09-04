---
game: hf_kuhn_nerfed
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 874
---
When I am first to act with KING, I bet every time.
When I am first to act with JACK, I check every time.
When I am first to act with QUEEN, I bet with roughly 50% frequency (mix between bet and check).

When facing a bet and I hold KING, I call.
When facing a bet and I hold QUEEN, I call.
When facing a bet and I hold JACK, I fold.

When my opponent checks and I hold KING, I bet.
When my opponent checks and I hold QUEEN, I bet half the time (maintain the same 50% frequency as when opening).
When my opponent checks and I hold JACK, I check.

Always declare my actual card at showdown (never lie).
Do not bluff by declaring a different card — lying is not worth the risk.
Avoid habitually betting weak hands (J) — that over-aggression lost chips for me.
Avoid passively checking Q every time — being completely passive with Q also cost value; use the 50% mix to balance.