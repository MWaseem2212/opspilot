DEPLOYMENTS_DATA_SOURCE = {
    "checkout-api": [
        {
            "deployment_id": "DEP-4471",
            "deployed_at": "2026-08-15T02:04:00Z",
            "changed_by": "ci-pipeline",
            "change_summary": "Reduced payment gateway timeout from 5000ms to 3000ms",
        }
    ],
    "catalog-api": [],
    "auth-service": [
        {
            "deployment_id": "DEP-4502",
            "deployed_at": "2026-08-16T14:00:00Z",
            "changed_by": "ci-pipeline",
            "change_summary": "Updated auth token validation module",
        }
    ],
    "orders-api": [
        {
            "deployment_id": "DEP-4518",
            "deployed_at": "2026-08-16T18:00:00Z",
            "changed_by": "ci-pipeline",
            "change_summary": "Deployed new background job: order-reconciliation-worker",
        }
    ],
    "notification-worker": [
        {
            "deployment_id": "DEP-4530",
            "deployed_at": "2026-08-16T16:45:00Z",
            "changed_by": "ci-pipeline",
            "change_summary": "Refactored notification object processing pipeline",
        }
    ],
    "payment-worker": [],
    "logging-service": [],
}


def get_recent_deployments(service: str) -> list:
    """
    Returns recent deployment history for a service.
    Data source: simulated for local development and evaluation.
    """
    return DEPLOYMENTS_DATA_SOURCE.get(service, [])