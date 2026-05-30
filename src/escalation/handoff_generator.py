import json
from pathlib import Path
from typing import Dict, List, Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLASSIFIED_TICKETS_FILE = PROJECT_ROOT / "data" / "outputs" / "classified_tickets.json"
TROUBLESHOOTING_FILE = PROJECT_ROOT / "data" / "outputs" / "troubleshooting_findings.json"
RETRIEVAL_FILE = PROJECT_ROOT / "data" / "outputs" / "retrieval_results.json"

OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "engineering_handoffs.json"


def load_json(file_path: Path) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_lookup(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {record["ticket_id"]: record for record in records}


def determine_priority(severity: str, root_causes: List[str]) -> str:
    if severity == "critical":
        return "P1 - Immediate engineering review"

    if severity == "high":
        return "P2 - Engineering review required"

    if any("timeout" in cause.lower() for cause in root_causes):
        return "P2 - Performance investigation required"

    return "P3 - Review during normal support workflow"


def summarize_evidence(troubleshooting_result: Dict[str, Any]) -> Dict[str, Any]:
    evidence = troubleshooting_result.get("evidence_summary", {})

    return {
        "services": evidence.get("services", []),
        "status_codes": evidence.get("status_codes", []),
        "log_levels": evidence.get("log_levels", {}),
        "max_latency_ms": evidence.get("max_latency_ms"),
        "root_cause_findings": evidence.get("root_cause_findings", [])
    }


def create_engineering_handoff(
    classified_ticket: Dict[str, Any],
    troubleshooting_result: Dict[str, Any],
    retrieval_result: Dict[str, Any]
) -> Dict[str, Any]:
    root_causes = retrieval_result.get("root_causes", [])
    recommended_actions = retrieval_result.get("recommended_actions_from_logs", [])

    severity = classified_ticket.get("predicted_severity", "unknown")

    return {
        "handoff_id": f"ENG-{classified_ticket.get('ticket_id')}",
        "ticket_id": classified_ticket.get("ticket_id"),
        "customer": classified_ticket.get("customer"),
        "subject": classified_ticket.get("subject"),
        "environment": classified_ticket.get("environment"),
        "predicted_category": classified_ticket.get("predicted_category"),
        "predicted_severity": severity,
        "priority": determine_priority(severity, root_causes),
        "escalation_required": classified_ticket.get("escalation_required"),
        "business_context": {
            "original_severity": classified_ticket.get("original_severity"),
            "original_requires_escalation": classified_ticket.get("original_requires_escalation"),
            "recommended_next_action": classified_ticket.get("recommended_next_action")
        },
        "operational_evidence": summarize_evidence(troubleshooting_result),
        "knowledge_base_reference": {
            "article_title": retrieval_result.get("kb_article_title"),
            "article_file": retrieval_result.get("kb_article_file"),
            "retrieval_status": retrieval_result.get("retrieval_status")
        },
        "root_causes": root_causes,
        "recommended_engineering_actions": recommended_actions,
        "handoff_summary": generate_handoff_summary(
            classified_ticket,
            root_causes,
            recommended_actions
        ),
        "handoff_status": "ready_for_engineering_review",
        "handoff_method": "classification_log_analysis_kb_retrieval"
    }


def generate_handoff_summary(
    classified_ticket: Dict[str, Any],
    root_causes: List[str],
    recommended_actions: List[str]
) -> str:
    ticket_id = classified_ticket.get("ticket_id")
    category = classified_ticket.get("predicted_category")
    severity = classified_ticket.get("predicted_severity")
    customer = classified_ticket.get("customer")

    root_cause_text = "; ".join(root_causes) if root_causes else "No root cause detected"
    action_text = "; ".join(recommended_actions) if recommended_actions else "Further investigation required"

    return (
        f"{ticket_id} for {customer} was classified as {category} with {severity} severity. "
        f"Detected root cause signals: {root_cause_text}. "
        f"Recommended engineering actions: {action_text}."
    )


def generate_handoffs() -> List[Dict[str, Any]]:
    classified_tickets = load_json(CLASSIFIED_TICKETS_FILE)
    troubleshooting_findings = load_json(TROUBLESHOOTING_FILE)
    retrieval_results = load_json(RETRIEVAL_FILE)

    troubleshooting_lookup = build_lookup(troubleshooting_findings)
    retrieval_lookup = build_lookup(retrieval_results)

    handoffs = []

    for ticket in classified_tickets:
        if not ticket.get("escalation_required"):
            continue

        ticket_id = ticket.get("ticket_id")
        troubleshooting_result = troubleshooting_lookup.get(ticket_id, {})
        retrieval_result = retrieval_lookup.get(ticket_id, {})

        handoff = create_engineering_handoff(
            ticket,
            troubleshooting_result,
            retrieval_result
        )

        handoffs.append(handoff)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(handoffs, file, indent=2)

    return handoffs


if __name__ == "__main__":
    results = generate_handoffs()

    print(f"Generated {len(results)} engineering handoff records.")
    print(f"Output saved to: {OUTPUT_FILE}")