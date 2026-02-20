import re
from dataclasses import dataclass


@dataclass
class Rule:
    id: str
    name: str
    pattern: str
    message: str
    severity: str = "warning"
    enabled: bool = True


def apply_rules(code: str, rules: list[Rule]) -> list[str]:
    findings: list[str] = []
    for rule in rules:
        if not rule.enabled:
            continue
        if re.search(rule.pattern, code, re.MULTILINE):
            findings.append(f"[{rule.severity}] {rule.name}: {rule.message}")
    return findings
