# demo/aliases.sh — load before the talk with:  source demo/aliases.sh
DATASET=tests/eval/datasets/concierge-dataset.json

d1ls()     { ls -lh demo/v1/; }
d1call()   { jq '.. | .function_call? // empty | select(.name=="book" and ((.args.n // "") | test("kids")))' demo/v1/traces.json; }
d1resp()   { jq '.. | .function_response? // empty | select(.name=="book" and .response.party_size==40)' demo/v1/traces.json; }
d1cancel() { jq '.. | .function_call? // empty | select(.name=="cancel")' demo/v1/traces.json; }
d1scores() { jq '.summary_metrics[] | {metric_name, mean_score}' demo/v1/results.json; }
d1live()   { agents-cli eval grade --traces demo/v1/traces.json --output /tmp/live_grades/; }

d2raw()    { agents-cli eval compare demo/v1/results.json demo/v4/results.json | jq '.changed_keys'; }
d2gate()   { python3 scripts/eval_gate.py demo/v1/results.json demo/v4/results.json --dataset "$DATASET"; }
d2fixed()  { python3 scripts/eval_gate.py demo/v4/results.json demo/v5/results.json --dataset "$DATASET"; }
