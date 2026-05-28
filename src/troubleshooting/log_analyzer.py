import json
import re
from pathlib import Path
from typing import Dict, List, Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TICKET_FILE = PROJECT_ROOT / "data" / "tickets" / "developer_support_tickets.json"
LOG_DIR = PROJECT_ROOT / "data" / "logs"
OUTPUT_DIR = PROJECT_ROOT / "data" / "outputs"
OUTPUT_FILE = OUTPUT_DIR / "troubleshooting_findings.json"


ROOT_CAUSE_PATTERNS = {
    "expired_api_token": {
        "root_cause": "Expired API token",
        "recommended_action": "Rotate the API token and verify token expiration policy.",
        "severity_signal": "high"
    },
    "token_expired": {
        "root_cause": "Expired authentication token",
        "recommended_action": "Generate a new token and validate authentication configuration.",
        "severity_signal": "high"
    },
    "retry exhaustion": {
        "root_cause": "Webhook delivery failed after retry exhaustion",
        "recommended_action": "Verify receiving endpoint health and review webhook retry configuration.",
        "severity_signal": "medium"
    },
    "missing_environment_variable": {
        "root_cause": "Missing SDK environment variable",
        "recommended_action": "Set the required environment variable and rerun SDK initialization.",
        "severity_signal": "low"
    },
    "required_config_missing": {
        "root_cause": "Missing required SDK configuration",
        "recommended_action": "Review SDK setup documentation and validate local configuration.",
        "severity_signal": "low"
    },
    "Gateway timeout": {
        "root_cause": "API gateway timeout",
        "recommended_action": "Review upstream service health, latency, and timeout thresholds.",
        "severity_signal": "critical"
    },
    "Upstream payment processor timeout": {
        "root_cause": "Upstream payment processor timeout",
        "recommended_action": "Escalate to engineering with payment API logs and affected endpoint data.",
        "severity_signal": "critical"
    },
    "Rate limit exceeded": {
        "root_cause": "API rate limit exceeded",
        "recommended_action": "Review request volume, quota limits, and retry/backoff strategy.",
        "severity_signal": "medium"
    },
    "Too many requests": {
        "root_cause": "Too many API requests",
        "recommended_action": "Implement exponential backoff and review API usage limits.",
        "severity_signal": "medium"
    },
    "invalid_field_mapping": {
        "root_cause": "Invalid integration field mapping",
        "recommended_action": "Correct the field mapping and rerun the sync job.",
        "severity_signal": "high"
    },
    "Field mapping validation failed": {
        "root_cause": "CRM field mapping validation failure",
        "recommended_action": "Validate CRM schema mapping for the failed field.",
        "severity_signal": "high"
    }
}


def load_tickets(file_path: Path = TICKET_FILE) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def read_log_file(log_file_name: str) -> List[str]:
    log_path = LOG_DIR / log_file_name

    if not log_path.exists():
        return []

    with open(log_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


def extract_status_codes(log_lines: List[str]) -> List[str]:
    status_codes = set()

    for line in log_lines:
        matches = re.findall(r"status=([0-9]{3}|failed)", line)
        status_codes.update(matches)

    return sorted(status_codes)


def extract_log_levels(log_lines: List[str]) -> Dict[str, int]:
    levels = {}

    for line in log_lines:
        match = re.search(r"level=([A-Z]+)", line)

        if match:
            level = match.group(1)
            levels[level] = levels.get(level, 0) + 1

    return levels


def extract_services(log_lines: List[str]) -> List[str]:
    services = set()

    for line in log_lines:
        match = re.search(r"service=([a-zA-Z0-9-]+)", line)

        if match:
            services.add(match.group(1))

    return sorted(services)


def extract_latency_values(log_lines: List[str]) -> List[int]:
    latency_values = []

    for line in log_lines:
        match = re.search(r"latency_ms=([0-9]+)", line)

        if match:
            latency_values.append(int(match.group(1)))

    return latency_values


def detect_root_causes(log_lines: List[str]) -> List[Dict[str, str]]:
    findings = []
    combined_logs = "\n".join(log_lines)

    for pattern, details in ROOT_CAUSE_PATTERNS.items():
        if pattern.lower() in combined_logs.lower():
            findings.append({
                "pattern": pattern,
                "root_cause": details["root_cause"],
                "recommended_action": details["recommended_action"],
                "severity_signal": details["severity_signal"]
            })

    return findings


def summarize_log_evidence(log_lines: List[str]) -> Dict[str, Any]:
    latency_values = extract_latency_values(log_lines)

    return {
        "line_count": len(log_lines),
        "services": extract_services(log_lines),
        "status_codes": extract_status_codes(log_lines),
        "log_levels": extract_log_levels(log_lines),
        "max_latency_ms": max(latency_values) if latency_values else None,
        "root_cause_findings": detect_root_causes(log_lines)
    }


def analyze_ticket_logs(ticket: Dict[str, Any]) -> Dict[str, Any]:
    log_file = ticket.get("sample_log_ref")
    log_lines = read_log_file(log_file)

    evidence_summary = summarize_log_evidence(log_lines)

    return {
        "ticket_id": ticket.get("ticket_id"),
        "customer": ticket.get("customer"),
        "subject": ticket.get("subject"),
        "affected_service": ticket.get("affected_service"),
        "log_file": log_file,
        "log_found": len(log_lines) > 0,
        "evidence_summary": evidence_summary,
        "analysis_method": "deterministic_log_pattern_analysis"
    }


def analyze_all_ticket_logs() -> List[Dict[str, Any]]:
    tickets = load_tickets()
    findings = [analyze_ticket_logs(ticket) for ticket in tickets]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(findings, file, indent=2)

    return findings


if __name__ == "__main__":
    results = analyze_all_ticket_logs()

    print(f"Analyzed logs for {len(results)} tickets.")
    print(f"Output saved to: {OUTPUT_FILE}")