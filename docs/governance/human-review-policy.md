# Human Review Policy

This document defines when human review is required in the AI Developer Support Operations Lab.

---

# Purpose

The human review policy ensures that AI-assisted outputs remain subject to appropriate operational oversight, evidence validation, and human accountability.

---

# Human Review Required

Human review is required when:

- the issue affects production
- severity is high or critical
- customer data may be affected
- authentication, access, or credentials are involved
- engineering escalation is recommended
- logs are incomplete or ambiguous
- deterministic evidence conflicts with AI-assisted recommendations
- the recommended action requires a configuration change
- the recommendation could affect customer-facing systems

---

# Human Review Recommended

Human review is recommended when:

- severity confidence is low
- category confidence is low
- ticket details are incomplete
- root cause findings conflict
- KB retrieval status is missing or unclear
- the issue affects a new or unknown service

---

# Actions AI Should Not Perform Autonomously

The system should not autonomously:

- close customer tickets
- send customer-facing responses
- rotate credentials
- modify access permissions
- change customer configurations
- approve engineering escalations
- suppress alerts
- resolve production incidents

---

# Review Workflow

```text
AI-Assisted Output
      ↓
Support Engineer Review
      ↓
Evidence Validation
      ↓
KB Confirmation
      ↓
Escalation or Response Decision
      ↓
Human-Owned Action
```

---

# Accountability Position

The system may assist with decision preparation.

Humans remain accountable for operational decisions, escalation outcomes, and customer-impacting actions.
