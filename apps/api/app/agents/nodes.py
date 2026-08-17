from app.agents.state import IncidentState
from app.tools.metrics import get_service_metrics
from app.tools.logs import search_logs
from app.tools.deployments import get_recent_deployments

def fetch_metrics(state: IncidentState) -> IncidentState:
    """
    Node: calls the metrics tool and writes the result into state.
    """
    service = state["service"]
    metrics_result = get_service_metrics(service)

    return {"metrics": metrics_result}

def fetch_logs(state: IncidentState) -> IncidentState:
    """
    Node: calls the logs tool and writes the result into state.
    """
    service = state["service"]
    logs_result = search_logs(service, level="ERROR")

    return {"logs": logs_result}

def fetch_deployments(state: IncidentState) -> IncidentState:
    """
    Node: calls the deployments tool and writes the result into state.
    """
    service = state["service"]
    deployments_result = get_recent_deployments(service)

    return {"deployments": deployments_result} 


def generate_summary(state: IncidentState) -> IncidentState:
    """
    Node: combines gathered evidence into a human-readable summary.
    Rule-based for now — will be replaced with an LLM call in the next step.
    """

    metrics = state.get("metrics", {})
    logs = state.get("logs", [])
    deployments = state.get("deployments", [])

    summary_parts = []

    if metrics:
        summary_parts.append(
            f"Error rate is {metrics.get('error_rate_percent')}% "
            f"with p95 latency {metrics.get('p95_latency_ms')}ms."
        )

    if logs:
        summary_parts.append(f"Found {len(logs)} error log entries.")

    if deployments:
        latest = deployments[0]
        summary_parts.append(
            f"Recent deployment {latest['deployment_id']}: {latest['change_summary']}."

        )
    else:
        summary_parts.append("No recent deployments found for this service.")

    summary_text = " ".join(summary_parts)

    return {"summary": summary_text}