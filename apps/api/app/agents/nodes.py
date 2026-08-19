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

    prompt = f"""You are an SRE incident analysis assistant. Analyze the evidence below.

Incident: {state['error_signature']} on service '{state['service']}'

Metrics:
{state.get('metrics')}

Error Logs:
{state.get('logs')}

Recent Deployments:
{state.get('deployments')}

Based ONLY on the evidence above, analyze the incident. Do not speculate beyond
what the evidence shows. If evidence is insufficient, reflect that in your
confidence level.

For requires_approval: set to True if your recommended action would change
system state (e.g. rollback a deployment, restart a service, scale resources,
change configuration). Set to False if the action is purely informational
(e.g. "investigate further", "gather more data", "monitor").
"""

    analysis: IncidentAnalysis = structured_llm.invoke(prompt)

    return {"summary": analysis.model_dump()}



    