from hidden_commitment.residuals import Position, position_indices


def test_named_position_indices() -> None:
    kwargs = {"prompt_length": 10, "response_length": 8, "decision_token_indices": [3, 4]}
    assert position_indices(Position.PRE_RESPONSE_LAST, **kwargs) == (9,)
    assert position_indices(Position.RESPONSE_FIRST, **kwargs) == (10,)
    assert position_indices(Position.MEAN_DECISION, **kwargs) == (13, 14)
    assert position_indices(Position.PRE_DECISION_LAST, **kwargs) == (12,)
