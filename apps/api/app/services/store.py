from typing import Optional
from app.schemas.incident import IncidentRecord

_RECORDS: dict[str, IncidentRecord] = {}

def save_record(record: IncidentRecord) -> None:
    _RECORDS[record.record_id] = record

def get_record(record_id: str) -> Optional[IncidentRecord]:
    return _RECORDS.get(record_id)

def list_records() -> list[IncidentRecord]:
    return list(_RECORDS.values())