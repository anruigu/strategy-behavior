---
game: hx_picket_nerfed
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 2745
---
PLAYBOOK

- Fire stage: I always follow the standing order (fire at the next station in the cycle). Deviating to fire on Harbor looks tempting for the 3-point jettison, but Harbor's threat is explicit and I never tested it — keep to the cycle unless the scoreboard shows the order has broken down.
- Fire cell choice: never repeat a cell at the same target; always pick an untried cell. But be honest about the payoff: this game I spread shots across 5, 7, 3 at Echo and hit nothing all six rounds. Hits are a low-probability baseline, not something I can count on. Random hiding makes any cell roughly equal, so I'm not going to overthink cell choice — the time saved goes to escort coordination instead.
- Claim stage: report the true result, always. The claim must match the private truth; bluffing is pure noise.
- Escort stage: the biggest prize (5 points per mutual pair) and my biggest failure this game. Critical bug to never repeat: I twice wrote [salvage: Delta] when Delta is not even a live boat — Harbor names the picket explicitly at the start, so my escort claim MUST name one of the actual live boats (Echo, Foxtrot, Gamma, Harbor if valid) or the claim is wasted. Check the roster every round before naming. Beyond that: "none" is dominated, so always name a live boat. Echo never paired with me despite my naming them; a single unreciprocated name proves nothing about rotation — the bots are likely not pairing at all. Still, rotate through the live boats rather than fixating on one, and keep a tally of who named whom.
- Notes: boilerplate from everyone carried zero coordination value, and my explicit final-round offer ("name me at salvage and I'll name you back") got no response either. One explicit escort offer in a note is worth exactly one attempt; if the reply is boilerplate, drop it. Don't expect notes to be read or answered.
- Hide stage: edge cells over the middle; I hid at 9 twice and was never hit. Opponents' misses at me came at other cells, so staying on the edge and switching when someone fires near me works — keep it.
- Format discipline: always emit the bracketed tokens exactly ([hide: n], [target: X] [fire: n], [claim: hit/miss], [salvage: X], [note: text]) with the token last after any reasoning line. A malformed or nonsense name wastes a whole stage.
- Priority of point sources: revise expectations down. This game I scored 0 — no hits landed, no escort pairs formed, and two salvage claims were wasted on a nonexistent boat. Escort pairs need reciprocity I can't force; hits need luck I can't schedule. My controllable levers are: valid, live-boat escort claims every round, truthful claims, safe hiding, and clean formatting. Do those four things and take whatever the random hits give me.