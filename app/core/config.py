import os
from dataclasses import dataclass

from dotenv import load_dotenv

from app.core.paths import app_dir, resource_root

PROJECT_ROOT = resource_root()
# A .env next to Akeso.exe wins (so a build can be pointed at another
# Supabase project without rebuilding); otherwise the one bundled inside it,
# or the project's own .env when running from IntelliJ.
for _env in (app_dir() / ".env", PROJECT_ROOT / ".env"):
    if _env.is_file():
        load_dotenv(_env)
        break


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
                "Check that .env exists in the project root (or next to Akeso.exe) "
                "and has no quotes."
            )
        return cls(supabase_url=url, supabase_key=key)


config = Config.load()