from fastapi import FastAPI
from app.schemas.incident import IncidentAlert
from app.tools.metrics import get_service_metrics

app = FastAPI(title="OpsPilot API")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "opspilot-api"}

@app.post("/incidents")
def receive_incident(incident: IncidentAlert):
    return {
        "message": "Incident received",
        "alert_id": incident.alert_id,
        "severity": incident.severity,
    }

@app.get("/tools/metrics/{service}")
def read_service_metrics(service: str):
    return get_service_metrics(service)