"""Tests for the mock store connector (pure)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shopai.connectors.mock import MockStore  # noqa: E402
from shopai.models import Product, Seo  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = str(ROOT / "data" / "sample_products.json")


def test_mock_store_loads_catalog():
    products = MockStore(DATA).fetch_products()
    assert len(products) >= 8
    assert all(isinstance(p, Product) for p in products)
    first = products[0]
    assert first.id and first.title and first.price >= 0


def test_update_product_is_recorded():
    store = MockStore(DATA)
    p = Product(id="1001", title="X", seo=Seo(description="new"))
    store.update_product(p)
    assert store._updates and store._updates[0].id == "1001"
