import json
from pathlib import Path
from typing import Dict, List, Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CLASSIFIED_TICKETS_FILE = PROJECT_ROOT / "data" / "outputs" / "classified_tickets.json"
TROUBLESHOOTING_FILE = PROJECT_ROOT / "data" / "outputs" / "troubleshooting_findings.json"
KB_DIR = PROJECT_ROOT / "data" / "kb"
OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "retrieval_results.json"


KB_INDEX = {
    "authentication": {
        "file": "api-authentication.md",
        "title": "API Authentication Troubleshooting"
    },
    "webhook": {
        "file": "webhook-troubleshooting.md",
        "title": "Webhook Troubleshooting"
    },
    "sdk": {
        "file": "sdk-configuration.md",
        "title": "SDK Configuration Troubleshooting"
    },
    "api_performance": {
        "file": "api-timeouts.md",
        "title": "API Timeout Troubleshooting"
    },
    "rate_limiting": {
        "file": "rate-limiting.md",
        "title": "API Rate Limiting Troubleshooting"
    },
    "integration_sync": {
        "file": "integration-sync.md",
        "title": "Integration Sync Troubleshooting"
    }
}


def load_json(file_path: Path) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def read_kb_article(file_name: str) -> str:
    article_path = KB_DIR / file_name

    if not article_path.exists():
        return ""

    with open(article_path, "r", encoding="utf-8") as file:
        return file.read()


def build_troubleshooting_lookup(findings: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {finding["ticket_id"]: finding for finding in findings}


def extract_root_causes(troubleshooting_result: Dict[str, Any]) -> List[str]:
    root_causes = []

    findings = (
        troubleshooting_result
        .get("evidence_summary", {})
        .get("root_cause_findings", [])
    )

    for finding in findings:
        root_causes.append(finding.get("root_cause", ""))

    return [cause for cause in root_causes if cause]


def extract_recommended_actions(troubleshooting_result: Dict[str, Any]) -> List[str]:
    actions = []

    findings = (
        troubleshooting_result
        .get("evidence_summary", {})
        .get("root_cause_findings", [])
    )

    for finding in findings:
        actions.append(finding.get("recommended_action", ""))

    return [action for action in actions if action]


def retrieve_article_for_ticket(
    classified_ticket: Dict[str, Any],
    troubleshooting_lookup: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    ticket_id = classified_ticket.get("ticket_id")
    category = classified_ticket.get("predicted_category")
    kb_match = KB_INDEX.get(category)

    troubleshooting_result = troubleshooting_lookup.get(ticket_id, {})

    if not kb_match:
        return {
            "ticket_id": ticket_id,
            "subject": classified_ticket.get("subject"),
            "predicted_category": category,
            "retrieval_status": "no_match",
            "kb_article_title": None,
            "kb_article_file": None,
            "root_causes": extract_root_causes(troubleshooting_result),
            "recommended_actions_from_logs": extract_recommended_actions(troubleshooting_result),
            "retrieval_method": "category_to_kb_mapping"
        }

    article_text = read_kb_article(kb_match["file"])

    return {
        "ticket_id": ticket_id,
        "subject": classified_ticket.get("subject"),
        "customer": classified_ticket.get("customer"),
        "predicted_category": category,
        "predicted_severity": classified_ticket.get("predicted_severity"),
        "escalation_required": classified_ticket.get("escalation_required"),
        "kb_article_title": kb_match["title"],
        "kb_article_file": kb_match["file"],
        "kb_excerpt": article_text[:700],
        "root_causes": extract_root_causes(troubleshooting_result),
        "recommended_actions_from_logs": extract_recommended_actions(troubleshooting_result),
        "retrieval_status": "matched",
        "retrieval_method": "category_to_kb_mapping"
    }


def retrieve_for_all_tickets() -> List[Dict[str, Any]]:
    classified_tickets = load_json(CLASSIFIED_TICKETS_FILE)
    troubleshooting_findings = load_json(TROUBLESHOOTING_FILE)

    troubleshooting_lookup = build_troubleshooting_lookup(troubleshooting_findings)

    retrieval_results = [
        retrieve_article_for_ticket(ticket, troubleshooting_lookup)
        for ticket in classified_tickets
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(retrieval_results, file, indent=2)

    return retrieval_results


if __name__ == "__main__":
    results = retrieve_for_all_tickets()

    print(f"Retrieved knowledge base articles for {len(results)} tickets.")
    print(f"Output saved to: {OUTPUT_FILE}")