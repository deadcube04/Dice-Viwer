"""Pytest bootstrap for local and CI environment setup."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent

# Load project environment variables from .env when present.
load_dotenv(ROOT_DIR / ".env")

pythonpath_value = os.getenv("PYTHONPATH", "")
for raw_path in pythonpath_value.split(os.pathsep):
    if not raw_path:
        continue

    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = (ROOT_DIR / candidate).resolve()

    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)
