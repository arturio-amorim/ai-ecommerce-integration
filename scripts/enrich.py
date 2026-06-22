#!/usr/bin/env python
"""Enrich products with LLM-generated SEO copy (needs an API key). Before/after.

    python scripts/enrich.py --limit 2
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shopai.config import get_settings  # noqa: E402
from shopai.connectors.mock import MockStore  # noqa: E402
from shopai.enrich import enrich_product  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    s = get_settings()
    ap = argparse.ArgumentParser(description="LLM SEO enrichment (before/after).")
    ap.add_argument("--data", default=str(ROOT / "data" / "sample_products.json"))
    ap.add_argument("--limit", type=int, default=2)
    args = ap.parse_args()

    products = MockStore(args.data).fetch_products()[: args.limit]
    for product in products:
        seo = enrich_product(product, s)
        print("=" * 72)
        print("PRODUCT:", product.title)
        print("\n[BEFORE]", product.description)
        print("\n[AFTER ]", seo.description)
        print("SEO title:", seo.seo_title)
        print("Meta     :", seo.meta_description)
        print("Tags     :", ", ".join(seo.tags))
        print()


if __name__ == "__main__":
    main()
