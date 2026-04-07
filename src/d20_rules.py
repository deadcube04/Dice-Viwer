from __future__ import annotations


def validate_face(face: int) -> int:
    if not isinstance(face, int):
        raise TypeError("A face do dado deve ser um inteiro.")
    if face < 1 or face > 20:
        raise ValueError("A face do D20 deve estar entre 1 e 20.")
    return face


def opposite_face(face: int) -> int:
    """Return opposite D20 face using the rule opposite = 21 - face."""
    valid_face = validate_face(face)
    return 21 - valid_face
