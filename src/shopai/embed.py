"""Local sentence-transformers embedder (no API key). Returns plain float lists."""
from __future__ import annotations

from typing import List


class LocalEmbedder:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as e:  # pragma: no cover
                raise ImportError("pip install sentence-transformers") from e
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def encode(self, texts: List[str]) -> List[List[float]]:
        embs = self.model.encode(
            texts, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False
        )
        return [[float(x) for x in v] for v in embs]

    def encode_one(self, text: str) -> List[float]:
        return self.encode([text])[0]
