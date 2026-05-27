import json
from pathlib import Path
from typing import Dict, List, Any

from src.classification.rules import (
    CATEGORY_RULES,
    SEVERITY_RULES,
    ESCALATION_TRIGGERS,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TICKET_FILE = PROJECT_ROOT / "data" / "tickets" / "developer_support_tickets.json"
OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "classified_tickets.json"


def load_tickets(file_path: Path = TICKET_FILE) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def combine_ticket_text(ticket: Dict[str, Any]) -> str:
    fields = [
        ticket.get("subject", ""),
        ticket.get("description", ""),
        ticket.get("error_message", ""),
        ticket.get("business_impact", ""),
        ticket.get("affected_service", ""),
        ticket.get("environment", ""),
    ]

    return " ".join(fields).lower()


def score_rules(text: str, rules: Dict[str, List[str]]) -> Dict[str, int]:
    scores = {}

    for label, keywords in rules.items():
        score = sum(1 for keyword in keywords if keyword.lower() in text)
        scores[label] = score

    return scores


def select_best_label(scores: Dict[str, int], fallback: str = "unknown") -> str:
    best_label = max(scores, key=scores.get)

    if scores[best_label] == 0:
        return fallback

    return best_label


def calculate_confidence(scores: Dict[str, int]) -> float:
    total_matches = sum(scores.values())

    if total_matches == 0:
        return 0.0

    highest_score = max(scores.values())
    confidence = highest_score / total_matches

    return round(confidence, 2)


def determine_escalation(ticket: Dict[str, Any], text: str, predicted_severity: str) -> bool:
    if predicted_severity in ["critical", "high"]:
        return True

    if ticket.get("environment", "").lower() == "production":
        for trigger in ESCALATION_TRIGGERS:
            if trigger in text:
                return True

    return False


def recommend_next_action(category: str, severity: str, escalation_required: bool) -> str:
    if escalation_required:
        return "Create engineering handoff with logs, reproduction steps, and business impact."

    if category == "authentication":
        return "Validate API key, token expiration, scopes, and authentication configuration."

    if category == "webhook":
        return "Check webhook endpoint availability, retry history, signature validation, and delivery logs."

    if category == "sdk":
        return "Verify SDK configuration, required environment variables, package version, and initialization settings."

    if category == "api_performance":
        return "Review API gateway logs, timeout patterns, latency metrics, and affected endpoints."

    if category == "rate_limiting":
        return "Review request volume, quota limits, burst behavior, and retry/backoff strategy."

    if category == "integration_sync":
        return "Validate field mappings, failed records, sync job history, and external integration configuration."

    return "Review ticket details and gather additional operational evidence."


def classify_ticket(ticket: Dict[str, Any]) -> Dict[str, Any]:
    text = combine_ticket_text(ticket)

    category_scores = score_rules(text, CATEGORY_RULES)
    severity_scores = score_rules(text, SEVERITY_RULES)

    predicted_category = select_best_label(category_scores)
    predicted_severity = select_best_label(severity_scores, fallback=ticket.get("severity", "unknown"))

    category_confidence = calculate_confidence(category_scores)
    severity_confidence = calculate_confidence(severity_scores)

    escalation_required = determine_escalation(ticket, text, predicted_severity)

    return {
        "ticket_id": ticket.get("ticket_id"),
        "subject": ticket.get("subject"),
        "customer": ticket.get("customer"),
        "environment": ticket.get("environment"),
        "predicted_category": predicted_category,
        "original_category": ticket.get("category"),
        "predicted_severity": predicted_severity,
        "original_severity": ticket.get("severity"),
        "category_confidence": category_confidence,
        "severity_confidence": severity_confidence,
        "escalation_required": escalation_required,
        "original_requires_escalation": ticket.get("requires_escalation"),
        "recommended_next_action": recommend_next_action(
            predicted_category,
            predicted_severity,
            escalation_required
        ),
        "classification_method": "deterministic_keyword_rules"
    }


def classify_all_tickets() -> List[Dict[str, Any]]:
    tickets = load_tickets()
    classified_tickets = [classify_ticket(ticket) for ticket in tickets]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(classified_tickets, file, indent=2)

    return classified_tickets


if __name__ == "__main__":
    results = classify_all_tickets()

    print(f"Classified {len(results)} tickets.")
    print(f"Output saved to: {OUTPUT_FILE}")