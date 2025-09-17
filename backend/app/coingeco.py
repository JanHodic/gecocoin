from __future__ import annotations
import json
import httpx
from .settings import COINGECKO_BASE
from .cache import cache_get, cache_setex


async def search_symbol(symbol: str) -> dict | None:
    q = symbol.lower()
    key = f"cg:search:{q}"
    cached = await cache_get(key)
    if cached:
        data = json.loads(cached)
        coins = data.get("coins", [])
        exact = next((c for c in coins if (c.get("symbol") or "").lower() == q), None)
        return exact or (coins[0] if coins else None)

    url = f"{COINGECKO_BASE}/search?query={q}"
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url)
        r.raise_for_status()
    data = r.json()
    await cache_setex(key, 300, json.dumps(data)) # 5 min
    coins = data.get("coins", [])
    exact = next((c for c in coins if (c.get("symbol") or "").lower() == q), None)
    return exact or (coins[0] if coins else None)

async def get_coin_details(coingecko_id: str) -> dict:
    key = f"cg:coin:{coingecko_id}"
    cached = await cache_get(key)
    if cached:
        return json.loads(cached)
    url = (
        f"{COINGECKO_BASE}/coins/{coingecko_id}?"
        "localization=false&tickers=false&community_data=false&developer_data=false&sparkline=false"
    )

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()
    await cache_setex(key, 120, json.dumps(data)) # 2 min
    return data