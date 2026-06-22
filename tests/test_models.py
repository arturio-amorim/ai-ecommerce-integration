"""Tests for the domain models (pure)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shopai.models import Product  # noqa: E402


def test_text_blob_concatenates_searchable_fields():
    p = Product(id="1", title="Running Shoes", description="Light and grippy",
                category="Footwear", tags=["running", "trail"])
    blob = p.text_blob()
    for token in ("Running Shoes", "Footwear", "Light and grippy", "running", "trail"):
        assert token in blob


def test_text_blob_skips_empty_fields():
    p = Product(id="2", title="Mug")
    assert p.text_blob() == "Mug"
