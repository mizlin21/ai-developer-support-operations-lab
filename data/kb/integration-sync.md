# Integration Sync Troubleshooting

## Applies To

CRM sync failures, field mapping problems, partial synchronization, stale records, and invalid external system mappings.

## Common Signals

- partial sync failure
- invalid field mapping
- failed records
- stale customer data
- field validation failure

## Troubleshooting Steps

1. Identify failed records.
2. Review field mapping configuration.
3. Validate external system schema.
4. Correct invalid mappings.
5. Rerun the sync job.
6. Confirm failed records are resolved.

## Escalation Criteria

Escalate if production customer data is stale, many records fail, or the sync service itself appears degraded.

## Recommended Response

The logs indicate field mapping failures during sync. Review the failed field, correct the mapping configuration, and rerun the sync job.