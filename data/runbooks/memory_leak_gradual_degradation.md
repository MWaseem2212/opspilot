# Runbook: Gradual Memory Growth / OOM Restarts

## Symptoms
- Memory usage climbs steadily over hours, not a sudden spike
- Periodic OOM kill and restart events
- Performance degrades before each restart

## Likely Causes
1. Memory leak in recently changed code (unreleased references)
2. Unbounded cache or queue growing without eviction
3. Third-party library known memory leak issue

## Diagnosis Steps
1. Correlate memory growth start time with deployment history
2. Check if any in-memory cache/queue lacks a size limit
3. Review recent code changes for object retention patterns

## Recommended Action
- If tied to recent deployment: rollback
- If long-standing: use scheduled restarts as mitigation while root cause is investigated

## Severity Guidance
- Medium: degraded performance with automated recovery via restarts
- High: if restarts cause user-facing downtime