# Runbook: 5xx Spike on checkout-api After Deployment

## Symptoms
- Sudden increase in 5xx errors on `/checkout/complete`
- Timing correlates with a recent deployment (within 15 minutes)
- Error logs show timeout-related failures

## Likely Causes
1. Recent deployment changed a timeout or config value
2. Downstream dependency (payment gateway) became slower than expected
3. New code path introduced an unhandled exception

## Diagnosis Steps
1. Check deployment history for `checkout-api` in the last 30 minutes
2. Compare error rate before/after deployment timestamp
3. Check payment-gateway latency metrics for the same window

## Recommended Action
- If error spike directly follows a deployment: **rollback the deployment**
- If no recent deployment: escalate to on-call payment team

## Severity Guidance
- High: error rate > 5% sustained for 5+ minutes
- Critical: error rate > 20% or checkout fully unavailable