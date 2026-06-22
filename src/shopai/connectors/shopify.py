"""A Shopify Admin API connector (real shape).

Needs SHOPIFY_STORE (e.g. my-shop.myshopify.com) and SHOPIFY_TOKEN. Shown to
demonstrate how a real integration plugs into the same interface as the mock.
"""
from __future__ import annotations

import os
import re
from typing import List

from ..models import Product
from .base import StoreConnector

_TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(html: str) -> str:
    return _TAG_RE.sub("", html or "").strip()


class ShopifyConnector(StoreConnector):
    def __init__(self, store: str | None = None, token: str | None = None, api_version: str = "2024-10"):
        self.store = store or os.getenv("SHOPIFY_STORE")
        self.token = token or os.getenv("SHOPIFY_TOKEN")
        self.api_version = api_version

    def _require_creds(self) -> None:
        if not (self.store and self.token):
            raise RuntimeError("Set SHOPIFY_STORE and SHOPIFY_TOKEN to use the Shopify connector")

    def _headers(self) -> dict:
        return {"X-Shopify-Access-Token": self.token, "Content-Type": "application/json"}

    def fetch_products(self) -> List[Product]:
        self._require_creds()
        import requests

        url = f"https://{self.store}/admin/api/{self.api_version}/products.json?limit=250"
        resp = requests.get(url, headers=self._headers(), timeout=30)
        resp.raise_for_status()

        products: List[Product] = []
        for p in resp.json().get("products", []):
            variants = p.get("variants") or [{}]
            price = float(variants[0].get("price", 0) or 0)
            tags = [t.strip() for t in (p.get("tags", "") or "").split(",") if t.strip()]
            products.append(
                Product(
                    id=str(p["id"]),
                    title=p.get("title", ""),
                    description=_strip_html(p.get("body_html", "")),
                    price=price,
                    category=p.get("product_type", ""),
                    tags=tags,
                )
            )
        return products

    def update_product(self, product: Product) -> None:
        self._require_creds()
        import requests

        body = product.seo.description if product.seo else product.description
        url = f"https://{self.store}/admin/api/{self.api_version}/products/{product.id}.json"
        payload = {"product": {"id": product.id, "body_html": body}}
        resp = requests.put(url, json=payload, headers=self._headers(), timeout=30)
        resp.raise_for_status()
