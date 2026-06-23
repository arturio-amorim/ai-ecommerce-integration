"""Configuration, read from environment (.env supported)."""
from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover
    pass


@dataclass
class Settings:
    llm_provider: str = os.getenv("LLM_PROVIDER", "anthropic")
    gen_model: str = os.getenv("GEN_MODEL", "claude-sonnet-4-6")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    index_dir: str = os.getenv("INDEX_DIR", ".index")

    @property
    def model(self) -> str:
        if self.llm_provider == "anthropic":
            return self.gen_model
        if self.llm_provider == "ollama":
            return self.ollama_model
        return self.openai_model


def get_settings() -> Settings:
    return Settings()
