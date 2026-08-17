from langgraph.graph import StateGraph, START, END
from app.agents.state import IncidentState
from app.agents.nodes import fetch_metrics, fetch_logs, fetch_deployments, generate_summary

def build_incident_graph():
    graph = StateGraph(IncidentState)

    graph.add_node("fetch_metrics", fetch_metrics)
    graph.add_node("fetch_logs", fetch_logs)
    graph.add_node("fetch_deployments", fetch_deployments)
    graph.add_node("generate_summary", generate_summary)

    graph.add_edge(START, "fetch_metrics")
    graph.add_edge("fetch_metrics", "fetch_logs")
    graph.add_edge("fetch_logs", "fetch_deployments")
    graph.add_edge("fetch_deployments", "generate_summary")
    graph.add_edge("generate_summary", END)

    return graph.compile()
