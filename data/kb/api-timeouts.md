# API Timeout Troubleshooting

## Applies To

API latency, gateway timeouts, upstream service delays, degraded service performance, and timeout errors.

## Common Signals

- 504 Gateway Timeout
- elevated latency
- upstream timeout
- repeated timeout detected
- checkout or payment failure

## Troubleshooting Steps

1. Confirm the affected endpoint.
2. Review latency values.
3. Check upstream service health.
4. Identify whether timeouts are isolated or repeated.
5. Compare against normal latency thresholds.
6. Escalate to engineering if production transactions are impacted.

## Escalation Criteria

Escalate immediately if production checkout, payment processing, or customer-facing workflows are affected.

## Recommended Response

The logs show repeated timeout errors and elevated latency. Review upstream service health, affected endpoints, and escalate to engineering if production transactions are impacted.