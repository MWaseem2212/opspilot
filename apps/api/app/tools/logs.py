LOGS_DATA_SOURCE = {
    "checkout-api": [
        {"timestamp": "2026-08-15T02:11:32Z", "level": "ERROR", "message": "Payment gateway timeout after 3000ms on /checkout/complete"},
        {"timestamp": "2026-08-15T02:12:05Z", "level": "ERROR", "message": "Payment gateway timeout after 3000ms on /checkout/complete"},
        {"timestamp": "2026-08-15T02:13:47Z", "level": "WARN", "message": "Retry attempt 2/3 for payment confirmation"},
    ],
    "catalog-api": [
        {"timestamp": "2026-08-16T09:28:10Z", "level": "WARN", "message": "Redis eviction triggered, key count reduced under memory pressure"},
        {"timestamp": "2026-08-16T09:29:44Z", "level": "WARN", "message": "Cache miss rate elevated for search queries"},
    ],
    "auth-service": [
        {"timestamp": "2026-08-16T14:04:10Z", "level": "ERROR", "message": "Container failed readiness probe: startup error in auth token module"},
        {"timestamp": "2026-08-16T14:04:15Z", "level": "ERROR", "message": "Pod crash loop detected, restart count exceeded threshold"},
    ],
    "orders-api": [
        {"timestamp": "2026-08-16T18:18:02Z", "level": "ERROR", "message": "connection pool exhausted: unable to acquire connection after 5000ms"},
        {"timestamp": "2026-08-16T18:19:30Z", "level": "ERROR", "message": "connection pool exhausted: unable to acquire connection after 5000ms"},
    ],
    "notification-worker": [
        {"timestamp": "2026-08-16T22:35:00Z", "level": "WARN", "message": "Memory usage exceeded 85% threshold"},
        {"timestamp": "2026-08-16T22:38:12Z", "level": "ERROR", "message": "OOM killer terminated worker process, restarting"},
    ],
    "payment-worker": [
        {"timestamp": "2026-08-17T03:08:00Z", "level": "ERROR", "message": "Timeout connecting to external payment gateway (upstream_timeout)"},
        {"timestamp": "2026-08-17T03:09:15Z", "level": "ERROR", "message": "Timeout connecting to external payment gateway (upstream_timeout)"},
    ],
    "logging-service": [
        {"timestamp": "2026-08-17T07:50:00Z", "level": "ERROR", "message": "Write failed: no space left on device"},
        {"timestamp": "2026-08-17T07:52:33Z", "level": "ERROR", "message": "Write failed: no space left on device"},
    ],
}


def search_logs(service: str, level: str = "ERROR") -> list:
    """
    Returns recent log entries for a service, filtered by log level.
    Data source: simulated for local development and evaluation.
    """
    all_logs = LOGS_DATA_SOURCE.get(service, [])
    return [log for log in all_logs if log["level"] == level]