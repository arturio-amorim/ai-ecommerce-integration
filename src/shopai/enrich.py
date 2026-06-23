"""LLM-powered SEO enrichment for a product (provider-swappable)."""
from __future__ import annotations

import json
import re

from .config import Settings
from .models import Product, Seo

SYSTEM_PROMPT = (
    "You are an expert e-commerce SEO copywriter. Write concise, accurate, "
    "keyword-rich copy. Never invent specs, sizes, or claims not implied by the input."
)


def _prompt(product: Product) -> str:
    return (
        "Product:\n"
        f"Title: {product.title}\n"
        f"Category: {product.category or '(none)'}\n"
        f"Current description: {product.description or '(none)'}\n"
        f"Tags: {', '.join(product.tags) or '(none)'}\n\n"
        "Return ONLY JSON with keys: "
        'seo_title (<=60 chars), meta_description (<=155 chars), '
        "description (2-3 persuasive sentences), tags (array of 5-8 lowercase keywords)."
    )


def _parse_json(raw: str) -> dict:
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        m = re.search(r"\{.*\}", raw or "", re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except ValueError:
                return {}
        return {}


def enrich_product(product: Product, settings: Settings) -> Seo:
    raw = _call(_prompt(product), settings)
    d = _parse_json(raw)
    return Seo(
        seo_title=d.get("seo_title", ""),
        meta_description=d.get("meta_description", ""),
        description=d.get("description", ""),
        tags=list(d.get("tags", [])),
    )


def _call(prompt: str, settings: Settings) -> str:
    if settings.llm_provider == "anthropic":
        import anthropic

        client = anthropic.Anthropic()
        msg = client.messages.create(
            model=settings.gen_model,
            max_tokens=600,
            temperature=0.4,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in msg.content if b.type == "text").strip()

    from openai import OpenAI

    if settings.llm_provider == "ollama":
        client = OpenAI(base_url=settings.ollama_base_url, api_key="ollama")  # local, free
        model = settings.ollama_model
    else:
        client = OpenAI()
        model = settings.openai_model
    resp = client.chat.completions.create(
        model=model,
        temperature=0.4,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return (resp.choices[0].message.content or "").strip()
