from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentAlert(BaseModel):
    alert_id: str
    service: str
    error_signature: str
    timestamp: datetime
    severity: Severity