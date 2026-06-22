#!/usr/bin/env python
"""Pull the catalog, build the semantic index, and save it. (No API key.)

    python scripts/sync.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shopai.config import get_settings  # noqa: E402
from shopai.connectors.mock import MockStore  # noqa: E402
from shopai.embed import LocalEmbedder  # noqa: E402
from shopai.search import SemanticIndex  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    s = get_settings()
    ap = argparse.ArgumentParser(description="Sync catalog + build semantic index.")
    ap.add_argument("--data", default=str(ROOT / "data" / "sample_products.json"))
    ap.add_argument("--index-dir", default=s.index_dir)
    args = ap.parse_args()

    products = MockStore(args.data).fetch_products()
    print(f"Pulled {len(products)} products from the store")

    index = SemanticIndex.build(products, LocalEmbedder(s.embedding_model))
    index.save(args.index_dir)
    print(f"Built + saved semantic index -> {args.index_dir}")


if __name__ == "__main__":
    main()
