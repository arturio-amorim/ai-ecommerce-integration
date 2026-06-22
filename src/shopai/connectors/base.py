"""The connector interface every store integration implements."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from ..models import Product


class StoreConnector(ABC):
    """Abstract store. Swap implementations (mock, Shopify, ...) freely."""

    @abstractmethod
    def fetch_products(self) -> List[Product]:
        """Return the store's catalog as Product objects."""

    def update_product(self, product: Product) -> None:
        """Push enriched fields back to the store (optional per connector)."""
        raise NotImplementedError(f"{type(self).__name__} does not support writes")
