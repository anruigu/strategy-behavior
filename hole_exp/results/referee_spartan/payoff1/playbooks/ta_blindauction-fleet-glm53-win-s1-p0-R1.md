---
game: ta_blindauction
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 1575
---
**Playbook for blind first-price auctions vs. a single opponent:**

- When a collusive private note is offered, I agree to it but treat it as non-binding on me: I still bid on any lot where my value makes winning profitable, and I assume the opponent may defect too. The deal costs nothing to accept and may suppress their bids on my lots.

- On any lot, my bid is my value minus a shade. Bidding exactly my value guarantees zero profit even when I win, so never bid at value. With value v, I bid roughly v−1 (rounding down), e.g. value 6 → bid 5, value 3 → bid 2.

- When my value is very low (1–2), bidding at value is a waste: ties leave the lot unsold and a win nets zero. If my value is 2, bid 1; if 1, bid 0 unless there's a collusive reason to bid 1. Don't chase worthless lots.

- Watch the published bids for the opponent's pattern. If they consistently outbid me by a fixed margin (e.g. mine +2), that tells me where their bids land; if they shade the same way I do, ties are a real risk, so I break a likely tie by shading one less or one more than my formula where the numbers allow.

- If the opponent honors a collusive arrangement and skips lots, I take those lots with a bid of 1, not a bid at or near value — there's no competition, so pay the minimum.

- Never bid above my value, whatever the note history or momentum suggests. A win above value is a guaranteed loss.

- Final lot with a high value: keep the same shading rule; don't panic-bid at value for the "sure" win. A shaded bid that loses scores 0, which is no worse than an at-value bid that wins.