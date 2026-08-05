"""Step-3 per-language validation screen (D-055 gate; execution step 1 of D-063).

Runs the D-028 ground-truth validity screen over the declared validation
samples (sample-selection.json: first ~10 post-gate rows per candidate
language, created_at ASC, ties instance_id): at base_commit with ONLY the
test patch applied, every declared F2P test must be reported and fail, and
P2P must be non-empty with every reported P2P test passing. Outcome-blind:
runs before any patch is authored. Container work, not sessions (D-055).

Two dataset schemas:
  - SWE-bench-Live/MultiLang (go/cs/cpp/java/rust): the pilot's flow verbatim
    (gt-screen-runner.py) — git apply test_patch -> rebuild_cmds -> test_cmds
    (noise redirected) -> print_cmds; the record's own log_parser code.
  - nebius/SWE-rebench-leaderboard (python, 2026_03): per-instance prebuilt
    eval image; git apply test_patch -> install_config.test_cmd with stdout
    captured; standard pytest -rA parser (install_config.log_parser =
    parse_log_pytest on every sampled row).

Verdicts: PASS / FAIL (label integrity, D-049) / ERROR (harness, never a
ground-truth verdict) / INFEASIBLE (platform_infeasible, D-048/D-030 — either
(time): the per-row wall-clock caps below, or (crash): the test command dies
with a core dump / illegal instruction under amd64 emulation, the bun
precedent — rig-relative, never a label verdict). Declared caps: image pull
<= 60 min, container run <= 60 min per row. Images are removed after each row
(docker rmi) to bound VM disk.

Harness fixes logged mid-screen (incoherence discipline — the first pass
surfaced them; settled PASS/FAIL/INFEASIBLE verdicts were produced by
unaffected code paths and stand; ERROR rows re-run under the fixed harness):
  1. PATH: `bash -l` sources the image profile, which RESETS PATH and
     clobbers the Docker ENV PATH (go toolchain lives there -> every go row
     ERRORed with "go: command not found"; bun conversely needs the login
     profile). Fix: read the image's ENV PATH via docker inspect and export
     ENV_PATH:$PATH inside the script — both sources on PATH.
  2. Crash classification: "core dumped"/"Illegal instruction" in stderr with
     zero parsed tests is platform_infeasible(crash) (keras/TF needs AVX,
     absent under emulation), not ERROR.
  3. Diagnosability: the MultiLang build/test log tail is emitted to stderr
     (captured per-row) so an empty canonical log is explainable post-hoc.

Usable rate per language = PASS / screened; full breakdown reported. Pilot
comparator (JS/TS): 5 PASS / 17 screened ~= 29% (report §4/§8).

Run:  python3 screen-runner.py <outdir>
"""
import base64, json, pathlib, subprocess, sys, time, urllib.parse, urllib.request

HERE = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
OUT.mkdir(parents=True, exist_ok=True)
SAMPLES = json.loads((HERE / "sample-selection.json").read_text())
PULL_CAP = 3600   # s, per row (D-048 cap, declared in brief §2)
RUN_CAP = 3600    # s, per row

LANG_ORDER = ["python", "go", "cs", "cpp", "java", "rust"]
DATASET = {"python": ("nebius/SWE-rebench-leaderboard", "2026_03")}
for _l in ("go", "cs", "cpp", "java", "rust"):
    DATASET[_l] = ("SWE-bench-Live/MultiLang", _l)


def fetch(dataset, split, iid):
    q = urllib.parse.urlencode({"dataset": dataset, "config": "default",
        "split": split, "where": f"\"instance_id\"='{iid}'", "limit": 1})
    for i in range(6):
        try:
            with urllib.request.urlopen(
                    f"https://datasets-server.huggingface.co/filter?{q}", timeout=120) as r:
                return json.load(r)["rows"][0]["row"]
        except Exception as e:
            print(f"  retry fetch {iid} ({i+1}): {e}", flush=True)
            time.sleep(15 + 15 * i)
    return None


def lst(v):
    if isinstance(v, str):
        try:
            return json.loads(v)
        except Exception:
            return [v]
    return list(v or [])


def parse_log_pytest(log):
    """Standard SWE-bench pytest -rA summary parser."""
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


def run_row(lang, iid, results):
    dataset, split = DATASET[lang]
    r = fetch(dataset, split, iid)
    if r is None:
        return {"verdict": "ERROR", "reason": "record fetch failed"}
    (OUT / f"{iid}.record.json").write_text(json.dumps(r, indent=2))
    img = r["docker_image"]
    f2p, p2p = lst(r["FAIL_TO_PASS"]), lst(r["PASS_TO_PASS"])
    print(f"  image={img}  F2P={len(f2p)} P2P={len(p2p)}", flush=True)
    t0 = time.time()
    try:
        pull = subprocess.run(["docker", "pull", "--platform", "linux/amd64", img],
                              capture_output=True, text=True, timeout=PULL_CAP)
    except subprocess.TimeoutExpired:
        return {"verdict": "INFEASIBLE", "reason": f"platform_infeasible(time): pull > {PULL_CAP}s (D-048)"}
    if pull.returncode != 0:
        return {"verdict": "ERROR", "reason": "image pull failed", "stderr": pull.stderr[-500:]}
    insp = subprocess.run(["docker", "inspect", "-f",
                           "{{range .Config.Env}}{{println .}}{{end}}", img],
                          capture_output=True, text=True)
    env_path = next((l[5:] for l in insp.stdout.splitlines() if l.startswith("PATH=")), "")
    path_line = f'export PATH="{env_path}:$PATH"' if env_path else "true"
    patch_b64 = base64.b64encode(r["test_patch"].encode()).decode()
    if lang == "python":
        ic = r["install_config"]
        ic = json.loads(ic) if isinstance(ic, str) else ic
        assert ic.get("log_parser") == "parse_log_pytest", f"unexpected parser {ic.get('log_parser')}"
        script = "\n".join([
            "set +e", "cd /testbed", path_line,
            f"printf '%s' '{patch_b64}' | base64 -d | git apply -",
            ic["test_cmd"],
        ])
        parser = parse_log_pytest
    else:
        # Pilot flow verbatim: own-line commands (heredoc-safe), build/test
        # noise via exec redirect, login shell for image PATH, print_cmds as
        # the canonical log emitter (never infer the output path).
        script = "\n".join([
            "set +e", "cd /testbed", path_line,
            f"printf '%s' '{patch_b64}' | base64 -d | git apply -",
            "exec 3>&1 4>&2 1>/tmp/screen-build.log 2>&1",
            *lst(r.get("rebuild_cmds")),
            *lst(r.get("test_cmds")),
            "exec 1>&3 2>&4",
            *lst(r.get("print_cmds")),
            "tail -c 3000 /tmp/screen-build.log 1>&2",
        ])
        ns = {}
        exec(r["log_parser"], ns)
        parser = ns["parser"]
    try:
        proc = subprocess.run(["docker", "run", "-i", "--rm", "--platform",
                               "linux/amd64", img, "bash", "-l"],
                              input=script, capture_output=True, text=True, timeout=RUN_CAP)
    except subprocess.TimeoutExpired:
        subprocess.run(["docker", "ps", "-q", "--filter", f"ancestor={img}"],
                       capture_output=True, text=True)
        subprocess.run(f"docker ps -q --filter ancestor={img} | xargs -r docker kill",
                       shell=True, capture_output=True)
        return {"verdict": "INFEASIBLE", "reason": f"platform_infeasible(time): run > {RUN_CAP}s (D-048)",
                "wall_s": round(time.time() - t0)}
    (OUT / f"{iid}.raw.txt").write_text(proc.stdout)
    (OUT / f"{iid}.stderr.txt").write_text(proc.stderr[-20000:])
    parsed = parser(proc.stdout)
    f2p_pass = [t for t in f2p if parsed.get(t) == "pass"]
    f2p_miss = [t for t in f2p if t not in parsed]
    p2p_bad = [t for t in p2p if t in parsed and parsed[t] != "pass"]
    crashed = any(sig in proc.stderr for sig in
                  ("core dumped", "Illegal instruction", "Segmentation fault"))
    # Go runtime fatal (e.g. GC worker crash under emulation): only when the
    # parser saw nothing — a test-level panic would still yield parsed output.
    crashed = crashed or ("fatal error:" in proc.stderr and "runtime/mgc.go" in proc.stderr)
    if not parsed and crashed:
        verdict, reason = "INFEASIBLE", ("platform_infeasible(crash): test command died under "
                                         "amd64 emulation (D-048/D-030 bun precedent)")
    elif not parsed:
        verdict, reason = "ERROR", "parser returned no tests (harness/emit problem, not ground truth)"
    elif f2p and not f2p_pass and not f2p_miss and len(p2p) > 0 and not p2p_bad:
        verdict, reason = "PASS", ""
    else:
        verdict, reason = "FAIL", "F2P not all-failing at base, and/or P2P empty or not all-passing"
    return {"verdict": verdict, "reason": reason, "parsed_tests": len(parsed),
            "F2P": {"n": len(f2p), "PASS_at_base": len(f2p_pass), "not_reported": len(f2p_miss)},
            "P2P": {"n": len(p2p), "not_pass_at_base": len(p2p_bad)},
            "wall_s": round(time.time() - t0)}


def main():
    outfile = OUT / "screen.json"
    results = json.loads(outfile.read_text()) if outfile.exists() else {}
    for lang in LANG_ORDER:
        for row in SAMPLES[lang]:
            iid = row["instance_id"]
            key = f"{lang}:{iid}"
            if key in results and results[key].get("verdict") in ("PASS", "FAIL", "INFEASIBLE"):
                print(f"=== {key} (cached {results[key]['verdict']}) ===", flush=True)
                continue
            print(f"\n=== {key} ===", flush=True)
            try:
                res = run_row(lang, iid, results)
            except Exception as e:
                res = {"verdict": "ERROR", "reason": f"runner exception: {e}"}
            results[key] = res
            outfile.write_text(json.dumps(results, indent=2))
            print(f"  -> {res['verdict']}: {res.get('reason','')} "
                  f"({res.get('wall_s','?')}s)", flush=True)
            # bound VM disk: drop the per-instance image (re-pullable)
            r = json.loads((OUT / f"{iid}.record.json").read_text()) if (OUT / f"{iid}.record.json").exists() else None
            if r:
                subprocess.run(["docker", "rmi", r["docker_image"]], capture_output=True)
    print("\n=== PER-LANGUAGE SUMMARY ===")
    for lang in LANG_ORDER:
        vs = [results.get(f"{lang}:{row['instance_id']}", {}).get("verdict", "?")
              for row in SAMPLES[lang]]
        n = len(vs)
        print(f"  {lang:7} screened={n} PASS={vs.count('PASS')} FAIL={vs.count('FAIL')} "
              f"ERROR={vs.count('ERROR')} INFEASIBLE={vs.count('INFEASIBLE')} "
              f"usable={vs.count('PASS')}/{n}")


if __name__ == "__main__":
    main()
