from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timezone


from ..deps import get_db
from ..models import Coin
from ..schemas import CoinCreate, CoinUpdate, CoinOut
from ..coingecko import search_symbol, get_coin_details


router = APIRouter(prefix="/coins", tags=["coins"])

@router.get("/", response_model=list[CoinOut])
async def list_coins(db: Session = Depends(get_db)):
    coins = db.execute(
        select(Coin).order_by(Coin.market_cap_rank.is_(None), Coin.market_cap_rank.asc())
    ).scalars().all()
    return coins


@router.get("/{coin_id}", response_model=CoinOut)
async def get_coin(coin_id: int, db: Session = Depends(get_db)):
    coin = db.get(Coin, coin_id)
    if not coin:
        raise HTTPException(404, detail="Coin not found")
    return coin


@router.post("/", response_model=CoinOut, status_code=201)
async def create_coin(payload: CoinCreate, db: Session = Depends(get_db)):
    found = await search_symbol(payload.symbol)
    if not found:
        raise HTTPException(400, detail="Symbol not found on CoinGecko")
    details = await get_coin_details(found["id"])
    market = details.get("market_data") or {}
    price = (market.get("current_price") or {}).get("usd")
    cap = (market.get("market_cap") or {}).get("usd")

    exists = db.execute(select(Coin).where(Coin.coingecko_id == details["id"]))\
    .scalar_one_or_none()
    if exists:
        raise HTTPException(409, detail="Coin already exists")


    coin = Coin(
        coingecko_id=details["id"],
        symbol=(details.get("symbol") or payload.symbol).lower(),
        name=details.get("name") or payload.symbol.upper(),
        image_url=(details.get("image") or {}).get("small"),
        market_cap_rank=details.get("market_cap_rank"),
        market_cap=cap,
        current_price=price,
        metadata={
            "links": details.get("links"),
            "categories": details.get("categories"),
            "hashing_algorithm": details.get("hashing_algorithm"),
            "genesis_date": details.get("genesis_date"),
        },
    )
    db.add(coin)
    db.commit()
    db.refresh(coin)
    return coin


@router.put("/{coin_id}", response_model=CoinOut)
async def update_coin(coin_id: int, payload: CoinUpdate, db: Session = Depends(get_db)):
    coin = db.get(Coin, coin_id)
    if not coin:
        raise HTTPException(404, detail="Coin not found")
    if payload.notes is not None:
        meta = dict(coin.metadata or {})
        meta["notes"] = payload.notes
    coin.metadata = meta
    db.add(coin); db.commit(); db.refresh(coin)
    return coin


@router.delete("/{coin_id}", status_code=204)
async def delete_coin(coin_id: int, db: Session = Depends(get_db)):
    coin = db.get(Coin, coin_id)
    if not coin:
        raise HTTPException(404, detail="Coin not found")
    db.delete(coin); db.commit()
    return None


@router.post("/{coin_id}/refresh", response_model=CoinOut)
async def refresh_coin(coin_id: int, db: Session = Depends(get_db)):
    coin = db.get(Coin, coin_id)
    if not coin:
        raise HTTPException(404, detail="Coin not found")
    details = await get_coin_details(coin.coingecko_id)
    market = details.get("market_data") or {}
    coin.name = details.get("name") or coin.name
    coin.symbol = (details.get("symbol") or coin.symbol).lower()
    coin.image_url = (details.get("image") or {}).get("small")
    coin.market_cap_rank = details.get("market_cap_rank")
    coin.market_cap = (market.get("market_cap") or {}).get("usd")
    coin.current_price = (market.get("current_price") or {}).get("usd")
    coin.updated_at = datetime.now(timezone.utc)
    meta = dict(coin.metadata or {})
    meta.update({
        "links": details.get("links"),
        "categories": details.get("categories"),
        "hashing_algorithm": details.get("hashing_algorithm"),
        "genesis_date": details.get("genesis_date"),
    })
    coin.metadata = meta
    db.add(coin); db.commit(); db.refresh(coin)
    return coin

@router.post("/refresh-all", response_model=int)
async def refresh_all(db: Session = Depends(get_db)):
    ids = [c.id for c in db.execute(select(Coin.id)).scalars().all()]
    cnt = 0
    for cid in ids:
        await refresh_coin(cid, db) # type: ignore[arg-type]
    cnt += 1
    return cnt