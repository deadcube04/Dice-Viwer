from __future__ import annotations

from typing import Any

import cv2
import numpy as np


def _to_gray(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def extract_die_roi(image: np.ndarray, pad: int = 8) -> tuple[np.ndarray, dict[str, Any]]:
    gray = _to_gray(image)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        h, w = gray.shape[:2]
        return image.copy(), {"bbox": [0, 0, w, h], "contour_found": False}

    contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(contour)

    x0 = max(0, x - pad)
    y0 = max(0, y - pad)
    x1 = min(image.shape[1], x + w + pad)
    y1 = min(image.shape[0], y + h + pad)

    roi = image[y0:y1, x0:x1]
    return roi, {"bbox": [int(x0), int(y0), int(x1 - x0), int(y1 - y0)], "contour_found": True}


def extract_number_roi(die_roi: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
    gray = _to_gray(die_roi)
    denoised = cv2.medianBlur(gray, 3)
    binary = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        31,
        5,
    )

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        h, w = binary.shape[:2]
        cx0, cy0 = int(w * 0.2), int(h * 0.2)
        cx1, cy1 = int(w * 0.8), int(h * 0.8)
        fallback = binary[cy0:cy1, cx0:cx1]
        return fallback, {"number_bbox": [cx0, cy0, cx1 - cx0, cy1 - cy0], "number_found": False}

    h, w = binary.shape[:2]
    center = np.array([w / 2.0, h / 2.0])

    candidates: list[tuple[float, tuple[int, int, int, int]]] = []
    min_area = max(20, int((w * h) * 0.002))
    max_area = int((w * h) * 0.65)

    for contour in contours:
        x, y, cw, ch = cv2.boundingRect(contour)
        area = cw * ch
        if area < min_area or area > max_area:
            continue

        centroid = np.array([x + cw / 2.0, y + ch / 2.0])
        distance = float(np.linalg.norm(centroid - center))
        score = distance + (1.0 / max(area, 1)) * 1000.0
        candidates.append((score, (x, y, cw, ch)))

    if not candidates:
        x, y, cw, ch = 0, 0, w, h
    else:
        _, (x, y, cw, ch) = min(candidates, key=lambda item: item[0])

    number_roi = binary[y : y + ch, x : x + cw]
    return number_roi, {"number_bbox": [int(x), int(y), int(cw), int(ch)], "number_found": bool(candidates)}


def prepare_feature_vector(number_roi: np.ndarray, size: tuple[int, int] = (32, 32)) -> np.ndarray:
    resized = cv2.resize(number_roi, size, interpolation=cv2.INTER_AREA)
    normalized = resized.astype(np.float32) / 255.0
    return normalized.flatten()


def image_to_feature(image: np.ndarray) -> tuple[np.ndarray, dict[str, Any], np.ndarray]:
    die_roi, die_meta = extract_die_roi(image)
    number_roi, number_meta = extract_number_roi(die_roi)
    feature = prepare_feature_vector(number_roi)
    meta = {**die_meta, **number_meta}
    return feature, meta, number_roi
