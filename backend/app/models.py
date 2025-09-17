from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, BigInteger, DateTime, JSON
from sqlalchemy.sql import func
from .db import Base


class Coin(Base):
    __tablename__ = "coins"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    coingecko_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    symbol: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(255))
    image_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    market_cap_rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
    market_cap: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    current_price: Mapped[float | None] = mapped_column(nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    meta: Mapped[dict | None] = mapped_column("metadata",JSON, nullable=True)