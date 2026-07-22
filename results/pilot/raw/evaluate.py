"""Correct SWE-bench-style oracle evaluation (D-038).

The test_patch is AUTHORITATIVE: the model must never supply oracle test files.
For each file the test_patch touches, reset it to its base state BEFORE applying
test_patch:
  - exists at base_commit -> `git checkout HEAD -- <f>` (restore base version;
    the model's edits to it are discarded)
  - net-new at base       -> `rm -f <f>` (remove the model's colliding creation)
The idiom `git checkout HEAD -- f 2>/dev/null || rm -f f` does exactly this.
"""
import json, base64, subprocess, re, sys

SP=sys.argv[1]
r=json.load(open(f"{SP}/task-record.json"))
def lst(v): return json.loads(v) if isinstance(v,str) else list(v or [])
authored=open(f"{SP}/authored.patch").read()
oracle_files=sorted(set(re.findall(r'^\+\+\+ b/(.*)$', r["test_patch"], re.M)))
a=base64.b64encode(authored.encode()).decode(); t=base64.b64encode(r["test_patch"].encode()).decode()
resets="\n".join(f"git checkout HEAD -- '{f}' 2>/dev/null || rm -f '{f}'" for f in oracle_files)
script="\n".join(["set +e","cd /testbed",
 f"printf '%s' '{a}' | base64 -d | git apply - ; echo AUTHORED_RC=$? >&2",
 "# D-038: oracle test files are authoritative",
 resets,
 f"printf '%s' '{t}' | base64 -d | git apply - ; echo TESTPATCH_RC=$? >&2",
 "exec 3>&1 4>&2 1>/tmp/e.log 2>&1", *lst(r.get("rebuild_cmds")), *lst(r.get("test_cmds")),
 "exec 1>&3 2>&4", *lst(r.get("print_cmds"))])
p=subprocess.run(["docker","run","-i","--rm","--platform","linux/amd64","--memory=6g",r["docker_image"],"bash","-l"],
 input=script,capture_output=True,text=True,timeout=5400)
open(f"{SP}/eval-raw.txt","w").write(p.stdout)
rcs=[x for x in p.stderr.splitlines() if "_RC=" in x]
ns={}; exec(r["log_parser"], ns); parsed=ns["parser"](p.stdout)
f2p=lst(r["FAIL_TO_PASS"]); p2p=lst(r["PASS_TO_PASS"])
f2p_pass=[x for x in f2p if parsed.get(x)=="pass"]; f2p_fail=[x for x in f2p if parsed.get(x)=="fail"]
f2p_miss=[x for x in f2p if x not in parsed]; p2p_bad=[x for x in p2p if x in parsed and parsed[x]!="pass"]
testpatch_ok = any("TESTPATCH_RC=0" in x for x in rcs)
killed = "Killed" in open(f"{SP}/eval-raw.txt").read() if False else False  # emit-log check below
raw_txt = None
try: raw_txt = open(f"{SP}/eval-raw.txt").read()
except Exception: raw_txt = ""
# D-030/D-038 discipline: parsed==0 is a FAILURE TO MEASURE -> HARNESS-ERROR
# (verdict unknown), NEVER CONFIRMED DEFECTIVE. A test runner Killed under
# emulation (OOM) parses to nothing; that is an environment fact, not a defect.
if not testpatch_ok:
    verdict = "HARNESS-ERROR: test_patch failed to apply"
    resolved = False
elif len(parsed)==0:
    verdict = "HARNESS-ERROR: parser reported no tests (runner Killed/OOM or emit failure) -- verdict UNKNOWN, not defective"
    resolved = False
else:
    resolved = (len(f2p_pass)==len(f2p) and len(f2p)>0 and not f2p_miss and not p2p_bad)
    verdict = "not-confirmed-defective (authoring success)" if resolved else "CONFIRMED DEFECTIVE"
out={"oracle_files_reset":oracle_files,"apply_rcs":rcs,"testpatch_applied":testpatch_ok,
 "parsed":len(parsed),"f2p":{x:parsed.get(x,"MISSING") for x in f2p},
 "f2p_pass":len(f2p_pass),"f2p_fail":len(f2p_fail),"f2p_missing":len(f2p_miss),
 "p2p_regressions":p2p_bad,"resolved":resolved,"verdict":verdict}
json.dump(out,open(f"{SP}/eval-result.json","w"),indent=1)
print(json.dumps(out,indent=1))
