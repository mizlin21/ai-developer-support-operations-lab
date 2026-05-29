# API Rate Limiting Troubleshooting

## Applies To

429 responses, quota enforcement, burst traffic, throttling, and delayed batch jobs.

## Common Signals

- 429 Too Many Requests
- rate limit exceeded
- quota exceeded
- burst limit reached
- delayed sync job

## Troubleshooting Steps

1. Review request volume.
2. Compare usage against quota limits.
3. Identify burst traffic patterns.
4. Implement exponential backoff.
5. Reduce unnecessary retry loops.
6. Request limit review if business usage has changed.

## Escalation Criteria

Escalate if rate limiting appears incorrect, affects production-critical workflows, or impacts a customer with approved higher limits.

## Recommended Response

The logs indicate rate limit enforcement. Review request volume, quota limits, retry behavior, and implement exponential backoff where appropriate.