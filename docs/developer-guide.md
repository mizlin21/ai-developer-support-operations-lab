# Developer Guide

This guide explains how to run and understand the AI Developer Support Operations Lab.

---

# Project Purpose

The AI Developer Support Operations Lab simulates an enterprise developer support environment where AI-assisted workflows help classify technical issues, analyze logs, retrieve documentation, generate engineering handoffs, and produce operational metrics.

The lab is designed to demonstrate how developer support operations can be structured around evidence, documentation, escalation, and governance.

---

# System Pipeline

```text
Support Tickets
      ↓
Classification Engine
      ↓
Troubleshooting Engine
      ↓
Knowledge Base Retrieval
      ↓
Engineering Handoff Generator
      ↓
Operations Metrics Generator
```

# Main Input Files

| File                                          | Purpose                                              |
| --------------------------------------------- | ---------------------------------------------------- |
| `data/tickets/developer_support_tickets.json` | Simulated developer support tickets                  |
| `data/logs/`                                  | Operational log files connected to tickets           |
| `data/kb/`                                    | Knowledge base articles and troubleshooting runbooks |

# Main Output Files

| File                                         | Purpose                                   |
| -------------------------------------------- | ----------------------------------------- |
| `data/outputs/classified_tickets.json`       | Ticket classification results             |
| `data/outputs/troubleshooting_findings.json` | Log analysis and root cause findings      |
| `data/outputs/retrieval_results.json`        | Knowledge base retrieval results          |
| `data/outputs/engineering_handoffs.json`     | Structured engineering handoff records    |
| `data/outputs/operations_metrics.json`       | Operational analytics and support metrics |

# How to Run the Full Pipeline

From the project root, run:

```powershell
python -m src.classification.classifier
python -m src.troubleshooting.log_analyzer
python -m src.retrieval.retriever
python -m src.escalation.handoff_generator
python -m src.analytics.metrics_generator
```


# How the Components Work Together

## Classification Engine

Reads support tickets and predicts:

- issue category
- severity
- escalation need
- confidence scores
- recommended next action

## Troubleshooting Engine

Reads related log files and extracts:

- services
- status codes
- log levels
- latency values
- root cause findings
- recommended actions

## Retrieval Layer

Maps classified ticket categories to approved knowledge base articles.

This keeps support guidance grounded in documentation.

## Escalation Layer

Generates structured engineering handoffs for tickets that require review.

## Analytics Layer

Produces operational metrics such as:

- escalation rate
- category distribution
- severity distribution
- KB match rate
- root cause frequency
- handoff priority distribution

# Design Philosophy

This project follows an evidence-first workflow:

```text
Raw ticket
    ↓
Structured classification
    ↓
Log evidence
    ↓
Approved documentation
    ↓
Human-reviewed escalation
    ↓
Operational reporting
```

The system does not rely solely on unsupported AI-generated answers.

Instead, it prioritizes evidence, deterministic analysis, approved documentation, and human-reviewed escalation workflows.
