"""A mock store backed by a local JSON catalog — runs fully offline."""
from __future__ import annotations

import json
from typing import List

from ..models import Product
from .base import StoreConnector


class MockStore(StoreConnector):
    def __init__(self, path: str):
        self.path = path
        self._updates: List[Product] = []

    def fetch_products(self) -> List[Product]:
        with open(self.path, encoding="utf-8") as f:
            raw = json.load(f)
        return [
            Product(
                id=str(d["id"]),
                title=d["title"],
                description=d.get("description", ""),
                price=float(d.get("price", 0) or 0),
                category=d.get("category", ""),
                tags=list(d.get("tags", [])),
            )
            for d in raw
        ]

    def update_product(self, product: Product) -> None:
        # In a real store this would PUT to the API; here we just record it.
        self._updates.append(product)
