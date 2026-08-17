from typing import TypedDict, Optional

class IncidentState(TypedDict):
    alert_id: str
    service: str
    error_signature: str

    metrics: Optional[dict]
    logs: Optional[list]
    deployments: Optional[list]

    summary: Optional[str]