"""Pass rate per tag for one metric.

Usage: python scripts/slice_by_tag.py RESULTS.json DATASET.json [METRIC] [PASS_AT]
"""
import json
import sys
from collections import defaultdict

with open(sys.argv[1], encoding="utf-8") as f:
    results = json.load(f)
with open(sys.argv[2], encoding="utf-8") as f:
    dataset = json.load(f)
metric = sys.argv[3] if len(sys.argv) > 3 else "multi_turn_task_success"
pass_at = float(sys.argv[4]) if len(sys.argv) > 4 else 0.8

tags = [c.get("tags", []) for c in dataset["eval_cases"]]
by_tag = defaultdict(list)
for r in results["eval_case_results"]:
    score = (r["response_candidate_results"][0]["metric_results"].get(metric) or {}).get("score")
    if score is not None:
        for t in tags[r["eval_case_index"]] or ["untagged"]:
            by_tag[t].append(score >= pass_at)

for t, v in sorted(by_tag.items(), key=lambda kv: sum(kv[1]) / len(kv[1])):
    print(f"{t:20}{100 * sum(v) / len(v):6.0f}%   ({len(v)} cases)")
