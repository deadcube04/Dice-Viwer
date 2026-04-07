from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


@dataclass
class CentroidClassifier:
    centroids: dict[int, np.ndarray]

    def predict(self, feature: np.ndarray) -> tuple[int, float]:
        if feature.ndim != 1:
            feature = feature.reshape(-1)

        labels = sorted(self.centroids.keys())
        distances: list[float] = []

        for label in labels:
            centroid = self.centroids[label]
            dist = float(np.linalg.norm(feature - centroid))
            distances.append(dist)

        distances_arr = np.array(distances, dtype=np.float64)
        logits = -distances_arr
        logits -= logits.max()
        probs = np.exp(logits) / np.sum(np.exp(logits))

        best_idx = int(np.argmax(probs))
        return labels[best_idx], float(probs[best_idx])

    def predict_batch(self, features: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        preds = []
        confs = []
        for feature in features:
            pred, conf = self.predict(feature)
            preds.append(pred)
            confs.append(conf)
        return np.array(preds, dtype=np.int32), np.array(confs, dtype=np.float32)


def train_centroid_classifier(features: np.ndarray, labels: np.ndarray) -> CentroidClassifier:
    unique_labels = np.unique(labels)
    centroids: dict[int, np.ndarray] = {}

    for label in unique_labels:
        class_vectors = features[labels == label]
        centroids[int(label)] = np.mean(class_vectors, axis=0)

    return CentroidClassifier(centroids=centroids)


def _confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, classes: list[int]) -> np.ndarray:
    idx_map = {label: idx for idx, label in enumerate(classes)}
    matrix = np.zeros((len(classes), len(classes)), dtype=np.int32)
    for true_label, pred_label in zip(y_true, y_pred):
        matrix[idx_map[int(true_label)], idx_map[int(pred_label)]] += 1
    return matrix


def evaluate_classifier(
    classifier: CentroidClassifier,
    features: np.ndarray,
    labels: np.ndarray,
) -> dict[str, Any]:
    preds, confs = classifier.predict_batch(features)
    accuracy = float(np.mean(preds == labels))
    classes = sorted({int(v) for v in labels.tolist()})
    conf_mat = _confusion_matrix(labels, preds, classes)

    return {
        "accuracy": accuracy,
        "mean_confidence": float(np.mean(confs)) if len(confs) else 0.0,
        "classes": classes,
        "confusion_matrix": conf_mat.tolist(),
        "samples": int(len(labels)),
    }


def save_model_bundle(
    output_path: str | Path,
    classifier: CentroidClassifier,
    metrics: dict[str, Any],
    preprocessing: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> None:
    payload = {
        "classifier": classifier,
        "metrics": metrics,
        "preprocessing": preprocessing or {},
        "metadata": metadata or {},
    }

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("wb") as f:
        pickle.dump(payload, f)


def load_model_bundle(model_path: str | Path) -> dict[str, Any]:
    with Path(model_path).open("rb") as f:
        return pickle.load(f)
