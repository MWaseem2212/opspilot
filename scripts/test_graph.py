import json
import sys
import os
import glob

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps", "api"))

from app.agents.graph import build_incident_graph

incident_files = sorted(glob.glob("data/incidents/*.json"))
graph = build_incident_graph()

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

    result = graph.invoke(initial_state)

    print(f"\n{'=' * 60}")
    print(f"Incident: {incident_data['alert_id']} — {incident_data['service']}")
    print(f"{'=' * 60}")
    print(f"Ground truth cause: {incident_data['ground_truth']['likely_cause']}")
    print(f"Ground truth action: {incident_data['ground_truth']['correct_action']}")
    print(f"\nAgent output:")
    print(f"  Cause: {result['summary']['likely_cause']}")
    print(f"  Severity: {result['summary']['severity']}")
    print(f"  Action: {result['summary']['recommended_action']}")
    print(f"  Confidence: {result['summary']['confidence']}")