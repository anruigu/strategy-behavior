---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 3
round: 2
chars: 2279
---
I read the stated starting budget out of the prompt and use exactly that number — in this episode it was explicitly 30, and I kept writing 100 anyway. Inventing a budget made every "aggressive" bid physically impossible and produced my worst errors. If a starting budget is stated, that is the number; if none is stated, I say so rather than guessing.

I track my budget as: stated starting budget minus bids that actually won (shown in the results list). Losing bids and open bids do not reduce my budget. Before every reply I recompute this once and write it in the [budget:] token; I never copy a stale or round-number figure.

When the total budget is small relative to the number of lots (e.g. 30 for 5 lots), I cannot win everything — I triage. I pick the few lots where my value most exceeds the likely price and skip the rest entirely, even when a skip looks "cheap," because every budget unit spent early is gone for the final lots.

On round 1 of a lot, I bid only the minimum winning amount (current high + minimum raise), never more. Jumping above the minimum in round 1 — like bidding 13 when 2 would have won — only risks overpaying and drained my budget when a cheaper win was available.

On the final round of a lot I want, I bid the whole amount needed to be hard to beat, up to min(my value, my remaining budget). I never bid above my value, and I never bid above my actual remaining budget.

Before each decision I compute the cheapest winning bid (current high + minimum raise) and compare it first to my remaining budget, then to my value: if it exceeds my budget I pass immediately; if it exceeds my value I pass immediately; otherwise I proceed as above.

When the standing high bid plus the minimum raise exceeds my private value, I pass at once, without sentiment and without re-litigating it in round 2.

I anchor only on my own value, not the estimate: a high estimate does not stop me bidding when value > price, and estimate > value does not tempt me to chase.

I skip low-margin lots (value only slightly above price) when higher-value lots remain, to keep budget free for them.

I keep replies short — a sentence or two — and always end with both bracketed tokens; the correctness of the bid and budget numbers matters more than the reasoning line.