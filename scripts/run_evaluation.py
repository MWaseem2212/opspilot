import json
import sys
import os
import glob
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps", "api"))

from app.agents.graph import build_incident_graph
from app.services.llm import get_llm

incident_files = sorted(glob.glob("data/incidents/*.json"))
graph = build_incident_graph()
llm = get_llm()

results = []


def invoke_with_retry(graph, state, max_retries=3):
    """
    Calls the graph, retrying on transient LLM/API failures.
    """
    for attempt in range(max_retries):
        try:
            return graph.invoke(state)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"  Retry {attempt + 1}/{max_retries} after error: {e}")
            time.sleep(2)


def judge_cause_match(agent_cause: str, ground_truth_cause: str) -> bool:
    """
    Uses the LLM as a judge to determine if the agent's stated cause
    semantically matches the ground truth cause, even with different wording.
    """
    prompt = f"""You are evaluating an SRE incident analysis system.

Ground truth root cause: {ground_truth_cause}

Agent's stated root cause: {agent_cause}

Does the agent's root cause identify the same underlying issue as the ground
truth, even if worded differently? Answer with exactly one word: YES or NO."""

    response = llm.invoke(prompt)
    return "YES" in response.content.upper()


for file_path in incident_files:
    with open(file_path) as f:
        incident_data = json.load(f)

    initial_state = {
        "alert_id": incident_data["alert_id"],
        "service": incident_data["service"],
        "error_signature": incident_data["error_signature"],
        "metrics": None,
        "logs": None,
        "deployments": None,
        "summary": None,
    }

    result = invoke_with_retry(graph, initial_state)
    analysis = result["summary"]
    ground_truth = incident_data["ground_truth"]

    cause_correct = judge_cause_match(
        analysis["likely_cause"], ground_truth["likely_cause"]
    )
    severity_correct = analysis["severity"].value == ground_truth["expected_severity"]

    results.append(
        {
            "alert_id": incident_data["alert_id"],
            "service": incident_data["service"],
            "cause_correct": cause_correct,
            "severity_correct": severity_correct,
            "agent_cause": analysis["likely_cause"],
            "ground_truth_cause": ground_truth["likely_cause"],
            "agent_severity": analysis["severity"].value,
            "ground_truth_severity": ground_truth["expected_severity"],
        }
    )

    status = "PASS" if cause_correct else "FAIL"
    print(f"[{status}] {incident_data['alert_id']} — cause_correct={cause_correct}, severity_correct={severity_correct}")

# Summary
total = len(results)
cause_accuracy = sum(r["cause_correct"] for r in results) / total * 100
severity_accuracy = sum(r["severity_correct"] for r in results) / total * 100

print(f"\n{'=' * 50}")
print(f"EVALUATION SUMMARY")
print(f"{'=' * 50}")
print(f"Total scenarios: {total}")
print(f"Cause accuracy: {cause_accuracy:.1f}%")
print(f"Severity accuracy: {severity_accuracy:.1f}%")

# Save report to file
report = {
    "run_at": datetime.now(timezone.utc).isoformat(),
    "total_scenarios": total,
    "cause_accuracy_percent": round(cause_accuracy, 1),
    "severity_accuracy_percent": round(severity_accuracy, 1),
    "results": results,
}

with open("data/evaluation_report.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"\nReport saved to data/evaluation_report.json")