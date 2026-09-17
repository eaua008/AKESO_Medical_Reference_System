import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Config:
    """Immutable application settings."""

    supabase_url: str
    supabase_key: str

    @classmethod
    def load(cls) -> "Config":
        url = os.getenv("SUPABASE_URL")

        # Newer Supabase projects issue a publishable key; older ones an anon
        # key. Accept either so the app runs against both.
        key = os.getenv("SUPABASE_PUBLISHABLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

        if not url or not key:
            raise RuntimeError(
                "Missing SUPABASE_URL or SUPABASE_PUBLISHABLE_KEY. "
                "Check that .env exists in the project root and has no quotes."
            )
        return cls(supabase_url=url, supabase_key=key)


config = Config.load()