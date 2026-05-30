import json
from pathlib import Path
from typing import Dict, List, Any
from collections import Counter


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLASSIFIED_TICKETS_FILE = PROJECT_ROOT / "data" / "outputs" / "classified_tickets.json"
TROUBLESHOOTING_FILE = PROJECT_ROOT / "data" / "outputs" / "troubleshooting_findings.json"
RETRIEVAL_FILE = PROJECT_ROOT / "data" / "outputs" / "retrieval_results.json"
HANDOFFS_FILE = PROJECT_ROOT / "data" / "outputs" / "engineering_handoffs.json"

OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "operations_metrics.json"


def load_json(file_path: Path) -> List[Dict[str, Any]]:
    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def percentage(part: int, whole: int) -> float:
    if whole == 0:
        return 0.0

    return round((part / whole) * 100, 2)


def count_by_field(records: List[Dict[str, Any]], field: str) -> Dict[str, int]:
    values = [record.get(field, "unknown") for record in records]
    return dict(Counter(values))


def count_log_levels(troubleshooting_records: List[Dict[str, Any]]) -> Dict[str, int]:
    total_levels = Counter()

    for record in troubleshooting_records:
        log_levels = record.get("evidence_summary", {}).get("log_levels", {})
        total_levels.update(log_levels)

    return dict(total_levels)


def count_status_codes(troubleshooting_records: List[Dict[str, Any]]) -> Dict[str, int]:
    status_codes = Counter()

    for record in troubleshooting_records:
        codes = record.get("evidence_summary", {}).get("status_codes", [])
        status_codes.update(codes)

    return dict(status_codes)


def count_root_causes(troubleshooting_records: List[Dict[str, Any]]) -> Dict[str, int]:
    root_causes = Counter()

    for record in troubleshooting_records:
        findings = record.get("evidence_summary", {}).get("root_cause_findings", [])

        for finding in findings:
            cause = finding.get("root_cause", "unknown")
            root_causes.update([cause])

    return dict(root_causes)


def calculate_avg_category_confidence(classified_tickets: List[Dict[str, Any]]) -> float:
    confidence_values = [
        ticket.get("category_confidence", 0)
        for ticket in classified_tickets
    ]

    if not confidence_values:
        return 0.0

    return round(sum(confidence_values) / len(confidence_values), 2)


def calculate_avg_severity_confidence(classified_tickets: List[Dict[str, Any]]) -> float:
    confidence_values = [
        ticket.get("severity_confidence", 0)
        for ticket in classified_tickets
    ]

    if not confidence_values:
        return 0.0

    return round(sum(confidence_values) / len(confidence_values), 2)


def generate_metrics() -> Dict[str, Any]:
    classified_tickets = load_json(CLASSIFIED_TICKETS_FILE)
    troubleshooting_records = load_json(TROUBLESHOOTING_FILE)
    retrieval_records = load_json(RETRIEVAL_FILE)
    handoffs = load_json(HANDOFFS_FILE)

    total_tickets = len(classified_tickets)
    escalated_tickets = len([ticket for ticket in classified_tickets if ticket.get("escalation_required")])
    kb_matches = len([record for record in retrieval_records if record.get("retrieval_status") == "matched"])

    metrics = {
        "summary": {
            "total_tickets_processed": total_tickets,
            "tickets_escalated": escalated_tickets,
            "tickets_not_escalated": total_tickets - escalated_tickets,
            "engineering_handoffs_generated": len(handoffs),
            "escalation_rate_percent": percentage(escalated_tickets, total_tickets),
            "knowledge_base_match_rate_percent": percentage(kb_matches, total_tickets),
            "average_category_confidence": calculate_avg_category_confidence(classified_tickets),
            "average_severity_confidence": calculate_avg_severity_confidence(classified_tickets)
        },
        "ticket_distribution": {
            "by_category": count_by_field(classified_tickets, "predicted_category"),
            "by_severity": count_by_field(classified_tickets, "predicted_severity"),
            "by_environment": count_by_field(classified_tickets, "environment")
        },
        "operational_evidence": {
            "log_levels": count_log_levels(troubleshooting_records),
            "status_codes": count_status_codes(troubleshooting_records),
            "root_causes": count_root_causes(troubleshooting_records)
        },
        "handoff_distribution": {
            "by_priority": count_by_field(handoffs, "priority"),
            "by_category": count_by_field(handoffs, "predicted_category"),
            "by_severity": count_by_field(handoffs, "predicted_severity")
        },
        "analytics_method": "deterministic_pipeline_metrics"
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    return metrics


if __name__ == "__main__":
    results = generate_metrics()

    print("Generated operational metrics.")
    print(f"Output saved to: {OUTPUT_FILE}")
    print(json.dumps(results["summary"], indent=2))