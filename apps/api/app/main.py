from fastapi import FastAPI
from app.schemas.incident import IncidentAlert, IncidentRecord, ApprovalStatus
from app.tools.metrics import get_service_metrics
from app.tools.logs import search_logs
from app.tools.deployments import get_recent_deployments
from app.agents.graph import build_incident_graph
from app.services.store import save_record, get_record, list_records

app = FastAPI(title="OpsPilot API")
incident_graph = build_incident_graph()

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "opspilot-api"}

# @app.post("/incidents")
# def receive_incident(incident: IncidentAlert):
#     return {
#         "message": "Incident received",
#         "alert_id": incident.alert_id,
#         "severity": incident.severity,
#     }

# @app.get("/tools/metrics/{service}")
# def read_service_metrics(service: str):
#     return get_service_metrics(service)

# @app.get("/tools/logs/{service}")
# def read_service_logs(service: str, level: str = "ERROR"):
#     return search_logs(service, level)

# @app.get("/tools/deployments/{service}")
# def read_recent_deployments(service: str):
#     return get_recent_deployments(service)

@app.post("/incidents/analyze")
def analyze_incident(incident: IncidentAlert):
    initial_state = {
        "alert_id": incident.alert_id,
        "service": incident.service,
        "error_signature": incident.error_signature,
        "metrics": None,
        "logs": None,
        "deployments": None,
        "summary": None,
    }

    result = incident_graph.invoke(initial_state)
    analysis = result["summary"]

    status = ApprovalStatus.PENDING if analysis["requires_approval"] else ApprovalStatus.NOT_REQUIRED

    record = IncidentRecord(
        alert_id=incident.alert_id,
        service=incident.service,
        analysis=analysis,
        approval_status=status,
    )

    save_record(record)
    return record

@app.get("/incidents")
def get_all_incidents():
    return list_records()

@app.get("/incidents/{record_id}")
def get_incident(record_id: str):
    record = get_record(record_id)
    if not record:
        return {"error": "Record not found"}
    return record

@app.post("/incidents/{record_id}/approve")
def approve_incident(record_id: str):
    record = get_record(record_id)
    if not record:
        return {"error": "Record not found"}

    if record.approval_status != ApprovalStatus.PENDING:
        return {"error": f"Record is not pending approval (current status: {record.approval_status})"}

    record.approval_status = ApprovalStatus.APPROVED
    save_record(record)
    return record


@app.post("/incidents/{record_id}/reject")
def reject_incident(record_id: str):
    record = get_record(record_id)
    if not record:
        return {"error": "Record not found"}

    if record.approval_status != ApprovalStatus.PENDING:
        return {"error": f"Record is not pending approval (current status: {record.approval_status})"}

    record.approval_status = ApprovalStatus.REJECTED
    save_record(record)
    return record