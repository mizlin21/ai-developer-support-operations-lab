# AI Usage Guidelines

This document defines how AI should and should not be used in the AI Developer Support Operations Lab.

---

# Purpose

The lab demonstrates AI-assisted developer support operations.

AI may help summarize, classify, retrieve, and organize information, but it should not silently make high-trust operational decisions without review.

---

# Approved AI Uses

AI can assist with:

- summarizing support tickets
- classifying issue categories
- suggesting severity levels
- retrieving relevant documentation
- drafting engineering handoffs
- summarizing log findings
- generating operational reports
- identifying repeated patterns

---

# Restricted AI Uses

AI should not independently:

- close production incidents
- rotate credentials
- change customer configurations
- modify access permissions
- approve escalations without human review
- send customer-facing responses without validation
- override deterministic evidence
- invent root causes not found in logs or documentation

---

# Evidence-First Principle

The system should prioritize:

```text
ticket data
    ↓
log evidence
    ↓
knowledge base documentation
    ↓
human review
    ↓
AI-assisted summary
```

AI output should be grounded in available evidence.

---

# Human-in-the-Loop Requirements

Human review is required when:

- production systems are affected
- severity is high or critical
- the issue involves authentication or access control
- customer data may be affected
- the recommendation involves engineering action
- logs are incomplete or ambiguous

---

# Explainability Requirements

AI-assisted outputs should include:

- source ticket
- related logs
- classification method
- retrieval method
- root cause evidence
- recommended actions
- escalation reason

---

# Deterministic Validation Principle

AI-assisted outputs should not override deterministic operational evidence.

Classification rules, log analysis, and retrieval workflows provide structured evidence that should remain reviewable and reproducible.

AI-generated summaries should support operational understanding, not replace validated evidence.

---

# Governance Position

This lab treats AI as an operational assistant that supports human decision-making, not an autonomous operational authority.

The system improves speed and consistency, while humans remain responsible for final operational decisions.