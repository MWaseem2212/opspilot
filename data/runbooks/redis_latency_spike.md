# Runbook: Redis Latency / Cache Hit Rate Drop

## Symptoms
- p95 latency increases significantly with no recent deployment
- Cache hit rate metric drops
- Primary database load increases

## Likely Causes
1. Redis memory pressure causing key eviction
2. Redis instance under-provisioned for current traffic
3. A recent change in cache key patterns increasing cardinality

## Diagnosis Steps
1. Check Redis memory usage and eviction count
2. Compare cache hit rate before/after the latency increase
3. Check if database query volume increased proportionally

## Recommended Action
- If eviction count is high: scale Redis memory or add a node
- If no eviction but hit rate still low: investigate recent cache key changes

## Severity Guidance
- Medium: latency degraded but service still functional
- High: latency causing timeouts or user-facing failures