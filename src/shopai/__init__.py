"""shopai — AI layer for an e-commerce catalog: SEO enrichment + semantic search.

Light top-level import; the embedding model / LLM SDKs load lazily on use.
    from shopai.connectors.mock import MockStore
    from shopai.search import SemanticIndex
"""
from .config import Settings, get_settings
from .models import Product, Seo

__version__ = "0.1.0"
__all__ = ["Settings", "get_settings", "Product", "Seo", "__version__"]
