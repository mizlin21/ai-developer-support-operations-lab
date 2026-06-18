# Demo Walkthrough

This walkthrough explains how to demonstrate the AI Developer Support Operations Lab during interviews or portfolio reviews.

---

# Demo Goal

The purpose of the demo is to show how the pipeline processes developer support issues from intake through governance review.

---

# Step 1 — Run the Pipeline

From the project root:

```powershell
python -m src.classification.classifier
python -m src.troubleshooting.log_analyzer
python -m src.retrieval.retriever
python -m src.escalation.handoff_generator
python -m src.analytics.metrics_generator
python -m src.utils.governance_audit_summary
```
---

# Step 2 — Review Ticket Classification

Open:

```text
data/outputs/classified_tickets.json
```

Explain:

- issue categories
- severity classification
- escalation logic
- confidence scoring
- deterministic rules

---

# Step 3 — Review Troubleshooting Findings

Open:

```text
data/outputs/troubleshooting_findings.json
```

Explain:

- log parsing
- status code extraction
- root cause detection
- evidence analysis
- operational recommendations

---

# Step 4 — Review Retrieval Results

Open:

```text
data/outputs/retrieval_results.json
```

Explain:

- category-to-KB mapping
- evidence-grounded retrieval
- support workflow consistency

---

# Step 5 — Review Engineering Handoffs

Open:

```text
data/outputs/engineering_handoffs.json
```

Explain:

- escalation criteria
- operational context
- root cause packaging
- engineering-ready workflows

---

# Step 6 — Review Operational Metrics

Open:

```text
data/outputs/operations_metrics.json
```

Explain:

- escalation rate
- ticket distribution
- root cause trends
- operational visibility
- support workflow analytics

---

# Step 7 — Review Governance Controls

Open:

```text
data/outputs/governance_audit_summary.json
```

Explain:

- human review requirements
- governance boundaries
- auditability
- AI operational safety
- deterministic controls

---

# Key Talking Point

The project is designed to demonstrate how AI-assisted operational workflows can remain:

- explainable
- evidence-based
- reviewable
- human-supervised
- operationally structured

---

# Demo Goal

The walkthrough is designed to help explain the operational architecture, governance model, and evidence-first workflow philosophy of the project during interviews and technical discussions.

---

# Key Talking Point

The project intentionally prioritizes operational traceability and human accountability over autonomous AI behavior.
