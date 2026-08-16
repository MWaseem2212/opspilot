# Runbook: Disk Space Full

## Symptoms
- Disk usage near or at 100%
- Write failures across the service
- Gradual buildup over days/weeks, not sudden

## Likely Causes
1. Log rotation/cleanup job disabled or failing
2. Unexpected data growth (large uploads, debug dumps)
3. Old backups or temp files not being cleaned up

## Diagnosis Steps
1. Check disk usage growth trend over the past weeks
2. Check status of scheduled cleanup/rotation jobs
3. Identify largest directories consuming space

## Recommended Action
- Immediate: manually clear safe-to-delete old logs/temp files to restore headroom
- Follow-up: re-enable or fix the automated cleanup job

## Severity Guidance
- High: active write failures affecting service functionality