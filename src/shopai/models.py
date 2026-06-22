"""Domain models (pure dataclasses)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Seo:
    seo_title: str = ""
    meta_description: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class Product:
    id: str
    title: str
    description: str = ""
    price: float = 0.0
    category: str = ""
    tags: List[str] = field(default_factory=list)
    seo: Optional[Seo] = None

    def text_blob(self) -> str:
        """Concatenated text used for embedding/semantic search."""
        parts = [self.title, self.category, self.description, " ".join(self.tags)]
        return " ".join(p for p in parts if p).strip()
