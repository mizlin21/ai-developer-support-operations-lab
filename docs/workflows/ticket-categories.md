# Ticket Categories

This document defines the issue categories used in the AI Developer Support Operations Lab.

---

# Authentication

Issues involving API keys, OAuth flows, access tokens, expired credentials, invalid scopes, or identity configuration.

Example signals:

- 401 Unauthorized
- invalid API key
- expired token
- OAuth callback failure
- missing permission scope

---

# Webhook

Issues involving event delivery, endpoint failures, retries, malformed payloads, or signature verification.

Example signals:

- failed webhook delivery
- endpoint returned 500
- missing event
- invalid webhook signature
- retry exhaustion

---

# SDK

Issues involving client libraries, local configuration, missing environment variables, package versions, or initialization errors.

Example signals:

- SDK initialization failure
- missing config
- package version conflict
- local environment mismatch

---

# API Performance

Issues involving latency, timeouts, degraded services, gateway errors, or production performance degradation.

Example signals:

- 504 Gateway Timeout
- slow API response
- elevated latency
- service degradation

---

# Rate Limiting

Issues involving usage limits, request throttling, quota enforcement, or burst traffic.

Example signals:

- 429 Too Many Requests
- quota exceeded
- burst limit reached
- delayed sync job

---

# Integration Sync

Issues involving data synchronization, field mappings, partial sync failures, or external system integration problems.

Example signals:

- partial sync failure
- invalid field mapping
- missing records
- stale customer data

---

# Deployment

Issues involving CI/CD failures, rollback events, release errors, failed builds, or environment-specific deployment problems.

Example signals:

- failed deployment
- rollback triggered
- failed build pipeline
- environment mismatch

---

# Permissions

Issues involving role-based access control, account permissions, missing privileges, or restricted resources.

Example signals:

- 403 Forbidden
- missing role
- insufficient privileges
- access denied