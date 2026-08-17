import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps", "api"))

from app.agents.graph import build_incident_graph

with open("data/incidents/incident_001_checkout_5xx.json") as f:
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

graph = build_incident_graph()
result = graph.invoke(initial_state)

print("\n--- FINAL SUMMARY ---")
print(result["summary"])