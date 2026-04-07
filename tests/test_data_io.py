import pytest

from src.data_io import parse_label_from_filename


def test_parse_label_from_filename_valid_patterns() -> None:
    assert parse_label_from_filename("d20_07_001.jpg") == 7
    assert parse_label_from_filename("D20-20-sample.png") == 20
    assert parse_label_from_filename("dice_face_2.jpeg") == 2


def test_parse_label_from_filename_invalid() -> None:
    with pytest.raises(ValueError):
        parse_label_from_filename("d20_25_001.jpg")

    with pytest.raises(ValueError):
        parse_label_from_filename("sem_numero.jpg")
