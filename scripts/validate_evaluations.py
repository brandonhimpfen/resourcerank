import json
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "data" / "evaluations.jsonl"
required = {"schema_version", "id", "resource", "submission", "assessment", "decision", "provenance"}
seen=set()
for n,line in enumerate(p.read_text(encoding="utf-8").splitlines(),1):
    obj=json.loads(line)
    missing=required-obj.keys()
    if missing: raise SystemExit(f"line {n}: missing {sorted(missing)}")
    if obj["id"] in seen: raise SystemExit(f"line {n}: duplicate id {obj['id']}")
    seen.add(obj["id"])
print(f"Validated {len(seen)} evaluation records.")
