CATEGORY_RULES = {
    "authentication": [
        "401",
        "unauthorized",
        "api key",
        "token",
        "oauth",
        "invalid credentials",
        "expired"
    ],
    "webhook": [
        "webhook",
        "event delivery",
        "retry",
        "signature",
        "endpoint"
    ],
    "sdk": [
        "sdk",
        "client",
        "environment variable",
        "package",
        "configuration"
    ],
    "api_performance": [
        "timeout",
        "504",
        "latency",
        "slow",
        "gateway"
    ],
    "rate_limiting": [
        "429",
        "rate limit",
        "too many requests",
        "quota",
        "throttled"
    ],
    "integration_sync": [
        "sync",
        "field mapping",
        "records",
        "integration",
        "partial failure"
    ],
    "deployment": [
        "deployment",
        "ci/cd",
        "build",
        "rollback",
        "pipeline"
    ],
    "permissions": [
        "403",
        "forbidden",
        "permission",
        "access denied",
        "role"
    ]
}


SEVERITY_RULES = {
    "critical": [
        "checkout",
        "outage",
        "cannot complete",
        "production down",
        "revenue",
        "critical"
    ],
    "high": [
        "production",
        "blocked",
        "failing",
        "major",
        "business impact"
    ],
    "medium": [
        "delayed",
        "inconsistent",
        "partial",
        "rate limit",
        "sync"
    ],
    "low": [
        "staging",
        "testing",
        "configuration",
        "minor"
    ]
}


ESCALATION_TRIGGERS = [
    "production",
    "critical",
    "high",
    "blocked",
    "timeout",
    "504",
    "payment",
    "checkout",
    "data sync",
    "partial failure",
    "security",
    "outage"
]