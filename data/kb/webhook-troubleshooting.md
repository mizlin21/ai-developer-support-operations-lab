# Webhook Troubleshooting

## Applies To

Webhook delivery issues, failed event delivery, retries, endpoint failures, and signature validation problems.

## Common Signals

- webhook delivery failed
- retry exhaustion
- endpoint returned 500
- missing events
- invalid webhook signature

## Troubleshooting Steps

1. Confirm the receiving endpoint is online.
2. Check endpoint response codes.
3. Review webhook retry history.
4. Validate signature verification logic.
5. Confirm the subscribed event type is enabled.
6. Replay failed events if supported.

## Escalation Criteria

Escalate if webhook delivery failures affect production automation, multiple event types, or retry exhaustion continues after endpoint recovery.

## Recommended Response

The logs indicate webhook delivery failures after retry attempts. Verify endpoint health, inspect server-side errors, validate webhook signature handling, and review retry history.