import json
from pathlib import Path
from typing import Dict, List, Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CLASSIFIED_TICKETS_FILE = PROJECT_ROOT / "data" / "outputs" / "classified_tickets.json"
HANDOFFS_FILE = PROJECT_ROOT / "data" / "outputs" / "engineering_handoffs.json"
METRICS_FILE = PROJECT_ROOT / "data" / "outputs" / "operations_metrics.json"

OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "governance_audit_summary.json"


def load_json(file_path: Path) -> Any:
    if not file_path.exists():
        return [] if file_path.name != "operations_metrics.json" else {}

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def identify_review_required_tickets(classified_tickets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    review_required = []

    for ticket in classified_tickets:
        reasons = []

        if ticket.get("environment") == "production":
            reasons.append("production environment")

        if ticket.get("predicted_severity") in ["high", "critical"]:
            reasons.append("high or critical severity")

        if ticket.get("predicted_category") in ["authentication", "permissions"]:
            reasons.append("authentication or access-related issue")

        if ticket.get("escalation_required"):
            reasons.append("engineering escalation recommended")

        if ticket.get("category_confidence", 1) < 0.6:
            reasons.append("low category confidence")

        if ticket.get("severity_confidence", 1) < 0.6:
            reasons.append("low severity confidence")

        if reasons:
            review_required.append({
                "ticket_id": ticket.get("ticket_id"),
                "customer": ticket.get("customer"),
                "predicted_category": ticket.get("predicted_category"),
                "predicted_severity": ticket.get("predicted_severity"),
                "review_required": True,
                "review_reasons": reasons
            })

    return review_required


def summarize_governance_controls(
    classified_tickets: List[Dict[str, Any]],
    handoffs: List[Dict[str, Any]],
    metrics: Dict[str, Any]
) -> Dict[str, Any]:
    review_required = identify_review_required_tickets(classified_tickets)

    return {
        "governance_summary": {
            "total_tickets_reviewed": len(classified_tickets),
            "tickets_requiring_human_review": len(review_required),
            "engineering_handoffs_generated": len(handoffs),
            "escalation_rate_percent": metrics.get("summary", {}).get("escalation_rate_percent"),
            "knowledge_base_match_rate_percent": metrics.get("summary", {}).get("knowledge_base_match_rate_percent")
        },
        "human_review_required": review_required,
        "controls_applied": [
            "deterministic classification",
            "confidence scoring",
            "log evidence analysis",
            "knowledge base retrieval",
            "engineering handoff generation",
            "human review policy",
            "audit artifact preservation"
        ],
        "restricted_autonomous_actions": [
            "customer ticket closure",
            "credential rotation",
            "access permission changes",
            "customer configuration changes",
            "production incident resolution",
            "customer-facing response delivery"
        ],
        "governance_method": "human_review_and_audit_summary"
    }


def generate_governance_audit_summary() -> Dict[str, Any]:
    classified_tickets = load_json(CLASSIFIED_TICKETS_FILE)
    handoffs = load_json(HANDOFFS_FILE)
    metrics = load_json(METRICS_FILE)

    summary = summarize_governance_controls(
        classified_tickets,
        handoffs,
        metrics
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    return summary


if __name__ == "__main__":
    result = generate_governance_audit_summary()

    print("Generated governance audit summary.")
    print(f"Output saved to: {OUTPUT_FILE}")
    print(json.dumps(result["governance_summary"], indent=2))