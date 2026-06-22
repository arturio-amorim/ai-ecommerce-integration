"""Semantic catalog search.

Pure-Python cosine similarity (fine for catalog scale) with a *pluggable*
embedder, so the ranking logic is unit-testable without any ML dependency.
"""
from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass
from typing import List, Tuple

from .models import Product


def cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


@dataclass
class SemanticIndex:
    products: List[Product]
    vectors: List[List[float]]

    @classmethod
    def build(cls, products: List[Product], embedder) -> "SemanticIndex":
        vectors = embedder.encode([p.text_blob() for p in products])
        return cls(products=list(products), vectors=[list(v) for v in vectors])

    def search(self, query: str, embedder, k: int = 5) -> List[Tuple[Product, float]]:
        qv = embedder.encode_one(query)
        scored = [(p, cosine(qv, v)) for p, v in zip(self.products, self.vectors)]
        scored.sort(key=lambda t: t[1], reverse=True)
        return scored[:k]

    def save(self, path: str) -> None:
        os.makedirs(path, exist_ok=True)
        payload = {
            "products": [
                {
                    "id": p.id, "title": p.title, "description": p.description,
                    "price": p.price, "category": p.category, "tags": p.tags,
                }
                for p in self.products
            ],
            "vectors": self.vectors,
        }
        with open(os.path.join(path, "catalog.json"), "w", encoding="utf-8") as f:
            json.dump(payload, f)

    @classmethod
    def load(cls, path: str) -> "SemanticIndex":
        with open(os.path.join(path, "catalog.json"), encoding="utf-8") as f:
            payload = json.load(f)
        products = [
            Product(
                id=d["id"], title=d["title"], description=d.get("description", ""),
                price=d.get("price", 0.0), category=d.get("category", ""), tags=d.get("tags", []),
            )
            for d in payload["products"]
        ]
        return cls(products=products, vectors=payload["vectors"])
