from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel


class ProjectConfig(BaseModel):
    input_dir: Path = Path("input/d20")
    model_path: Path = Path("models/d20_model_v1.pkl")
    results_path: Path = Path("results.json")
    model_version: str = "d20_v1"
    train_ratio: float = 0.8
    random_seed: int = 42
