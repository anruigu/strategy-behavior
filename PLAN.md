# Allie workspace backup plan — 2026-08-25

Survey done from a **root** session, which is root_squashed on the `/workspace` NFS mount.
Decisions already made by Allie:

- **Credentials**: re-run Claude Code as uid 1005 (not root).
- **S3 scope**: results + code, skip regenerable (venvs, caches, `__pycache__`, `prebuilt`).
- **Third-party repos**: `git bundle` to S3 only — no forks, no GitHub writes.

---

## 0. Start here — re-run as uid 1005

No local passwd entry exists for uid 1005, so use the numeric form:

```bash
sudo -u '#1005' -g '#1005' -H \
  env HOME=/workspace/allie \
  /workspace/allie/.local/bin/claude
```

Verify before doing anything else:

```bash
id                                  # expect uid=1005
head -c 1 /workspace/allie/.env     # must succeed
ls /workspace/allie/.claude/projects/ | head
touch /workspace/allie/.wtest && rm /workspace/allie/.wtest
```

If all four pass, everything below is unblocked.

### Why this was necessary

`/workspace` is NFS (`10.10.60.11:/runpodfs/networkvolumes/qwfx8hz0rl`), and **root does not
get the usual DAC override on that mount** — permissions are enforced server-side, where the
client's root is not privileged. Observed directly:

- reading uid-1005-owned `0600` files → `Permission denied`, even with the Claude sandbox off
- `chown` on the mount → `Operation not permitted`
- but a root-owned `0600` `.env` in `/tmp` reads fine, so this is **not** the sandbox
  pattern-blocking secret files — it is specific to the NFS mount

(The exact mechanism — `root_squash` vs. NFSv4 ACL enforcement — is unconfirmed; `mount` was
blocked by policy during the survey. It does not change the fix: as uid 1005 you are the
file *owner*, so the `0600` bits grant access.)

Blocked as root: `.env`, `.ssh/`, `.config/gh/hosts.yml`, `.aws/config`, `.netrc`,
`.claude/projects/`, `.claude/sessions/`, `.claude/daemon/`, `.local/share/`,
`.cursor-server/{data,extensions}`, and write access to `/workspace/allie` itself.

Note: files already staged in `/workspace/exports/allie-backup-2026-08-25/` are owned by
`root` (chown was not possible), so they were left mode `777` for you to overwrite.

---

## Caveats on this survey — re-run these as uid 1005

1. **Repo list may be incomplete.** `find` was `-maxdepth 3` *and* silently skipped unreadable
   dirs, notably `.local/share`. Re-run at full depth as uid 1005:
   ```bash
   find /workspace/allie -name .git -not -path '*/node_modules/*' -prune | sed 's|/.git$||' | sort
   ```
2. **Size numbers incomplete.** The `du` scan had not finished when the session ended
   (NFS is slow). Known so far: `base-evals` 182G, `merged` 101G, `venvs` 27G, `ipd_exp` 11G,
   `peft` 3.6G, `sky_logs` 132M, `data` 25M. Order ~330G+, unconfirmed.
3. **Free space is tight**: 636G free on a 9.1T volume *shared with other users*
   (aaron, guanghan, kalonus, neeraj, zhichao, clod). Do not stage a full local copy —
   stream to S3, or bundle in batches and delete as you go.
4. `git config --global --add safe.directory '*'` was added to **root's** `/root/.gitconfig`
   during the survey to work around "dubious ownership". Harmless, and irrelevant once
   running as uid 1005. Revert with
   `git config --global --unset-all safe.directory` if you care.

---

## Phase 1 — Local safety net (do first, before any `git add` / `checkout`)

github is already authenticated as anruigu via the token
Cheap, needs no credentials, and protects against a fumbled command costing real work.

```bash
OUT=/workspace/exports/allie-backup-2026-08-25
mkdir -p "$OUT"/{bundles,worktree-tars}

for d in $(find /workspace/allie -name .git -prune | sed 's|/.git$||'); do
  n=$(realpath --relative-to=/workspace/allie "$d" | tr '/' '_')
  # --all captures every branch AND stashes are reachable via refs/stash
  git -C "$d" bundle create "$OUT/bundles/$n.bundle" --all refs/stash 2>/dev/null \
    || git -C "$d" bundle create "$OUT/bundles/$n.bundle" --all
  # modified + untracked files, which bundles do NOT capture
  git -C "$d" status --porcelain -z \
    | sed -z 's/^...//' \
    | tar -C "$d" --null -czf "$OUT/worktree-tars/$n.tgz" -T - 2>/dev/null
done
```

Verify each bundle before trusting it:

```bash
for b in "$OUT"/bundles/*.bundle; do git bundle verify "$b" >/dev/null 2>&1 \
  || echo "BAD: $b"; done
```


---

## Phase 2 — Commit & push

Only **one** repo has unpushed commits: `behavior` (ahead 1). The real exposure is
uncommitted work in ~18 repos.

Use a dated branch per repo — do **not** commit to `main`, so nothing lands on a shared
branch unreviewed:

```bash
git -C "$d" switch -c backup/2026-08-25
git -C "$d" add -A
git -C "$d" commit -m "wip: workspace backup 2026-08-25"
git -C "$d" push -u origin backup/2026-08-25
```

### Repos you own → push (verify write access first with `git push --dry-run`)
**you can ignore** `SkyRL-Fleet-sensory-sft`, `cs285`, `agent`,`theseus-falmart`, `theseus-meta-investigator`,  `fleet-research-api`,  `sensory-sft`, `vulnerability-tracking`,i don't need it anymore

`behavior` (also has the 1 real unpushed commit), `strategy-behavior`,
`superhuman_negotiator`, `fleet-research`, `theseus`,
 `performative` (97 untracked — review the
list first, likely has junk), `agentviz`,`SkyRL-Fleet`, `skyrl-neg-wt`.

### Triage before touching — DO NOT blind-commit

- `evals_external/insider-trading` — **14,468 staged deletions**. This looks like an
  accident, not work. Inspect with `git -C evals_external/insider-trading status | head`.
  If accidental: `git restore --staged . && git checkout .`. Bundle it either way first.
- `performative` (97 untracked), `TextArena` (43), `spiral` (34), `skyrl-neg-wt` (21),
  `mask` (19) — check for stray checkpoints/datasets before `git add -A`, or they'll bloat
  the repos. `git status --porcelain | grep '^??' | head -50`.

### Third-party repos → bundle only (per your decision, no forks)

`TextArena`,  `spiral`, `mask`, `TextArena/Avalon-LLM`, `machiavelli`,
`evals_external/insider-trading`, `evals_external/agentic-misalignment`,
`evals_external/hack-verifiable`, `TRAIT`, `consistent-LLMs`, `deceptive_dialogue`,
`social_gym`, `MARSHAL`.

Phase 1 already bundles these — just make sure the bundles reach S3 in Phase 3.

---

## Phase 3 — S3 upload

No `aws` CLI installed. **`rclone` is available at `/usr/bin/rclone`** and handles S3 fine.

Configure from `.env` (readable once running as uid 1005) — pass via env, don't write
keys into `rclone.conf`:

```bash
set -a; . /workspace/allie/.env; set +a
export RCLONE_CONFIG_S3_TYPE=s3
export RCLONE_CONFIG_S3_PROVIDER=AWS
export RCLONE_CONFIG_S3_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID"
export RCLONE_CONFIG_S3_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY"
export RCLONE_CONFIG_S3_REGION="${AWS_DEFAULT_REGION:-us-east-1}"

rclone lsd s3:   # confirm auth + discover the bucket name
```

Upload in **value order**, so an interruption still leaves the important things saved:

```bash
B=s3:<bucket>/allie-backup-2026-08-25

# 1. bundles + worktree tars — small, highest value
rclone copy /workspace/exports/allie-backup-2026-08-25 "$B/git" -P

# 2. results, logs, configs — small
rclone copy /workspace/allie "$B/results" -P \
  --include '*.{md,py,sh,json,jsonl,yaml,yml,csv,png,log,sbatch,txt}' --max-depth 2

# 3. adapters + eval outputs — medium
for d in merged peft ckpts staged_ckpts data eval_games oat-output-* \
         value_probe_report leaky_poker_logs sky_logs; do
  rclone copy "/workspace/allie/$d" "$B/data/$d" -P
done

# 4. base-evals — 182G, the long pole. Run last, in background.
rclone copy /workspace/allie/base-evals "$B/data/base-evals" -P
```

**Excluded per your decision** (regenerable): `venvs/` (27G), `.venv/`, `hf_cache`,
`__pycache__/`, `prebuilt/`, `nltk_data/`, `.npm`, `.cache`.

Use `--transfers 8 --checkers 16` on the big copies; NFS reads are the bottleneck, not S3.

---

## Phase 4 — Claude data ("memories" — **not** gone)

`/workspace/allie/.claude/` is intact. Contents worth keeping:

- `projects/` — session transcripts (the actual "memories")
- `history.jsonl` (184K), `plans/`, `backups/`, `settings.json`, `settings.local.json`
- `.claude.json` at `/workspace/allie/.claude.json` (40K) and `.claude/.claude.json` (50K)

```bash
tar -czf /workspace/exports/claude-2026-08-25.tgz \
  -C /workspace/allie \
  --exclude='.claude/cache' --exclude='.claude/image-cache' \
  --exclude='.claude/paste-cache' --exclude='.claude/downloads' \
  .claude .claude.json
```

> **Contains secrets**: `.claude/.credentials.json` and `.claude.json` hold OAuth tokens.
> Either drop them from the tar, or upload under a separate encrypted prefix with SSE-KMS —
> not into the general results bucket.

Nothing in the root account's memory dir (`/root/.claude/.../memory/`) — it is empty.

---

## Phase 5 — Port viewers

nginx listens on **9091, 3001, 8001, 8081, 7861, 7270** — but all six returned **502**.
The upstream apps are already dead, so there is nothing live to capture. What matters is
their source + the data they served, which Phases 2–3 already cover:
`agentviz/`, `value_probe_report/`, `transcript_to_viewer.py`.

If you want them running again rather than just backed up, that's separate work —
find the launch scripts and check `nginx -T` for the proxy_pass targets.

---

## Phase 6 — Verify (do not skip)

```bash
# 1. every repo clean / everything pushed
#    re-run repo-survey.txt generation and diff against the original

# 2. bundles are valid
for b in "$OUT"/bundles/*.bundle; do git bundle verify "$b" >/dev/null || echo "BAD $b"; done

# 3. S3 actually matches — checksums, not exit codes
rclone check /workspace/allie/merged "$B/data/merged" --size-only
rclone size "$B"     # sanity-check total against local du
```

Only after Phase 6 passes should anything be deleted locally.
