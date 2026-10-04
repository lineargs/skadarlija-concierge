"""Readable compare + CI gate. Exits 1 if any metric drops more than --max-drop."""
import argparse
import glob
import json
import sys


def load(pattern):
    paths = sorted(glob.glob(pattern))
    if not paths:
        sys.exit(f"No file matches {pattern}")
    with open(paths[-1], encoding="utf-8") as f:
        return json.load(f)


def means(res):
    return {m["metric_name"]: m["mean_score"]
            for m in res.get("summary_metrics", []) if m.get("mean_score") is not None}


def case_scores(res, metric):
    out = {}
    for r in res.get("eval_case_results", []):
        mr = r["response_candidate_results"][0]["metric_results"].get(metric) or {}
        out[r["eval_case_index"]] = mr.get("score")
    return out


p = argparse.ArgumentParser()
p.add_argument("baseline")
p.add_argument("candidate")
p.add_argument("--max-drop", type=float, default=0.05)
p.add_argument("--dataset", help="dataset JSON, to label flipped cases with their tags")
p.add_argument("--pass-at", type=float, default=0.8)
a = p.parse_args()

base, cand = load(a.baseline), load(a.candidate)
mb, mc = means(base), means(cand)
tags = []
if a.dataset:
    with open(a.dataset, encoding="utf-8") as f:
        tags = [c.get("tags", []) for c in json.load(f)["eval_cases"]]

failed = False
print(f"{'metric':32}{'baseline':>10}{'candidate':>11}{'delta':>8}")
for name in sorted(mb.keys() | mc.keys()):
    b, c = mb.get(name), mc.get(name)
    if c is None:
        print(f"{name:32}{'MISSING in candidate':>29}")
        failed = True
        continue
    if b is None:
        print(f"{name:32}{'new':>10}{c:>11.2f}")
        continue
    bad = c - b < -a.max_drop
    failed |= bad
    print(f"{name:32}{b:>10.2f}{c:>11.2f}{c - b:>+8.2f}{'   REGRESSION' if bad else ''}")
    if bad and tags:
        sb, sc = case_scores(base, name), case_scores(cand, name)
        flips = [i for i, s in sc.items() if (sb.get(i) or 0) >= a.pass_at > (s or 0)]
        labels = sorted({t for i in flips for t in tags[i]})
        print(f"  newly failing: {len(flips)} cases, tags: {', '.join(labels)}")
sys.exit(1 if failed else 0)
