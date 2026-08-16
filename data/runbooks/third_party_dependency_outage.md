# Runbook: Third-Party Dependency Outage

## Symptoms
- Timeouts or failures calling an external service
- No correlation with our own recent deployments
- External provider's status page shows an incident

## Likely Causes
1. Third-party provider outage
2. Network/DNS issue reaching the third party
3. Rate limiting from the third-party provider

## Diagnosis Steps
1. Check our own deployment history first — rule out self-inflicted cause
2. Check the third-party provider's public status page
3. Check if error is isolated to one provider or affects multiple external calls

## Recommended Action
- Do NOT rollback our own deployments if no correlation found
- Enable fallback provider if available, or queue requests for retry
- Notify stakeholders this is an external dependency issue, not ours

## Severity Guidance
- Critical: if this blocks a core user flow like payments