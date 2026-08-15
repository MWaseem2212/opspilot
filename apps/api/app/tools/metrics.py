from datetime import datetime

METRICS_DATA_SOURSE = {
    "checkout-api": {
        "error_rate_percent": 8.4,
        "p95_latency_ms": 2400,
        "requests_per_min": 1200,
        "checked_at": datetime.utcnow().isoformat(),
    }
}

def get_service_metrics(service: str) -> dict:
    """
    Returns current error rate, latency, and traffic metrics for a service.

    Data source: simulated for local development and evaluation.
    Production implementation would call the monitoring provider's API
    (e.g. Datadog) using the same return contract.
    """

    return METRICS_DATA_SOURSE.get(
        service,
        {"error_rate_percent": 0.1, "p95_latency_ms": 120, "requests_per_min": 500},
    )