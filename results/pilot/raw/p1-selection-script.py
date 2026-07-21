import json, urllib.parse, urllib.request, secrets, random, sys

GATE = "2026-03-01"
P0_TASK = "thlorenz__doctoc-328"
BASE = "https://datasets-server.huggingface.co/filter"

def fetch(split):
    rows, offset = [], 0
    while True:
        q = urllib.parse.urlencode({
            "dataset": "SWE-bench-Live/MultiLang", "config": "default", "split": split,
            "where": f"\"created_at\">'{GATE}'", "orderby": '"created_at"',
            "offset": offset, "length": 100,
        })
        with urllib.request.urlopen(f"{BASE}?{q}", timeout=90) as r:
            d = json.load(r)
        batch = d.get("rows", [])
        rows += [x["row"] for x in batch]
        total = d["num_rows_total"]
        offset += len(batch)
        if offset >= total or not batch:
            return rows, total

cands = []
for split in ("js", "ts"):
    rows, total = fetch(split)
    print(f"{split}: {total} post-gate rows fetched={len(rows)}", file=sys.stderr)
    for r in rows:
        cands.append({"instance_id": r["instance_id"], "repo": r.get("repo"),
                      "created_at": r["created_at"], "lang": split,
                      "base_commit": r.get("base_commit")})

# §8 fixed rule (harness/corpus/intake.py select_first_n): created_at ASC, ties by instance_id
cands.sort(key=lambda c: (c["created_at"], c["instance_id"]))
print(f"combined post-gate JS+TS: {len(cands)}", file=sys.stderr)
assert cands[0]["instance_id"] == P0_TASK, f"row1 drifted: {cands[0]['instance_id']} != {P0_TASK}"
p1 = cands[1:6]

# OQ-11 ruling: one recorded coin flip sets position 1, then alternate (3/2)
flip = secrets.choice(["anthropic", "openai"])
other = "openai" if flip == "anthropic" else "anthropic"
for i, t in enumerate(p1):
    t["position"] = i + 1
    t["author_vendor"] = flip if i % 2 == 0 else other

# OQ-12 ruling: seeded random draw of 2 of 5, seed recorded before use
seed = secrets.randbelow(2**32)
repeats = sorted(random.Random(seed).sample([1, 2, 3, 4, 5], 2))
for t in p1:
    t["k2_repeat"] = t["position"] in repeats

out = {"gate": GATE, "rule": "SWE-bench-Live/MultiLang combined js+ts, created_at > gate, ORDER BY created_at ASC ties by instance_id, rows 2-6 (row 1 = P0)",
       "combined_post_gate_count": len(cands), "p0_row1_verified": P0_TASK,
       "coin_flip_position1": flip, "repeat_seed": seed, "repeat_positions": repeats,
       "tasks": p1}
print(json.dumps(out, indent=2))
