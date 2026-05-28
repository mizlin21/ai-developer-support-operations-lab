# Operational Logs

This folder contains simulated operational logs for the AI Developer Support Operations Lab.

The logs represent evidence connected to developer support tickets, including:

- authentication failures
- webhook delivery failures
- SDK configuration errors
- API timeouts
- rate limiting
- integration sync failures

Each ticket in `data/tickets/developer_support_tickets.json` references one log file using the `sample_log_ref` field.

These logs are used by the troubleshooting engine to extract operational evidence and produce structured findings.