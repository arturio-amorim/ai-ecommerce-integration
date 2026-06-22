"""Glue: pull -> (enrich) -> index -> search."""
from __future__ import annotations

from typing import List

from .config import Settings
from .connectors.base import StoreConnector
from .models import Product
from .search import SemanticIndex


def pull(connector: StoreConnector) -> List[Product]:
    return connector.fetch_products()


def build_index(products: List[Product], embedder) -> SemanticIndex:
    return SemanticIndex.build(products, embedder)


def enrich_all(products: List[Product], settings: Settings) -> List[Product]:
    """Attach LLM-generated SEO fields to every product (in place)."""
    from .enrich import enrich_product  # imported lazily (needs an SDK + key)

    for product in products:
        product.seo = enrich_product(product, settings)
    return products
