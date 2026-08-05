"""Accrual screening driver (D-028 screen over the frozen ordering).

Reuses the validation screen's committed row machinery (screen-runner.py
run_row: same flow, same caps, same INFEASIBLE/ERROR taxonomy, ENV-PATH fix,
build-log capture) over a tranche of unscreened ordered-pool positions.
Container work, not sessions (D-055). Counts toward the D-065.3 own-harvest
trigger's cumulative screened rows.

Run:  python3 screen-accrual.py <tranche.json> <outdir>
"""
import importlib.util, json, pathlib, sys

HERE = pathlib.Path(__file__).parent
tranche = json.loads(pathlib.Path(sys.argv[1]).read_text())
OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location(
    "screen_runner", HERE.parent / "validation" / "screen-runner.py")
mod = importlib.util.module_from_spec(spec)
sys.argv = ["screen-runner.py", str(OUT)]   # module reads OUT from argv
spec.loader.exec_module(mod)
mod.OUT = OUT
for lang in ("js", "ts"):                    # extend dataset map beyond validation langs
    mod.DATASET[lang] = ("SWE-bench-Live/MultiLang", lang)

outfile = OUT / "screen.json"
results = json.loads(outfile.read_text()) if outfile.exists() else {}
for t in tranche:
    key = f"{t['lang']}:{t['instance_id']}"
    if key in results and results[key].get("verdict") in ("PASS", "FAIL", "INFEASIBLE"):
        print(f"=== {key} (cached {results[key]['verdict']}) ===", flush=True)
        continue
    print(f"\n=== pos{t['position']} {key} ===", flush=True)
    try:
        res = mod.run_row(t["lang"], t["instance_id"], results)
    except Exception as e:
        res = {"verdict": "ERROR", "reason": f"runner exception: {e}"}
    res["position"] = t["position"]
    results[key] = res
    outfile.write_text(json.dumps(results, indent=2))
    print(f"  -> {res['verdict']}: {res.get('reason','')} ({res.get('wall_s','?')}s)", flush=True)
    rec = OUT / f"{t['instance_id']}.record.json"
    if rec.exists():
        import subprocess
        subprocess.run(["docker", "rmi", json.loads(rec.read_text())["docker_image"]],
                       capture_output=True)
print("\n=== TRANCHE SUMMARY ===")
for k, v in results.items():
    print(f"  {v['verdict']:10} pos{v.get('position','?'):>3} {k}")
