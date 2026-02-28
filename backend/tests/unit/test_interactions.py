"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_excludes_interaction_with_different_learner_id() -> None:
    interactions = [_make_log(1, 2, 1)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].item_id == 1
    assert result[0].learner_id == 2


def test_filter_returns_empty_when_no_item_ids_match() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2), _make_log(3, 3, 3)]
    result = _filter_by_item_id(interactions, 99)
    assert result == []


def test_filter_returns_all_interactions_with_same_item_id() -> None:
    interactions = [
        _make_log(1, 10, 2),
        _make_log(2, 11, 1),
        _make_log(3, 12, 2),
        _make_log(4, 13, 2),
    ]
    result = _filter_by_item_id(interactions, 2)
    assert [interaction.id for interaction in result] == [1, 3, 4]


def test_filter_preserves_order_of_matching_interactions() -> None:
    interactions = [
        _make_log(10, 1, 5),
        _make_log(11, 2, 7),
        _make_log(12, 3, 5),
        _make_log(13, 4, 5),
    ]
    result = _filter_by_item_id(interactions, 5)
    assert [interaction.id for interaction in result] == [10, 12, 13]


def test_filter_matches_item_id_zero_boundary_value() -> None:
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_matches_negative_item_id_boundary_value() -> None:
    interactions = [_make_log(1, 1, -1), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, -1)
    assert len(result) == 1
    assert result[0].id == 1
