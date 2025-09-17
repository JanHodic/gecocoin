from __future__ import annotations
from pydantic import BaseModel, Field, AliasChoices
from typing import Optional


class CoinCreate(BaseModel):
    symbol: str = Field(..., examples=["btc", "eth"]) # case-insensitive


class CoinUpdate(BaseModel):
    notes: Optional[str] = None


class CoinOut(BaseModel):
    id: int
    coingecko_id: str
    symbol: str
    name: str
    image_url: Optional[str] = None
    market_cap_rank: Optional[int] = None
    market_cap: Optional[int] = None
    current_price: Optional[float] = None
    created_at: str
    updated_at: str
    metadata: Optional[dict] = Field(default=None, validation_alias=AliasChoices("meta", "metadata"))


    model_config = {
        "from_attributes": True
    }