from __future__ import annotations
import os
from typing import List


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://appuser:super_secret@db:5432/crypto")
COINGECKO_BASE = os.getenv("COINGECKO_BASE", "https://api.coingecko.com/api/v3")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:8080").split(",")