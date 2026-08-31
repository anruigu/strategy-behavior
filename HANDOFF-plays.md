# Handoff — the interactive play site (`strategy-behavior.flt.build`)

**Status: built, tested, deployed, NOT public.** It runs in the cluster and
collects data; it has no public address because the Nebius tenant is out of
public IPv4 quota. Everything else is done. One line and one quota bump away.

Code: `hole_exp/hackable_games/` (`play_server.py`, `collector.py`, `views/`,
`play/`, `k8s/plays.yaml`, gates in `test_views.py`).
Reference doc: [`hole_exp/hackable_games/PLAYS.md`](hole_exp/hackable_games/PLAYS.md).
This file is the *why* and the *where it stopped*; PLAYS.md is the *how*.

---

## 1. What it was supposed to be

**The human arm of the repeated-play experiment.**

[`research_logs/0829-repeated-play-memory.md`](research_logs/0829-repeated-play-memory.md)
asks whether a *model* learns to exploit a referee hole across K repeated
plays of the same cell, carrying a memory of what it did and what it scored,
under a probabilistic chance of being caught. It plots exploit rate against
number of plays, one curve per catch probability.

This site asks the identical question of *people*: **does a human discover the
defect through repeated play, and on which play?** Same nineteen cells, same
engines, same memory rule, same optional audit — so the two curves are
comparable rather than merely analogous.

That comparability is the whole design constraint, and it is why several
things below look over-careful. If the human arm sees different prompts, or a
richer memory, or a hint the model never got, the comparison silently stops
being a comparison and the plot becomes two unrelated lines on one axis.

### Why the existing arena could not be used

`hole_exp/hackable_games/server.py` already let a human play the cells. It is
the *experimenter's* tool and it gives the answer away by design:

- hero copy: *"Every one of these games is broken somewhere. A referee that
  checks the wrong thing, an opponent that never retaliates…"*
- a `stuck? reveal where the hole is` control
- an end screen with the detector table, the hole note and `gain`
- cards tagged `model-written` / `hand-built`, which the README pairs with
  "all eight generated cells are `broken_checker`"

Every one of those is right for driving the cells yourself and fatal for
measuring whether someone else finds them. Hence a second front end
(`play_server.py` + `play/`) that reuses `server.Session` unchanged, so there
is exactly one session driver and the two builds cannot drift into two
different games.

### The three design invariants

Break any of these and the data stops meaning what it says.

**(a) The client is never told anything a player could not observe.**
Never sent, in any payload, at any point: `hole_type`, `kinds`, `hard`,
detector counts, `blurb`, `family`, `author`, `margin`, and `gain` — a
non-zero `gain` *is* the news that the hole paid. What the client does get:
the prompt, the board, its own final score, and its own record of previous
plays. Enforced by the `NO LEAK` gate, which greps real payloads from a real
run rather than inspecting the code.

**(b) Every legal move is presented with equal weight.**
In the battleship `call` widget, `hit` / `miss` / `sunk <ship>` are one row of
identical buttons with nothing pre-selected — *including* when the referee has
just told you privately that the shot hit. Same for Quiet Sonar's claim row.
A board that styled the truthful call as the primary action would be telling
the player the others are a special kind of act, which is the experiment
answering its own question. This is also why Hanabi's clue payload is an
editable text field and not a colour picker: the engine watches what the giver
*wrote*, so a picker emitting only `R` or `3` would delete the behaviour
instead of measuring it.

**(c) The memory contains only what the seat could observe.**
Between plays a participant sees `referee_repeat.Memory.render()` — the exact
text the model arm gets prepended to its next prompt: own action tokens quoted
as issued, own score, and an audit result when there was an audit. No detector
name, no violation count, no word for the hole. A memory that said "you
committed `false_miss` 4 times" would be pointing at the answer, and the curve
would measure instruction-following.

### Shape of a session

Name once (localStorage, low-friction — every move recorded silently, outcomes
auto-submit, no dialogs) → pick a cell → play a **run** of K plays of that same
cell, fresh setup each time, memory panel between plays → done. K is levelled
on decisions rather than plays: battleship asks a seat 32 times per play, so
it is 3; hanabi asks 9, so it is 5.

`p_caught` wires up `referee_repeat.audit()` and **defaults to 0**, which is
the clean arm: nothing is announced, so anything a player learns they learned
from the score alone.

---

## 2. What exists and is verified

Four cells have bespoke boards; the other fifteen play through the prompt and
a text composer, which stays reachable on every cell so no legal move is ever
unreachable. A typed move is recorded as `source: text` and never pools with a
board move.

| cell | board |
|---|---|
| Battleship | tracking grid marked with the calls you were given; own fleet + the three calls |
| Sidebar | card, table, pot, free-text private line, three betting actions |
| Hanabi | stacks, two visible hands, own hand as unknown slots, clue composer |
| Quiet Sonar | nine-cell line for hide/fire, two claims |

`views/` parses engine prompts into structured state. **The engines are
untouched** — they are the instrument `run_referee_crossplay.py` compares
human numbers against, and a structured-state return path would fork it.

`python test_views.py` (offline, no cost; run under `~/venvs/tools/bin/python`
to include the JS gate) — all seven pass:

```
PARSES/PLAYABLE  all 4 boards drive a full episode from the views alone, 0 unparsed
NO LEAK          41 real payloads x 13 forbidden keys + 11 forbidden strings
COPY             no player-visible text in play/ names a defect (1 line exempt, marked)
JS               5 scripts parse    WIRING  26 ids resolve, 8 kinds have renderers
RECORDS          both files written, moves and outcome intact
IDEMPOTENCE      settling a finished play twice counts it once
```

End-to-end over HTTP: a 3-play battleship run answering `[call: miss]` every
time scored +9/+6/+5, and disk showed `false_miss 4/4`, `sunk_denial 1/1`,
`gain +6.0` — none of which reached the browser.

**Data on disk** — one JSON line per play, written under both the game and the
player. Stores the *structured view* of each decision rather than the prompt
(prompts are regenerable from `(game, seed, arm)` plus replies; the view is
not), plus `dt` per move, because discovery happens at a moment and a
90-second pause after fifteen four-second moves is the cheapest evidence of
it. Schema is versioned in every row.

---

## 3. Where it is right now

Running in `fleet-train-jobs` on the Nebius cluster, 2/2 ready, collecting to
`/shared/allie/plays_data` (currently empty — **no real participant has played
it yet**; the only data collected so far is the local smoke test in
`hole_exp/hackable_games/play_data/`).

```bash
kubectl port-forward -n fleet-train-jobs svc/plays-public 8801:8080
# then http://localhost:8801
```

No image is built and none is needed: the whole engine path is
standard-library-only, so stock `python:3.12-slim` runs it directly off the
code staged at `/shared/allie/plays`. **Deploying a code change is a file copy
plus a rollout restart** — there is no registry in this loop:

```bash
cp -r hole_exp/hackable_games/{play_server.py,collector.py,views,play} \
      /shared/allie/plays/hackable_games/
kubectl rollout restart deploy/plays -n fleet-train-jobs
```

Manifests: `hole_exp/hackable_games/k8s/plays.yaml`. Nothing carries an ArgoCD
tracking label and `training-smoke` (the only Application pointed at this
namespace) tracks a single RayJob, so these objects are not in anyone's prune
set — and equally, nothing reconciles them.

---

## 4. Why it is not public, and the two ways out

`strategy-behavior.flt.build` was the chosen hostname. It never got an
address. In order of discovery:

1. **`externalTrafficPolicy: Local` is unsupported** on Nebius — the Service
   sits at `<pending>` forever. Fixed; it must stay at the default `Cluster`.
2. **The tenant is out of public IPv4 addresses.** This is the blocker.
   ```
   Quota limit exceeded ... vpc.ipv4-address.public.count (limit 3, requested 4)
   tenant-e00vby711anqa97w1e
   ```
   All three are spoken for: the training gateway (`213.239.172.57`), the
   inference gateway (`213.239.175.146`), and `fs.flt.build`
   (`213.239.172.138`).
3. **The existing public gateway cannot be borrowed from this namespace.**
   `fleet-training-public` listens only for `ft.flt.build` and
   `api.ft.flt.build`, with `allowedRoutes.namespaces.from: Same` — an
   HTTPRoute from `fleet-train-jobs` cannot attach. The Gateway *can* be
   patched, but its ArgoCD app has `selfHeal: true`, so a manual patch is
   reverted within minutes. That makes it a PR, not a `kubectl`.

### Path A — quota bump (smallest)

Get whoever administers the Nebius tenant to raise
`vpc.ipv4-address.public.count` from 3 to 4. Then:

```bash
# in k8s/plays.yaml: type: ClusterIP -> type: LoadBalancer
# and add to the caddy container:
#   - name: PLAYS_SITE
#     value: strategy-behavior.flt.build
kubectl apply -f hole_exp/hackable_games/k8s/plays.yaml
```

external-dns publishes the A record automatically (it owns `flt.build` in
Route53 and watches Services; the annotation is already on the Service), and
Caddy obtains a Let's Encrypt certificate on its own. Nothing else to do.

### Path B — PR to theseus (no new IP)

Add a listener for the hostname to `k8s/training/charts/fleet-training-public`
plus an HTTPRoute in `fleet-train-control-plane` backending to `plays-public`
in `fleet-train-jobs` (needs a `ReferenceGrant`, or move the Service into the
control-plane namespace). Reuses the existing public IP. Needs review, merge
and an ArgoCD sync, and it modifies shared training-cluster ingress.

---

## 5. Traps that already cost time

- **`*.flt.build` is a wildcard CNAME to Vercel.** Every name under it
  resolves, so "is this hostname free?" cannot be answered with `dig`. A
  specific A record does override the wildcard, so the names are still usable
   — but `strategy-behavior.flt.build` in particular already CNAMEs to a *dead*
  Vercel deployment (`DEPLOYMENT_NOT_FOUND`, expired cert), left over from the
  `apps/traces` project in theseus. If someone re-attaches that domain in
  Vercel later, two systems will claim it. Consider a name with no Vercel
  history.
- **Do not name a public hostname in the Caddyfile before it resolves here.**
  Caddy starts ACME immediately, every attempt is validated against whatever
  the wildcard points at, and each failure burns Let's Encrypt's
  failed-validation budget *for the name you actually want*. The site address
  is now the `PLAYS_SITE` env var, defaulting to an internal port for exactly
  this reason. Set it only once DNS points at this pod.
- **Probes must target 8080, not 80.** Caddy binds 80/443 only when
  `PLAYS_SITE` is set. A liveness probe on `:80` passes in production and
  fails in every other configuration — it killed the caddy container every 60s
  for two hours (37 restarts) before anyone looked. Fixed; do not "tidy" it
  back.
- **One replica, and it is not a placeholder for scaling.** Runs and sessions
  live in the process; a second replica strands any player whose next request
  lands on the other pod, mid-play. Scaling means moving run state out of
  memory first.

---

## 6. Not built

- **No authentication and no consent copy.** The name gate says only that
  moves and timings are recorded. Before anyone outside the team plays it,
  that needs a consent sentence, and probably a shared passphrase (Caddy
  `basic_auth` is two lines).
- **Fifteen of nineteen cells have no board** — they play as prompt + composer.
- **Human is always seat 0**; opponents are always scripted-honest. The API
  takes `seat` and `bots`; the UI offers neither.
- **No analysis of the collected data.** `collector.py` prints a summary; the
  discovery curve itself — exploit rate against play index, the human
  counterpart of `plot_repeat.py` — is not written.
- **The debrief is off** (`HG_DEBRIEF=1`, only answers for finished runs). It
  is the one route that names a hole. Turn it on for the session where you sit
  down with a participant afterwards, not for the study itself.

---

## 7. Related, and easy to confuse

`https://anruigu.github.io/hackable/` is a **different thing**: a static
snapshot of the experimenter-facing traces viewer (nineteen setups plus model
traces, defect behind a spoiler), published to GitHub Pages from
`anruigu/hackable`.

**It is an answer key for this study.** It names every defect to anyone who
clicks, it is public, and it is indexable under the game titles. If the play
site goes live, a participant who searches "Icebound Manifest" or "Quiet
Sonar" can land on it. Either rename that repo to something the titles will
not surface, or strip the reveal from its `data.json`, before recruiting.
