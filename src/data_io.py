from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

_VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
_D20_PATTERN = re.compile(r"d20[_\- ]*(?P<label>\d{1,2})(?=$|[_\- .])", re.IGNORECASE)
_FALLBACK_PATTERNS = (
    re.compile(r"(?:face|label)[_\- ]*(?P<label>[1-9]|1\d|20)(?=$|[_\- .])", re.IGNORECASE),
    re.compile(r"(?<!\d)(?P<label>[1-9]|1\d|20)(?!\d)"),
)


def list_image_paths(input_dir: str | Path) -> list[Path]:
    root = Path(input_dir)
    if not root.exists():
        return []

    image_paths = [
        path for path in root.glob("**/*") if path.is_file() and path.suffix.lower() in _VALID_EXTENSIONS
    ]
    return sorted(image_paths)


def parse_label_from_filename(file_name: str, patterns: Iterable[re.Pattern[str]] | None = None) -> int:
    stem = Path(file_name).stem

    d20_match = _D20_PATTERN.search(stem)
    if d20_match:
        label = int(d20_match.group("label"))
        if 1 <= label <= 20:
            return label
        raise ValueError(
            "Label apos d20 fora do intervalo 1..20. "
            "Use um padrao como d20_07_001.jpg"
        )

    checks = tuple(patterns) if patterns is not None else _FALLBACK_PATTERNS
    for pattern in checks:
        match = pattern.search(stem)
        if match:
            label = int(match.group("label"))
            if 1 <= label <= 20:
                return label
    raise ValueError(
        "Nao foi possivel extrair label 1..20 do nome do arquivo. "
        "Use um padrao como d20_07_001.jpg"
    )


def load_images_and_labels(input_dir: str | Path) -> tuple[list[object], list[int], list[Path]]:
    import cv2

    images: list[object] = []
    labels: list[int] = []
    paths: list[Path] = []

    for image_path in list_image_paths(input_dir):
        image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        if image is None:
            continue
        label = parse_label_from_filename(image_path.name)
        images.append(image)
        labels.append(label)
        paths.append(image_path)

    return images, labels, paths
