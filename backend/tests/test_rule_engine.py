from app.services.rule_engine import Rule, apply_rules


def test_apply_rules_detects_pattern() -> None:
    rules = [
        Rule(
            id="1",
            name="No eval",
            pattern=r"\beval\(",
            message="eval should not be used",
            severity="critical",
        )
    ]

    findings = apply_rules("const x = eval(input)", rules)

    assert len(findings) == 1
    assert "No eval" in findings[0]
