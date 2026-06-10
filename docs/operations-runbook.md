# Operations Runbook

This runbook explains how to operate the AI Developer Support Operations Lab pipeline.

---

# Purpose

The operations runbook provides a repeatable process for running the simulated support pipeline and reviewing its outputs.

---

# Full Pipeline Command Sequence

Run these commands from the project root:

```powershell
python -m src.classification.classifier
python -m src.troubleshooting.log_analyzer
python -m src.retrieval.retriever
python -m src.escalation.handoff_generator
python -m src.analytics.metrics_generator
```

---

# Expected Outputs

After running the full pipeline, the following files should be generated:

```text
data/outputs/classified_tickets.json
data/outputs/troubleshooting_findings.json
data/outputs/retrieval_results.json
data/outputs/engineering_handoffs.json
data/outputs/operations_metrics.json
```

# Operational Review Checklist

## 1. Classification Review

Open:

```text
data/outputs/classified_tickets.json
```


Check:

- Were all tickets classified?
- Do categories match the ticket content?
- Are severity levels reasonable?
- Are escalation decisions explainable?

## 2. Troubleshooting Review

Open:

```text
data/outputs/troubleshooting_findings.json
```

Check:

- Was the related log file found?
- Were status codes extracted?
- Were log levels extracted?
- Were root cause findings detected?
- Are recommended actions tied to log evidence?

## 3. Retrieval Review

Open:

```text
data/outputs/retrieval_results.json
```

Check:

- Did each ticket match a KB article?
- Is the article relevant to the issue category?
- Are root causes connected to documentation?
- Are recommendations grounded in approved guidance?

## 4. Engineering Handoff Review

Open:

```text
data/outputs/engineering_handoffs.json
```

Check:

- Are only escalated tickets included?
- Does each handoff include evidence?
- Does each handoff include root causes?
- Is priority assignment reasonable?
- Is the handoff ready for human review?

## 5. Metrics Review

Open:

```text
data/outputs/operations_metrics.json
```

Check:

- Total tickets processed
- Escalation rate
- Knowledge base match rate
- Category distribution
- Severity distribution
- Root cause frequency
- Handoff priority distribution

---

# Troubleshooting Common Issues

## Missing Output Files

Run the pipeline in order.

The retrieval layer depends on classification and troubleshooting outputs.

The escalation layer depends on classification, troubleshooting, and retrieval outputs.

The analytics layer depends on all prior outputs.

---

## Incorrect Retrieval Results

Check:

* `predicted_category` in `classified_tickets.json`
* `KB_INDEX` in `src/retrieval/retriever.py`
* available markdown files in `data/kb/`

---

## Unexpected Escalation Results

Check:

* `ESCALATION_TRIGGERS` in `src/classification/rules.py`
* severity rules in `src/classification/rules.py`
* environment field in the ticket dataset

---

# Operational Principle

Each stage produces artifacts that downstream stages consume.

This means the pipeline should always be run in order when major inputs or rules change.

# Operational Context

The runbook is designed to simulate how an operations or developer support team would validate pipeline outputs during daily workflow review.


