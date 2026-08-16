DEPLOYMENTS_DATA_SOURCE = {
    "checkout-api": [
        {
            "deployment_id": "DEP-4471",
            "deployed_at": "2026-08-15T02:04:00Z",
            "changed_by": "ci-pipeline",
            "change_summary": "Reduced payment gateway timeout from 5000ms to 3000ms",
        }
    ]
}

def get_recent_deployments(service: str) -> list:
    """
    Returns recent deployment history for a service.
    Data source: simulated for local development and evaluation.
    """
    return DEPLOYMENTS_DATA_SOURCE.get(service, [])