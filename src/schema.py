from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field, field_validator, model_validator


class InferenceResult(BaseModel):
    imagem: str
    face_inferida: int = Field(ge=1, le=20)
    face_oposta: int = Field(ge=1, le=20)
    confianca: float = Field(ge=0.0, le=1.0)
    timestamp: str
    versao_modelo: str

    @field_validator("timestamp")
    @classmethod
    def _validate_timestamp(cls, value: str) -> str:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return value

    @model_validator(mode="after")
    def _validate_opposite(self) -> "InferenceResult":
        if self.face_oposta != 21 - self.face_inferida:
            raise ValueError("face_oposta deve obedecer a regra 21 - face_inferida")
        return self


class InferenceBatch(BaseModel):
    generated_at: str
    results: list[InferenceResult]



def write_results_json(results: list[dict], output_path: str | Path) -> None:
    batch = InferenceBatch(
        generated_at=datetime.now(timezone.utc).isoformat(),
        results=[InferenceResult(**item) for item in results],
    )

    path = Path(output_path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(batch.model_dump(), f, ensure_ascii=False, indent=2)
