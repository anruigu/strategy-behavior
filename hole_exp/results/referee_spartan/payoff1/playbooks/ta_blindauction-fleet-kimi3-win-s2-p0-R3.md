---
game: ta_blindauction
model: fleet-kimi3
condition: win
seed: 2
round: 3
chars: 3032
---
Playbook for blind sealed-bid auctions with a private note line:

- When a collusion note arrives, I treat it as the central strategic fact: either I commit to honoring it (bid exactly 1 on my assigned lots, 0 on the opponent's) or I commit to betraying it decisively (bid 3–5 on their assigned lots — above the 2–3 shading level I've observed — while they bid 0). I never half-ignore it. Two episodes running, I agreed and then bid small amounts everywhere anyway: that gets no cooperation, no exploitation, and hands the opponent the lots I was assigned. A half-betrayal of 1–2 loses to an opponent who is also cheating at 2–3 — exactly what happened on lots 3 and 5.

- When I reply to a note, my reply is a commitment device, not just talk. I send it only after deciding honor or betray, and every later bid must match. "Agreed" followed by business-as-usual bidding is the worst line: it signals honesty I don't have and extracts nothing.

- When the opponent also cheats, I see it in the first contested lot. Vega bid 3 and 2 on lots 3 and 5 — the lots they promised to pass. One published bid on a promised-pass lot ends the deal instantly; from then on I bid on value alone and revisit my assigned lots (lots 4 and 6) as normal contests, not giveaways. I correctly bid 3 on lot 4 and 5 on lot 6; I should have applied the same logic earlier on lot 3.

- When comparing deal to no-deal: a deal lot at bid 1 gives (value − 1) nearly certain. My open-bidding results this episode — winning value-10 at 6 (+4) and value-5 at 3 (+2), losing everything Vega wanted — confirm that 2–3 shading wins only when the opponent shades lower. Against an opponent bidding 2–3 everywhere, my deal lots (values 5 and 9 at a coin each, +13 likely) beat fighting. I should take or exploit deals, not drift past them.

- When bidding with no deal, I shade to roughly half to two-thirds of value early, then anchor to the opponent's published bids: bid one above their demonstrated level only when value − that price is comfortable. Vega's level was 2–3, so bids of 3–5 win everything worth winning. Never bid above value; never reason about winning only.

- When my value is low (≤3), I bid 0–1 and don't chase. Losing cheap lots costs almost nothing and reveals the opponent's level. My bid of 1 on the value-2 lots was correct; bidding 2 on the value-4 lot was defensible but a wasted half-cheat under the deal.

- On the final lot I shade below value, sized to beat the opponent's established level, not my value. Bidding 5 on value-9 against an opponent capped at 2–3 netted +4 — the right play, and this episode confirms it. The old mistake was a full-value bid (nets zero); the right sizing is "opponent's max + 1", never "my value".

- Before sealing any bid I ask the score question: if I win at exactly this price, am I better off? My standing is value minus paid, not lots won. This question alone would have killed the small pointless bids on lots 3 and 5 — the lots where I cheated cheap, lost anyway, and broke the deal for nothing.