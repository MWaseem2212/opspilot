from pydantic import BaseModel, Field
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

class IncidentAnalysis(BaseModel):
    likely_cause: str = Field(description="One sentence explaining the most probable root cause based on evidence")
    severity: Severity = Field(description="Assessed severity based on the evidence")
    recommended_action: str = Field(description="One clear, actionable next step")
    confidence: str = Field(description="One of: low, medium, high - how confident the analysis is given the evidence")
    