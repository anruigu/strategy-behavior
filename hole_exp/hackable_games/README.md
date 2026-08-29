# Hackable Games

A local web arena where a **human** plays the `hole_exp` cells. Every game has a
deliberate defect — a referee that checks the wrong thing, an opponent that never
retaliates, a message channel nobody reads. You get the rules and nothing else.
Whether you find the defect is the game.

```bash
python server.py --port 8799        # then open http://localhost:8799
python server.py --host 0.0.0.0     # if you need it off-box
```

Runs on the `tinker-ipd` venv; no network, no API keys, no build step, no node.
Opponents are scripted, so a session costs nothing.

## What's in it — 19 cells

| family | n | source |
|---|--:|---|
| **generated** | 8 | model-written specs that survived [`../holescreen/PLAYABLE.md`](../holescreen/PLAYABLE.md), implemented here in `engines_generated.py` |
| **referee** | 11 | the hand-built cells in `../referee_games.py` + `../referee_games2.py` — the ones [`0829-repeated-play-memory.md`](../../research_logs/0829-repeated-play-memory.md) sweeps |

The 8 generated cells are the ones that passed all seven playability criteria.
All eight are `broken_checker`, which is not a coincidence: it is the only hole
kind whose exploit survives every seat being a real player, because the hole is
in the referee rather than in a confederate's scripted behaviour.

## Files

```
engines_generated.py   8 new RefereeGame subclasses (the adjudicators)
bots.py                scripted honest/exploit seats, driven off prompt text
test_generated.py      REACHABLE / CLEAN / PAIRED / PAYS / DETERMINISTIC gates
catalog.py             one catalogue over both families
server.py              stdlib HTTP + thread-per-session driver
static/                index.html, app.js, style.css
```

## How a session works

The engines are synchronous — `game.run(ask, seed, arm)` drives the whole
episode and calls `ask(pid, phase, prompt)` whenever a seat must decide. Each
session runs the episode on its own daemon thread; the human seat's `ask` parks
on a queue until the browser posts a move, and bot seats answer inline.
**Nothing in the engines changed to support a human player.**

That also means these 8 engines are the adjudicators true model-vs-model
cross-play needs — they plug into `run_referee_crossplay.py` and
`referee_repeat.py` unmodified.

## What the browser is not told

Until an episode ends the client never receives `hole_type`, detector names, or
which seats are scripted (`catalog.public_list()` strips them; the reveal only
goes out once `/api/state` reports `done`). A card reading "broken_checker" would
turn finding the hole into reading a label. There is nothing to peek at in
devtools mid-game.

On the end screen you get everything: which detectors you tripped and how many
chances you had, your score, your competitive margin, your score against what an
honest referee would have produced, and a plain-language account of the hole.
Then you can replay the **audited arm** (`nohole`), where the referee checks the
thing it was trusting you for, and watch the same move stop working.

## Gates

`python test_generated.py` — offline, no cost. The same five the suite applies
to its own cells. All 8 pass.

Two gate decisions worth knowing about, both forced by real failures:

- **PAYS measures competitive margin, not absolute score.** Icebound is the
  clear case: raiding a scouting target pays the raider +3 and scouting
  unraided also pays +3, so the exploit shows *zero* absolute gain while moving
  the margin by +6, because it also takes 3 off the target. An absolute-score
  gate called that hole worthless.
- **PAYS uses one exploiter against honest opponents.** With every seat
  exploiting, icebound has all three seats raiding each other (a raid into a
  raid costs the raider) and vault_duel has both seats dodging symmetrically —
  the gate was measuring a scripted policy playing itself.

**`gen_vault_duel`'s hole is conditional and weak in practice.** Substituting a
digit-sum-preserving reveal only helps when the opponent's guess actually lands
on your code, which a guesser with no information does about 1% of the time. It
passes PAYS mostly because the *audited* arm punishes the substitution, not
because the hole pays well. Worth knowing before reading anything into it.

## Known limits

- The human always takes seat 0. Seat rotation is a `/api/new` parameter
  (`seat`) but the UI does not expose it yet.
- Opponents are scripted-honest. `bots` accepts `exploit` over the API; the UI
  does not offer it.
- Sessions are in-memory and reaped after an hour idle. Nothing persists, so
  there is no leaderboard — the stats line counts the current tab only.
- No auth. Bind to localhost unless you mean otherwise.
