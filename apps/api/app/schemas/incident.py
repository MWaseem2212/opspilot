from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import Optional
import uuid

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
    requires_approval: bool = Field(description="True if the recommended action would change system state (rollback, restart, scale, config change). False if the action is informational or read-only only.")


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REGECTED = "regected"
    NOT_REQUIRED = "not_required"

class IncidentRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    alert_id: str
    service: str
    analysis: IncidentAnalysis
    approval_status: ApprovalStatus

