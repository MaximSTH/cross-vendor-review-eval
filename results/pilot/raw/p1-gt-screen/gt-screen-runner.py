"""Ground-truth validity screen (D-028): at base_commit with ONLY the test patch
applied, every declared F2P test must be reported and fail, and P2P must be
non-empty with every reported P2P test passing.

Outcome-blind: runs before any patch is authored.

Per-task container flow uses the record's own shipped fields, in order:
  git apply <test_patch>  ->  rebuild_cmds  ->  test_cmds  ->  print_cmds
print_cmds is the canonical log emitter; an earlier version of this script
assumed results always land in reports/*.json and produced a false FAIL on
NVIDIA__NemoClaw-330 (parsed=0). Never infer the output path.
"""
import base64, json, subprocess, sys, urllib.parse, urllib.request, pathlib, time

OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
TASKS = json.loads(sys.argv[2])   # [[split, instance_id], ...]

def fetch(split, iid):
    q = urllib.parse.urlencode({"dataset":"SWE-bench-Live/MultiLang","config":"default",
        "split":split,"where":f"\"instance_id\"='{iid}'","limit":1})
    for _ in range(5):
        try:
            with urllib.request.urlopen(f"https://datasets-server.huggingface.co/filter?{q}", timeout=120) as r:
                return json.load(r)["rows"][0]["row"]
        except Exception as e:
            print(f"  retry fetch {iid}: {e}", flush=True); time.sleep(15)
    return None

def lst(v):
    if isinstance(v,str):
        try: return json.loads(v)
        except Exception: return [v]
    return list(v or [])

results = {}
outfile = OUT/"screen.json"
if outfile.exists(): results = json.loads(outfile.read_text())

for split, iid in TASKS:
    if iid in results and results[iid].get("verdict") in ("PASS","FAIL"):
        print(f"=== {iid} (cached {results[iid]['verdict']}) ===", flush=True); continue
    print(f"\n=== {iid} ===", flush=True)
    r = fetch(split, iid)
    if r is None:
        results[iid] = {"verdict":"ERROR","reason":"record fetch failed"}; continue
    (OUT/f"{iid}.record.json").write_text(json.dumps(r, indent=2))
    img, f2p, p2p = r["docker_image"], lst(r["FAIL_TO_PASS"]), lst(r["PASS_TO_PASS"])
    print(f"  image={img}  F2P={len(f2p)} P2P={len(p2p)}", flush=True)
    pull = subprocess.run(["docker","pull","--platform","linux/amd64",img],
                          capture_output=True, text=True, timeout=7200)
    if pull.returncode != 0:
        results[iid] = {"verdict":"ERROR","reason":"image pull failed",
                        "stderr":pull.stderr[-500:]}
        outfile.write_text(json.dumps(results, indent=2)); print("  -> ERROR pull", flush=True); continue
    # Commands go on their OWN LINES, never joined with " ; ": several tasks
    # embed heredocs in test_cmds (GladysAssistant__Gladys-2504) which a
    # semicolon-join silently destroys. Build/test noise is redirected via
    # exec rather than a { } group, because grouping also breaks heredocs.
    # Login shell (bash -l) so image PATH setup applies (bun lives in ~/.bun/bin).
    # The patch travels base64-encoded inside the script, leaving stdin free.
    patch_b64 = base64.b64encode(r["test_patch"].encode()).decode()
    script = "\n".join([
        "set +e", "cd /testbed",
        f"printf '%s' '{patch_b64}' | base64 -d | git apply -",
        "exec 3>&1 4>&2 1>/tmp/screen-build.log 2>&1",
        *lst(r.get("rebuild_cmds")),
        *lst(r.get("test_cmds")),
        "exec 1>&3 2>&4",
        *lst(r.get("print_cmds")),
    ])
    proc = subprocess.run(["docker","run","-i","--rm","--platform","linux/amd64",img,"bash","-l"],
                          input=script, capture_output=True, text=True, timeout=7200)
    (OUT/f"{iid}.raw.txt").write_text(proc.stdout)
    (OUT/f"{iid}.stderr.txt").write_text(proc.stderr[-20000:])
    ns={}; exec(r["log_parser"], ns)
    parsed = ns["parser"](proc.stdout)
    f2p_pass = [t for t in f2p if parsed.get(t)=="pass"]
    f2p_miss = [t for t in f2p if t not in parsed]
    p2p_bad  = [t for t in p2p if t in parsed and parsed[t]!="pass"]
    p2p_miss = [t for t in p2p if t not in parsed]
    if not parsed:
        verdict, reason = "ERROR", "parser returned no tests (harness/emit problem, not ground truth)"
    elif f2p and not f2p_pass and not f2p_miss and len(p2p)>0 and not p2p_bad:
        verdict, reason = "PASS", ""
    else:
        verdict, reason = "FAIL", "F2P not all-failing at base, and/or P2P empty or not all-passing"
    results[iid] = {"verdict":verdict,"reason":reason,"parsed_tests":len(parsed),
        "F2P":{"n":len(f2p),"PASS_at_base":len(f2p_pass),"not_reported":len(f2p_miss)},
        "P2P":{"n":len(p2p),"not_pass_at_base":len(p2p_bad),"not_reported":len(p2p_miss)}}
    print(f"  -> {verdict}: {json.dumps(results[iid])}", flush=True)
    outfile.write_text(json.dumps(results, indent=2))

print("\n=== SUMMARY ===")
for k,v in results.items(): print(f"  {v['verdict']:5} {k}  {v.get('reason','')}")
