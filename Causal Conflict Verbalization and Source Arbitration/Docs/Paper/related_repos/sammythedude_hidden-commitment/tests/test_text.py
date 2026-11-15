from __future__ import annotations

import re

from hidden_commitment.text import DecisionLabel, label_response, locate_alias_span, swap_documents


class WordTokenizer:
    def __call__(self, text: str, **_kwargs):
        offsets = [(match.start(), match.end()) for match in re.finditer(r"\S+", text)]
        return {"offset_mapping": offsets}


def test_label_response_requires_unique_source() -> None:
    assert label_response("The year was 1922.", ["1922"], ["1985"]) == DecisionLabel.DOC1
    assert label_response("Sources say 1922 and 1985.", ["1922"], ["1985"]) == DecisionLabel.BOTH
    assert label_response("No date is given.", ["1922"], ["1985"]) == DecisionLabel.NEITHER


def test_alias_matching_does_not_match_inside_a_word() -> None:
    assert label_response("The code is 312.", ["12"], ["8"]) == DecisionLabel.NEITHER


def test_locate_alias_span_maps_tokens() -> None:
    span = locate_alias_span("It was New York City in 1999.", ["New York City"], WordTokenizer())
    assert span is not None
    assert span.text == "New York City"
    assert span.token_indices == (2, 3, 4)


def test_swap_documents() -> None:
    context = "Document: first\n\nDocument: second"
    assert swap_documents(context) == "Document: second\n\nDocument: first"
