#!/usr/bin/env python3
"""Poll the merged-model servers, then write the arm -> URL map the sweeps read.

    python wait_servers.py --ip 10.78.165.167 --port0 8300

Writes `think4_servers.json`. Also runs the ONE check that matters before any
sampling: every server must answer, and two different arms must produce
DIFFERENT tokens on a fixed probe at temperature 0. Identical output across
arms would mean the merges collapsed to the same weights -- which is what a
silent partial application looks like from the outside, and is the failure
this whole path exists to avoid.
"""
import argparse, json, pathlib, sys, time, urllib.request

ARM_OF = {"grim-nohole": "grim/nohole", "grim-eg": "grim/eg",
          "grim-inf": "grim/inf", "tft-nohole": "tft/nohole",
          "tft-eg": "tft/eg", "tft-inf": "tft/inf"}
PROBE = ("You are playing a repeated game. In one short sentence, state your "
         "plan for the final round.")


def gen(url, text, n=24):
    body = json.dumps({"text": text,
                       "sampling_params": {"max_new_tokens": n,
                                           "temperature": 0.0}}).encode()
    req = urllib.request.Request(url + "/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=180))
    r = r[0] if isinstance(r, list) else r
    return r.get("text", "")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ip", required=True)
    ap.add_argument("--port0", type=int, default=8300)
    ap.add_argument("--names", nargs="+", required=True,
                    help="merged dir names in port order")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--out", default=str(pathlib.Path(__file__).parent
                                         / "think4_servers.json"))
    a = ap.parse_args()

    urls = {n: f"http://{a.ip}:{a.port0 + i}" for i, n in enumerate(a.names)}
    t0 = time.time()
    up = {}
    while time.time() - t0 < a.timeout and len(up) < len(urls):
        for n, u in urls.items():
            if n in up:
                continue
            try:
                urllib.request.urlopen(u + "/health", timeout=5)
                up[n] = u
                print(f"[serve] {n} up at {u} ({time.time()-t0:.0f}s)", flush=True)
            except Exception:
                pass
        if len(up) < len(urls):
            time.sleep(15)
    if len(up) < len(urls):
        print(f"[serve] only {len(up)}/{len(urls)} came up: "
              f"missing {sorted(set(urls) - set(up))}")
        return 1

    print("[serve] probing at temperature 0 for cross-arm distinctness")
    outs = {n: gen(u, PROBE) for n, u in up.items()}
    for n, t in outs.items():
        print(f"   {n:18s} {t[:70]!r}")
    if len(set(outs.values())) == 1:
        print("[serve] ** ALL ARMS PRODUCED IDENTICAL TEXT -- the merges did "
              "not differentiate. Refusing to write the server map. **")
        return 1
    dup = [n for n in outs if list(outs.values()).count(outs[n]) > 1]
    if dup:
        print(f"[serve] warning: identical output from {dup}")

    m = {ARM_OF[n.replace("-step0035", "")]: u for n, u in up.items()}
    pathlib.Path(a.out).write_text(json.dumps(m, indent=1))
    print(f"[serve] wrote {a.out}: {json.dumps(m, indent=1)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
