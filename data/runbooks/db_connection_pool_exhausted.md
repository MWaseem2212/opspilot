# Runbook: Database Connection Pool Exhausted

## Symptoms
- "connection pool exhausted" or "too many connections" errors
- Traffic volume is normal, not spiking
- Often follows a new deployment involving background jobs or workers

## Likely Causes
1. Newly deployed code not releasing connections properly (connection leak)
2. Pool size configured too low for current concurrent load
3. Long-running queries holding connections open

## Diagnosis Steps
1. Check recent deployments, especially background jobs or workers
2. Check active connection count trend over time
3. Look for long-running or stuck queries

## Recommended Action
- If tied to a recent deployment: rollback that deployment
- If gradual growth with no deployment: investigate for a slow leak, consider restart as short-term mitigation

## Severity Guidance
- High: create/write operations failing, but reads may still work