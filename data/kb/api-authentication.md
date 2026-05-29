# API Authentication Troubleshooting

## Applies To

Authentication issues involving API keys, OAuth tokens, expired credentials, and unauthorized API requests.

## Common Signals

- 401 Unauthorized
- expired API token
- invalid API key
- OAuth token failure
- missing permission scope

## Troubleshooting Steps

1. Confirm the API key or token is present.
2. Check whether the token has expired.
3. Verify token scopes and permissions.
4. Rotate the API key if expiration or compromise is suspected.
5. Retry the request using a validated credential.

## Escalation Criteria

Escalate if the issue affects production systems, multiple customers, or appears related to authentication service availability.

## Recommended Response

The logs indicate an authentication failure. Validate the API token, confirm expiration status, rotate credentials if needed, and verify that the integration is using the correct scopes.