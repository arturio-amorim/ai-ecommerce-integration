"""Tests for semantic search — uses a FAKE embedder, so no ML deps needed."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shopai.models import Product  # noqa: E402
from shopai.search import SemanticIndex, cosine  # noqa: E402

VOCAB = ["running", "shoe", "coffee", "mug", "laptop"]


class FakeEmbedder:
    """Deterministic keyword one-hot embedder — enough to test ranking."""

    def encode(self, texts):
        return [[1.0 if w in t.lower() else 0.0 for w in VOCAB] for t in texts]

    def encode_one(self, text):
        return self.encode([text])[0]


PRODUCTS = [
    Product(id="1", title="Running Shoes", category="Footwear", tags=["running", "shoe"]),
    Product(id="2", title="Coffee Mug", category="Kitchen", tags=["coffee", "mug"]),
    Product(id="3", title="Laptop", category="Electronics", tags=["laptop"]),
]


def test_cosine_basics():
    assert cosine([1, 0], [1, 0]) == 1.0
    assert cosine([1, 0], [0, 1]) == 0.0
    assert cosine([0, 0], [1, 1]) == 0.0


def test_search_ranks_relevant_product_first():
    index = SemanticIndex.build(PRODUCTS, FakeEmbedder())
    results = index.search("running shoe", FakeEmbedder(), k=3)
    assert results[0][0].title == "Running Shoes"
    assert results[0][1] > results[1][1]


def test_save_and_load_roundtrip(tmp_path):
    index = SemanticIndex.build(PRODUCTS, FakeEmbedder())
    index.save(str(tmp_path))
    loaded = SemanticIndex.load(str(tmp_path))
    assert [p.title for p in loaded.products] == [p.title for p in PRODUCTS]
    assert loaded.vectors == index.vectors
