# Developer Support Ticket Schema

This document defines the structure of simulated developer support tickets used in the AI Developer Support Operations Lab.

---

# Purpose

The ticket schema creates consistent operational data for:

- AI-assisted ticket classification
- log analysis
- troubleshooting workflows
- knowledge base retrieval
- escalation decisions
- engineering handoff generation
- operational analytics

---

# Core Fields

| Field | Purpose |
|---|---|
| `ticket_id` | Unique ticket identifier |
| `customer` | Simulated customer or organization |
| `environment` | Production, staging, development, or sandbox |
| `severity` | Business/technical severity level |
| `category` | Issue category |
| `subject` | Short summary of the issue |
| `description` | Detailed user-reported issue |
| `reported_by` | Role of the person reporting the issue |
| `affected_service` | Platform service involved |
| `error_message` | Primary error observed |
| `timestamp` | Time the issue was reported |
| `sample_log_ref` | Related log file for troubleshooting |
| `expected_behavior` | What the user expected to happen |
| `actual_behavior` | What actually happened |
| `business_impact` | Operational impact of the issue |
| `requires_escalation` | Whether the issue should be escalated |

---

# Severity Levels

## Low

Minor issue with limited impact. Usually affects testing, staging, or configuration.

## Medium

Operational issue causing delay or partial disruption, but not a full outage.

## High

Production issue affecting important workflows or business operations.

## Critical

Production issue causing major customer impact, revenue impact, outage, or security concern.

---

# Example Categories

- authentication
- webhook
- sdk
- api_performance
- rate_limiting
- integration_sync
- deployment
- permissions
- data_pipeline

---

# Design Notes

The schema is intentionally structured so future phases can evaluate AI-assisted support decisions against deterministic fields.

The goal is to avoid vague support data and instead create evidence-driven workflows.