#!/usr/bin/env python
"""Semantic search over the indexed catalog. (No API key.)

    python scripts/search.py "comfortable shoes for jogging"
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shopai.config import get_settings  # noqa: E402
from shopai.embed import LocalEmbedder  # noqa: E402
from shopai.search import SemanticIndex  # noqa: E402


def main() -> None:
    s = get_settings()
    ap = argparse.ArgumentParser(description="Semantic catalog search.")
    ap.add_argument("query", nargs="+")
    ap.add_argument("--k", type=int, default=5)
    args = ap.parse_args()

    try:
        index = SemanticIndex.load(s.index_dir)
    except FileNotFoundError:
        print("No index found. Build it first:  python scripts/sync.py")
        sys.exit(1)

    results = index.search(" ".join(args.query), LocalEmbedder(s.embedding_model), k=args.k)
    print(f'Top {len(results)} for: "{" ".join(args.query)}"\n')
    for product, score in results:
        print(f"  {score:.3f}  {product.title}  (${product.price})  [{product.category}]")


if __name__ == "__main__":
    main()
