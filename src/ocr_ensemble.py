from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

import cv2
import numpy as np
import pytesseract

try:
    import easyocr
except Exception:  # pragma: no cover
    easyocr = None

_FACE_PATTERN = re.compile(r"(?<!\d)([1-9]|1\d|20)(?!\d)")


def _extract_face(text: str) -> int | None:
    match = _FACE_PATTERN.search(text)
    if not match:
        return None
    value = int(match.group(1))
    return value if 1 <= value <= 20 else None


def read_number_with_tesseract(image: np.ndarray) -> tuple[int | None, float]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    config = "--psm 8 -c tessedit_char_whitelist=0123456789"
    data: dict[str, Any] = pytesseract.image_to_data(
        binary,
        output_type=pytesseract.Output.DICT,
        config=config,
    )

    texts = data.get("text", [])
    confs = data.get("conf", [])

    best_face = None
    best_conf = -1.0
    for text, conf_raw in zip(texts, confs):
        face = _extract_face(str(text).strip())
        if face is None:
            continue
        try:
            conf = float(conf_raw)
        except Exception:
            conf = 0.0
        conf = max(0.0, min(100.0, conf)) / 100.0
        if conf > best_conf:
            best_conf = conf
            best_face = face

    return best_face, max(0.0, best_conf)


@lru_cache(maxsize=1)
def _easyocr_reader() -> Any:
    if easyocr is None:
        return None
    return easyocr.Reader(["en"], gpu=False)


def read_number_with_easyocr(image: np.ndarray) -> tuple[int | None, float]:
    reader = _easyocr_reader()
    if reader is None:
        return None, 0.0

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if image.ndim == 3 else image
    results = reader.readtext(rgb, detail=1)

    best_face = None
    best_conf = -1.0
    for _, text, conf in results:
        face = _extract_face(str(text).strip())
        if face is None:
            continue
        conf = float(conf)
        if conf > best_conf:
            best_conf = conf
            best_face = face

    return best_face, max(0.0, min(1.0, best_conf))


def read_number_ensemble(image: np.ndarray) -> tuple[int | None, float, str]:
    t_face, t_conf = read_number_with_tesseract(image)
    e_face, e_conf = read_number_with_easyocr(image)

    candidates: list[tuple[int, float, str]] = []
    if t_face is not None:
        candidates.append((t_face, t_conf, "pytesseract"))
    if e_face is not None:
        candidates.append((e_face, e_conf, "easyocr"))

    if not candidates:
        return None, 0.0, "none"

    best = max(candidates, key=lambda item: item[1])
    return best
