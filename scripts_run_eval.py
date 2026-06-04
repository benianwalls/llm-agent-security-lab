from pathlib import Path

from agentsec_lab.evaluator import run_evaluation, write_jsonl

results = []
results.extend(run_evaluation("vulnerable"))
results.extend(run_evaluation("defended"))

write_jsonl(results, Path("reports/results.jsonl"))

for item in results:
    print(item["case_id"], item["mode"], "attack_succeeded=", item["attack_succeeded"])