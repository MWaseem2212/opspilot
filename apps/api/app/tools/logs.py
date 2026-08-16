from datetime import datetime

LOGS_DATA_SOURCE = {
    "checkout-api": [
        {
            "timestamp": "2026-08-15T02:11:32Z",
            "level": "ERROR",
            "message": "Payment gateway timeout after 3000ms on /checkout/complete",
        },
        {
            "timestamp": "2026-08-15T02:12:05Z",
            "level": "ERROR",
            "message": "Payment gateway timeout after 3000ms on /checkout/complete",
        },
        {
            "timestamp": "2026-08-15T02:13:47Z",
            "level": "WARN",
            "message": "Retry attempt 2/3 for payment confirmation",
        },
    ]
}

def search_logs(service: str, level: str = "ERROR") -> list:
    """
    Returns recent log entries for a service, filtered by log level.
    Data source: simulated for local development and evaluation.
    """
    all_logs = LOGS_DATA_SOURCE.get(service, [])
    return [log for log in all_logs if log["level"] == level]