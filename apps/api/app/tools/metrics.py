from datetime import datetime

METRICS_DATA_SOURCE = {
    "checkout-api": {
        "error_rate_percent": 8.4,
        "p95_latency_ms": 2400,
        "requests_per_min": 1200,
        "checked_at": datetime.utcnow().isoformat(),
    },
    "catalog-api": {
        "error_rate_percent": 0.3,
        "p95_latency_ms": 3100,
        "requests_per_min": 2200,
        "cache_hit_rate_percent": 41,
        "checked_at": datetime.utcnow().isoformat(),
    },
    "auth-service": {
        "error_rate_percent": 100.0,
        "p95_latency_ms": 0,
        "requests_per_min": 0,
        "checked_at": datetime.utcnow().isoformat(),
    },
    "orders-api": {
        "error_rate_percent": 6.7,
        "p95_latency_ms": 4800,
        "requests_per_min": 950,
        "active_db_connections": 100,
        "max_db_connections": 100,
        "checked_at": datetime.utcnow().isoformat(),
    },
    "notification-worker": {
        "error_rate_percent": 1.2,
        "p95_latency_ms": 340,
        "requests_per_min": 600,
        "memory_usage_percent": 92,
        "checked_at": datetime.utcnow().isoformat(),
    },
    "payment-worker": {
        "error_rate_percent": 0.2,
        "p95_latency_ms": 180,
        "requests_per_min": 300,
        "checked_at": datetime.utcnow().isoformat(),
    },
    "logging-service": {
        "error_rate_percent": 4.5,
        "p95_latency_ms": 500,
        "requests_per_min": 800,
        "disk_usage_percent": 98,
        "checked_at": datetime.utcnow().isoformat(),
    },
}


def get_service_metrics(service: str) -> dict:
    """
    Returns current error rate, latency, and traffic metrics for a service.
    Data source: simulated for local development and evaluation.
    """
    return METRICS_DATA_SOURCE.get(
        service,
        {"error_rate_percent": 0.1, "p95_latency_ms": 120, "requests_per_min": 500},
    )