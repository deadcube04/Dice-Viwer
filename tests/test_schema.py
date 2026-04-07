import pytest

from src.schema import InferenceResult


def test_inference_result_rule_validation() -> None:
    item = InferenceResult(
        imagem="d20_02_001.jpg",
        face_inferida=2,
        face_oposta=19,
        confianca=0.91,
        timestamp="2026-04-07T12:00:00+00:00",
        versao_modelo="d20_v1",
    )
    assert item.face_oposta == 19


def test_inference_result_invalid_opposite() -> None:
    with pytest.raises(ValueError):
        InferenceResult(
            imagem="d20_02_001.jpg",
            face_inferida=2,
            face_oposta=18,
            confianca=0.91,
            timestamp="2026-04-07T12:00:00+00:00",
            versao_modelo="d20_v1",
        )
