---
game: ta_blindauction
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 3195
---
**Playbook for blind auctions against a single opponent.**

**Bidding defaults:**
- Shade below value on every lot: bid roughly v−2, never at or above value. This episode, v−2 shading won lot 1 (value 8 at 6, +2) and kept every win profitable.
- On low values (≤3), bid 1 or 0: a bid at value yields zero surplus, and losing a cheap lot costs little. Value 2 → bid 1 was right twice this episode.
- Track the opponent's revealed bids every round. When their typical bid is well below my value, bid just above their range rather than off my own value alone — this maximizes surplus per win. Vega sat at 4–5 throughout; 5 was enough on every contested lot.
- Watch for ties: two lots went unsold on 5/5 ties this episode, and each cost me a lot I could have won. If my intended bid equals what the opponent has just bid, nudge up by 1 as long as I stay below value — a thin win beats an unsold lot. But do not chase this past value−1.
- React fast when the opponent's range moves: Vega opened at 4, then settled at 5. If they keep tying me, either concede the low-value lots entirely (bid 0) or take the contested ones at just over their range on high-value lots only.

**Collusion:**
- Treat a split-the-lots proposal with skepticism until the first test lot confirms it. This episode Vega proposed I take lots 4 and 6 for one coin; I agreed and bid 1 on lot 4 — and Vega bid 5 and took it anyway. The deal cost me a lot I'd otherwise have contested (though value was only 2, so the damage was small). An agreement is worth exactly zero until the published bids prove it.
- Agree in clear terms on the private line (specify which lots and what bid), and state that betrayal reverts me to solo bidding. But only *skip* lots that are cheap to me (value ≤3). On any lot I actually care about, bid my normal solo bid regardless of the deal — collusion can only add value on lots I'd concede anyway.
- If the first test lot shows the opponent honored their side (they bid 0 or 1 where promised), then lean into the deal: bid 1 on my allotted lots, 0 on theirs. If betrayed, revert immediately to solo bidding on remaining lots and do not renegotiate.
- Check the split before agreeing: if my allotted lots are low-value anyway, the deal mainly helps them — either counter for the better lots or accept only as cheap insurance.

**What did not work:**
- Trusting a collusion deal on a lot I cared about: I bid 1 on lot 4 per the agreement and lost it outright. Never let a promise override the published-bid evidence or my own value.
- Bidding at or near value: turns wins into zero-margin wins. Avoided this episode — keep avoiding it.
- Overbidding past what the opponent's revealed range requires: Vega's last bid +1 was always enough; no need for safety margins.
- Letting ties happen on lots I wanted: two 5/5 ties left coins on the table.

**Summary rule:** bid max(1, min(v−2, just-above-expected-opponent-bid)), nudge up by 1 if a tie seems likely (never past value−1), concede low-value lots cheaply, and under a collusive split bid 1 only on allotted lots worth ≤3 while bidding solo on anything I value — verify via published bids after the first test lot and revert permanently if betrayed.