import pytest

from src.d20_rules import opposite_face


def test_opposite_face_basic_cases() -> None:
    assert opposite_face(1) == 20
    assert opposite_face(2) == 19
    assert opposite_face(10) == 11
    assert opposite_face(20) == 1


def test_opposite_face_invalid_range() -> None:
    with pytest.raises(ValueError):
        opposite_face(0)

    with pytest.raises(ValueError):
        opposite_face(21)
