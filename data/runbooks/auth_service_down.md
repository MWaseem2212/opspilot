# Runbook: Auth Service Complete Outage

## Symptoms
- 100% failure rate on login endpoints
- Health check endpoint failing
- Downstream services reporting auth token validation failures

## Likely Causes
1. Bad deployment causing pod crash loop
2. Database connection failure for auth-service specifically
3. Expired or misconfigured signing certificate

## Diagnosis Steps
1. Check deployment history immediately — this is the first suspect
2. Check pod/container restart count and crash logs
3. Verify auth database connectivity separately

## Recommended Action
- If recent deployment exists: rollback immediately, this is critical-severity
- If no recent deployment: escalate to platform team for infrastructure check

## Severity Guidance
- Critical: any full outage of auth blocks all user-facing functionality