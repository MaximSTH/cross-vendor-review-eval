"""Step-3 oracle evaluation (D-038 discipline; both feed schemas).

Extends the pilot's `results/pilot/raw/evaluate.py` to the admitted feeds:
  - MultiLang records (go/js/ts): rebuild_cmds/test_cmds/print_cmds + the
    record's own log_parser — the pilot flow verbatim.
  - SWE-rebench records (python): install_config.test_cmd + the standard
    pytest -rA parser (same as the step-1 validation screen).

The test_patch is AUTHORITATIVE (D-038): every file it touches is reset to
base state before it applies (`git checkout HEAD -- f || rm -f f`), so the
model can never supply oracle test files. ENV PATH is injected per the
step-1 harness fix (bash -l profile clobbers Docker ENV PATH).

Verdicts mirror the pilot: CONFIRMED DEFECTIVE / not-confirmed-defective
(authoring success) / HARNESS-ERROR (never a defect verdict; D-030).

Run:  python3 evaluate-step3.py <position-dir>
      (<position-dir> holds task-record.json + authored.patch; writes
       eval-raw.txt, eval-result.json there)
"""
import base64, json, re, subprocess, sys

SP = sys.argv[1]
r = json.load(open(f"{SP}/task-record.json"))


def lst(v):
    if isinstance(v, str):
        try:
            return json.loads(v)
        except Exception:
            return [v]
    return list(v or [])


def parse_log_pytest(log):
    out = {}
    for line in log.splitlines():
        line = line.strip()
        for status, mapped in (("PASSED", "pass"), ("XPASS", "pass"),
                               ("FAILED", "fail"), ("ERROR", "fail"),
                               ("XFAIL", "skip"), ("SKIPPED", "skip")):
            if line.startswith(status + " "):
                test = line[len(status) + 1:].split(" - ")[0].strip()
                if test:
                    out[test] = mapped
    return out


authored = open(f"{SP}/authored.patch").read()
oracle_files = sorted(set(re.findall(r'^\+\+\+ b/(.*)$', r["test_patch"], re.M)))
a = base64.b64encode(authored.encode()).decode()
t = base64.b64encode(r["test_patch"].encode()).decode()
resets = "\n".join(f"git checkout HEAD -- '{f}' 2>/dev/null || rm -f '{f}'"
                   for f in oracle_files)

img = r["docker_image"]
insp = subprocess.run(["docker", "inspect", "-f",
                       "{{range .Config.Env}}{{println .}}{{end}}", img],
                      capture_output=True, text=True)
if insp.returncode != 0:
    subprocess.run(["docker", "pull", "--platform", "linux/amd64", img],
                   capture_output=True, text=True, timeout=3600)
    insp = subprocess.run(["docker", "inspect", "-f",
                           "{{range .Config.Env}}{{println .}}{{end}}", img],
                          capture_output=True, text=True)
env_path = next((l[5:] for l in insp.stdout.splitlines() if l.startswith("PATH=")), "")
path_line = f'export PATH="{env_path}:$PATH"' if env_path else "true"

if "install_config" in r and r.get("install_config"):
    ic = r["install_config"]
    ic = json.loads(ic) if isinstance(ic, str) else ic
    assert ic.get("log_parser") == "parse_log_pytest", ic.get("log_parser")
    body = [ic["test_cmd"]]
    parser = parse_log_pytest
    redirect = []          # pytest output IS stdout; no canonical print step
    restore = []
else:
    body = lst(r.get("rebuild_cmds")) + lst(r.get("test_cmds"))
    redirect = ["exec 3>&1 4>&2 1>/tmp/e.log 2>&1"]
    restore = ["exec 1>&3 2>&4", *lst(r.get("print_cmds")),
               "head -c 4000 /tmp/e.log 1>&2",
               "echo '...[build-log truncated]...' 1>&2",
               "tail -c 8000 /tmp/e.log 1>&2"]
    ns = {}
    exec(r["log_parser"], ns)
    parser = ns["parser"]

script = "\n".join([
    "set +e", "cd /testbed", path_line,
    f"printf '%s' '{a}' | base64 -d | git apply - ; echo AUTHORED_RC=$? >&2",
    "# D-038: oracle test files are authoritative",
    resets,
    f"printf '%s' '{t}' | base64 -d | git apply - ; echo TESTPATCH_RC=$? >&2",
    *redirect, *body, *restore,
])
p = subprocess.run(["docker", "run", "-i", "--rm", "--platform", "linux/amd64",
                    "--memory=6g", img, "bash", "-l"],
                   input=script, capture_output=True, text=True, timeout=5400)
open(f"{SP}/eval-raw.txt", "w").write(p.stdout)
open(f"{SP}/eval-stderr.txt", "w").write(p.stderr[-20000:])
rcs = [x for x in p.stderr.splitlines() if "_RC=" in x]
parsed = parser(p.stdout)
f2p = lst(r["FAIL_TO_PASS"]); p2p = lst(r["PASS_TO_PASS"])
f2p_pass = [x for x in f2p if parsed.get(x) == "pass"]
f2p_fail = [x for x in f2p if parsed.get(x) == "fail"]
f2p_miss = [x for x in f2p if x not in parsed]
p2p_bad = [x for x in p2p if x in parsed and parsed[x] != "pass"]
testpatch_ok = any("TESTPATCH_RC=0" in x for x in rcs)
authored_ok = any("AUTHORED_RC=0" in x for x in rcs)

# D-030/D-038: parsed==0 is a FAILURE TO MEASURE -> HARNESS-ERROR, never a
# defect verdict.
if not authored_ok:
    verdict, resolved = "HARNESS-ERROR: authored patch failed to apply", False
elif not testpatch_ok:
    verdict, resolved = "HARNESS-ERROR: test_patch failed to apply", False
elif len(parsed) == 0:
    verdict, resolved = ("HARNESS-ERROR: parser reported no tests "
                         "(runner Killed/OOM or emit failure) -- verdict UNKNOWN"), False
else:
    resolved = (len(f2p_pass) == len(f2p) and len(f2p) > 0
                and not f2p_miss and not p2p_bad)
    verdict = ("not-confirmed-defective (authoring success)" if resolved
               else "CONFIRMED DEFECTIVE")
out = {"oracle_files_reset": oracle_files, "apply_rcs": rcs,
       "authored_applied": authored_ok, "testpatch_applied": testpatch_ok,
       "parsed": len(parsed),
       "f2p": {x: parsed.get(x, "MISSING") for x in f2p},
       "f2p_pass": len(f2p_pass), "f2p_fail": len(f2p_fail),
       "f2p_missing": len(f2p_miss), "p2p_regressions": p2p_bad,
       "resolved": resolved, "verdict": verdict}
json.dump(out, open(f"{SP}/eval-result.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ("verdict", "parsed", "f2p_pass",
                                      "f2p_fail", "f2p_missing")}, indent=1))
