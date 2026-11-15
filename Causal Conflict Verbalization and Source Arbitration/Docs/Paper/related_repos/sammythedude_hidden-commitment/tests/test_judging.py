from hidden_commitment.judging import parse_judgment


def test_parse_judgment_exposes_broad_and_strict_labels() -> None:
    judgment = parse_judgment(
        {
            "valid_conflict": True,
            "chosen_document": "neither",
            "surfacing_label": "conflict_aware_unresolved",
            "low_quality_or_truncated": False,
            "rationale": "The answer names both claims and abstains.",
        }
    )
    assert judgment.broad_surfacing
    assert judgment.strict_unresolved_surfacing
