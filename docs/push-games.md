# Push games into the public apps

There are two destinations. Neither reads your working tree.

## Playable study — `https://strategy-behavior.flt.build`

This is the human client. Games come from `hole_exp/hackable_games/` on
`anruigu/strategy-behavior` **`main`**.

1. Change engines, adapters, `views/`, `ui/*.js`, or `play/` in this repo.
2. Run `python hole_exp/hackable_games/test_views.py` until it passes.
3. Commit **only** those files and `git push origin HEAD:main`.
4. Wait. Cluster git-sync polls `main` every 60s. A Node sidecar checks every
   `hackable_games/**/*.js`. A Python revision gate then runs `test_views.py`
   and an HTTP preflight. Only an approved SHA is copied to `/runtime` and
   served.

Do **not** copy into `/shared/allie/plays`. Do **not** `kubectl patch` the
ConfigMap or `rollout restart` the pod: ArgoCD (`fleet-training-public`,
selfHeal) owns the workload and will revert live patches. Staging files never
become `frontend_build`.

If a new SHA is pulled and then rejected, the site stays on the last approved
runtime — or 502 if Recreate already wiped `/runtime`. Typical reject causes:

- `test_views.py` needs `hole_exp/configs/` (roster TOML). The checkout is
  sparse; that cone lives in Theseus
  `k8s/training/charts/fleet-training-public/files/plays-sparse-checkout`.
- The Python gate has no JS parser. It must see `HG_JS_SYNTAX_CHECKED=1` from
  the Node sidecar (`plays-revision-gate.py` in the same chart). Source
  `test_views.py` accepts that env flag; without it, no parser is a hard fail.

Chart/gate/sparse-checkout changes are **Theseus**, not this repo. Direct push
to `fleet-ai/theseus` `main` is blocked (PR + merge queue). Open a PR from a
branch, wait for Argo to sync, then confirm `/index.html` has `/board-ui/`
scripts and no typed-move composer.

## Trace viewer — `https://traces.flt.build`

This is the static evidence bundle. Games and traces are built here, copied
into Theseus, then deployed by Vercel on Theseus `main`.

**Hackable-games page** (`/hackable/`):

```bash
cd /shared/allie/strategy-behavior/hole_exp/hackable_games
python build_bundle.py    # -> bundle/data.json  (prompts from live engines)
cp bundle/data.json /shared/allie/theseus/apps/traces/public/hackable/data.json
```

`index.html` / `app.js` for that page live in Theseus `apps/traces/public/hackable/`.
`sync.sh` does **not** copy this directory.

**Exploit-bench pages** (`/`, `/domains.html`, `/referee.html`, …):

```bash
cd /shared/allie/strategy-behavior
# regenerate viz/*.json from viz/build_*.py (see viz/README.md), then:
VIZ_SRC=/shared/allie/strategy-behavior/viz /shared/allie/theseus/apps/traces/sync.sh
```

Then in Theseus: commit `apps/traces/public/…`, open a PR to `main`. Production
is the `traces` Vercel app; only `apps/traces` changes trigger it.

Benchmark-only artifacts (`benchmark/README.md`,
`benchmark/results/<run>/exploit_specs.json`, `source/benchmark/games.py`) are
**not** on either path until you add them to a bundle (hackable `data.json`, a
new `apps/traces` page, or a deck under `apps/traces/public/decks/`).
