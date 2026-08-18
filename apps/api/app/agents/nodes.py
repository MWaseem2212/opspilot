from app.agents.state import IncidentState
from app.tools.metrics import get_service_metrics
from app.tools.logs import search_logs
from app.tools.deployments import get_recent_deployments
from app.services.llm import get_llm
from app.schemas.incident import IncidentAnalysis

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
    Node: uses the LLM with structured output to analyze evidence
    and produce a typed, machine-readable incident analysis.
    """

    llm = get_llm()

    structured_llm = llm.with_structured_output(IncidentAnalysis)

    prompt = f"""You are an SRE incident analysis assistant. Analyze the evidence below
        and produce a concise summary.

        Incident: {state['error_signature']} on service '{state['service']}'

        Metrics:
        {state.get('metrics')}

        Error Logs:
        {state.get('logs')}

        Recent Deployments:
        {state.get('deployments')}

        Based ONLY on the evidence above, provide:
        1. Likely root cause (one sentence)
        2. Severity assessment (low/medium/high/critical)
        3. Recommended next action (one sentence)

        Do not speculate beyond what the evidence shows. If evidence is insufficient, say so.
        """

    analysis: IncidentAnalysis = structured_llm.invoke(prompt)

    return {"summary": analysis.model_dump()}

    # metrics = state.get("metrics", {})
    # logs = state.get("logs", [])
    # deployments = state.get("deployments", [])

    # summary_parts = []

    # if metrics:
    #     summary_parts.append(
    #         f"Error rate is {metrics.get('error_rate_percent')}% "
    #         f"with p95 latency {metrics.get('p95_latency_ms')}ms."
    #     )

    # if logs:
    #     summary_parts.append(f"Found {len(logs)} error log entries.")

    # if deployments:
    #     latest = deployments[0]
    #     summary_parts.append(
    #         f"Recent deployment {latest['deployment_id']}: {latest['change_summary']}."

    #     )
    # else:
    #     summary_parts.append("No recent deployments found for this service.")

    # summary_text = " ".join(summary_parts)

    # return {"summary": summary_text}